#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

import os
import sys
import csv
import time
import glob
import commands
import subprocess
import sqlite3
import shlex

from fabric.api import local, lcd
from fabric.decorators import task


settings = {
    'path_raw_data_base': 'data-raw/data/base/csv',
    'path_raw_data_diff': 'data-raw/data/diff/csv',
#   'file_sqlite3': 'data-sqlite3/data.sqlite3',
#   'file_sqlite3': 'data-sqlite3/data.4.sqlite3',
    'file_sqlite3': ':memory:',
    'output': {
        'file_xml':     'data.xml',
        'file_csv':     'data.csv',
        'file_tsv':     'data.tsv',
        'file_ltsv':    'data.ltsv',
        'file_yaml':    'data.yaml',
        'file_json':    'data.json',
        'file_sql':     'data.sql' } }

corporation_keys = [
    'corporateNumber',
    'process',
    'correct',
    'updateDate',
    'changeDate',
    'name',
    'nameImageId',
    'kind',
    'prefectureName',
    'cityName',
    'streetNumber',
    'addressImageId',
    'prefectureCode',
    'cityCode',
    'postCode',
    'addressOutside',
    'addressOutsideImageId',
    'closeDate',
    'closeCause',
    'successorCorporateNumber',
    'changeCause',
    'assignmentDate',
    'latest',
    'enName',
    'enPrefectureName',
    'enCityName',
    'enAddressOutside',
    'furigana',
    'hihyoji' ]



class SQLiteDB(object):
    db_name         = None
    db_connection   = None
    db_cursor       = None

    def __init__(self, db_name):
        self.db_name = db_name
        self.db_connection = sqlite3.connect(self.db_name)
        self.db_connection.text_factory = str
        self.db_cursor = self.db_connection.cursor()

    def __del__(self):
        self.close()

    def close(self):
        self.db_cursor.close()
        self.db_connection.close()


    def set(self, tag, value):
        """
            | tag               | value         | description       |
            |-------------------|---------------|-------------------|
            | base:<fileName>   | 'loaded'      | 読み込み済み      |
            | diff:<fileName>   | 'loaded'      | 読み込み済み      |
            | lastUpdateDate    | 'YYYY-MM-DD'  | 最終更新日        |

        """
        self.db_cursor.execute('SELECT COUNT(*) FROM settings WHERE tag = ?', [tag])
        if (self.db_cursor.fetchone()[0] == 0):
            self.write('INSERT INTO settings VALUES(?, ?, ?, ?)', [tag, value, int(time.time()), int(time.time())])
        else:
            self.write('UPDATE settings SET value = ?, updatedAt = ? WHERE tag = ?', [value, int(time.time()), tag])


    def create(self):
        self.write("""CREATE TABLE settings(tag TEXT PRIMARY KEY, value TEXT, updatedAt INTEGER, createdAt INTEGER)""")
        self.write("""CREATE TABLE corporations(
            corporateNumber TEXT PRIMARY KEY,
            process TEXT,
            correct TEXT,
            updateDate TEXT,
            changeDate TEXT,
            name TEXT,
            nameImageId TEXT,
            kind TEXT,
            prefectureName TEXT,
            cityName TEXT,
            streetNumber TEXT,
            addressImageId TEXT,
            prefectureCode TEXT,
            cityCode TEXT,
            postCode TEXT,
            addressOutside TEXT,
            addressOutsideImageId TEXT,
            closeDate TEXT,
            closeCause TEXT,
            successorCorporateNumber TEXT,
            changeCause TEXT,
            assignmentDate TEXT )""")
 
    def write(self, sql, row=[]):
        self.db_cursor.execute(sql, row)
        self.db_connection.commit()

    def commit(self):
        self.db_connection.commit()

    def exists(self):
        if os.path.exists(self.db_name) is False:
            return False

        self.db_cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type = 'table' AND name = 'corporations'")
        count = self.db_cursor.fetchone()[0]
        if count == 0:
            return False

        return True





@task
def setUp():
    """ set up

    使用する linux コマンド
        unzip
        gpg
        rm
    """
    sys.stderr.write("setup\n")
    sys.stderr.write("setup\n")
    sys.stderr.write("setup\n")
    sys.stderr.write("hoge\n")
    sys.stderr.write("fuga\n")
    sys.stderr.write("piyo\n")



"""
def existsDB():
    if os.path.exists(settings['file_sqlite3']) is False:
        return False

    with sqlite3.connect(settings['file_sqlite3']) as db_connection:
        db_connection.text_factory = str
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type = 'table' AND name = 'corporations'")
        count = db_cursor.fetchone()[0]
        db_cursor.close()
        if count == 0:
            return False

    return True
"""


