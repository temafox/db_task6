import psycopg2
import sys
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from db import connect, execute, execute_notrans

def create_database():
    execute_notrans("CREATE DATABASE cat_vet;", db="postgres")

def create_tables():
    execute( open("create_tables.sql", "r").read() )

def fill_tables():
    execute( open("fill_tables.sql", "r").read() )

def destroy_tables():
    execute( open("destroy_tables.sql", "r").read() )

def create_cat_disease_history_trigger():
    execute( "DROP FUNCTION IF EXISTS cat_disease_history_trigger CASCADE;" )
    execute(
        """CREATE OR REPLACE FUNCTION cat_disease_history_trigger(new_cat_id integer, new_disease varchar(30), new_date date, new_state varchar(30)) RETURNS trigger AS $cat_disease_history_trigger$
        BEGIN
            IF new_state = 'начало' THEN
                INSERT INTO cat_disease_history
                    (cat_id, disease, start_date)
                VALUES
                    (new_cat_id, new_disease, new_date);
            END IF;
            IF new_state = 'конец' THEN
                UPDATE cat_disease_history SET end_date = new_date WHERE cat_disease_id = (SELECT cdh.cat_disease_id FROM cat_disease AS cdh WHERE cdh.cat_id = new_cat_id AND cdh.disease = new_disease ORDER BY cdh.start_date DESC LIMIT 1);
            END IF;
            RETURN NULL;
        END;
        $cat_disease_history_trigger$ LANGUAGE plpgsql;"""
    )
    execute(
        "CREATE TRIGGER cat_disease_history_trigger AFTER UPDATE ON examination" +
        "FOR EACH ROW EXECUTE PROCEDURE cat_disease_history_trigger(NEW.cat_id, NEW.disease, make_date(floor(extract(year FROM NEW.date_time)), floor(extract(month FROM NEW.date_time)), floor(extract(day FROM NEW.date_time))), NEW.disease_state);"
    )

def init_database():
    create_database()
    create_tables()
    fill_tables()
    create_cat_disease_history_trigger()

def deinit_database():
    execute_notrans("DROP DATABASE IF EXISTS cat_vet;", db="postgres")

deinit_database()
init_database()
