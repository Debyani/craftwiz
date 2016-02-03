__author__ = 'dghosh'

import os
import sqlite3
import sys

class DbOperation(object):

    def __init__(self,dbName = None, dbPath = None ,dbType='sqlite'):
        self.dbType = dbType
        if dbType == 'sqlite':
            assert (dbPath) ,"dbPath cannot be null for sqllite"
            self.conn = sqlite3.connect(dbPath)


    def close(self):
        if  self.conn :
            self.conn.close()
            print 'Connection Closed'

    def executeFile(self,file):
        assert(file) , "Invalid file"
        file_data = open(file).read()
        if self.dbType == 'sqlite':
            try:
                cur = self.conn.cursor()
                cur.executescript(file_data)

            except sqlite3.Error as e:
                print "Cannot execute script" , e.args[0]

        self.conn.commit()
        cur.close()

    def executeSingleDML(self,file,t = None):
        assert(file) , "Invalid file"
        try:
            cur = self.conn.cursor()
            if t:
                cur.execute(open(file).read(),t)
            else:
                cur.execute(open(file).read())

        except sqlite3.Error as e:
                print "Cannot execute script" , e.args[0]

        self.conn.commit()
        cur.close()

    def executeSingleSQL(self,file,t = None):
        assert(file) , "Invalid file"
        try:
            cur = self.conn.cursor()
            if t is not None:
                return cur.execute(open(file).read(),t).fetchone()[0]
            else:
                try:
                    return cur.execute(open(file).read()).fetchone()[0]
                except:
                    raise
        except sqlite3.Error as e:
                print "Cannot execute script" , e.args[0]

        self.conn.commit()
        cur.close()

    def executeSingleSQLfetchall(self,file,t = None):
        assert(file) , "Invalid file"
        try:
            cur = self.conn.cursor()
            if t is not None:
                return cur.execute(open(file).read(),t).fetchall()
            else:
                try:
                    return cur.execute(open(file).read()).fetchall()
                except:
                    raise
        except sqlite3.Error as e:
                print "Cannot execute script" , e.args[0]

        self.conn.commit()
        cur.close()

def main():
        db = DbOperation(dbPath='/Users/agoel/DataScience/projects/skeleton/data/craftdb.sqlite')
        db.executeFile('/Users/agoel/DataScience/projects/skeleton/sql/create_data_model.sql')
        db.conn.close()

if __name__ == '__main__':
    main()


