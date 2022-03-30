import requests
import sqlite3

class DB(object):
    def __init__(self):
        self.con = sqlite3.connect(':memory:')
        self.cur = self.con.cursor()
        self._setup_schema()
    
    def _setup_schema(self):
        """
        Exmaple object:
        {
            "r": "115333",
            "v": "",
            "t": "BEAUTIFUL",
            "a": "10 YEARS"
        }
        """
        q = "CREATE TABLE IF NOT EXISTS music (id INT, v TEXT, title TEXT COLLATE NOCASE, artist TEXT COLLATE NOCASE)"
        try:
            self.cur.execute(q)
        except Exception as e:
            print('db table creation failed:', e)
    
    def popluate(self, data: list) -> None:
        try:
            self.cur.executemany('INSERT INTO music (id, v, title, artist) '
                            'VALUES (:r, :v, :t, :a)', data) 
        except Exception as e:
            raise

    def search_artist(self, artist: str) -> list:
        try:
            self.cur.execute('SELECT * FROM music WHERE artist=?', (artist, ))
            rows = self.cur.fetchall()
            return rows
        except Exception as e:
            print('query failed:', e)
            return []

    def search_title(self, title: str) -> list:
        try:
            self.cur.execute('SELECT * FROM music WHERE title=?', (title, ))
            rows = self.cur.fetchall()
            return rows
        except Exception as e:
            print('query failed:', e)
            return []
