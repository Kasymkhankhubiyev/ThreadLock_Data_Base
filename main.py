from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from time import sleep
import sqlite3 as db
import psycopg2
from config import host, user, password, db_name


def create_table():
    sql = """DROP TABLE IF EXISTS player"""
    cursor.execute(sql)
    data_base.commit()
    sql = """CREATE TABLE player(
            player_id INTEGER PRIMARY KEY,
            player_name TEXT,
            player_points INTEGER)"""
    cursor.execute(sql)
    data_base.commit()
    sql = """INSERT INTO player(player_name, player_points)
            VALUES
                    ('BigKing', 120),
                    ('Eagle', 10),
                    ('Commandor', 210);"""
    cursor.execute(sql)
    data_base.commit()
    sql = """SELECT * FROM player"""
    cursor.execute(sql)
    data_base.commit()
    array = cursor.fetchall()
    for arr in array:
        print(arr)


def get_source(number):
    print(f'Starting getting source {number}')
    sql = """SELECT player_points FROM player WHERE player_id = ?"""
    cursor.execute(sql, [number])
    data_base.commit()
    print(f'Source {number} is got')


def update_points(number):
    print(f'Statring changing points for {number}')
    sql = """UPDATE player SET player_points = player_points - 2 WHERE player_id = ?"""
    cursor.execute(sql, [number])
    data_base.commit()
    print(f'Points for source {number} is changed')



def thread_func():
    #data_base1 = psycopg2.connect(host='localhost', database='Thread_lock.db', user='postgres', password="12345")
    data_base1 = db.connect('Thread_lock.db')

    cursor1 = data_base1.cursor()
    number = 1
    print(f'Starting getting source {number}')
    sql = """SELECT player_points FROM player WHERE player_id = ?"""
    cursor1.execute(sql, [number])
    data_base1.commit()
    print(f'Source {number} is got')
    sleep(1)
    print(f'Statring changing points for {number+1}')
    sql = """UPDATE player SET player_points = player_points - 2 WHERE player_id = ?"""
    cursor1.execute(sql, [number+1])
    data_base1.commit()
    print(f'Points for source {number+1} is changed')
    data_base1.close()


if __name__ == '__main__':
    try:
        # data_base = psycopg2.connect(host='localhost', database='Thread_lock.db', port='5432')
        data_base = psycopg2.connect(host=host, user=user, password=password, database=db_name)
        data_base = db.connect('Thread_lock.db')
        print("data base opened successfuly")
        cursor = data_base.cursor()
        create_table()

        th = Thread(target=thread_func)
        th.start()

        get_source(2)
        sleep(1)
        update_points(1)



    except db.Error as error:
        print("Data Base Connection Error")
    finally:
        if data_base:
            data_base.close()
            print('Connection with SQL is closed')

    # source1 = Source1()
    # source2 = Source2()
    # transactions = [["A", "B"], [source1, source2], [source2, source1]]
    # with ThreadPoolExecutor(max_workers=2) as executor:
    #     executor.map(process, *transactions)
