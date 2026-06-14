import mysql.connector
from datetime import datetime


class Database:

    def __init__(self):

        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="YOUR_PASSWORD",
            database="wallet_system"
        )

        self.cursor = self.conn.cursor()



    def add_user(self,name,pin,balance):

        query = """
        INSERT INTO users
        (name,pin,balance)
        VALUES(%s,%s,%s)
        """

        self.cursor.execute(
            query,
            (name,pin,balance)
        )

        self.conn.commit()



    def get_user(self,name):

        query = """
        SELECT *
        FROM users
        WHERE name=%s
        """

        self.cursor.execute(
            query,
            (name,)
        )

        return self.cursor.fetchone()



    def update_balance(self,name,balance):

        query = """
        UPDATE users
        SET balance=%s
        WHERE name=%s
        """

        self.cursor.execute(
            query,
            (balance,name)
        )

        self.conn.commit()



    def save_transaction(
        self,
        sender,
        receiver,
        amount,
        status
    ):

        query = """
        INSERT INTO transactions
        (sender,receiver,amount,status,transaction_time)
        VALUES(%s,%s,%s,%s,%s)
        """

        self.cursor.execute(
            query,
            (
                sender,
                receiver,
                amount,
                status,
                datetime.now()
            )
        )

        self.conn.commit()



    def show_transactions(self):

        self.cursor.execute(
            "SELECT * FROM transactions"
        )

        return self.cursor.fetchall()