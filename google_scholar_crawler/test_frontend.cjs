const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const template = fs.readFileSync(path.join(__dirname, '../_includes/fetch_google_scholar_stats.html'), 'utf8');

function run({total = null, papers = [], responses = [], cdn = false}) {
    const urls = [];
    let warnings = 0;
    const script = template.replace(/<\/?script>/g, '')
        .replace(/{% if site.google_scholar_stats_use_cdn %}([\s\S]*?){% else %}([\s\S]*?){% endif %}/,
            (_, yes, no) => cdn ? yes : no)
        .replace(/{{ site.repository }}/g, 'test/site');
    const $ = () => ({ready: callback => callback()});
    $.ajax = options => {
        urls.push(options.url);
        const response = responses.shift();
        assert.ok(response, 'unexpected request');
        const request = {
            done(callback) { if (!response.error) callback(response.data); return request; },
            fail(callback) { if (response.error) callback(); return request; }
        };
        return request;
    };
    vm.runInNewContext(script, {$, document: {
        getElementById: () => total,
        getElementsByClassName: () => papers
    }, console: {warn: () => warnings++}});
    return {urls, warnings};
}
const paper = id => ({getAttribute: () => id, textContent: 'unchanged'});
const present = paper('known'), absent = paper('missing');
run({papers: [present, absent], responses: [{data: {publications: {known: {num_citations: 0}}}}]});
assert.equal(present.textContent, '| Citations: 0');
assert.equal(absent.textContent, 'unchanged');
const total = {textContent: 'old'};
const fallback = run({total, responses: [{error: true}, {data: {citedby: 1234, publications: {}}}]});
assert.equal(total.textContent, 1234);
assert.ok(fallback.urls[1].includes('cdn.jsdelivr.net'));
assert.equal(run({}).urls.length, 0);
const malformed = run({total, cdn: true, responses: [{data: null}, {error: true}]});
assert.ok(malformed.urls[0].includes('cdn.jsdelivr.net'));
assert.equal(malformed.warnings, 1);
run({total, responses: [{data: {citedby: null, publications: {}}}]});
assert.equal(total.textContent, 1234);
console.log('Frontend checks passed: missing elements/papers, zero counts, invalid data and CDN fallback.');
