import datetime

from collections import namedtuple


class make_model:

    def __init__(self, *, table_name, fields, connection):
        self.table = str(table_name)
        self.fields = dict(fields)
        self.con = connection
        self.con.row_factory = namedtuple_factory

    def create_table(self):
        fields = ', '.join(
            f'{k} {types_to_text(v)}' for k, v in self.fields.items()
        )
        try:
            self.con.execute(f'CREATE TABLE {self.table} ({fields})')
            self.con.commit()
        except Exception as e:
            self.con.rollback()
            raise e
        else:
            return self

    def create(self, **fields):
        keys = sorted(fields.keys())
        cols = ', '.join(keys)
        values = tuple(fields[k] for k in keys)
        qmarks = ', '.join('?' for _ in values)
        self.con.execute(
            f'INSERT INTO {self.table} ({cols}) VALUES ({qmarks})', values
        )
        self.con.commit()
        return next(
            iter(
                Result(
                    self.con, f'SELECT * FROM {self.table}', fields
                )
            )
        )

    def filter(self, **filters):
        return Result(
            self.con, f'SELECT * FROM {self.table}', filters=filters
        )


class Result:

    def __init__(self, con, query, filters=None):
        self.con = con
        self.query = str(query)
        self.filters = dict(filters) if filters is not None else dict()
        self.cache = None

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return all(
                self.con == other.con and
                self.query == other.query and
                self.filters == other.filters and
                self.values == other.values
            )
        return NotImplemented

    def __iter__(self):
        if self.cache is None:
            query = self.query
            values = tuple()
            if self.filters:
                keys = sorted(self.filters.keys())
                where = ' AND '.join(f'{k}=?' for k in keys)
                values = tuple(self.filters[k] for k in keys)
                query += f' WHERE ({where})'
            self.cache = self.con.execute(query, values).fetchall()
        yield from self.cache

    def filter(self, **filters):
        prev_filters = dict(self.filters)
        prev_filters.update(filters)
        return type(self)(self.con, self.query, prev_filters)


def types_to_text(_type):
    if _type is None:
        return 'NULL'
    elif issubclass(_type, str):
        return 'TEXT'
    elif issubclass(_type, int):
        return 'INTEGER'
    elif issubclass(_type, bool):
        return 'INTEGER'
    elif issubclass(_type, float):
        return 'REAL'
    elif issubclass(_type, datetime.datetime):
        return 'TIMESTAMP'
    raise Exception


def namedtuple_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    cls = namedtuple('Row', fields)
    return cls._make(row)
