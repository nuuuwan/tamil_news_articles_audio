import os

from gtts import gTTS
from pydub import AudioSegment
from utils import Log, hashx

HASH_LENGTH = 6
log = Log('TextToSpeech')


class TextToSpeech:
    def __init__(self, dir_tts):
        self.dir_tts = dir_tts

    def get_audio_file_path(self, text, lang):
        hash_id = hashx.md5(text)[:HASH_LENGTH]
        return os.path.join(self.dir_tts, f'{hash_id}-{lang}.mp3')

    def gen(self, text, lang):
        audio_file_path = self.get_audio_file_path(text, lang)
        if not os.path.exists(audio_file_path):
            try:
                tts = gTTS(text, lang=lang)
                tts.save(audio_file_path)
                log.debug('Saved ' + audio_file_path)
            except Exception as e:
                log.error(e)
                return AudioSegment.empty()

        return AudioSegment.from_mp3(audio_file_path)
