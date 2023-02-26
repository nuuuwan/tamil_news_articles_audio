from tnaa import TNAArticle, TNALibrary


def main():
    summary_list = TNALibrary().summary_tamil_articles
    for summary in summary_list:
        article = TNAArticle.from_hash(summary['hash'])
        article.save_text()
        article.save_audio()


if __name__ == '__main__':
    main()
