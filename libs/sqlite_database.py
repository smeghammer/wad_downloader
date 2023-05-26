'''
Created on 23 May 2023

@author: smegh
'''

import os
import sqlite3

class ServerDatabaseActions():
    '''
    classdocs
    '''

    FETCH_ALL = 10
    FETCH_ONE = 11

    def __init__(self):
        ''' Constructor '''
        path = os.path.abspath(os.getcwd())

        # create the path if needed
        if not os.path.isdir(path + '/database/'):
            print('Creating database directory path...')
            os.makedirs(path + '/database/')

        # create a database file, if needed:
        self.dbname = path + '/database/idgamesdata.db'

        # create database if not exists:
        if not os.path.isfile(self.dbname):
            conn = sqlite3.connect(self.dbname)
            c = conn.cursor()

            # and create the table:
            # FIELDS:
            # - id (string, the WAD name. Should be unique)
            # - author - (string, the WAD author. Will be duplicated entries of course)
            # - timestamp - (int, UNIX timestamp. Store as integer, so calculations are easy)
            c.execute("CREATE TABLE if not exists idgames_metadata (id int UNIQUE NOT NULL, title TEXT NOT NULL, author TEXT NOT NULL, timestamp integer NOT NULL)")

        else:
            # and connect:
            conn = sqlite3.connect(self.dbname)
            c = conn.cursor()

    '''
    Utilities to open, execute and close a SQLite DB and query
    NOTE: Queryvars is a List(), even if length 1
    '''
    def executeUpdateSql(self, sql, queryvars=None,_ok_msg='update successful'):
        try:
            conn = sqlite3.connect(self.dbname)
            c = conn.cursor()
            c.execute(sql,queryvars)
            conn.commit()
            conn.close()
            return({'status':'ok','message':_ok_msg})
        except sqlite3.Error as err:
            conn.close()
            return({'status':'error','message':'update, Sqlite3: '+str(err)})

        except Exception as e:
            conn.close()
            return({'status':'error','message':'update, Other: '+str(e)})

    def executeInsertSql(self, sql, queryvars=None,_ok_msg='insert successful'):
        try:
            conn = sqlite3.connect(self.dbname)
            c = conn.cursor()
            c.execute(sql,queryvars)
            conn.commit()
            conn.close()
            return({'status':'ok','message':_ok_msg})
        except sqlite3.Error as err:
            conn.close()
            return({'status':'error','message':'insert, Sqlite3: '+str(err)})

        except Exception as err:
            conn.close()
            return({'status':'error','message':'insert, Other: '+str(err)})

    def executeSelectSql(self, sql, queryvars=None, fetchAction=FETCH_ALL):
        try:
            conn = sqlite3.connect(self.dbname)    #probably want to open this and close it again in the calling function. Opening/closing each time round the loop is probably expensive...
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            if queryvars:
                res = c.execute(sql, queryvars)
            else:
                res = c.execute(sql)

            if fetchAction == ServerDatabaseActions.FETCH_ALL:
                results = [dict(row) for row in res.fetchall()]
            elif fetchAction == ServerDatabaseActions.FETCH_ONE:
                results = res.fetchone()
                if results:
                    results = dict(results)
            conn.close()
            return results
        except sqlite3.Error as e:
            conn.close()
            return({'status':'error','message':'select, Sqlite3: '+str(e)})

        except Exception as e:
            conn.close()
            return({'status':'error','message':'select, Other: '+str(e)})

    def executeDeleteSql(self, sql, queryvars=None):
        try:
            conn = sqlite3.connect(self.dbname)    #probably want to open this and close it again in the calling function. Opening/closing each time round the loop is probably expensive...
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            if queryvars:
                res = c.execute(sql, queryvars)
            else:
                res = c.execute(sql)
            conn.commit()
            conn.close()
            return({'status':'ok','message': 'deletion performed OK' })
        except sqlite3.Error as e:
            conn.close()
            return({'status':'error','message':'update, Sqlite3: '+str(e)})

        except Exception as e:
            conn.close()
            return({'status':'error','message':'update, Other: '+str(e)})

    def insertRecord(self,item_id,title,author,timestamp):
        res = self.executeSelectSql('select count (*) as count from idgames_metadata where id=? ',(item_id, ), self.FETCH_ONE)
        if not res['count']:  #it is None - i.e. no matching entry
            self.executeInsertSql('insert into idgames_metadata (id, title, author, timestamp) values (?,?,?,?)'
                      ,(item_id, title, author, timestamp), 'added new entry OK')

# select count(*) as count from idgames_metadata;
# select * from idgames_metadata where author like '%meghammer%';
# select distinct author from idgames_metadata;
# select author,title,timestamp from idgames_metadata order by upper(author) asc,timestamp asc ;
