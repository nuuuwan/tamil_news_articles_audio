from utils import Log

from tnaa import TNAArticle, TNALibrary

log = Log('build_text_and_audio')


def main():
    summary_list = TNALibrary().summary_tamil_articles
    n = len(summary_list)
    for i, summary in enumerate(summary_list):
        article = TNAArticle.from_hash(summary['hash'])
        article.save_text()
        article.save_audio()
        log.info(f'{i+1}/{n} {article.title} complete.')


if __name__ == '__main__':
    main()
