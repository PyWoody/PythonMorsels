import re

from collections import UserList


class parse_bullets:

    def __init__(self, data):
        self.ws = re.compile(r'^\s+')
        self.lines = data.splitlines()
        self.index = 0
        self.root = Bullet('')
        self.build(self.root)

    def __str__(self):
        output = []
        for child in self:
            output.append(f'- {child.text}')
            if child.children:
                output.append(''.join(to_str(child.children)))
            output.append('\n')
        return ''.join(output).strip()

    def __len__(self):
        return len(self.root.children)

    def __iter__(self):
        yield from self.root.children

    def __getitem__(self, index):
        return self.root.children[index]

    def build(self, node, parents=None):
        if parents is None:
            parents = []
        bullet = Bullet(
            self.lines[self.index],
            parent=node if node is not self.root else None
        )
        node.children.append(bullet)
        if self.index + 1 < len(self.lines):
            curr_match = self.ws.search(self.lines[self.index])
            curr_ident = len(curr_match.group()) // 4 if curr_match else 0
            self.index += 1
            next_match = self.ws.search(self.lines[self.index])
            next_ident = len(next_match.group()) // 4 if next_match else 0
            if next_ident == 0:
                self.build(self.root)
            elif next_ident > curr_ident:
                _parents = list(parents)
                _parents.append(node)
                self.build(bullet, parents=_parents)
            elif next_ident == curr_ident:
                self.build(node, parents=parents)
            else:
                _ = parents.pop()
                self.build(parents[-1])


class Bullet:

    def __init__(self, text, parent=None):
        self.text = str(text).lstrip('- ')
        self.children = Children()
        self.parent = parent

    def __str__(self):
        return f'- {self.text}{"".join(to_str(self.children))}'


class Children(UserList):

    def __init__(self, children=None):
        if children is None:
            children = []
        self.data = list(children)

    def __str__(self):
        return f'{"".join(to_str(self.data, indent=""))}'.strip()


def to_str(children, indent='    '):
    for child in children:
        yield f'\n{indent}- {child.text}'
        if child.children:
            yield from to_str(child.children, indent=indent + ' ' * 4)
