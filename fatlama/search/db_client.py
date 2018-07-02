import sqlite3


class DbClient:
    """Connects to the provided SQLLite database"""
    def __init__(self, db_file_path):
        """
        Create a new database client. Be sure to dispose of it afterward,
            call it inside a with statement.
        Parameters
        ----------
        db_file_path - path to the sqlite3 file to use
        """
        self.db_file_path = db_file_path
        self.connection = sqlite3.connect(db_file_path)
        self.cursor = self.connection.cursor()

    def get_items_by_id(self, ids):
        """
        Gets all items with the specified IDs
        Parameters
        ----------
        ids - list of integers

        Returns
        -------
        list of dictionaries with keys id, item_name, lat, and lng
        """
        sql_query = ("SELECT id, item_name, lat, lng " +
                     "FROM items WHERE id IN (" +
                     ",".join([str(x) for x in ids]) +
                     ")")
        return [row for row in self.cursor.execute(sql_query)]

    def get_all_records(self):
        """
        Gets the entire contents of the database
        Returns
        -------
        List of dictionaries with keys id, item_name, lat, lng
        """
        for row in self.cursor.execute("SELECT id, item_name, lat, lng FROM items"):
            yield self._row_to_dict(row)

    @staticmethod
    def _row_to_dict(row):
        """Converts a database sqlite3 object into a dict"""
        return {
            'id': row[0],
            'item_name': row[1],
            'lat': row[2],
            'lng': row[3]
        }

    def __enter__(self):
        """Called at the start of a with statement"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Called at the end of a with statement"""
        self.connection.close()
