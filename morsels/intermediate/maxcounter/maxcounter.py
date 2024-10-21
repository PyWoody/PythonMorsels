from collections import Counter


class MaxCounter(Counter):

    def max_keys(self):
        items = self.most_common()
        if not items:
            return []
        best = max(items, key=lambda x: x[1])[1]
        return [i[0] for i in items if i[1] == best]
