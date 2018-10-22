from contextlib import contextmanager

import click
import os
import sqlite3

@contextmanager
def open_db():
    con = sqlite3.connect(os.getenv('MISKATONIC_DB'))
    yield con.cursor()
    con.commit()
    con.close()

@click.command()
@click.option('--init', help='Init the database')
def main(init: bool = False):
    if init:
        print('Creating database')
        with open_db() as cur:
            cur.execute('create table python_articles (id integer primary key, title text, content text, date date)')
            cur.execute('create table lisp_articles (id integer primary key, title text, content text, date date)')


if __name__ == '__main__':
    main()
