from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from time import sleep
import sqlite3 as db
import psycopg2
from config import host, user, password, db_name


def thread_func():
    data_base1 = psycopg2.connect(host=host, user=user, password=password, database=db_name)

    cursor1 = data_base1.cursor()
    number = 1
    print(f'The second thread started')
    sql = """begin;
            update player
            set player_points = player_points + 2
            where player_id = 2;
            select pg_sleep(10);
            select player_points
            from player
            where player_id = 1
            for update;
            select * from player where player_id = 2;
            commit;"""
    cursor1.execute(sql)
    data_base1.commit()
    cursor1.close()
    print(f'The second thread finished')
    data_base1.close()


if __name__ == '__main__':
    try:
        # data_base = psycopg2.connect(host='localhost', database='Thread_lock.db', port='5432')
        data_base = psycopg2.connect(host=host, user=user, password=password, database=db_name)
        print("data base opened successfuly")
        cursor = data_base.cursor()

        th = Thread(target=thread_func)
        th.start()

        print('The main thread started')
        sql = """begin;
                    select player_points
                    from player
                    where player_id = 2
                    for update;
                    select pg_sleep(10);
                    update player
                    set player_points = player_points + 2
                    where player_id = 1;
                    select * from player where player_id = 1;
                    commit;"""
        cursor.execute(sql)
        data_base.commit()
        print('The main thread finished')



    except db.Error as error:
        print("Data Base Connection Error")
    finally:
        if data_base:
            data_base.close()
            cursor.close()
            print('Connection with SQL is closed')
