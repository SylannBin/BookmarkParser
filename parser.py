import re
import html
import pprint


class Bookmark(object):
    TYPE_TITLE = 'Title'
    TYPE_LINK = 'Link'

    def __init__(self, content):
        self.bookmarks = dict(name='Bookmark bar', children=[], parent=None)
        self.content = content
        self.depth = 0
        self.current_line = None
        self.current_parent = self.bookmarks
        self.parsed = False
        self.pprint = pprint.PrettyPrinter(indent=2).pprint

    def parse(self):
        for line in self.content:
            self.current_line = line
            self._resolve_behavior()
        self.parsed = True

    def show(self):
        if not self.parsed:
            print("Bookmarks were not parsed yet. Be sure to execute parse before.")
        else:
            self.pprint(self.bookmarks)

    def _resolve_behavior(self):
        if (self._is_group_start()):
            self._descend()
        elif (self._is_group_end()):
            self._ascend()
        elif (self._is_title()):
            self._add_title()
        elif (self._is_link()):
            self._add_link()

    def _descend(self):
        self.depth += 1

    def _ascend(self):
        self.depth -= 1
        self.current_parent = self.current_parent['parent']

    def _add_title(self):
        self.current_line = html.unescape(self.current_line)
        title = self._get_title_name()
        if not title:
            raise ValueError("Unreckognized title")
        new_parent = dict(
            name=title,
            type=self.TYPE_TITLE,
            created=self._get_add_date(),
            updated=self._get_last_modified(),
            depth=self.depth,
            children=[],
            parent=self.current_parent
        )
        self.current_parent['children'].append(new_parent)
        self.current_parent = new_parent

    def _add_link(self):
        new_link = dict(
            name=self._get_link_name(),
            type=self.TYPE_LINK,
            link=self._get_link_href(),
            created=self._get_add_date(),
            depth=self.depth,
            parent=self.current_parent
        )
        self.current_parent['children'].append(new_link)

    def _get_add_date(self):
        found = re.search('ADD_DATE="(\d+)"', self.current_line)
        return found.group(1) if found else None

    def _get_last_modified(self):
        found = re.search('LAST_MODIFIED="(\d+?)"', self.current_line)
        return found.group(1) if found else None

    def _get_link_href(self):
        found = re.search('HREF="(.+?)"', self.current_line)
        return found.group(1) if found else None

    def _get_title_name(self):
        found = re.search('">(.+?)</H3>', self.current_line)
        return found.group(1) if found else None

    def _get_link_name(self):
        found = re.search('">(.+?)</A>', self.current_line)
        return found.group(1) if found else None

    def _is_group_start(self):
        return self.current_line.lstrip().startswith('<DL><p>')

    def _is_group_end(self):
        return self.current_line.lstrip().startswith('</DL><p>')

    def _is_title(self):
        return self.current_line.lstrip().startswith('<DT><H3')

    def _is_link(self):
        return self.current_line.lstrip().startswith('<DT><A')
