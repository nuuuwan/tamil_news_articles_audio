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
        www = WWW(self.article.url_text)
        www.write()
        data = JSONFile(www.local_path).read()
        return data['lines_en']

    @property
    def translated_words(self):
        www = WWW(self.article.url_text)
        www.write()
        data = JSONFile(www.local_path).read()
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
                    ),
                    zip(self.article.body_lines, self.translated_lines),
                )
            ),
        )

    def render_vocab_table(self):
        tr_list = list(
            map(
                lambda x: _(
                    'tr',
                    [
                        _('td', x[0], {'class': 'lang-ta'}),
                        _('td', x[1], {'class': 'lang-en'}),
                    ],
                ),
                zip(self.article.words, self.translated_words),
            )
        )
        return _(
            'table',
            [
                _('tbody', tr_list),
            ],
        )

    def render_body(self):
        article = self.article
        return _(
            'body',
            [
                _('div', [_('time', article.time_str)]),
                _('a', article.url, dict(href=article.url)),
                _('h1', article.title, {'class': 'lang-ta'}),
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
                _('h2', 'Vocabulary', {'class': 'lang-ta'}),
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


if __name__ == '__main__':
    ArticlePage('c66fc173').render_and_save()
