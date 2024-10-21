def four(number):
    while number != 4:
        num_name = number_info(number)
        number = len(num_name.replace('-', '').replace(' ', ''))
        print(f'The word {num_name} has {number:,} letters in it.')
    print(f'The word four has 4 letters in it.')
    print('Done.')


def number_info(number):
    ones = {
        0: 'zero',
        1: 'one',
        2: 'two',
        3: 'three',
        4: 'four',
        5: 'five',
        6: 'six',
        7: 'seven',
        8: 'eight',
        9: 'nine',
        10: 'ten',
        11: 'eleven',
        12: 'twelve',
        13: 'thirteen',
        14: 'fourteen',
        15: 'fifteen',
        16: 'sixteen',
        17: 'seventeen',
        18: 'eighteen',
        19: 'nineteen',
    }
    tens = {
        2: 'twenty',
        3: 'thirty',
        4: 'forty',
        5: 'fifty',
        6: 'sixty',
        7: 'seventy',
        8: 'eighty',
        9: 'ninety',
    }
    illions = {
        1: 'thousand',
        2: 'million',
        3: 'billion',
        4: 'trillion',
        5: 'quadrillion',
        6: 'quintillion',
        7: 'sextillion',
        8: 'septillion',
        9: 'octillion',
        10: 'nonillion',
        11: 'decillion',
    }
    if number < 20:
        return ones[number]
    elif number < 100:
        div, mod = divmod(number, 10)
        if mod > 0:
            return '-'.join([tens[div], ones[mod]])
        return tens[div]
    elif number == 100:
        return 'one hundred'
    elif number < 1_000:
        return divide(number, 100, 'hundred')
    elif number == 1_000:
        return 'one thousand'
    else:
        for illion_number, illion_name in illions.items():
            if number < 1_000**(illion_number + 1):
                break
        return divide(number, 1_000**illion_number, illion_name)


def divide(dividend, divisor, magnitude):
    div, mod = divmod(dividend, divisor)
    return ' '.join([number_info(div), magnitude, number_info(mod)])


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('number', type=int)
    args = parser.parse_args()
    
    four(args.number)
