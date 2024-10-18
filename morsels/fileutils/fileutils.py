import io
import json
import os



def last_lines(filepath, encoding=None):
    with open(filepath, 'rb') as f:
        f.seek(0, os.SEEK_END)
        eof = f.tell()
        pos = eof
        prev_line = b''
        buffer_size = io.DEFAULT_BUFFER_SIZE
        while pos > 0:
            pos = pos - buffer_size
            if pos < 0:
                buffer_size = f.tell() - buffer_size
                pos = 0
            f.seek(pos)
            line = f.read(buffer_size) + prev_line
            if encoding is None:
                encoding = json.detect_encoding(line)
            index = line.index(b'\n') + 1 if b'\n' in line else None
            if index is not None:
                if pos == 0 and f.tell() == eof:
                    prev_line = b''
                else:
                    prev_line = line[:index]
                    line = line[index:]
            else:
                prev_line = b''
            for i in line.splitlines(keepends=True)[::-1]:
                yield i.decode(encoding)
        if prev_line:
            yield prev_line.decode(encoding)
