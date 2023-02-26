import os
from utils import Log, Directory
from utils.xmlx import _
from tnaa.render.STYLE import STYLE

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
                _('title', 'Tamil News Article Audio'),
                _('meta', None, dict(charset='utf-8')),
                _('style', STYLE),
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

    def render_and_save(self):
        Directory(DIR_BASE).mkdir()

        html = self.render_html()
        index_path = os.path.join(DIR_BASE, self.file_name_only + ".htm")
        html.store(index_path)
        log.debug('Saved ' + index_path)
