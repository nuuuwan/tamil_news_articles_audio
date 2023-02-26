import os

from utils import Directory, Log
from utils.xmlx import _

from tnaa import TNAArticle, TNALibrary

log = Log('build_gh_pages')
DIR_TMP = '/tmp/tnaa'


def main():
    Directory(DIR_TMP).mkdir()

    summary_list = TNALibrary().summary_tamil_articles
    n = len(summary_list)
    body_content_list = []

    body_content_list.append(_('h1', 'Tamil News Article Audio'))
    for i, summary in enumerate(summary_list):
        hash = summary['hash']
        log.info(f'{i+1}/{n} {hash}.')
        article = TNAArticle.from_hash(hash)
        try:
            if not article.remote_exists:
                log.debug('\tNot yet built. Skipping')
                break
        except BaseException:
            continue

        div_article = _(
            'div',
            [
                _('h2', str(article.title)),
                _(
                    'audio',
                    [
                        _(
                            'source',
                            None,
                            dict(src=article.url_audio, type='audio/mp3'),
                        ),
                    ],
                    dict(controls=True, style="width:300px;"),
                ),
            ],
        )
        body_content_list.append(div_article)

    html_path = os.path.join(DIR_TMP, 'index.htm')
    html = _(
        'html',
        [
            _(
                'head',
                [
                    _('title', 'Tamil News Article Audio'),
                    _('meta', None, dict(charset='utf-8')),
                ],
            ),
            _('body', body_content_list),
        ],
    )
    html.store(html_path)
    log.info(f'\tWrote {html_path}')


if __name__ == '__main__':
    main()
