from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from time import sleep
import sqlite3 as db


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

def get_source():
    pass

if __name__ == '__main__':
    try:
        data_base = db.connect('Thread_lock.db')
        cursor = data_base.cursor()
        create_table()

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
