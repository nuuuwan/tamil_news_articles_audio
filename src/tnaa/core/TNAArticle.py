import os
from dataclasses import dataclass

from pydub import AudioSegment
from utils import TIME_FORMAT_TIME, WWW, Directory, JSONFile, Log, Time

from utils_future import TextToSpeech, Translator

URL_BASE_NEWS = os.path.join(
    'https://raw.githubusercontent.com', 'nuuuwan/news_lk3_data/main'
)
URL_BASE_TNAA = os.path.join(
    'https://raw.githubusercontent.com',
    'nuuuwan/tamil_news_articles_audio/data',
)
DIR_BASE = os.path.join('/tmp', 'tnaa')
DIR_TTS = os.path.join(DIR_BASE, 'tts')
WORD_HASH_LENGTH = 6

log = Log('TNAArticle')


def clean_word(x):
    for k in ["'", ',', '.']:
        x = x.replace(k, '')
    x = x.strip()
    return x


@dataclass
class TNAArticle:
    hash: str
    title: str
    body_lines: list
    url: str
    time_ut: int

    @staticmethod
    def from_hash(hash):
        url = os.path.join(URL_BASE_NEWS, f'{hash}.json')
        www = WWW(url)
        www.write()
        d = JSONFile(www.local_path).read()

        return TNAArticle(
            hash,
            d['original_title'],
            d['original_body_lines'],
            d['url'],
            (int)(d['time_ut']),
        )

    @property
    def time_str(self):
        return TIME_FORMAT_TIME.stringify(Time(self.time_ut))

    @property
    def dir_article(self):
        return os.path.join(DIR_BASE, self.hash)

    @property
    def lines(self):
        return [self.title] + self.body_lines

    @property
    def words(self):
        content = ' '.join(self.lines)
        words = content.split(' ')
        cleaned_words = [clean_word(word) for word in words]
        cleaned_words = [word for word in cleaned_words if len(word) >= 1]
        return list(sorted(set(cleaned_words)))

    @property
    def url_article(self):
        return os.path.join(
            URL_BASE_TNAA,
            self.hash,
        )

    @property
    def url_text(self):
        return os.path.join(
            self.url_article,
            'text.json',
        )

    @property
    def url_audio(self):
        return os.path.join(
            self.url_article,
            'article.mp3',
        )

    @property
    def url_audio_vocab(self):
        return os.path.join(
            self.url_article,
            'vocab.mp3',
        )

    @property
    def remote_exists(self):
        return WWW(self.url_text).exists

    @property
    def tts(self):
        dir_tts = os.path.join(DIR_BASE, 'tts')
        return TextToSpeech(dir_tts)

    @property
    def translator(self):
        return Translator('ta', 'en')

    def init_dirs(self):
        Directory(DIR_BASE).mkdir()
        Directory(DIR_TTS).mkdir()
        Directory(self.dir_article).mkdir()

    def save_text_data(self):
        text_file = JSONFile(os.path.join(self.dir_article, 'text.json'))
        if text_file.exists:
            log.debug(f'Already exists {text_file.path}')
            return

        lines = self.lines
        translator = self.translator
        translated_lines = [translator.translate(line) for line in lines]
        data = dict(
            lines_ta=lines,
            lines_en=translated_lines,
        )
        text_file.write(data)
        log.info(f'Saved {text_file.path}')

    def save_audio(self, lines, file_name):
        audio_path = os.path.join(self.dir_article, file_name)

        if os.path.exists(audio_path):
            log.debug(f'Already exists {audio_path}')
            return

        translator = self.translator
        tts = self.tts
        audio_segment = AudioSegment.empty()
        for line in lines:
            if len(line) == 0:
                continue
            audio_segment += tts.gen(line, 'ta')
            translated_line = translator.translate(line)
            audio_segment += tts.gen(translated_line, 'en')

        audio_segment.export(audio_path, format='mp3')
        log.info(f'Saved {audio_path}')

    def save_article_audio(self):
        return self.save_audio(self.lines, 'article.mp3')

    def save_vocab_audio(self):
        return self.save_audio(self.words, 'vocab.mp3')
