import os
import sqlite3
from contextlib import contextmanager


@contextmanager
def open_db():
    con = sqlite3.connect(os.getenv('MISKATONIC_DB'))
    yield con.cursor()
    con.commit()
    con.close()
