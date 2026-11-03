import contextlib
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import requests

import main

AUTHOR = 'testID123'


def profile(paper='paper1', more=False, citations='1,234', paper_citations='2*'):
    return f'''
    <div id="gsc_prf_in">Test Author</div>
    <table id="gsc_rsb_st"><tr><td class="gsc_rsb_std">{citations}</td></tr></table>
    <span class="gsc_g_t">2025</span><span class="gsc_g_t">2026</span>
    <a class="gsc_g_a" href="?as_ylo=2026"><span class="gsc_g_al">2</span></a>
    <table><tbody id="gsc_a_b"><tr class="gsc_a_tr">
    <td><a class="gsc_a_at" href="?citation_for_view={AUTHOR}%3A{paper}">A &amp; B</a></td>
    <td><a class="gsc_a_ac">{paper_citations}</a></td><td class="gsc_a_y">2025</td>
    </tr></tbody></table>
    <button id="gsc_bpf_more" {' ' if more else 'disabled'}>Show more</button>
    '''


def api_page(paper='paper1', more=False):
    return {
        'author': {'name': 'Test Author'},
        'cited_by': {'table': [{'citations': {'all': 1234}}, {'h_index': {'all': 2}}],
                     'graph': [{'year': 2026, 'citations': 2}]},
        'articles': [{'citation_id': f'{AUTHOR}:{paper}', 'title': 'A & B',
                      'year': '2025', 'cited_by': {'value': None}}],
        'serpapi_pagination': {'next': 'https://serpapi.com/search.json?start=1'} if more else {},
    }


class CrawlerTests(unittest.TestCase):
    def test_profile_and_badge_use_all_time_count(self):
        author, more = main.parse_profile(profile(), AUTHOR)
        self.assertFalse(more)
        self.assertEqual(author['citedby'], 1234)
        self.assertEqual(author['cites_per_year'], {'2025': 0, '2026': 2})
        self.assertEqual(author['publications'][AUTHOR + ':paper1']['num_citations'], 2)
        with tempfile.TemporaryDirectory() as directory:
            main.write_results(author, Path(directory))
            badge = json.loads((Path(directory) / 'gs_data_shieldsio.json').read_text())
            self.assertEqual(badge['message'], '1234')
            self.assertIn('updated', json.loads((Path(directory) / 'gs_data.json').read_text()))

    def test_zero_is_valid(self):
        author, _ = main.parse_profile(profile(citations='0', paper_citations=''), AUTHOR)
        self.assertEqual(author['citedby'], 0)
        self.assertEqual(author['publications'][AUTHOR + ':paper1']['num_citations'], 0)

    def test_verification_and_incomplete_pages_are_rejected(self):
        for html in ['<html>Please show you are not a robot</html>',
                     profile().replace('gsc_rsb_std', 'missing'),
                     profile().replace('gsc_a_ac', 'missing'),
                     profile(citations='unknown')]:
            with self.subTest(html=html), self.assertRaises(main.FetchError):
                main.parse_profile(html, AUTHOR)

    def test_direct_pagination(self):
        session = Mock()
        session.get.side_effect = [Mock(text=profile(more=True)), Mock(text=profile('paper2'))]
        result = main.fetch_direct(session, AUTHOR)
        self.assertEqual(len(result['publications']), 2)
        self.assertEqual(session.get.call_args.kwargs['params']['cstart'], 1)

    def test_repeated_page_is_rejected(self):
        session = Mock()
        session.get.return_value = Mock(text=profile(more=True))
        with self.assertRaises(main.FetchError):
            main.fetch_direct(session, AUTHOR)
        self.assertEqual(session.get.call_count, 2)

    def test_serpapi_pagination_and_normalization(self):
        session = Mock()
        session.get.side_effect = [Mock(json=Mock(return_value=api_page(more=True))),
                                   Mock(json=Mock(return_value=api_page('paper2')))]
        result = main.fetch_serpapi(session, AUTHOR, 'test-key')
        self.assertEqual(result['citedby'], 1234)
        self.assertEqual(result['hindex'], 2)
        self.assertEqual(len(result['publications']), 2)
        self.assertEqual(result['publications'][AUTHOR + ':paper1']['num_citations'], 0)
        self.assertEqual(session.get.call_args.kwargs['params']['start'], 1)

    def test_serpapi_errors_and_partial_data_are_rejected(self):
        for data in [{'error': 'bad key'}, {}, {'author': {'name': 'Test Author'}},
                     api_page() | {'articles': None}]:
            session = Mock()
            session.get.return_value.json.return_value = data
            with self.subTest(data=data), self.assertRaises(main.FetchError):
                main.fetch_serpapi(session, AUTHOR, 'test-key')

    def test_network_error_does_not_leak_api_key(self):
        session = Mock()
        session.get.side_effect = requests.ConnectionError('https://serpapi.com/?api_key=private-key')
        with self.assertRaises(main.FetchError) as caught:
            main.fetch_serpapi(session, AUTHOR, 'private-key')
        self.assertNotIn('private-key', str(caught.exception))

    def test_failure_preserves_existing_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'results').mkdir()
            files = [root / 'results' / name for name in ['gs_data.json', 'gs_data_shieldsio.json']]
            for file in files:
                file.write_text('previous-data')
            with patch.object(main, 'ROOT', root), patch.object(main, 'scholar_id', return_value=AUTHOR), \
                    patch.dict(os.environ, {'SERPAPI_API_KEY': ''}), \
                    patch.object(main, 'fetch_direct', side_effect=main.FetchError('verification page')), \
                    contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(main.main(), 1)
            self.assertTrue(all(file.read_text() == 'previous-data' for file in files))

    def test_config_and_environment_author_ids(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / '_config.yml').write_text('author:\n  googlescholar: https://scholar.google.com/citations?user=configID\n')
            with patch.object(main, 'ROOT', root / 'crawler'), patch.dict(os.environ, {'GOOGLE_SCHOLAR_ID': ''}):
                self.assertEqual(main.scholar_id(), 'configID')
            with patch.dict(os.environ, {'GOOGLE_SCHOLAR_ID': 'https://scholar.google.com/citations?user=envID&hl=en'}):
                self.assertEqual(main.scholar_id(), 'envID')
            with patch.dict(os.environ, {'GOOGLE_SCHOLAR_ID': 'invalid value'}), self.assertRaises(main.FetchError):
                main.scholar_id()


if __name__ == '__main__':
    unittest.main()
