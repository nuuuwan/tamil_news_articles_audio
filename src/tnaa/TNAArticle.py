import os
from dataclasses import dataclass
from functools import cached_property

from deep_translator import GoogleTranslator
from gtts import gTTS
from pydub import AudioSegment
from utils import (TIME_FORMAT_TIME, WWW, Directory, File, JSONFile, Log, Time,
                   hashx)

URL_BASE = os.path.join(
    'https://raw.githubusercontent.com', 'nuuuwan/news_lk3_data/main'
)
DIR_DATA = os.path.join('/tmp')
LANG = 'ta'

log = Log('TNAArticle')


TRANSLATOR = GoogleTranslator(source='ta', target='en')

WORD_HASH_LENGTH = 6


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

    @cached_property
    def title_en(self):
        return TRANSLATOR.translate(self.title)

    @staticmethod
    def from_hash(hash):
        url = os.path.join(URL_BASE, f'{hash}.json')
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
    def file_base(self):
        return f'/tmp/tnaa.{self.hash}'

    @property
    def script_lines(self):
        return [self.title] + self.body_lines

    @property
    def words(self):
        content = ' '.join(self.script_lines)
        words = content.split(' ')
        cleaned_words = [clean_word(word) for word in words]
        cleaned_words = [word for word in cleaned_words if len(word) >= 1]        
        return list(sorted(set(cleaned_words)))

    @property
    def url_text(self):
        return os.path.join(
            'https://raw.githubusercontent.com',
            'nuuuwan/tamil_news_articles_audio/data',
            f'tnaa.{self.hash}/article.txt',
        )

    @property
    def url_audio(self):
        return os.path.join(
            'https://raw.githubusercontent.com',
            'nuuuwan/tamil_news_articles_audio/data',
            f'tnaa.{self.hash}/audio/article.mp3',
        )

    @property
    def url_audio_vocab(self):
        return os.path.join(
            'https://raw.githubusercontent.com',
            'nuuuwan/tamil_news_articles_audio/data',
            f'tnaa.{self.hash}/audio/vocab.mp3',
        )

    @property
    def remote_exists(self):
        return WWW(self.url_text).exists

    def save_text(self):
        Directory(self.file_base).mkdir()

        text_file = File(os.path.join(self.file_base, 'article.txt'))
        if text_file.exists:
            log.debug(f'Already exists {text_file.path}')
            return

        lines = '\n\n'.join(self.script_lines)
        text_file.write(lines)
        log.debug(f'Saved {text_file.path}')

    def save_audio(self):
        Directory(self.file_base).mkdir()

        dir_audio = os.path.join(self.file_base, 'audio')
        all_path = os.path.join(dir_audio, 'article.mp3')

        if os.path.exists(all_path):
            log.debug(f'Already exists {all_path}')
            return

        Directory(dir_audio).mkdir()

        audio_segment = AudioSegment.empty()
        n = len(self.script_lines)
        for i, line in enumerate(self.script_lines):
            item_path = os.path.join(
                dir_audio, f'article-para-{i:04d}-ta.mp3'
            )
            if os.path.exists(item_path):
                continue

            tts = gTTS(line, lang=LANG)
            tts.save(item_path)
            log.debug(f'{i+1}/{n} Saved {item_path}')

            item_audio_segment = AudioSegment.from_mp3(item_path)
            audio_segment += item_audio_segment

            # ---

            item_en_path = os.path.join(
                dir_audio, f'article-para-{i:04d}-en.mp3'
            )
            if os.path.exists(item_en_path):
                continue

            translated_line = TRANSLATOR.translate(line)
            tts = gTTS(translated_line, lang='en')
            tts.save(item_en_path)
            log.debug(f'{i+1}/{n} Saved {item_en_path}')

            item_en_audio_segment = AudioSegment.from_mp3(item_en_path)
            audio_segment += item_en_audio_segment

        audio_segment.export(all_path, format='mp3')
        log.info(f'Saved {all_path}')

    def save_audio_vocab(self):
        Directory(self.file_base).mkdir()

        dir_audio = os.path.join(self.file_base, 'audio')
        dir_vocab = os.path.join(self.file_base, 'vocab')
        all_path = os.path.join(dir_audio, 'vocab.mp3')

        if os.path.exists(all_path):
            log.debug(f'Already exists {all_path}')
            return

        Directory(dir_audio).mkdir()
        Directory(dir_vocab).mkdir()

        audio_segment = AudioSegment.empty()
        words = self.words
        n = len(words)
        for i, word in enumerate(words):
            if not word:
                continue

            word_ta_hash = hashx.md5(word)[:WORD_HASH_LENGTH]
            item_path = os.path.join(
                dir_vocab, f'vocab-word-{word_ta_hash}-ta.mp3'
            )
            if os.path.exists(item_path):
                continue

            tts = gTTS(word, lang=LANG)
            tts.save(item_path)
            log.debug(f'{i+1}/{n} Saved {item_path}')

            item_audio_segment = AudioSegment.from_mp3(item_path)
            audio_segment += item_audio_segment

            # ---
            translated_word = TRANSLATOR.translate(word)
            if not translated_word:
                continue
            word_en_hash = hashx.md5(translated_word)[:WORD_HASH_LENGTH]
            item_en_path = os.path.join(
                dir_audio, f'vocab-word-{word_en_hash}-en.mp3'
            )
            if os.path.exists(item_en_path):
                continue

            tts = gTTS(translated_word, lang='en')
            tts.save(item_en_path)
            log.debug(f'{i+1}/{n} Saved {item_en_path}')

            item_en_audio_segment = AudioSegment.from_mp3(item_en_path)
            audio_segment += item_en_audio_segment

        audio_segment.export(all_path, format='mp3')
        log.info(f'Saved {all_path}')
