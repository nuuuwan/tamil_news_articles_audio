from utils import Log

from tnaa import TNAArticle, TNALibrary

log = Log('build_text_and_audio')
MAX_NEW_ARTICLES_PER_RUN = 1


def build_article(summary):
    hash = summary['hash']
    article = TNAArticle.from_hash(hash)
    if article.remote_exists:
        log.debug(f'{hash}: already built. skipping.')
        return False

    article.init_dirs()
    article.save_text_data()
    article.save_article_audio()
    article.save_vocab_audio()
    log.info(f'{hash}: build complete.')
    return True


def main():
    summary_list = TNALibrary().summary_tamil_articles
    i_new = 0
    for summary in summary_list:
        if build_article(summary):
            i_new += 1
            if i_new >= MAX_NEW_ARTICLES_PER_RUN:
                break


if __name__ == '__main__':
    main()
