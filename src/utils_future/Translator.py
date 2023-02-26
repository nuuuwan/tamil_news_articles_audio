from functools import cache

from deep_translator import GoogleTranslator
from utils import Log

log = Log('Translator')


class Translator:
    def __init__(self, source, target):
        self.source = source
        self.target = target
        self.translator = GoogleTranslator(source, target)

    @cache
    def translate(self, text):
        try:
            translated_text = self.translator.translate(text)
            log.debug(f'"{text}" -> "{translated_text}"')
            return translated_text
        except Exception as e:
            log.warning(e)
            return text
