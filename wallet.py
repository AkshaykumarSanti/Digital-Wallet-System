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

        with open("transactions.txt", "a") as file:

            file.write(str(txn) + "\n")

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

            with open("transactions.txt", "r") as file:

                data = file.read()

                if data:

                    print("\n📂 Saved Transactions:\n")

                    print(data)

                else:

                    print("\n❌ No Saved Transactions")

        except FileNotFoundError:

            print("\n❌ Transaction File Not Found")


class Transaction:

    def __init__(self, sender, receiver, amount):

        self.sender = sender.name
        self.receiver = receiver.name
        self.amount = amount
        self.status = "PENDING"

    def __str__(self):

        return f"{self.sender} -> {self.receiver} : ₹{self.amount} [{self.status}]"


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

users["Akshay"] = User("Akshay", 1234)
users["Rahul"] = User("Rahul", 5678)


# ================= MAIN PROGRAM ================= #

while True:

    try:

        print("\n====== 💳 DIGITAL WALLET SYSTEM ======")
        print("1. Add Money")
        print("2. Send Money")
        print("3. Check Balance")
        print("4. Transaction History")
        print("5. View Saved Transactions")
        print("6. Link Bank Account")
        print("7. View Bank Details")
        print("8. View All Users")
        print("9. Exit")

        choice = input("\nEnter Choice: ")

        # ================= ADD MONEY ================= #

        if choice == "1":

            name = input("Enter User Name: ")

            if name not in users:

                print("\n❌ User Not Found")
                continue

            amount = int(input("Enter Amount: ₹"))

            users[name].wallet.add_money(amount)

            print("✅ Money Added Successfully")

        # ================= SEND MONEY ================= #

        elif choice == "2":

            sender_name = input("Enter Sender Name: ")
            receiver_name = input("Enter Receiver Name: ")

            if sender_name not in users or receiver_name not in users:

                print("\n❌ User Not Found")
                continue

            amount = int(input("Enter Amount: ₹"))

            pin = int(input("Enter PIN: "))

            sender = users[sender_name]
            receiver = users[receiver_name]

            txn = sender.wallet.send_money(
                sender,
                receiver,
                amount,
                pin
            )

            print(txn)

        # ================= CHECK BALANCE ================= #

        elif choice == "3":

            name = input("Enter User Name: ")

            if name not in users:

                print("\n❌ User Not Found")
                continue

            print(f"\n💰 Current Balance: ₹{users[name].wallet.get_balance()}")

        # ================= TRANSACTION HISTORY ================= #

        elif choice == "4":

            name = input("Enter User Name: ")

            if name not in users:

                print("\n❌ User Not Found")
                continue

            users[name].wallet.show_transactions()

        # ================= SAVED TRANSACTIONS ================= #

        elif choice == "5":

            users["Akshay"].wallet.show_saved_transactions()

        # ================= LINK BANK ACCOUNT ================= #

        elif choice == "6":

            name = input("Enter User Name: ")

            if name not in users:

                print("\n❌ User Not Found")
                continue

            bank_name = input("Enter Bank Name: ")
            account_number = input("Enter Account Number: ")
            balance = int(input("Enter Bank Balance: ₹"))

            users[name].link_bank_account(
                bank_name,
                account_number,
                balance
            )

        # ================= VIEW BANK DETAILS ================= #

        elif choice == "7":

            name = input("Enter User Name: ")

            if name not in users:

                print("\n❌ User Not Found")
                continue

            if users[name].bank_account is None:

                print("\n❌ No Bank Account Linked")
                continue

            users[name].bank_account.show_bank_details()

        # ================= VIEW USERS ================= #

        elif choice == "8":

            print("\n👥 Registered Users:\n")

            for user in users:

                print(user)

        # ================= EXIT ================= #

        elif choice == "9":

            print("\n👋 Exiting Wallet System...")
            break

        # ================= INVALID CHOICE ================= #

        else:

            print("\n❌ Invalid Choice")

    except ValueError:

        print("\n⚠️ Invalid Input! Please enter numbers only.")