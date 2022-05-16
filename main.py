from concurrent.futures import ThreadPoolExecutor
import threading
import time
import sqlite3 as db


class Source1:

    def __init__(self):
        self.lock = threading.Lock()

    def acquire(self, name):
        print(f'{name} is acquiring the source1')
        if not self.lock.locked():
            self.lock.acquire()
            print(f'The source1 is granted to {name}')
        else:
            print(f'Ooops, {name} is already locked by another thread')
            self.lock.acquire()

    def release(self, name):
        self.lock.release()
        print(f'{name} released the source1')


class Source2:

    def __init__(self):
        self.lock = threading.Lock()

    def acquire(self, name):
        print('')
        print(f'{name} is acquiring the source2')
        if not self.lock.locked():
            self.lock.acquire()
            print(f'The source2 is granted to {name}')
            print('')
        else:
            print(f'Ooops, {name} is already locked by another thread')
            self.lock.acquire()

    def release(self, name):
        self.lock.release()
        print(f'{name} released the source2')


def process(name, source1, source2):
    source1.acquire(name)
    time.sleep(2)
    source2.acquire(name)
    time.sleep(2)
    print('now release all the sources')
    source1.release(name)
    source2.release(name)


def create_table():
    sql="""DROP TABLE"""


if __name__ == '__main__':
    try:
        data_base = db.connect('Thread_lock.db')
        cursor = data_base.cursor()


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
