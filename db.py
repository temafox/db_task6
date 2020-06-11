import psycopg2
import sys
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def connect(db):
    try:
        connection = psycopg2.connect( database = db,
                                       user = "postgres",
                                       password = "postgres",
                                       host = "localhost" )
        connection.set_isolation_level( ISOLATION_LEVEL_AUTOCOMMIT )
        return connection
    except Exception as ex:
        #print("Exception:", ex)
        sys.exit()

def execute(query, *parameters, db="cat_vet"):
    connection = connect( db )

    # As we have canceled the autotransaction mode,
    # we must ensure transactions by ourselves
    try:
        cursor = connection.cursor()
        cursor.execute( "BEGIN;" )
        cursor.execute( query, parameters )
        cursor.execute( "END;" )
        query_result = cursor.fetchall()
    except Exception as ex:
        #print("Exception:", ex)
        query_result = None
    finally:
        connection.close()
        return query_result

def execute_notrans(query, *parameters, db="cat_vet"):
    connection = connect( db )

    # No transaction, e.g. for SELECT
    try:
        cursor = connection.cursor()
        cursor.execute( query, parameters )
        query_result = cursor.fetchall()
    except Exception as ex:
        #print("Exception:", ex)
        query_result = None
    finally:
        connection.close()
        return query_result
