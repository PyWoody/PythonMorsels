from functools import total_ordering
from numbers import Number


RN = {
    'I': 1,
    'IV': 4,
    'V': 5,
    'IX': 9,
    'X': 10,
    'XL': 40,
    'L': 50,
    'XC': 90,
    'C': 100,
    'CD': 400,
    'D': 500,
    'CM': 900,
    'M': 1_000,
}

@total_ordering
class RomanNumeral:

    def __init__(self, numeral):
        self.numeral = numeral

    def __repr__(self):
        cls = self.__class__.__name__
        return f'{cls}({self.numeral!r})'

    def __str__(self):
        return self.numeral

    def __eq__(self, other):
        if isinstance(other, (RomanNumeral, Number)):
            return int(self) == int(other)
        elif isinstance(other, str):
            return str(self) == other
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, (RomanNumeral, Number)):
            return int(self) < int(other)
        return NotImplemented

    def __int__(self):
        return to_int(self.numeral)

    def __add__(self, other):
        return self.from_int(int(self) + int(other))

    @classmethod
    def from_int(cls, value):
        return cls(to_str(value))


def to_str(num):
    output = []
    numerals = sorted(RN.items(), key=lambda x: x[1], reverse=True)
    for numeral, value in numerals:
        if (count := num // value) > 0:
            num -= count * value
            output.append(count * numeral)
    return ''.join(output)


def to_int(numeral):
    num = numeral[::-1]
    index = 0
    total = 0
    while index < len(num):
        if index + 1 < len(num) and RN[num[index + 1]] < RN[num[index]]:
            total += RN[num[index]] - RN[num[index + 1]]
            index += 1
        else:
            total += RN[num[index]]
        index += 1
    return total
