import MySQLdb

class SQLConnector:
    def __init__(self, host, user, passwd, db):
        self.mysql = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
        self.curs = self.mysql.cursor()


    def checkInjection(self, args):
        for arg in args:
            pass

    def select(self, querry, args):
        if self.checkInjection(args):
            exit
        try:
            self.curs.execute(querry, args)
            result = self.curs.fetchall()
            return (True, result)
        except Exception as e:
            return (False, str(e))
        # cur.close()

    def execute(self, querry, args):
        if self.checkInjection(args):
            exit
        try:
            self.curs.execute(querry, args)
            self.mysql.commit()
            return (True, "")
        except Exception as e:
            self.mysql.rollback()
            return (False, str(e))
        # finally:
        #     cur.close()
