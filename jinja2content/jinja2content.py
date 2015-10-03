import logging
import os

from pelican import signals

from jinja2 import Environment, ChoiceLoader, FileSystemLoader
from pelican.readers import MarkdownReader
from pelican.utils import pelican_open

_LOGGER = logging.getLogger(__name__)


class JinjaMarkdownReader(MarkdownReader):
    def parse_jinja(self, text):
        base_path = os.path.dirname(os.path.abspath(__file__))
        jinja2_env = Environment(
            trim_blocks=True,
            lstrip_blocks=True,
            loader=ChoiceLoader([
                FileSystemLoader(
                    os.path.join(base_path, self.settings['THEME'], 'templates')
                ),
            ]),
            extensions=self.settings['JINJA_EXTENSIONS'],
        )

        return jinja2_env.from_string(text).render(self.settings)

    def read(self, source_path):
        _, metadata = super(JinjaMarkdownReader, self).read(source_path)

        with pelican_open(source_path) as text:
            content = self._md.convert(self.parse_jinja(text))

        return content, metadata


def add_reader(readers):
    readers.reader_classes['md'] = JinjaMarkdownReader


def register():
    signals.readers_init.connect(add_reader)
