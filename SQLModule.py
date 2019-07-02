import MySQLdb

class SQLConnector:
    def __init__(self, host, user, passwd, db):
        self.mysql = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
        self.curs = self.mysql.cursor()

    def select(self, querry, args):
        self.curs.execute(querry, args)
        result = self.curs.fetchall()
        return result

    def execute(self, querry, args):
        try:
            self.curs.execute(querry, args)
            self.mysql.commit()
            return
        except Exception as e:
            self.mysql.rollback()
            raise e
