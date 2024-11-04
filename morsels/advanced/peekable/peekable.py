from itertools import islice


SENTINEL = object()


class peekable:

    def __init__(self, iterable):
        self.iterable = iter(iterable)
        self.prepend_values = []
        self.peek_value = SENTINEL
        self.remaining_item = True

    def __bool__(self):
        if self.prepend_values:
            return True
        if self.remaining_item:
            self.peek(default=object())
        return self.remaining_item

    def __next__(self):
        if self.peek_value is not SENTINEL:
            try:
                return self.peek_value
            finally:
                self.peek_value = SENTINEL
        if self.prepend_values:
            return self.prepend_values.pop(0)
        try:
            return next(self.iterable)
        except StopIteration as e:
            self.remaining_item = False
            raise e from None
    
    def __iter__(self):
        return self

    def __getitem__(self, index):
        self.prepend_values = list(self)
        return self.prepend_values[index]

    def peek(self, default=SENTINEL):
        if self.peek_value is SENTINEL:
            try:
                self.peek_value = next(self)
            except StopIteration as e:
                if default is SENTINEL:
                    raise e from None
                return default
        return self.peek_value

    def prepend(self, item):
        if self.peek_value is not SENTINEL:
            self.prepend_values.append(self.peek_value)
            self.peek_value = SENTINEL
        self.prepend_values.insert(0, item)
