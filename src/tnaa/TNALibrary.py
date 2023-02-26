import os
from functools import cached_property

from utils import WWW, TSVFile, hashx

URL_SUMMARY = os.path.join(
    'https://raw.githubusercontent.com',
    'nuuuwan/news_lk3_data/main/reports/summary.tsv',
)
HASH_SALT = '123019839120398'
HASH_LENGTH = 8


class TNALibrary:
    @cached_property
    def summary(self):
        www = WWW(URL_SUMMARY)
        www.write()
        d_list = TSVFile(www.local_path).read()
        # hack - add hash
        for d in d_list:
            hash = hashx.md5(d['url'] + HASH_SALT)[:HASH_LENGTH]
            d['hash'] = hash

        return d_list

    @cached_property
    def summary_tamil_articles(self):
        return [x for x in self.summary if x['original_lang'] == 'ta']


if __name__ == '__main__':
    print(TNALibrary().summary_tamil_articles)
