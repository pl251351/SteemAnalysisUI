import sqlite3
from sqlite3 import Error

import pandas as pd


class DataRepository:

    def __init__(self, db_file, conn=None):
        """ constructor create new object
        :param db_file of file to use for database
        """
        self.db_file = db_file

        # create a database connection
        self.connection = sqlite3.connect(self.db_file) if not conn else conn

        # create table SQL commands
        sql_create_comments_table = """ CREATE TABLE IF NOT EXISTS comments (id integer PRIMARY KEY,
        post_id integer,
        post_author text,
        post_title text,
        comment_author text,
        comment_title text,
        file_name text,
        update_time datetime NOT NULL default current_timestamp,
        create_time datetime NOT NULL default current_timestamp);"""

        sql_create_urls_table = """ CREATE TABLE IF NOT EXISTS urls (id integer PRIMARY KEY,
        post_id integer,
        comment_id integer,
        other_id integer,
        post_url text UNIQUE,
        comment_url text UNIQUE,
        other_url text,
        update_time datetime NOT NULL default current_timestamp,
        create_time datetime NOT NULL default current_timestamp,
        CONSTRAINT fk_column
        FOREIGN key (post_id)
        REFERENCES comments(id) ON DELETE CASCADE,
        FOREIGN key (comment_id)
        REFERENCES comments(id) ON DELETE CASCADE,
        FOREIGN key (other_id)
        REFERENCES comments(id)
        ON DELETE CASCADE);"""

        sql_create_responses_table = """ CREATE TABLE IF NOT EXISTS responses (id integer PRIMARY KEY,
        url_id integer NOT NULL UNIQUE,
        response json NOT NULL,
        update_time datetime NOT NULL default current_timestamp,
        create_time datetime NOT NULL default current_timestamp,
        CONSTRAINT fk_column
        FOREIGN key (url_id)
        REFERENCES urls(id)
        ON DELETE CASCADE);"""

        sql_create_google_responses_table = """ CREATE TABLE IF NOT EXISTS google_responses (id integer PRIMARY KEY,
        url_id integer NOT NULL UNIQUE,
        response json NOT NULL,
        update_time datetime NOT NULL default current_timestamp,
        create_time datetime NOT NULL default current_timestamp,
        CONSTRAINT fk_column
        FOREIGN key (url_id)
        REFERENCES urls(id)
        ON DELETE CASCADE);"""

        sql_create_ibm_responses_table = """ CREATE TABLE IF NOT EXISTS ibm_responses (id integer PRIMARY KEY,
        url_id integer NOT NULL UNIQUE,
        response json NOT NULL,
        update_time datetime NOT NULL default current_timestamp,
        create_time datetime NOT NULL default current_timestamp,
        CONSTRAINT fk_column
        FOREIGN key (url_id)
        REFERENCES urls(id)
        ON DELETE CASCADE);"""

        sql_create_textblob_responses_table = """ CREATE TABLE IF NOT EXISTS textblob_responses (id integer PRIMARY KEY,
        url_id integer NOT NULL UNIQUE,
        response json NOT NULL,
        update_time datetime NOT NULL default current_timestamp,
        create_time datetime NOT NULL default current_timestamp,
        CONSTRAINT fk_column
        FOREIGN key (url_id)
        REFERENCES urls(id)
        ON DELETE CASCADE);"""

        sql_create_flair_responses_table = """ CREATE TABLE IF NOT EXISTS flair_responses (id integer PRIMARY KEY,
        url_id integer NOT NULL UNIQUE,
        response json NOT NULL,
        update_time datetime NOT NULL default current_timestamp,
        create_time datetime NOT NULL default current_timestamp,
        CONSTRAINT fk_column
        FOREIGN key (url_id)
        REFERENCES urls(id)
        ON DELETE CASCADE);"""

        sql_create_values_table = """ CREATE TABLE IF NOT EXISTS value_earned (id integer PRIMARY KEY,
        url_id integer NOT NULL UNIQUE,
        value_earned number NOT NULL,
        extracted_text text NOT NULL,
        update_time datetime NOT NULL default current_timestamp,
        create_time datetime NOT NULL default current_timestamp,
        CONSTRAINT fk_column
        FOREIGN key (url_id)
        REFERENCES urls(id)
        ON DELETE CASCADE);"""
        # trigger so we can have created and updated
        sql_comments_table_trigger = """
        CREATE TRIGGER IF NOT EXISTS UPDATE_COMMENTS_TRIGGER AFTER UPDATE ON comments
        BEGIN
        UPDATE comments SET update_time = current_timestamp WHERE ID = old.rowid;
        END;
        """
        sql_urls_table_trigger = """
        CREATE TRIGGER IF NOT EXISTS UPDATE_URLS_TRIGGER AFTER UPDATE ON urls
        BEGIN
        UPDATE comments SET update_time = current_timestamp WHERE ID = old.rowid;
        END;
        """
        sql_responses_table_trigger = """
        CREATE TRIGGER IF NOT EXISTS UPDATE_RESPONSES_TRIGGER AFTER UPDATE ON responses
        BEGIN
        UPDATE comments SET update_time = current_timestamp WHERE ID = old.rowid;
        END;
        """
        sql_google_responses_table_trigger = """
        CREATE TRIGGER IF NOT EXISTS UPDATE_GOOGLE_RESPONSES_TRIGGER AFTER UPDATE ON google_responses
        BEGIN
        UPDATE comments SET update_time = current_timestamp WHERE ID = old.rowid;
        END;
        """
        sql_ibm_responses_table_trigger = """
        CREATE TRIGGER IF NOT EXISTS UPDATE_IBM_RESPONSES_TRIGGER AFTER UPDATE ON ibm_responses
        BEGIN
        UPDATE comments SET update_time = current_timestamp WHERE ID = old.rowid;
        END;
        """
        sql_textblob_responses_table_trigger = """
        CREATE TRIGGER IF NOT EXISTS UPDATE_TEXTBLOG_RESPONSES_TRIGGER AFTER UPDATE ON textblob_responses
        BEGIN
        UPDATE comments SET update_time = current_timestamp WHERE ID = old.rowid;
        END;
        """
        sql_flair_responses_table_trigger = """
        CREATE TRIGGER IF NOT EXISTS UPDATE_FLAIR_RESPONSES_TRIGGER AFTER UPDATE ON flair_responses
        BEGIN
        UPDATE comments SET update_time = current_timestamp WHERE ID = old.rowid;
        END;
        """
        sql_value_earned_table_trigger = """
        CREATE TRIGGER IF NOT EXISTS UPDATE_RESPONSES_TRIGGER AFTER UPDATE ON responses
        BEGIN
        UPDATE comments SET update_time = current_timestamp WHERE ID = old.rowid;
        END;
        """

        # create tables in db now
        if self.connection is not None:
            self.__create_table(sql_create_comments_table)
            self.__create_table(sql_create_urls_table)
            self.__create_table(sql_create_responses_table)
            self.__create_table(sql_create_google_responses_table)
            self.__create_table(sql_create_ibm_responses_table)
            self.__create_table(sql_create_textblob_responses_table)
            self.__create_table(sql_create_flair_responses_table)
            self.__create_table(sql_create_values_table)

            self.__create_table(sql_comments_table_trigger)
            self.__create_table(sql_urls_table_trigger)
            self.__create_table(sql_responses_table_trigger)
            self.__create_table(sql_google_responses_table_trigger)
            self.__create_table(sql_ibm_responses_table_trigger)
            self.__create_table(sql_textblob_responses_table_trigger)
            self.__create_table(sql_flair_responses_table_trigger)
            self.__create_table(sql_value_earned_table_trigger)
        else:
            print("Error! cannot create the database connection.")

    def __create_table(self, create_table_sql):
        """ create a table from the create_table_sql statement
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = self.connection.cursor()
            c.execute(create_table_sql)
            c.close()
        except Error as e:
            print(e)

    def create_comments(self, comments):
        """
        Create a new comment into the comments table
        :param comments needed to create db entry need 5 post_id, post_author,post_title,comment_author, comment_title
        :return: comment id
        """
        sql = '''INSERT OR IGNORE INTO 
            comments(post_id, post_author,post_title,comment_author, comment_title, file_name) 
            VALUES(?,?,?,?,?,?) '''
        cur = self.connection.cursor()
        cur.execute(sql, comments)
        self.connection.commit()
        cur.close()

        select_sql = """SELECT id 
            FROM comments 
            where post_id=? and 
            post_author=? and 
            post_title=? and 
            comment_author=? and 
            comment_title=? and 
            file_name=?"""

        cur = self.connection.cursor()
        cur.execute(select_sql, comments)

        row_id = cur.fetchone()
        cur.close()

        return row_id[0] if row_id and len(row_id) > 0 else None

    def create_urls(self, url):
        """
        Create a new task
        :param url: post_url,comment_url,other_url,post_id, comment_id, other_id
        :return: new url id
        """
        sql = ''' INSERT OR IGNORE 
            INTO urls(post_url,comment_url,other_url,post_id, comment_id, other_id) 
            VALUES(?,?,?,?,?,?) '''
        cur = self.connection.cursor()
        cur.execute(sql, url)
        self.connection.commit()
        cur.close()

        select_sql = """SELECT id 
            FROM urls 
            where 1=1"""
        # and post_id IS ? and comment_id IS ? and other_id IS ?
        select_val = ()
        if url[0]:
            select_sql += " and post_url = ?"
            select_val = (url[0],)
        else:
            select_sql += " and post_url is null"

        if url[1]:
            select_sql += " and comment_url = ?"
            select_val = select_val + (url[1],)
        else:
            select_sql += " and comment_url is null"

        if url[2]:
            select_sql += " and other_url = ?"
            select_val = select_val + (url[2],)
        else:
            select_sql += " and other_url is null"

        if url[3]:
            select_sql += " and post_id = ?"
            select_val = select_val + (url[3],)
        else:
            select_sql += " and post_id is null"

        if url[4]:
            select_sql += " and comment_id = ?"
            select_val = select_val + (url[4],)
        else:
            select_sql += " and comment_id is null"

        if url[5]:
            select_sql += " and other_id = ?"
            select_val = select_val + (url[5],)
        else:
            select_sql += " and other_id is null"

        cur = self.connection.cursor()
        cur.execute(select_sql, select_val)

        row_id = cur.fetchone()
        cur.close()

        return row_id[0] if row_id and len(row_id) > 0 else None

    def create_responses(self, response):
        """
        Create a new task
        :param response: response,url_id
        :return: id of the response
        """

        sql = '''INSERT INTO responses(response,url_id)
     VALUES(?,?) 
     ON CONFLICT(url_id) 
     DO UPDATE SET response = excluded.response'''

        cur = self.connection.cursor()
        cur.execute(sql, response)
        self.connection.commit()
        cur.close()

        select_sql = """SELECT id 
     FROM responses 
     where response=? and url_id=?"""
        cur = self.connection.cursor()
        cur.execute(select_sql, response)

        row_id = cur.fetchone()
        cur.close()

        return row_id[0] if row_id and len(row_id) > 0 else None

    def create_google_responses(self, response):
        """
        Create a new task
        :param response: response,url_id
        :return: id of the response
        """

        sql = '''INSERT INTO google_responses(response,url_id)
     VALUES(?,?) 
     ON CONFLICT(url_id) 
     DO UPDATE SET response = excluded.response'''

        cur = self.connection.cursor()
        cur.execute(sql, response)
        self.connection.commit()
        cur.close()

        select_sql = """SELECT id 
     FROM google_responses 
     where response=? and url_id=?"""
        cur = self.connection.cursor()
        cur.execute(select_sql, response)

        row_id = cur.fetchone()
        cur.close()

        return row_id[0] if row_id and len(row_id) > 0 else None

    def create_ibm_responses(self, response):
        """
        Create a new task
        :param response: response,url_id
        :return: id of the response
        """

        sql = '''INSERT INTO ibm_responses(response,url_id)
     VALUES(?,?) 
     ON CONFLICT(url_id) 
     DO UPDATE SET response = excluded.response'''

        cur = self.connection.cursor()
        cur.execute(sql, response)
        self.connection.commit()
        cur.close()

        select_sql = """SELECT id 
     FROM ibm_responses 
     where response=? and url_id=?"""
        cur = self.connection.cursor()
        cur.execute(select_sql, response)

        row_id = cur.fetchone()
        cur.close()

        return row_id[0] if row_id and len(row_id) > 0 else None

    def create_textblob_responses(self, response):
        """
        Create a new task
        :param response: response,url_id
        :return: id of the response
        """

        sql = '''INSERT INTO textblob_responses(response,url_id)
     VALUES(?,?) 
     ON CONFLICT(url_id) 
     DO UPDATE SET response = excluded.response'''

        cur = self.connection.cursor()
        cur.execute(sql, response)
        self.connection.commit()
        cur.close()

        select_sql = """SELECT id 
     FROM textblob_responses 
     where response=? and url_id=?"""
        cur = self.connection.cursor()
        cur.execute(select_sql, response)

        row_id = cur.fetchone()
        cur.close()

        return row_id[0] if row_id and len(row_id) > 0 else None

    def create_flair_responses(self, response):
        """
        Create a new task
        :param response: response,url_id
        :return: id of the response
        """

        sql = '''INSERT INTO flair_responses(response,url_id)
     VALUES(?,?) 
     ON CONFLICT(url_id) 
     DO UPDATE SET response = excluded.response'''

        cur = self.connection.cursor()
        cur.execute(sql, response)
        self.connection.commit()
        cur.close()

        select_sql = """SELECT id 
     FROM flair_responses 
     where response=? and url_id=?"""
        cur = self.connection.cursor()
        cur.execute(select_sql, response)

        row_id = cur.fetchone()
        cur.close()

        return row_id[0] if row_id and len(row_id) > 0 else None

    def create_value_earned(self, val):
        """
        Create a new value earned value_earned, extracted_text, url_id
        :param val: number value that is retrieved from steem page
        :return: id of the value
        """

        sql = ''' INSERT INTO value_earned(value_earned,extracted_text,url_id) 
     VALUES(?,?,?)
     ON CONFLICT(url_id) 
     DO UPDATE SET extracted_text = excluded.extracted_text, value_earned = excluded.value_earned'''

        cur = self.connection.cursor()
        cur.execute(sql, val)
        self.connection.commit()
        cur.close()

        select_sql = """SELECT id 
     FROM value_earned 
     where value_earned=? and extracted_text = ? and url_id=?"""
        cur = self.connection.cursor()
        cur.execute(select_sql, val)

        row_id = cur.fetchone()
        cur.close()

        return row_id[0] if row_id and len(row_id) > 0 else None

    def update_value_earned(self, val):
        """
        update priority, begin_date, and end date of a task
        :param val: new value
        :return:
        """
        sql = ''' UPDATE value_earned
                      SET value_earned = ? ,
                      WHERE id = ?'''
        cur = self.connection.cursor()
        cur.execute(sql, val)
        self.connection.commit()

    def update_response(self, response):
        """
        update response
        :param response: response, id
        :return: project id
        """
        # TODO: this is not proper
        sql = ''' UPDATE responses
                      SET response = ? ,
                      WHERE id = ?'''
        cur = self.connection.cursor()
        cur.execute(sql, response)
        self.connection.commit()

    def update_urls(self, urls):
        """
        update priority, begin_date, and end date of a task
        :param urls:
        :return: project id
        """
        # : TODO: this is broken - not sure what fields we need updating
        sql = ''' UPDATE urls
                      SET response = ? ,
                      WHERE id = ?'''
        cur = self.connection.cursor()
        cur.execute(sql, urls)
        self.connection.commit()

    def update_comment(self, new_comment):
        """
        update priority, begin_date, and end date of a task
        :param new_comment:
        :return: project id
        """
        # TODO broken not sure what fields we need to update
        sql = ''' UPDATE comments
                      SET response = ? ,
                      WHERE id = ?'''
        cur = self.connection.cursor()
        cur.execute(sql, new_comment)
        self.connection.commit()

    def select_post_details_from_url(self, post_id):
        """
        Query all rows in the comments table
        :return: all rows
        """
        cur = self.connection.cursor()
        select_rows = '''select ve.* from value_earned ve inner join urls u on u.id = ve.url_id where u.post_id=?'''
        cur.execute(select_rows, [post_id])

        return cur.fetchone()

    def select_google_response_from_url(self, post_id):
        """
        Query all rows in the comments table
        :return: all rows
        """
        cur = self.connection.cursor()
        select_rows = '''select gr.response from google_responses gr inner join urls u on u.id = gr.url_id where u.post_id =?'''
        cur.execute(select_rows, [post_id])

        return cur.fetchone()

    def select_ibm_response_from_url(self, post_id):
        """
        Query all rows in the comments table
        :return: all rows
        """
        cur = self.connection.cursor()
        select_rows = '''select gr.response from ibm_responses gr inner join urls u on u.id = gr.url_id where u.post_id =?'''
        cur.execute(select_rows, [post_id])

        return cur.fetchone()

    def select_textblob_response_from_url(self, post_id):
        """
        Query all rows in the comments table
        :return: all rows
        """
        cur = self.connection.cursor()
        select_rows = '''select gr.response from textblob_responses gr inner join urls u on u.id = gr.url_id where u.post_id =?'''
        cur.execute(select_rows, [post_id])

        return cur.fetchone()

    def select_response_from_url(self, post_id):
        """
        Query all rows in the comments table
        :return: all rows
        """
        cur = self.connection.cursor()
        select_rows = '''select gr.response from responses gr inner join urls u on u.id = gr.url_id where 
        u.post_id =? '''
        cur.execute(select_rows, [post_id])

        return cur.fetchone()

    def count_comment_by_file_name(self, file_name, view_all=False):
        """
        Query all rows in the comments table
        :return: all rows
        """
        cur = self.connection.cursor()
        select_rows = '''SELECT count(*) 
    from comments ce 
    inner join urls u on ce.id = u.post_id 
    inner join value_earned ve on u.id = ve.url_id
    where ce.file_name=? and ve.extracted_text is not NULL'''

        if view_all:
            select_rows = '''SELECT count(*) 
                    from comments ce 
                    inner join urls u on ce.id = u.post_id 
                    where ce.file_name=?'''

        cur.execute(select_rows, [file_name])

        return cur.fetchone()[0]

    def select_for_vader_correlation_analysis(self, value=-1):
        select_rows = f'''select 
        json_extract(re.response, '$.compound') compound, 
        ve.value_earned 
        FROM responses re 
        join value_earned ve 
        on re.url_id = ve.url_id'''

        return pd.read_sql_query(select_rows, self.connection)

    def select_for_combined_correlation_analysis(self, value=-1):
        select_rows = f'''SELECT
            json_extract(re.response, '$.compound') vader,
            json_extract(gr.response, '$.score') google,
            json_extract(im.response, '$.sentiment.document.score') ibm,
--             json_extract(flair.response, '$.score') flair,
--             json_extract(tb.response, '$[0]') tb,
            ve.value_earned
            from ibm_responses im
            inner join responses re on re.url_id = im.url_id
            inner join google_responses gr on im.url_id = gr.url_id
--             inner join textblob_responses tb on im.url_id = tb.url_id
--             inner join flair_responses flair on im.url_id = flair.url_id
            inner join value_earned ve on gr.url_id = ve.url_id'''

        return pd.read_sql_query(select_rows, self.connection)

    def select_for_google_correlation_analysis(self, value=-1):
        select_rows = f'''select 
        json_extract(re.response, '$.score') compound, 
        ve.value_earned 
        FROM google_responses re 
        join value_earned ve 
        on re.url_id = ve.url_id'''

        return pd.read_sql_query(select_rows, self.connection)

    def select_comment_by_file_name(self, file_name, limit, offset, view_all=False):
        """
        Query all rows in the comments table
        :return: all rows
        """
        cur = self.connection.cursor()
        select_rows = f'''SELECT ce.post_author,ce.post_title,ce.id,ce.file_name,ve.value_earned,u.post_url 
    FROM comments ce 
    inner join urls u on ce.id = u.post_id 
    inner join value_earned ve on u.id = ve.url_id
    where ce.file_name=? and ve.extracted_text is not NULL
    LIMIT {limit} OFFSET {offset}'''

        if view_all:
            select_rows = f'''SELECT ce.post_author,ce.post_title,ce.id,ce.file_name, u.post_url 
        FROM comments ce 
        inner join urls u on ce.id = u.post_id 
        where ce.file_name=?
        LIMIT {limit} OFFSET {offset}'''

        cur.execute(select_rows, [file_name])

        return cur.fetchall()

    def select_extracted_text_from_url(self, post_id):
        """
        Query all rows in the comments table
        :return: all rows
        """
        cur = self.connection.cursor()
        select_rows = '''select ve.extracted_text, u.id 
    from value_earned ve 
    inner join urls u 
    on u.id = ve.url_id 
    where u.post_id=?'''
        cur.execute(select_rows, [post_id])

        return cur.fetchone()

    def select_post_url_from_post_id(self, post_id):
        """
        Query all rows in the comments table
        :return: all rows
        """
        cur = self.connection.cursor()
        select_rows = '''SELECT post_url, id from urls where post_id=?'''
        cur.execute(select_rows, [post_id])

        return cur.fetchone()

    def select_all_comments(self):
        """
        Query all rows in the comments table
        :return: all rows
        """
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM comments")

        return cur.fetchall()

    def select_all_urls(self):
        """
        Query all rows in the url table
        :return: all rows
        """
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM urls")

        return cur.fetchall()

    def select_all_responses(self):
        """
        Query all rows in the response table
        :return: all rows
        """
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM responses")

        return cur.fetchall()

    def select_json_query_responses(self, json_query):
        """
        Query all rows in the tasks table
        :param json_query for selecting value from json like json_extract(response, '$.name')
        :return:
        """
        cur = self.connection.cursor()
        cur.execute("SELECT " + json_query + " FROM responses")

        return cur.fetchall()

    def select_all_value_earned(self):
        """
        Query all rows in the value_earned table
        :return: all rows
        """
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM value_earned")

        return cur.fetchall()

    def select_text_with_values(self, count=10, value=0.0):
        """
        Query random rows from url table
        :return:
        """
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM value_earned where extracted_text is not null and value_earned > " + str(
            value) + " ORDER BY RANDOM() LIMIT " + str(count) + ";")

        return cur.fetchall()

    def select_random_post_url(self, count=10):
        """
        Query random rows from url table
        :return:
        """
        cur = self.connection.cursor()
        cur.execute(
            "SELECT post_url, id FROM urls where post_url is not null ORDER BY RANDOM() LIMIT " + str(count) + ";")

        return cur.fetchall()

    def select_top_value_earned(self, count=10):
        """
        Query count rows for top values in table
        : param number to select default 10
        :return:
        """
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM value_earned ORDER BY value_earned DESC LIMIT " + str(count) + ";")

        return cur.fetchall()

    def select_bottom_value_earned(self, count):
        """
        Query 'count' rows for bottom values in table
        : param number to select default 10
        :return:
        """
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM value_earned ORDER BY value_earned LIMIT " + count + ";")

        return cur.fetchall()

    def delete_comments(self, comm_id):
        """
        Delete a task by task id
        :param comm_id: id of the task
        :return:
        """
        sql = 'DELETE FROM comments WHERE id=?'
        cur = self.connection.cursor()
        cur.execute(sql, (comm_id,))
        self.connection.commit()

    def delete_urls(self, urls_id):
        """
        Delete a task by task id
        :param urls_id: id of the task
        :return:
        """
        sql = 'DELETE FROM urls WHERE id=?'
        cur = self.connection.cursor()
        cur.execute(sql, (urls_id,))
        self.connection.commit()

    def delete_responses(self, response_id):
        """
        Delete a task by task id
        :param response_id: id of the task
        :return:
        """
        sql = 'DELETE FROM responses WHERE id=?'
        cur = self.connection.cursor()
        cur.execute(sql, (response_id,))
        self.connection.commit()

    def delete_value_earned(self, val_id):
        """
        Delete a task by task id
        :param val_id: id of the task
        :return:
        """
        sql = 'DELETE FROM value_earned WHERE id=?'
        cur = self.connection.cursor()
        cur.execute(sql, (val_id,))
        self.connection.commit()

    def select_comment_by_post_id(self, post_id):
        """
        Query tasks by priority
        :param post_id:
        :return:
        """
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM comments WHERE post_id=?", (post_id,))

        return cur.fetchall()

    def select_urls_by_comment_id(self, comm_id):
        """
        Query tasks by priority
        :param comm_id:
        :return:
        """
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM urls WHERE comment_id=?", (comm_id,))

        return cur.fetchall()

    def select_responses_by_url_id(self, comm_id):
        """
        Query tasks by priority
        :param comm_id:
        :return:
        """
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM responses WHERE url_id=?", (comm_id,))

        return cur.fetchall()

    def delete_all_comments(self):
        """
        Delete all rows in the tasks table
        :return:
        """
        sql = 'DELETE FROM comments'
        cur = self.connection.cursor()
        cur.execute(sql)
        self.connection.commit()

    def delete_all_urls(self):
        """
        Delete all rows in the tasks table
        :return:
        """
        sql = 'DELETE FROM urls'
        cur = self.connection.cursor()
        cur.execute(sql)
        self.connection.commit()

    def delete_all_responses(self):
        """
        Delete all rows in the tasks table
        :return:
        """
        sql = 'DELETE FROM responses'
        cur = self.connection.cursor()
        cur.execute(sql)
        self.connection.commit()

    def delete_all_value_earned(self):
        """
        Delete all rows in the tasks table
        :return:
        """
        sql = 'DELETE FROM value_earned'
        cur = self.connection.cursor()
        cur.execute(sql)
        self.connection.commit()

# if __name__ == '__main__':
#     database = r"sentiment_analysis.sqlite"
#
#     repo = DataRepository(database)
#     comment = (234, 'auth', 'title', 'comment', 'co title')
#     comment_id = repo.create_comments(comment)
#     print(comment_id)
#     comment_id = repo.create_comments(comment)
#     print(comment_id)
#
#     urls_1 = ('https://1', None, None, comment_id, None, None)
#     urls_2 = (None, 'https://2a', None, None, comment_id, None)
#     urls_3 = (None, None, 'https://3a', None, None, comment_id)
#
#     url_1_id = repo.create_urls(urls_1)
#     url_2_id = repo.create_urls(urls_2)
#     url_3_id = repo.create_urls(urls_3)
#
#     responses_1 = ("{'a':'b'}", url_1_id)
#     responses_2 = ("{'c':'d'}", url_2_id)
#     responses_3 = ("{'e':'f'}", url_3_id)
#
#     repo.create_responses(responses_1)
#     repo.create_responses(responses_2)
#     repo.create_responses(responses_3)
#
#     print("1. Query comments by post id:")
#     print(repo.select_comment_by_post_id(234))
#
#     print("2. Query all urls")
#     print(repo.select_urls_by_comment_id(1))
#
#     print("3. Query all response")
#     print(repo.select_responses_by_url_id(1))
#
#     print(repo.select_all_comments())
#     print(repo.select_all_urls())
#     print(repo.select_all_responses())

# TODO: test later
# with conn:
#     update_task(conn, (2, '2015-01-04', '2015-01-06', 2))

# delete_responses(1)
# delete_urls(1)
# delete_comments(1)
#
# delete_all_responses(db_conn)
# delete_all_urls(db_conn)
# delete_all_comments(db_conn)
