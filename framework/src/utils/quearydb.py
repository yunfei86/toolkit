"""
This module provides a way to interact with databases. This class inherits LogBase and
provides logging capability to its methods.
"""

import psycopg2
from   logbase import LogBase
from   random  import randint

class IonDB(LogBase):
    def __init__(self, host='localhost', debug=False):
        """
        @type host: string
        @param host: This is a valid name of the host where the database is residing. This is
                     an optional parameter with a default value C{localhost}.
        @type debug: boolean
        @param debug: This flag either enables or disables the debug status of the class. This is
                     an optional parameter with a default value C{False}.
        """
        super(IonDB, self).__init__('IonDB%s'%randint(0, 99), 'debug')
        #super(ProtonAnalysis, self).__init__('ProtonAnalysis', 'info')
        self.createRotatingFileLogger('log/ionunittest.log')
        self.debug        = debug
        self.__host     = host
        self.__database = 'iondb'
        self.__user     = 'ion'
        conStr = "dbname='%s' user='%s' host='%s'"%(self.__database, self.__user, self.__host)
        self.logger.debug('Connection String: %s'%conStr)
        self.__connection = psycopg2.connect(conStr)
        self.__cursor     = self.__connection.cursor()
        self.rows         = None
        """@ivar: This varialbe holds the rows of a succeful query"""

    def queary(self, quearyString):
        """
        This method executes a queary passed by the argument and stores the rows in the variable C{rows}.
        @type quearyString: string
        @param quearyString: This is the query executed on the database. The result is stored in the variable C{rows}.
        """
        self.logger.debug('Queary String: %s'%quearyString)
        self.__cursor.execute(quearyString)
        self.rows = self.__cursor.fetchall()
        self.logger.debug('Rows: %s'%self.rows)
