import itertools


class CyclicList:

    def __init__(self, data):
        self.data = list(data)

    def __iter__(self):
        while True:
            yield from self.data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        if isinstance(index, slice):
            i_start = index.start if index.start is not None else 0
            i_stop = index.stop if index.stop is not None else 0
            if i_start == 0 and i_stop == 0:
                return self.data[:]
            if i_start < 0 or i_stop < 0:
                min_len = i_start * -1 if i_start < 0 else i_start
                min_len += i_stop * -1 if i_stop < 0 else i_stop
                if min_len < len(self):
                    return self.data[index]
                output = []
                for i in self:
                    if len(output) == min_len:
                        break
                    output.append(i)
                if index.start and index.stop:
                    return [output[index.start]] + output[:index.stop]
                elif index.start:
                    return output[index.start:]
                return output[:index.stop]
            return list(itertools.islice(self, index.start, index.stop))
        if index < 0:
            if (index * -1) > len(self):
                index += len(self)
            return self.data[index]
        elif index >= len(self):
            return next(itertools.islice(self, index))
        return self.data[index]

    def __setitem__(self, index, value):
        if index > len(self):
            index -= len(self)
        self.data[index] = value

    def append(self, item):
        self.data.append(item)

    def pop(self, index=-1):
        return self.data.pop(index)
