from .main import Table


def from_csv(file_name, split=','):
    with open(file_name) as file:
        indexes = file.readline().split(split)
        table = Table([], indexes=indexes)
        for line in file:
            table.append(line.split(split))
        return table
