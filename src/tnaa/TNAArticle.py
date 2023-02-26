import os
from dataclasses import dataclass

from gtts import gTTS
from pydub import AudioSegment
from utils import WWW, Directory, File, JSONFile, Log

URL_BASE = os.path.join(
    'https://raw.githubusercontent.com', 'nuuuwan/news_lk3_data/main'
)
DIR_DATA = os.path.join('/tmp')
LANG = 'ta'

log = Log('TNAArticle')


def clean_word(x):
    return x


@dataclass
class TNAArticle:
    hash: str
    title: str
    body_lines: list

    @staticmethod
    def from_hash(hash):
        url = os.path.join(URL_BASE, f'{hash}.json')
        www = WWW(url)
        www.write()
        d = JSONFile(www.local_path).read()
        return TNAArticle(hash, d['original_title'], d['original_body_lines'])

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
        return list(sorted(set(cleaned_words)))

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
            item_path = os.path.join(dir_audio, f'article-para-{i:04d}.mp3')
            if os.path.exists(item_path):
                continue

            tts = gTTS(line, lang=LANG)
            tts.save(item_path)
            log.debug(f'{i+1}/{n} Saved {item_path}')

            item_audio_segment = AudioSegment.from_mp3(item_path)
            audio_segment += item_audio_segment

        audio_segment.export(all_path, format='mp3')
        log.info(f'Saved {all_path}')


if __name__ == '__main__':
    article = TNAArticle.from_hash('1550a0ed')
    article.save_text()
    article.save_audio()
