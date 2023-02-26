from utils import Log

from tnaa import TNAArticle, TNALibrary

log = Log('build_text_and_audio')
MAX_NEW_ARTICLES_PER_RUN = 1


def main():
    summary_list = TNALibrary().summary_tamil_articles
    n = len(summary_list)
    i_new = 0
    for i, summary in enumerate(summary_list):
        hash = summary['hash']
        log.info(f'{i+1}/{n} {hash}.')

        article = TNAArticle.from_hash(hash)
        if article.remote_exists:
            log.debug('\tAlready built.')
            continue

        log.debug('\tBuilding...')

        article.save_text()
        article.save_audio()
        article.save_audio_vocab()

        log.debug('\tComplete.')

        i_new += 1
        if i_new >= MAX_NEW_ARTICLES_PER_RUN:
            break


if __name__ == '__main__':
    main()
