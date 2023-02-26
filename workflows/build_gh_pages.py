import os

from utils import Directory, Log
from utils.xmlx import _

from tnaa import TRANSLATOR, TNAArticle, TNALibrary

log = Log('build_gh_pages')
DIR_TMP = '/tmp/tnaa'

STYLE = '''
body {
    font-family: Futura;
    width: 600px;
    margin: auto;
}

a {
    text-decoration: none;
}

a:hover {
    color: orange;
}

audio {
    width: 300px;
}

.lang-en {
    color: lightgray;
}

'''


def build_article(hash, article):
    paragraph_list = []
    for i, line in enumerate(article.script_lines):
        paragraph_list.append(_('p', line))
        translated_line = TRANSLATOR.translate(line)
        paragraph_list.append(_('p', translated_line, {'class': 'lang-en'}))

    div_article = _(
        'div',
        [
            _('h1', str(article.title)),
            _('h2', str(article.title_en), {'class': 'lang-en'}),
            _(
                'audio',
                [
                    _(
                        'source',
                        None,
                        dict(src=article.url_audio, type='audio/mp3'),
                    ),
                ],
                dict(controls=True),
            ),
        ]
        + paragraph_list,
    )

    html_path = os.path.join(DIR_TMP, f'{hash}.htm')
    html = _(
        'html',
        [
            _(
                'head',
                [
                    _('title', 'Tamil News Article Audio'),
                    _('meta', None, dict(charset='utf-8')),
                    _('style', STYLE),
                ],
            ),
            _('body', [div_article]),
        ],
    )
    html.store(html_path)
    log.info(f'\tWrote {html_path}')


def build_index():
    Directory(DIR_TMP).mkdir()

    summary_list = TNALibrary().summary_tamil_articles
    n = len(summary_list)
    body_content_list = []

    body_content_list.append(_('h1', 'Tamil News Article Audio'))
    for i, summary in enumerate(summary_list):
        hash = summary['hash']
        log_prefix = f'{i+1}/{n} {hash}.'
        article = TNAArticle.from_hash(hash)
        
        if not article.remote_exists:
            log.debug(f'{log_prefix} Not yet built. Skipping')
            continue
        

        log.debug(f'{log_prefix} Building...')

        href = f'{hash}.htm'
        div_article = _(
            'ul',
            [
                _(
                    'li',
                    [
                        _(
                            'a',
                            [
                                _('span', str(article.title)),
                                
                            ],
                            dict(href=href),
                        ),
                        _(
                            'span',
                            f' ({article.title_en})',
                            {'class': 'lang-en'},
                        ),
                    ],
                ),
            ],
        )
        body_content_list.append(div_article)

        build_article(hash, article)

    html_path = os.path.join(DIR_TMP, 'index.htm')
    html = _(
        'html',
        [
            _(
                'head',
                [
                    _('title', 'Tamil News Article Audio'),
                    _('meta', None, dict(charset='utf-8')),
                    _('style', STYLE),
                ],
            ),
            _('body', body_content_list),
        ],
    )
    html.store(html_path)
    log.info(f'\tWrote {html_path}')


if __name__ == '__main__':
    build_index()

