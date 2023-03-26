from utils import Log
from utils.xmlx import _

from tnaa import TNAArticle, TNALibrary
from tnaa.render.ArticlePage import ArticlePage
from tnaa.render.BasePage import BasePage

log = Log('IndexPage')
MAX_ARTICLES_IN_INDEX = 100


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
            try:
                article = TNAArticle.from_hash(hash)
            except BaseException:
                log.error(f'{hash}: Error while accessing. Skipping.')

            if article.remote_exists:
                log.info(f'{hash}: exists')
                articles.append(article)
                if len(articles) >= MAX_ARTICLES_IN_INDEX:
                    break
            else:
                log.debug(f'{hash}: does not exist. Skippiing.')
        return articles

    def render_article_list_item(self, article):
        ArticlePage(article.hash).render_and_save()
        return ArticlePage.render_article_header(article)

    def render_article_list(self):
        return _(
            'div',
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
                _('h1', 'Tamil News Articles'),
                self.render_article_list(),
            ],
        )
