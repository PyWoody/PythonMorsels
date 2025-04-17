import re
import shutil


CHARS = {
    '0': '██████\n██  ██\n██  ██\n██  ██\n██████',
    '1': '   ██ \n  ███ \n   ██ \n   ██ \n   ██ ',
    '2': '██████\n    ██\n██████\n██    \n██████',
    '3': '██████\n    ██\n █████\n    ██\n██████',
    '4': '██  ██\n██  ██\n██████\n    ██\n    ██',
    '5': '██████\n██    \n██████\n    ██\n██████',
    '6': '██████\n██    \n██████\n██  ██\n██████',
    '7': '██████\n    ██\n   ██ \n  ██  \n  ██  ',
    '8': ' ████ \n██  ██\n ████ \n██  ██\n ████ ',
    '9': '██████\n██  ██\n██████\n    ██\n █████',
    ':': '  \n██\n  \n██\n  ',
}
CLEAR = "\033[H\033[J"


MINUTES_RE = re.compile(r'(\d+)m')
SECONDS_RE = re.compile(r'(\d+)s')


def duration(time_str):
    total = 0
    match = False
    if minutes := MINUTES_RE.search(time_str):
        total += int(minutes.group(1)) * 60
        match = True
    if seconds := SECONDS_RE.search(time_str):
        total += int(seconds.group(1))
        match = True
    if not match:
        raise ValueError
    return total


def get_number_lines(seconds):
    def to_str(integer):
        timestamp = str(integer).zfill(2)
        yield CHARS[timestamp[0]]
        yield CHARS[timestamp[1]]
    hours, minutes = divmod(seconds, 60)
    numbers = []
    for n in to_str(hours):
        numbers.append(n.splitlines())
    numbers.append(CHARS[':'].splitlines())
    for n in to_str(minutes):
        numbers.append(n.splitlines())
    output = []
    for line in range(5):
        output.append(' '.join(n[line] for n in numbers))
    return output


def print_full_screen(timestamp_lines):
    print(CLEAR, end='')
    term_width, term_height = shutil.get_terminal_size()
    text_width = max(len(i) for i in timestamp_lines)
    text_height = len(timestamp_lines)
    lines_before = (term_height - text_height) // 2
    indentation = (term_width - text_width) // 2
    print('\n' * lines_before, end='')
    for line in timestamp_lines:
        print(f'{" " * indentation}{line}')


if __name__ == '__main__':
    import time
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('duration')
    args = parser.parse_args()

    try:
        print("\x1b[?25l", end='')
        remaining_seconds = duration(args.duration)
        slept = 0
        while remaining_seconds >= 0:
            print_full_screen(get_number_lines(remaining_seconds))
            remaining_seconds -= 1
            time.sleep(1)
            slept += 1
    except KeyboardInterrupt:
        pass
    finally:
        print("\x1b[?25h", end='')
