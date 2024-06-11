import sqlite3
class PassDB:
    def __init__(self):
        try:
            self.connection = sqlite3.connect("passfinder.db")
            self.fail = False
        except Exception as e:
            print(e)
            self.fail = True
    def is_connected(self):
        return not self.fail
    def add_paste(self, source, pasteid, text):
        cursor = self.connection.cursor()
        cursor.execute('create table if not exists pastes (source TEXT, pasteid TEXT)')
        # cursor.execute()
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
    def flush_table(self):
        cursor = self.connection.cursor()
        cursor.execute('drop table accounts')
        cursor.execute('drop table pastes')
        cursor.execute('drop table topics')
    def get_user(self, source, pasteid):
        cursor = self.connection.cursor()
        rows = cursor.execute('select ')
    def add_topic(self, header, source):
        cursor = self.connection.cursor()
        # <a class="topic_title highlight_unread" href="https://www.nulled.to/topic/1620375-81k-leak-website-dump-top-hashed/" 
        cursor.execute('create table if not exists topics (header TEXT, source TEXT)')
        cursor.execute('insert into topics (header, source) values (?, ?)', (header, source))
    def check_topics(self, header, source):
        cursor = self.connection.cursor()
        rows = cursor.execute('select * from topic where header = ? and source = ?', (header, source))
        if len(rows) == 0:
            return False
        else:
            return True
    # TODO:
    # getter for users and passwords
    # getter by source
    # implement a check to see if paste exists, then excluding the pastes from google queries?
            
        