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
    sql = """SELECT player_points FROM player WHERE player_id = 2 FOR UPDATE"""
    cursor.execute(sql)
    data_base.commit()
    print(f'Source {number} is got')


def update_points(number):
    print(f'Statring changing points for {number}')
    sql = """UPDATE player SET player_points = player_points - 2 WHERE player_id = 1"""
    cursor.execute(sql)
    data_base.commit()
    print(f'Points for source {number} is changed')



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
    # array = cursor1.fetchall()
    print(f'The second thread finished')
    # for arr in array:
    #     print(arr)

    #print(f'Starting getting source {number}')
    # sql = """SELECT player_points FROM player WHERE player_id = 1 FOR UPDATE"""
    # cursor1.execute(sql)
    # data_base1.commit()
    # print(f'Source {number} is got')
    # sleep(1000)
    # print(f'Statring changing points for {number+1}')
    # sql = """UPDATE player SET player_points = player_points - 2 WHERE player_id = 2"""
    # cursor1.execute(sql)
    # data_base1.commit()
    # print(f'Points for source {number+1} is changed')
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
        # array = cursor.fetchall()
        # for arr in array:
        #     print(arr)

        # get_source(2)
        # sleep(1000)
        # update_points(1)



    except db.Error as error:
        print("Data Base Connection Error")
    finally:
        if data_base:
            data_base.close()
            cursor.close()
            print('Connection with SQL is closed')

    # source1 = Source1()
    # source2 = Source2()
    # transactions = [["A", "B"], [source1, source2], [source2, source1]]
    # with ThreadPoolExecutor(max_workers=2) as executor:
    #     executor.map(process, *transactions)
