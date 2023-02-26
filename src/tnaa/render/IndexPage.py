from utils import Log
from utils.xmlx import _

from tnaa import TNAArticle, TNALibrary
from tnaa.render.ArticlePage import ArticlePage
from tnaa.render.BasePage import BasePage

log = Log('IndexPage')


class IndexPage(BasePage):
    @property
    def file_name_only(self):
        return 'index'

    @property
    def articles(self):
        summary_list = TNALibrary().summary_tamil_articles
        articles = []
        for summary in summary_list:
            hash = summary['hash']
            article = TNAArticle.from_hash(hash)
            if article.remote_exists:
                log.info(f'{hash}: exists')
                articles.append(article)
                break
            else:
                log.debug(f'{hash}: does not exist. Skippiing.')
        return articles

    def render_article_list_item(self, article):
        ArticlePage(article.hash).render_and_save()

        return _(
            'li',
            [
                _(
                    'div',
                    [
                        _('span', article.time_str + ' '),
                        _(
                            'a',
                            article.title,
                            dict(href=article.hash + '.htm'),
                        ),
                    ],
                )
            ],
        )

    def render_article_list(self):
        return _(
            'ul',
            list(
                map(
                    lambda article: self.render_article_list_item(article),
                    self.articles,
                )
            ),
        )

    def render_body(self):
        return _(
            'body',
            [
                _('h1', 'Tamil News Article Audio'),
                self.render_article_list(),
            ],
        )
