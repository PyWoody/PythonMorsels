import re


def tags_equal(tag1, tag2):
    tag1 = tag1.lower().replace('<', '').replace('>', '')
    tag2 = tag2.lower().replace('<', '').replace('>', '')
    if tag1 == tag2:
        return True
    if tag1.split()[0] == tag2.split()[0]:
        return str_to_attrs(tag1) == str_to_attrs(tag2)
    return False


def str_to_attrs(string):
    attrs_re = re.compile(r'\s?(\w+)=([_a-z0-9]*)\s?')
    attrs_ws_re = re.compile(r'''\s?(\w+)=(?:'|")([_a-z0-9\s]*)(?:'|")''')
    output = dict()
    bad_chars = ['"', "'", '=']
    for match in attrs_re.finditer(string):
        key, value = match.groups()
        if key and value and key not in output:
            output[key] = value
    for match in attrs_ws_re.finditer(string):
        key, value = match.groups()
        if key not in output:
            output[key] = value
    for tag in string.split():
        if tag not in output and not any(i in tag for i in bad_chars):
            output[tag] = None
    return output


# print(tags_equal("<img src=cats.jpg height=40>", "<IMG SRC=cats.jpg height=40>"))
# # True
# print(tags_equal("<img src=dogs.jpg width=99>", "<img src=dogs.jpg width=20>"))
# # False
# print(tags_equal("<p>", "<P>"))
# # True
# print(tags_equal("<b>", "<p>"))
# # False
# print(tags_equal('<img height=200 width=400>', '<img width=400 height=200>'))
# # True
# print(tags_equal("<LABEL FOR=id_email for=id_username>", "<LABEL FOR=id_email>"))
# True
# print(tags_equal("<LABEL FOR=id_email for=id_username>", "<LABEL FOR=id_username>"))
# # False
# print(tags_equal('<img type=checkbox checked>', '<Img type=checkbox>'))
# False
# print(tags_equal('<input type=checkbox checked>', '<input checked type=checkbox>'))
# # True
# print(tags_equal('<input type="text">', '<input type=text>'))
# # True
print(tags_equal('<input type=text placeholder=\'Hi there\' value="Hi friend">', '<input type=text value="Hi friend" placeholder="Hi there">'))
# True