# def createDB():
#     """
#     """
#     with sqlite3.connect(settings['file_sqlite3']) as db_connection:
#         db_connection.text_factory = str
#         db_cursor = db_connection.cursor()
# 
#         db_cursor.execute("""CREATE TABLE settings(tag TEXT PRIMARY KEY, value TEXT, updatedAt INTEGER, createdAt INTEGER)""")
# 
#         db_cursor.execute("""CREATE TABLE corporations(
#             corporateNumber TEXT PRIMARY KEY,
#             process TEXT,
#             correct TEXT,
#             updateDate TEXT,
#             changeDate TEXT,
#             name TEXT,
#             nameImageId TEXT,
#             kind TEXT,
#             prefectureName TEXT,
#             cityName TEXT,
#             streetNumber TEXT,
#             addressImageId TEXT,
#             prefectureCode TEXT,
#             cityCode TEXT,
#             postCode TEXT,
#             addressOutside TEXT,
#             addressOutsideImageId TEXT,
#             closeDate TEXT,
#             closeCause TEXT,
#             successorCorporateNumber TEXT,
#             changeCause TEXT,
#             assignmentDate TEXT )""")
#         db_connection.commit()
# 
#         db_cursor.close()



def unzipRawData():
    """ 生データ 解凍
    """
    """
    for file_zip in glob.glob(os.path.join(path, '*.zip')):
        print file_zip
    """
    # base
    path = os.path.join(os.getcwd(), settings['path_raw_data_base'])
    with lcd(path):
        local('/usr/bin/unzip "*.zip"')
    # diff
    path = os.path.join(os.getcwd(), settings['path_raw_data_diff'])
    with lcd(path):
        local('/usr/bin/unzip "*.zip"')


def rmRawCSV():
    """
    """
    pass

@task
# def insertRawDataToSQLiteDB():
def createSQLiteDB():
    """ base data を SQLite DB に insert
    """
    db = SQLiteDB(':memory:')
    db.exists()

    if db.exists() is True:
        sys.stderr.write("Already created.\n")
        return

    db.create()
    sys.stderr.write("create DB\n")

#   unzipRawData()

    path = os.path.join(os.getcwd(), settings['path_raw_data_base'])
    # file 読込 & DB 書込
    for csv_file_path in glob.glob('%s/*.csv' % (path)):
        csv_file_name = os.path.basename(csv_file_path)
        sys.stderr.write("load %s\n" % (csv_file_name))
        with open(csv_file_path, 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                # sequenceNumber 排除
                row.pop(0)
                db.write('INSERT INTO corporations VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', row)
                # db_cursor.execute("""INSERT INTO corporations VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", row)

    # db_connection.commit()
    # db_cursor.close()

    del db


@task
def updateSQLiteDB():
    """ diff data を SQLite DB に update
    """
    pass



@task
# def isValid(file_pub, file_asc, file_csv):
def isValid():
    """
    """
    # see: https://www.houjin-bangou.nta.go.jp/download/kokaikagi/index.html
    command = 'gpg --import pgp.pub'
    print '%s : %s' % (command, subprocess.call(shlex.split(command)))

    command = 'gpg --verify --openpgp /Users/ukyooo/Documents/git/bitbucket/houjin-bangou/source-data/data-raw/data/diff/csv/diff_20160301.csv.asc /Users/ukyooo/Documents/git/bitbucket/houjin-bangou/source-data/data-raw/data/diff/csv/diff_20160301.csv'
    print '%s : %s' % (command, subprocess.call(shlex.split(command)))
    if not subprocess.call(shlex.split(command)) == 0:
        return False
    return True


@task
def dumpCSV():
    """
    """
    pass

@task
def dumpTSV():
    """
    """
    pass

@task
def dumpXML():
    """
    """
    pass

@task
def dumpYAML():
    """
    """
    pass

@task
def dumpJSON():
    """
    """
    pass

@task
def dumpMySQL():
    """
    """
    pass


"""
# curl -X GET "https://api.houjin-bangou.nta.go.jp/1/diff?id=<jp.go.nta.houjin-bangou.api.id>&from=2015-12-01&to=2015-12-31&type=02"
"""

"""
# SELECT <x>, <y>, COUNT(*) AS count FROM corporations WHERE <filter> NOT IN ("<filterValue>", ...) GROUP BY <x>, <y> ;
SELECT kind, process, COUNT(*) AS count FROM corporations WHERE prefectureCode NOT IN ("03") GROUP BY kind, process ;
101|01|823
101|11|1
101|12|2
201|01|7280
201|12|5
301|01|1861613
301|11|3728
301|12|29298
301|21|17249
301|22|16
301|71|1080
301|72|2
301|81|1
302|01|1650488
302|11|530
302|12|8207
302|21|20612
302|22|11
303|01|18408
303|11|12
303|12|32
303|21|188
303|22|1
304|01|93266
304|11|9
304|12|98
304|21|855
305|01|96551
305|11|218
305|12|2231
305|21|687
305|71|12
399|01|455251
399|11|441
399|12|2980
399|21|3637
399|22|3
399|71|71
401|01|4636
401|11|1
401|12|20
401|13|46
499|01|7822
499|11|10
499|12|42
"""

