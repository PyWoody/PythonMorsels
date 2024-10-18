from textwrap import dedent


import csv


def condense_csv(text, id_name=None):
    output = []
    data = [
        [r.strip() if ',' not in r else f'"{r.strip()}"' for r in row]
        for row in csv.reader(text.splitlines())
    ]
    id_name, header = build_header(data, id_name=id_name)
    output.append(','.join(header))
    row_data = dict.fromkeys(header, '')
    row_data[id_name] = data[0][0]
    for row in data:
        if row[0] != row_data[id_name]:
            output.append(','.join(row_data.values()))
            row_data = dict.fromkeys(header, '')
            row_data[id_name] = row[0]
        row_data[row[1]] = row[2]
    output.append(','.join(row_data.values()))
    return '\n'.join(output)


def build_header(data, id_name=None):
    header = []
    if id_name is None:
        id_name = data[0][0]
        header.append(id_name)
        _ = data.pop(0)
    else:
        header.append(id_name)
    for row in data:
        if row[1] not in header:
            header.append(row[1])
    return id_name, header

text = """\
 ball,color,purple
 ball,size,4
 ball,notes,it's round
 cup,color,blue
 cup,size,1
 cup,notes,none"""


condense_csv(text, id_name='object')
print('*' * 80)
text = """\
object,property,value
ball,color,purple
ball,size,4
ball,notes,it's round
cup,color,blue
cup,size,1
cup,notes,none"""
condense_csv(text)


text = dedent("""
    01,Artist,Otis Taylor
    01,Title,Ran So Hard the Sun Went Down
    01,Time,3:52
    02,Artist,Waylon Jennings
    02,Title,Honky Tonk Heroes (Like Me)
    02,"Time","3:29"
    03,Artist,David Allan Coe
    03,Title,"Willie, Waylon, And Me"
    03,Time,3:26
""").strip()
expected = dedent("""
    Track,Artist,Title,Time
    01,Otis Taylor,Ran So Hard the Sun Went Down,3:52
    02,Waylon Jennings,Honky Tonk Heroes (Like Me),3:29
    03,David Allan Coe,"Willie, Waylon, And Me",3:26
""").strip()
wtf = condense_csv(text, id_name='Track')
breakpoint()
assert condense_csv(text, id_name='Track') ==  expected
