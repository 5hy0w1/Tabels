class BinaryArray(list):
    def __init__(self, iterable):
        for i in range(len(iterable)):
            iterable[i] = bool(iterable[i])

        super().__init__(iterable)

    def logic(self, func, arr):
        binary = BinaryArray([])
        if len(self) != len(arr):
            raise Exception("Different sizes of sequences")
        for exp1, exp2 in zip(self, arr):
            binary.append(func(exp1, exp2))
        return binary

    def __and__(self, arg):
        return self.logic(lambda a, b: a and b, arg)

    def __or__(self, arg):
        return self.logic(lambda a, b: a or b, arg)

    def __rand__(self, arg):
        return self.logic(lambda a, b: a and b, arg)

    def __ror__(self, arg):
        return self.logic(lambda a, b: a or b, arg)

    def __invert__(self):
        binary = BinaryArray([])
        for i in self:
            binary.append(not i)
        return binary


class Sequence(list):

    def __init__(self, iterable):
        super().__init__(iterable)
        self.is_binary = False

    def get_binary(self, func):
        binary = BinaryArray([])
        binary.is_binary = True
        for item in self:
            binary.append(func(item))

        return binary

    def __str__(self):
        return '  '.join(map(str, self))

    def __repr__(self):
        return self.__str__()

    def __ge__(self, arg):
        return self.get_binary(lambda x: x >= arg)

    def __le__(self, arg):
        return self.get_binary(lambda x: x <= arg)

    def __eq__(self, arg):
        return self.get_binary(lambda x: x == arg)

    def __gt__(self, arg):
        return self.get_binary(lambda x: x > arg)

    def __lt__(self, arg):
        return self.get_binary(lambda x: x < arg)

    def __ne__(self, arg):
        return self.get_binary(lambda x: x != arg)

    def __getitem__(self, item):
        if isinstance(item, BinaryArray):
            ans = Sequence([])
            for i, b in zip(self, item):
                if b:
                    ans.append(i)
            return ans
        else:
            return list.__getitem__(self, item)


class Table(list):

    def __init__(self, data, indexes=[]):
        if not indexes:
            indexes = Sequence(map(str, range(len(data))))
        self.indexes = indexes
        for row in range(len(data)):
            if not isinstance(data[row], Sequence):
                data[row] = Sequence(data[row])

        super().__init__(data)

    def __isiterable__(self, obj):
        try:
            iter(obj)
            return True
        except TypeError:
            return False

    def __getitem__(self, arg):
        if isinstance(arg, str):
            if arg in self.indexes:
                j = self.indexes.index(arg)
                data = Sequence([])
                for i in range(len(self)):
                    data.append(list.__getitem__(self, i)[j])
                return data
            else:
                Exception("Not Found")
        elif isinstance(arg, BinaryArray):
            if len(arg) != len(self):
                Exception("Different sizes of sequences")
            t = Table([], indexes=self.indexes)
            for row, binary in zip(self, arg):
                if binary:
                    t.append(row)
            return t
        elif isinstance(arg, int):
            return list.__getitem__(self, arg)
        else:
            raise Exception("Unsupported type")


    def __repr__(self):
        body = ''
        head = ' '
        spaces = []
        for i in self.indexes:
            l = len(str(max(self[i], key=lambda x: len(str(x)))))
            l = max(len(i), l)
            l = min(15, l)
            spaces.append(l)
            if len(i) > 12:
                i = i[:12] + '...'
            head += ("{:<%i}" % l).format(i) + ' | '

        hr = '-' * len(head) + "\n"
        head += '\n'
        body += head + hr
        for row in self:
            body += ' '
            for cell, sp in zip(row, spaces):
                if len(str(cell)) >= 12:
                    cell = str(cell[:12]) + '...'
                body += ("{:<%i}" % sp).format(cell) + ' | '
            body += "\n" + hr
        return body

    def to_csv(self, file_name):
        with open(file_name, 'w') as file:
            file.write(','.join(self.indexes))
            for row in self:
                file.write(','.join(row))

    def to_txt(self, file_name):
        with open(file_name, 'w') as file:
            file.write(self.__repr__())
