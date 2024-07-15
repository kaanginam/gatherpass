import os
import pyodbc, struct
from azure import identity

from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
class AzureDB:
    def __init__(self, config):
        
        credential = identity.DefaultAzureCredential(exclude_interactive_browser_credential=False)
        token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
        token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
        SQL_COPT_SS_ACCESS_TOKEN = 1256  # This connection option is defined by microsoft in msodbcsql.h
        self.connection = pyodbc.connect(config.get_db_conn_str(), attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})  
    def add_paste(self, source, pasteid, text):
        cursor = self.connection.cursor()
        cursor.execute('create table if not exists pastes (source varchar(255), pasteid varchar(255), text varchar(3000), is_leak int DEFAULT 0, password varchar(255) DEFAULT NULL, UNIQUE(source,pasteid))')
        cursor.execute('insert or ignore into pastes (source, pasteid, text) values (?, ?, ?)', (source, pasteid, text))
        self.connection.commit()
        # cursor.execute(
    def paste_exists(self, source, pasteid):
        cursor = self.connection.cursor()
        cursor.execute('create table if not exists pastes (source varchar(255), pasteid varchar(255), text varchar(3000), is_leak int DEFAULT 0, password varchar(255) DEFAULT NULL, UNIQUE(source,pasteid))')
        self.connection.commit()
        rows = cursor.execute('select * from pastes where source = ? and pasteid = ?', (source, pasteid)).fetchall()
        if len(rows) == 0:
            return False
        else:
            return True
    def paste_is_leak(self, source, pasteid, pw):
        cursor = self.connection.cursor()
        cursor.execute('create table if not exists pastes (source varchar(255), pasteid varchar(255), text varchar(255), is_leak int DEFAULT 0, password varchar(255) DEFAULT NULL, UNIQUE(source,pasteid))')
        cursor.execute('update pastes set is_leak=1 where source = ? and pasteid = ?',(source, pasteid))
        cursor.execute('update pastes set password=? where source = ? and pasteid = ?',(pw, source, pasteid))
        self.connection.commit()
    def add_links(self, source, url):
        cursor = self.connection.cursor()
        cursor.execute('create table if not exists tlinks (source varchar(255), url varchar(255), UNIQUE(source,url))')
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
        cursor.execute('create table if not exists accounts (user varchar(255), pw varchar(255), source varchar(255), pasteid varchar(255))')
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
        cursor.execute('create table if not exists thread (source varchar(255), url varchar(255), UNIQUE(source,url))')
        cursor.execute('insert into thread (source, url) values (?, ?)', (source, url))
        self.connection.commit()
        
    def thread_exists(self, source, url):
        cursor = self.connection.cursor()
        cursor.execute('create table if not exists thread (source varchar(255), url varchar(255), UNIQUE(source,url))')
        self.connection.commit()
        rows = cursor.execute('select * from thread where source = ? and url = ?', (source, url)).fetchall()
        if len(rows) == 0:
            return False
        else:
            return True
    def add_topic(self, header, source):
        cursor = self.connection.cursor()
        # <a class="topic_title highlight_unread" href="https://www.nulled.to/topic/1620375-81k-leak-website-dump-top-hashed/" 
        cursor.execute('create table if not exists topics (header varchar(255), source varchar(255))')
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
            
        