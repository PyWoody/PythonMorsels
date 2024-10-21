from html.parser import HTMLParser


class Parser(HTMLParser):

    def __init__(self, *args, **kwargs):
        self.pairs = {}
        super().__init__(*args, **kwargs)

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if not attrs:
            self.pairs.setdefault(tag, {})[tag] = tag
        else:
            for _type, value in attrs:
                if _type not in self.pairs.get(tag, {}):
                    self.pairs.setdefault(tag, {})[_type] = value


def tags_equal(tag1, tag2):
    p1 = Parser()
    p1.feed(tag1)
    p2 = Parser()
    p2.feed(tag2)
    return p1.pairs == p2.pairs
