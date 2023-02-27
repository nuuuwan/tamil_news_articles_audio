from utils import WWW, JSONFile
from utils.xmlx import _

from tnaa import TNAArticle
from tnaa.render.BasePage import BasePage


class ArticlePage(BasePage):
    def __init__(self, hash):
        self.hash = hash

    @property
    def article(self):
        return TNAArticle.from_hash(self.hash)

    @property
    def file_name_only(self):
        return self.hash

    @property
    def translated_lines(self):
        data = JSONFile(WWW(self.article.url_text).download()).read()
        return data['lines_en']

    @property
    def translated_words(self):
        data = JSONFile(WWW(self.article.url_text).download()).read()
        return data['words_en']

    def render_lines(self):
        return _(
            'div',
            list(
                map(
                    lambda x: _(
                        'div',
                        [
                            _('p', x[0], {'class': 'lang-ta'}),
                            _('p', x[1], {'class': 'lang-en'}),
                        ],
                        {'class': 'article-line'},
                    ),
                    zip(self.article.lines, self.translated_lines),
                )
            ),
        )

    def render_vocab_table(self):
        tr_list = list(
            map(
                lambda x: _(
                    'tr',
                    [
                        _('td', str(x[0] + 1), {'class': 'lang-en'}),
                        _('td', x[1][0], {'class': 'lang-ta'}),
                        _('td', x[1][1], {'class': 'lang-en'}),
                    ],
                ),
                enumerate(zip(self.article.words, self.translated_words)),
            )
        )
        return _(
            'table',
            [
                _('tbody', tr_list),
            ],
        )

    @staticmethod
    def render_article_header(article):
        return _(
            'div',
            [
                _('div', [_('time', article.time_str)]),
                _(
                    'a',
                    article.url,
                    {'class': 'article-url', 'href': article.url},
                ),
                _(
                    'a',
                    [
                        _('h1', article.title, {'class': 'lang-ta'}),
                    ],
                    {'class': 'article-title', 'href': article.hash + '.htm'},
                ),
            ],
            {'class': 'article-header'},
        )

    def render_body(self):
        article = self.article
        return _(
            'body',
            [
                ArticlePage.render_article_header(article),
                _(
                    'audio',
                    [
                        _(
                            'source',
                            None,
                            dict(
                                src=article.url_article_audio,
                                type='audio/mpeg',
                            ),
                        ),
                    ],
                    dict(controls=True),
                ),
                self.render_lines(),
                _('h2', 'சொல்லகராதி', {'class': 'lang-ta'}),
                _('h2', 'Vocabulary', {'class': 'lang-en'}),
                _(
                    'audio',
                    [
                        _(
                            'source',
                            None,
                            dict(
                                src=article.url_vocab_audio, type='audio/mpeg'
                            ),
                        ),
                    ],
                    dict(controls=True),
                ),
                self.render_vocab_table(),
            ],
        )
