from utils import Log

from tnaa import TNAArticle, TNALibrary

log = Log('build_text_and_audio')
MAX_NEW_ARTICLES_PER_RUN = 3


def main():
    summary_list = TNALibrary().summary_tamil_articles
    n = len(summary_list)
    i_new = 0
    for i, summary in enumerate(summary_list):
        article = TNAArticle.from_hash(summary['hash'])
        article.save_text()
        article.save_audio()
        log.info(f'{i+1}/{n} {article.title} complete.')

        i_new += 1
        if i_new >= MAX_NEW_ARTICLES_PER_RUN:
            break


if __name__ == '__main__':
    main()
