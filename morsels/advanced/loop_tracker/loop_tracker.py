class loop_tracker:

    def __init__(self, iterable):
        self.iterable = iter(iterable)
        self.__len = 0
        self.__empty = 0
        self.checked_items = []
        self.__first = None
        self.__last = None

    def __len__(self):
        return self.__len

    def __iter__(self):
        return self

    def __next__(self):
        if self.checked_items:
            self.__len += 1
            return self.checked_items.pop(0)
        try:
            item = next(self.iterable)
        except StopIteration as e:
            self.__empty += 1
            raise e
        else:
            self.__len += 1
            if self.__first is None:
                self.__first = item
            self.__last = item
            return item

    @property
    def first(self):
        if self.__first is None:
            try:
                next_item = next(self)
            except StopIteration:
                raise AttributeError
            else:
                self.checked_items.append(next_item)
                self.__len -= 1
        return self.__first

    @property
    def last(self):
        if len(self) == 0:
            raise AttributeError
        return self.__last

    @property
    def empty_accesses(self):
        return self.__empty

    def is_empty(self):
        if self.empty_accesses > 0:
            return True
        try:
            next_item = next(self)
        except StopIteration:
            self.__empty -= 1
            return True
        else:
            self.checked_items.append(next_item)
            self.__len -= 1
            return False
