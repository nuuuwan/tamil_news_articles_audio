import os

from utils import Directory, Log
from utils.xmlx import _

DIR_BASE = os.path.join('/tmp', 'tnaa')

log = Log('BasePage')


class BasePage:
    @property
    def file_name_only(self):
        raise NotImplementedError

    def render_head(self):
        return _(
            'head',
            [
                _('title', 'Tamil News Articles'),
                _('meta', None, dict(charset='utf-8')),
                _('link', None, dict(rel='stylesheet', href='style.css')),
            ],
        )

    def render_body(self):
        raise NotImplementedError

    def render_html(self):
        return _(
            'html',
            [
                self.render_head(),
                self.render_body(),
            ],
        )

    @staticmethod
    def copy_css():
        source = 'src/tnaa/render/style.css'
        target = os.path.join(DIR_BASE, 'style.css')
        os.system(f'cp "{source}" "{target}"')

    def render_and_save(self):
        Directory(DIR_BASE).mkdir()
        BasePage.copy_css()

        html = self.render_html()
        index_path = os.path.join(DIR_BASE, self.file_name_only + ".htm")
        html.store(index_path)
        log.debug('Saved ' + index_path)
