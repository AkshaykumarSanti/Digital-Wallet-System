from datetime import datetime
import json
import os

# ================= DATABASE ================= #

USER_FILE = "users.json"
TRANSACTION_FILE = "transactions.json"


def save_users():

    data = {}

    for name, user in users.items():

        data[name] = {
            "pin": user.wallet._Wallet__pin,
            "balance": user.wallet.get_balance(),
            "bank": None
        }

        if user.bank_account:

            data[name]["bank"] = {
                "name": user.bank_account.bank_name,
                "account": user.bank_account.account_number,
                "balance": user.bank_account.balance
            }


    with open(USER_FILE,"w") as file:
        json.dump(data,file,indent=4)



def load_users():

    if not os.path.exists(USER_FILE):
        return


    with open(USER_FILE,"r") as file:

        data = json.load(file)


    for name,info in data.items():

        user = User(
            name,
            info["pin"]
        )

        user.wallet._Wallet__balance = info["balance"]


        if info["bank"]:

            user.link_bank_account(
                info["bank"]["name"],
                info["bank"]["account"],
                info["bank"]["balance"]
            )


        users[name] = user

class Wallet:

    def __init__(self, pin):
        self.__balance = 0
        self.__pin = pin
        self.transactions = []

    def verify_pin(self, pin):
        return self.__pin == pin

    def add_money(self, amount):

        if amount > 0:
            self.__balance += amount

    def get_balance(self):
        return self.__balance

    def apply_cashback(self, amount):

        cashback = amount * 0.02

        self.__balance += cashback

        print(f"\n💸 Cashback Received: ₹{cashback}")

    def save_transaction_to_file(self, txn):

        transaction = {

            "time": txn.timestamp,
            "sender": txn.sender,
            "receiver": txn.receiver,
            "amount": txn.amount,
            "status": txn.status
        }

        data=[]

        if os.path.exists(TRANSACTION_FILE):

            with open(TRANSACTION_FILE,"r") as file:

                data=json.load(file)



        data.append(transaction)


        with open(TRANSACTION_FILE,"w") as file:

            json.dump(
                data,
                file,
                indent=4
            )

    def send_money(self, sender, receiver, amount, pin):

        txn = Transaction(sender, receiver, amount)

        # Incorrect PIN
        if not self.verify_pin(pin):

            txn.status = "FAILED - Incorrect PIN"

            self.transactions.append(txn)

            self.save_transaction_to_file(txn)

            return txn

        # Successful Transaction
        if self.__balance >= amount:

            self.__balance -= amount

            receiver.wallet.add_money(amount)

            txn.status = "SUCCESS"

            self.apply_cashback(amount)

        # Insufficient Balance
        else:

            txn.status = "FAILED - Insufficient Balance"

        self.transactions.append(txn)

        self.save_transaction_to_file(txn)

        return txn

    def show_transactions(self):

        if not self.transactions:

            print("\n❌ No Transactions Found")
            return

        print("\n📜 Transaction History:\n")

        for txn in self.transactions:
            print(txn)



    def show_saved_transactions(self):

        try:
            if not os.path.exists(TRANSACTION_FILE):
                print("\n❌ Transaction File Not Found")
                return

            with open(TRANSACTION_FILE, "r") as file:
                data = json.load(file)

            if data:
                print("\n📂 Saved Transactions:\n")
                for txn in data:
                    time = txn.get("time", "")
                    sender = txn.get("sender", "")
                    receiver = txn.get("receiver", "")
                    amount = txn.get("amount", "")
                    status = txn.get("status", "")
                    print(f"{time} | {sender} -> {receiver} : ₹{amount} [{status}]")
            else:
                print("\n❌ No Saved Transactions")

        except (FileNotFoundError, json.JSONDecodeError):
            print("\n❌ Transaction File Not Found or Corrupted")


    def show_analytics(self):

        total_sent = 0
        successful = 0
        failed = 0

        for txn in self.transactions:

            if txn.status == "SUCCESS":

                total_sent += txn.amount
                successful += 1

            else:

                failed += 1


        print("\n📊 EXPENSE ANALYTICS")
        print(f"💸 Total Amount Sent: ₹{total_sent}")
        print(f"✅ Successful Transactions: {successful}")
        print(f"❌ Failed Transactions: {failed}")


class Transaction:

    def __init__(self, sender, receiver, amount):

        self.sender = sender.name
        self.receiver = receiver.name
        self.amount = amount
        self.status = "PENDING"

        self.timestamp = datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        )

    def __str__(self):

        return f"{self.timestamp} | {self.sender} -> {self.receiver} : ₹{self.amount} [{self.status}]"


class BankAccount:

    def __init__(self, bank_name, account_number, balance):

        self.bank_name = bank_name
        self.account_number = account_number
        self.balance = balance

    def show_bank_details(self):

        print("\n🏦 Bank Name:", self.bank_name)
        print("🔢 Account Number:", self.account_number)
        print("💰 Bank Balance: ₹", self.balance)


