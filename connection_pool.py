from dbutils.persistent_db import PersistentDB
import sqlite3


class Pool(object):  # 数据库连接池
    __pool = None  # 记录第一个被创建的对象引用
    config = {
        'database': 'token.db'  # 数据库文件路径
    }

    def __new__(cls, *args, **kwargs):
        """创建连接池对象  单例设计模式(每个线程中只创建一个连接池对象)  PersistentDB为每个线程提供专用的连接池"""
        if cls.__pool is None:  # 如果__pool为空，说明创建的是第一个连接池对象
            cls.__pool = PersistentDB(sqlite3, maxusage=None, closeable=False, **cls.config)
        return cls.__pool


class Connect:
    def __enter__(self):
        try:
            db_pool = Pool()
            self.conn = db_pool.connection()
            self.cur = self.conn.cursor()
            return self
        except sqlite3.Error as e:
            print(f"Error connecting to the database: {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            # 如果有异常发生，回滚事务
            self.conn.rollback()
        else:
            # 如果没有异常，提交事务
            self.conn.commit()
        self.cur.close()
        self.conn.close()
