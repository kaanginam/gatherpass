import sqlite3
import logging
import os
class PassDB:
    def __init__(self, dbName, prefix=''):
        try:
            logging.info("Attempting connection to database")
            self.connection = sqlite3.connect(prefix+dbName)
            self.fail = False
        except Exception as e:
            logging.exception("Exception when trying to connect to database")
            logging.exception(e)
            self.fail = True
    def is_connected(self):
        return not self.fail
    def add_paste(self, source, pasteid, text):
        cursor = self.connection.cursor()
        cursor.execute('create table if not exists pastes (source TEXT, pasteid TEXT, text TEXT, is_leak INTEGER DEFAULT 0, password TEXT DEFAULT NULL, UNIQUE(source,pasteid))')
        cursor.execute('insert or ignore into pastes (source, pasteid, text) values (?, ?, ?)', (source, pasteid, text))
        self.connection.commit()
        logging.info("Added paste")
        # cursor.execute(
    def paste_exists(self, source, pasteid):
        cursor = self.connection.cursor()
        cursor.execute('create table if not exists pastes (source TEXT, pasteid TEXT, text TEXT, is_leak INTEGER DEFAULT 0, password TEXT DEFAULT NULL, UNIQUE(source,pasteid))')
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
        cursor.execute('create table if not exists pastes (source TEXT, pasteid TEXT, text TEXT, is_leak INTEGER DEFAULT 0, password TEXT DEFAULT NULL, UNIQUE(source,pasteid))')
        cursor.execute('update pastes set is_leak=1 where source = ? and pasteid = ?',(source, pasteid))
        cursor.execute('update pastes set password=? where source = ? and pasteid = ?',(pw, source, pasteid))
        self.connection.commit()
    def add_links(self, source, url):
        cursor = self.connection.cursor()
        cursor.execute('create table if not exists tlinks (source TEXT, url TEXT, UNIQUE(source,url))')
        cursor.execute('insert or ignore into tlinks (source, url) values (?, ?)', (source, url))
        self.connection.commit()
        
    def add_accounts_from_file(self, text, source, pasteid, parser):
        for line in text.split('\n'):
            retcode, sep = parser.check_patterns(text)
            if retcode > 0:
                user = line.strip().split(f"{sep}")[0]
                pw = line.strip().split(f"{sep}")[1]
                self.add_account(user, pw, source, pasteid)
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
        
    def get_user(self, source, pasteid):
        cursor = self.connection.cursor()
        rows = cursor.execute('select ')
    def add_thread(self, source, url):
        cursor = self.connection.cursor()
        cursor.execute('create table if not exists thread (source TEXT, url TEXT,UNIQUE(source,url))')
        cursor.execute('insert into thread (source, url) values (?, ?)', (source, url))
        self.connection.commit()
        
    def thread_exists(self, source, url):
        cursor = self.connection.cursor()
        cursor.execute('create table if not exists thread (source TEXT, url TEXT, UNIQUE(source,url))')
        self.connection.commit()
        rows = cursor.execute('select * from thread where source = ? and url = ?', (source, url)).fetchall()
        if len(rows) == 0:
            return False
        else:
            return True
    def add_topic(self, header, source):
        cursor = self.connection.cursor()
        # <a class="topic_title highlight_unread" href="https://www.nulled.to/topic/1620375-81k-leak-website-dump-top-hashed/" 
        cursor.execute('create table if not exists topics (header TEXT, source TEXT)')
        cursor.execute('insert into topics (header, source) values (?, ?)', (header, source))
    def check_topics(self, header, source):
        cursor = self.connection.cursor()
        rows = cursor.execute('select * from topic where header = ? and source = ?', (header, source)).fetchall()
        if len(rows) == 0:
            return False
        else:
            return True
    # TODO:
    # getter for users and passwords
    # getter by source
    # implement a check to see if paste exists, then excluding the pastes from google queries?
            
        