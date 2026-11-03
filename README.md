<h1 align="center">
AcadHomepage
</h1>

<div align="center">

[![](https://img.shields.io/github/stars/RayeRen/acad-homepage.github.io)](https://github.com/RayeRen/acad-homepage.github.io)
[![](https://img.shields.io/github/forks/RayeRen/acad-homepage.github.io)](https://github.com/RayeRen/acad-homepage.github.io)
[![](https://img.shields.io/github/issues/RayeRen/acad-homepage.github.io)](https://github.com/RayeRen/acad-homepage.github.io)
[![](https://img.shields.io/github/license/RayeRen/acad-homepage.github.io)](https://github.com/RayeRen/acad-homepage.github.io/blob/main/LICENSE)  | [English README](./docs/README-en.md)

</div>

<p align="center">一个现代、响应式的个人学术主页</p>

<p align="center">
    <br>
    <img src="docs/screenshot.png" width="100%"/>
    <br>
</p>

一些例子：

- [样例页面](https://rayeren.github.io/acad-homepage.github.io/)
- [作者的个人主页](https://rayeren.github.io/)

## 主要特点

- **自动更新谷歌学术引用**: 借助谷歌学术爬虫和github action功能，本仓库可以自动更新作者的引用数和论文引用数。
- **支持谷歌Analytics**: 你可以通过简单的配置来实现使用谷歌Analytics跟踪网页的流量。
- **响应式的**: 此主页会针对不同的屏幕尺寸自动调整布局。
- **美观而简约**: 此主页美观而简约，适合个人学术主页的搭建。
- **搜索引擎优化**: 搜索引擎优化 (SEO) 帮助搜索引擎轻松找到您在主页上发布的信息，然后将其与类似网站进行排名，并获得排名优势。

## 快速开始

1. Fork本仓库到 `USERNAME/USERNAME.github.io`，其中 `USERNAME`是你的github用户名。
2. 配置谷歌学术引用爬虫：
   1. 在你的谷歌学术引用页面的url里找到你的谷歌学术ID：例如，在url https://scholar.google.com/citations?user=SCHOLAR_ID 中，`SCHOLAR_ID`部分即为你的谷歌学术ID。
   2. 爬虫默认读取 `_config.yml` 中的 `author.googlescholar`。也可在仓库 `Settings -> Secrets and variables -> Actions` 中添加 `GOOGLE_SCHOLAR_ID` Secret 覆盖此设置（支持 ID 或完整个人主页 URL）。
   3. 在 Actions 中启用 `Get Citation Data`，可用 `Run workflow` 手动运行。工作流每天北京时间 20:00（12:00 UTC）运行，在 `master`/`main` 上修改爬虫、配置或工作流也会触发。成功后将统计和徽章 JSON 更新到 `google-scholar-stats` 分支；失败会报错并保留上次发布的数据。
   4. Google Scholar 可能对直连请求返回 403、429 或 HTTP 200 的机器人验证页。可添加 `SERPAPI_API_KEY` Secret，切换到 [SerpApi Google Scholar Author API](https://serpapi.com/google-scholar-author-api)（需自行提供密钥及可用额度）；或添加 `GOOGLE_SCHOLAR_PROXY` Secret 配置可访问 Scholar 的 HTTP/HTTPS 代理。未配置密钥时使用直连，支持读取本地 `HTTPS_PROXY`。不要把密钥或代理凭据提交到仓库。
   5. 本地运行：`python -m pip install -r google_scholar_crawler/requirements.txt`，然后执行 `python google_scholar_crawler/main.py`。输出位于 `google_scholar_crawler/results/`。验证命令：`python -m unittest discover -s google_scholar_crawler -p 'test_*.py'` 和 `node google_scholar_crawler/test_frontend.cjs`。
3. 使用 [favicon-generator](https://redketchup.io/favicon-generator)生成favicon（网页icon文件），并下载所有文件到 `REPO/images`。
4. 修改主页配置文件[_config.yml](../_config.yml):
   1. `title`: 主页标题
   2. `description`: 主页的描述
   3. `repository`: USER_NAME/REPO_NAME
   4. `google_analytics_id` (可选的): 谷歌Analytics ID
   5. SEO相关的键值 (可选的): 从搜索引擎的控制台里获得对应的ID (例如：Google, Bing and Baidu)，然后粘贴到这里。
   6. `author`: 主页作者信息，包括其他网页、Email、所在城市、大学等。
   7. `google_scholar_stats_use_cdn`: 使用CDN读取存储于 `https://raw.githubusercontent.com/`的google scholar引用统计数据，防止中国大陆地区被墙无法访问的情况。但是CDN有缓存，因此 `google_scholar_stats_use_cdn : True`时，引用数据更新会有延迟。
   8. 更多的配置信息在注释中有详细描述。
5. 将你的主页内容添加到 [_pages/about.md](../_pages/about.md).
6. 你的主页将会被部署到 `https://USERNAME.github.io`.

## 本地调试

1. 使用 `git clone`将本项目克隆到本地。
2. 安装Jekyll的构建环境，包括 `Ruby`、`RubyGems`、`GCC`和 `Make`。可参考[该教程](https://jekyllrb.com/docs/installation/#requirements)。
3. 运行 `bash run_server.sh` 来启动Jekyll实时重载服务器。
4. 在浏览器里打开 [http://127.0.0.1:4000](http://127.0.0.1:4000)。如果你修改了网页的源码，服务器会自动重新编译并刷新页面。
5. 当你修改完毕你的页面以后, 使用 `git`命令，`commit`你的改动并 `push`到你的github仓库中。

# Acknowledges

- AcadHomepage incorporates Font Awesome, which is distributed under the terms of the SIL OFL 1.1 and MIT License.
- AcadHomepage is influenced by the github repo [mmistakes/minimal-mistakes](https://github.com/mmistakes/minimal-mistakes), which is distributed under the MIT License.
- AcadHomepage is influenced by the github repo [academicpages/academicpages.github.io](https://github.com/academicpages/academicpages.github.io), which is distributed under the MIT License.
