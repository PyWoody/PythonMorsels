import itertools

from collections import UserList


class BulletList:

    def __init__(self, data):
        self.data = data.splitlines()
        self.root = Bullet('')
        self.build(self.root)

    def __str__(self):
        return '\n'.join(to_str(self))

    __repr__ = __str__

    def __len__(self):
        return sum(1 for i in self.data if i.find('-') == 0)

    def __iter__(self):
        yield from self.root.children

    def __getitem__(self, index):
        if isinstance(index, slice):
            return list(itertools.islice(self, index))
        return next(itertools.islice(self, index, index+1))

    def build(self, node, *, parents=None, index=0):
        if parents is None:
            parents = []
        bullet = Bullet(
            self.data[index], parent=node if node is not self.root else None
        )
        node.children.append(bullet)
        if index + 1 < len(self.data):
            curr_indent = self.data[index].find('-')
            index += 1
            next_indent = self.data[index].find('-')
            if next_indent == -1:
                bullet.note = self.data[index]
                index += 1
                self.build(node, parents=parents, index=index)
            elif next_indent == 0:
                self.build(self.root, index=index)
            elif next_indent > curr_indent:
                _parents = list(parents)
                _parents.append(node)
                self.build(bullet, parents=_parents, index=index)
            elif next_indent == curr_indent:
                self.build(node, parents=parents, index=index)
            else:
                _ = parents.pop()
                self.build(parents[-1], index=index)

    @property
    def incomplete(self):
        return '\n'.join(to_str(self, incomplete=True))


class Bullet:

    def __init__(self, text, *, parent=None, note=None):
        self.complete = '[COMPLETE]' in text
        self.text = text.replace('[COMPLETE]', '').lstrip(' -')
        self.children = Children()
        self.parent = parent
        self.note = str(note) if note is not None else ''

    def __str__(self):
        return '\n'.join(
            [
                f'- {"[COMPLETE] " if self.complete else ""}{self.text}',
                '\n'.join(to_str(self.children, indent='    '))
            ]
        ).strip()

    __repr__ = __str__


class Children(UserList):

    def __init__(self, children=None):
        if children is None:
            children = []
        self.data = list(children)

    def __str__(self):
        return '\n'.join(to_str(self.data)).strip()

    @property
    def incomplete(self):
        return '\n'.join(to_str(self, incomplete=True))


def parse_bullets(data):
    return BulletList(data)


def to_str(bullets, indent='', incomplete=False):
    for bullet in bullets:
        if incomplete and bullet.complete:
            continue
        yield (
            f'{indent}- '
            f'{"[COMPLETE] " if bullet.complete else ""}'
            f'{bullet.text}'
        )
        if bullet.note:
            yield bullet.note
        yield from to_str(
            bullet.children, indent=indent + '    ', incomplete=incomplete
        )
