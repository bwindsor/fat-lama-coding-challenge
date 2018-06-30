import sqlite3


class DbClient:
    def __init__(self, db_file_path):
        self.db_file_path = db_file_path
        self.connection = sqlite3.connect(db_file_path)
        self.cursor = self.connection.cursor()

    def get_items_by_id(self, ids):
        sql_query = ("SELECT id, item_name, lat, lng " +
                     "FROM items WHERE id IN (" +
                     ",".join([str(x) for x in ids]) +
                     ")")
        return [row for row in self.cursor.execute(sql_query)]

    def get_all_records(self):
        for row in self.cursor.execute("SELECT id, item_name, lat, lng FROM items"):
            yield self._row_to_dict(row)

    @staticmethod
    def _row_to_dict(row):
        return {
            'id': row[0],
            'item_name': row[1],
            'lat': row[2],
            'lng': row[3]
        }

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
