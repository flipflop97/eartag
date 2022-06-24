# file.py
#
# Copyright 2022 knuxify
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE X CONSORTIUM BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Except as contained in this notice, the name(s) of the above copyright
# holders shall not be used in advertising or otherwise to promote the sale,
# use or other dealings in this Software without prior written
# authorization.

from gi.repository import GObject
import taglib

class EartagFile(GObject.Object):
    """GObject wrapper that provides information about a file."""
    __gtype_name__ = 'EartagFile'

    handled_properties = ['title', 'artist', 'album', 'albumartist', 'comment']
    _is_modified = False

    def __init__(self, path):
        """Initializes an EartagFile for the given file path."""
        super().__init__()
        try:
            self.tl_file = taglib.File(path)
        except OSError:
            # TODO: display some kind of user-friendly warning about this
            raise ValueError

        for prop in self.handled_properties:
            self.notify(prop)
        self.notify('is_modified')

    def save(self):
        """Saves the changes to the file."""
        self.tl_file.save()
        self._is_modified = False
        self.notify('is_modified')

    def set_modified(self):
        self._is_modified = True
        self.notify('is_modified')

    @GObject.Property(type=bool, default=False)
    def is_modified(self):
        """Returns whether the values have been modified or not."""
        return self._is_modified

    # GObject properties

    @GObject.Property(type=str)
    def title(self):
        if 'TITLE' in self.tl_file.tags:
            return self.tl_file.tags['TITLE'][0]
        return ''

    @title.setter
    def set_title(self, value):
        self.tl_file.tags['TITLE'] = [value]
        self.set_modified()

    @GObject.Property(type=str)
    def artist(self):
        if 'ARTIST' in self.tl_file.tags:
            return self.tl_file.tags['ARTIST'][0]
        return ''

    @artist.setter
    def set_artist(self, value):
        self.tl_file.tags['ARTIST'] = [value]
        self.set_modified()

    @GObject.Property(type=str)
    def album(self):
        if 'ALBUM' in self.tl_file.tags:
            return self.tl_file.tags['ALBUM'][0]
        return ''

    @album.setter
    def set_album(self, value):
        self.tl_file.tags['ALBUM'] = [value]
        self.set_modified()

    @GObject.Property(type=str)
    def albumartist(self):
        if 'ALBUMARTIST' in self.tl_file.tags:
            return self.tl_file.tags['ALBUMARTIST'][0]
        return ''

    @albumartist.setter
    def set_albumartist(self, value):
        self.tl_file.tags['ALBUMARTIST'] = [value]
        self.set_modified()

    @GObject.Property(type=str)
    def comment(self):
        if 'COMMENT' in self.tl_file.tags:
            return self.tl_file.tags['COMMENT'][0]
        return ''

    @comment.setter
    def set_comment(self, value):
        self.tl_file.tags['COMMENT'] = [value]
        self.set_modified()