class User:

    def __init__(self, name, pin):

        self.name = name
        self.wallet = Wallet(pin)
        self.bank_account = None

    def link_bank_account(self, bank_name, account_number, balance):

        self.bank_account = BankAccount(
            bank_name,
            account_number,
            balance
        )

        print("\n✅ Bank Account Linked Successfully")


# ================= USERS ================= #

users = {}
load_users()

current_user = None


# ================= MAIN PROGRAM ================= #

while True:

    try:

        print("\n====== 💳 DIGITAL WALLET SYSTEM ======")

        print("1. Register User")
        print("2. Login")
        print("3. Add Money")
        print("4. Send Money")
        print("5. Check Balance")
        print("6. Transaction History")
        print("7. View Saved Transactions")
        print("8. Link Bank Account")
        print("9. View Bank Details")
        print("10. Expense Analytics")
        print("11. View All Users")
        print("12. Logout")
        print("13. Exit")

        choice = input("\nEnter Choice: ")

        # ================= REGISTER USER ================= #

        if choice == "1":

            name = input("Create Username: ")

            if name in users:

                print("\n❌ Username Already Exists")
                continue

            pin = int(input("Create 4-Digit PIN: "))

            users[name] = User(name, pin)
            save_users()

            print("\n✅ User Registered Successfully")

        # ================= LOGIN ================= #

        elif choice == "2":

            name = input("Enter Username: ")
            pin = int(input("Enter PIN: "))

            if name not in users:

                print("\n❌ User Not Found")
                continue

            if users[name].wallet.verify_pin(pin):

                current_user = users[name]

                print(f"\n✅ Welcome {name}")

            else:

                print("\n❌ Incorrect PIN")

        # ================= ADD MONEY ================= #

        elif choice == "3":

            if current_user is None:

                print("\n❌ Please Login First")
                continue

            amount = int(input("Enter Amount: ₹"))

            current_user.wallet.add_money(amount)
            save_users()

            print("✅ Money Added Successfully")

        # ================= SEND MONEY ================= #

        elif choice == "4":

            if current_user is None:

                print("\n❌ Please Login First")
                continue

            receiver_name = input("Enter Receiver Name: ")

            if receiver_name not in users:

                print("\n❌ User Not Found")
                continue

            amount = int(input("Enter Amount: ₹"))

            pin = int(input("Enter PIN: "))

            sender = current_user
            receiver = users[receiver_name]

            txn = sender.wallet.send_money(
                sender,
                receiver,
                amount,
                pin
            )

            print(txn)
            save_users()

        # ================= CHECK BALANCE ================= #

        elif choice == "5":

            if current_user is None:

                print("\n❌ Please Login First")
                continue

            print(f"\n💰 Current Balance: ₹{current_user.wallet.get_balance()}")

        # ================= TRANSACTION HISTORY ================= #

        elif choice == "6":

            if current_user is None:

                print("\n❌ Please Login First")
                continue

            current_user.wallet.show_transactions()

        # ================= SAVED TRANSACTIONS ================= #

        elif choice == "7":

            if current_user is None:

                print("\n❌ Please Login First")
                continue

            current_user.wallet.show_saved_transactions()

        # ================= LINK BANK ACCOUNT ================= #

        elif choice == "8":

            if current_user is None:

                print("\n❌ Please Login First")
                continue

            bank_name = input("Enter Bank Name: ")
            account_number = input("Enter Account Number: ")
            balance = int(input("Enter Bank Balance: ₹"))

            current_user.link_bank_account(
                bank_name,
                account_number,
                balance
            )
            save_users()

        # ================= VIEW BANK DETAILS ================= #

        elif choice == "9":

            if current_user is None:

                print("\n❌ Please Login First")
                continue

            if current_user.bank_account is None:

                print("\n❌ No Bank Account Linked")
                continue

            current_user.bank_account.show_bank_details()

        # ================= VIEW USERS ================= #
        elif choice == "10":

            if current_user is None:

                print("\n❌ Please Login First")
                continue

            current_user.wallet.show_analytics()

        elif choice == "11":

            print("\n👥 Registered Users:\n")

            for user in users:

                print(user)

        # ================= LOGOUT ================= #

        elif choice == "12":

            if current_user is None:

                print("\n❌ No User Logged In")

            else:

                print(f"\n👋 {current_user.name} Logged Out")

                current_user = None

        # ================= EXIT ================= #

        elif choice == "13":

            print("\n👋 Exiting Wallet System...")
            break

        # ================= INVALID CHOICE ================= #

        else:

            print("\n❌ Invalid Choice")

    except ValueError:

        print("\n⚠️ Invalid Input! Please enter numbers only.")