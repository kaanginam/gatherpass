import sqlite3
import logging
"""
Database manager that adds paste, checks if one exists and more.
"""
class PassDB:
    def __init__(self, dbName, prefix=''):
        try:
            logging.info("Attempting connection to database")
            self.connection = sqlite3.connect(prefix + dbName)
            self.fail = False
        except Exception as e:
            logging.exception("Exception when trying to connect to database")
            logging.exception(e)
            self.fail = True
    def is_connected(self):
        return not self.fail
    def add_paste(self, source, pasteid, text):
        cursor = self.connection.cursor()
        cursor.execute('create table if not exists pastes (source TEXT, pasteid TEXT, text TEXT, is_leak INTEGER DEFAULT 0, password TEXT DEFAULT NULL, dt datetime default current_timestamp, UNIQUE(source,pasteid))')
        cursor.execute('insert or ignore into pastes (source, pasteid, text) values (?, ?, ?)', (source, pasteid, text))
        self.connection.commit()
        logging.info("Added paste")
    def paste_exists(self, source, pasteid):
        cursor = self.connection.cursor()
        cursor.execute('create table if not exists pastes (source TEXT, pasteid TEXT, text TEXT, is_leak INTEGER DEFAULT 0, password TEXT DEFAULT NULL, dt datetime default current_timestamp, UNIQUE(source,pasteid))')
        self.connection.commit()
        rows = cursor.execute('select * from pastes where source = ? and pasteid = ?', (source, pasteid)).fetchall()
        if len(rows) == 0:
            logging.info("Paste not in database")
            return False
        else:
            logging.info("Paste in database")
            return True
    def paste_is_leak(self, source, pasteid, pw):
        cursor = self.connection.cursor()
        cursor.execute('create table if not exists pastes (source TEXT, pasteid TEXT, text TEXT, is_leak INTEGER DEFAULT 0, password TEXT DEFAULT NULL, dt datetime default current_timestamp, UNIQUE(source,pasteid))')
        cursor.execute('update pastes set is_leak=1 where source = ? and pasteid = ?',(source, pasteid))
        cursor.execute('update pastes set password=? where source = ? and pasteid = ?',(pw, source, pasteid))
        self.connection.commit()
        logging.info("Set paste in database to leak")
    def add_links(self, source, url):
        cursor = self.connection.cursor()
        cursor.execute('create table if not exists tlinks (source TEXT, url TEXT, dt datetime default current_timestamp, UNIQUE(source,url))')
        cursor.execute('insert or ignore into tlinks (source, url) values (?, ?)', (source, url))
        self.connection.commit()
        logging.info("Added link to database")
    def add_account(self, user, pw, source, pasteid):
        cursor = self.connection.cursor()
        cursor.execute('create table if not exists accounts (user TEXT, pw TEXT, source TEXT, pasteid TEXT)')
        cursor.execute('insert into accounts (user, pw, source, pasteid) VALUES (?, ?, ?, ?)', (user, pw, source, pasteid))
        self.connection.commit()
    def flush_table(self):
        cursor = self.connection.cursor()
        cursor.execute('drop table accounts')
        cursor.execute('drop table pastes')
        cursor.execute('drop table topics')
        self.connection.commit()
    def add_thread(self, source, url):
        cursor = self.connection.cursor()
        cursor.execute('create table if not exists thread (source TEXT, url TEXT, text TEXT, dt datetime default current_timestamp, UNIQUE(source,url))')
        cursor.execute('insert into thread (source, url) values (?, ?)', (source, url))
        self.connection.commit()
        logging.info("Added thread to database")
    def thread_exists(self, source, url):
        cursor = self.connection.cursor()
        cursor.execute('create table if not exists thread (source TEXT, url TEXT, text TEXT, dt datetime default current_timestamp, UNIQUE(source,url))')
        self.connection.commit()
        rows = cursor.execute('select * from thread where source = ? and url = ?', (source, url)).fetchall()
        if len(rows) == 0:
            logging.info("Thread is already in database")
            return False
        else:
            logging.info("Thread not in database")
            return True
    """
    Saves results of scanned paste to file for debug purposes
    """
    def save_results(self, filename, content, source):
        from datetime import datetime
        ct = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f'{ct} from {source}\n')
            f.write(content)