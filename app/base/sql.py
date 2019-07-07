import psycopg2
from psycopg2.extras import RealDictCursor

from config import database


class Sql:
    @staticmethod
    def connect():
        config_connect = "dbname='{dbname}' user='{user}' host='{host}' password='{password}'"
        try:
            connect = psycopg2.connect(config_connect.format(**database))
            return connect, connect.cursor(cursor_factory=RealDictCursor)
        except:
            pass

    @staticmethod
    def exec(query=None, args=None, file=None):
        try:
            return Sql._switch(query=query, args=args, file=file)
        except:
            pass

    @staticmethod
    def _switch(query=None, args=None, file=None):
        if query and args:
            return Sql._query_exec_args(query, args)
        if query and not args:
            return Sql._query_exec(query)
        if file and args:
            return Sql._query_file_args_exec(file, args)
        if file:
            return Sql._query_file_exec(file)

    @staticmethod
    def _query_exec(query):
        print(query)
        return Sql._exec(query)

    @staticmethod
    def _query_file_exec(file):
        with open(file, 'r') as f:
            query = f.read()
            return Sql._exec(query)

    @staticmethod
    def _query_file_args_exec(file, args):
        with open(file, 'r') as f:
            query = f.read().format(**args)
            return Sql._exec(query)

    @staticmethod
    def _query_exec_args(query, args):
        query = query.format(**args)
        print(query)
        return Sql._exec(query)

    @staticmethod
    def _exec(query):
        """
        Метод выполняет SQL запрос к базе
        :param query: str SQL запрос
        :return: dict результат выполнения запроса
        """
        try:
            connect, current_connect = Sql.connect()
            current_connect.autocommit = True
            result = None
        except:
            pass
        try:
            current_connect.execute(query)
            connect.commit()
        except psycopg2.Error as e:
            print(e.pgerror)
            print(e.diag.message_primary)
            print(psycopg2.errorcodes.lookup(e.pgcode))
        finally:
            try:
                result = current_connect.fetchall()
            except:
                pass
            finally:
                connect.close()
                return result
