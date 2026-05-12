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

    def send_money(self, sender, receiver, amount, pin):

        txn = Transaction(sender, receiver, amount)

        if not self.verify_pin(pin):

            txn.status = "FAILED - Incorrect PIN"
            self.transactions.append(txn)

            return txn

        if self.__balance >= amount:

            self.__balance -= amount
            receiver.wallet.add_money(amount)

            txn.status = "SUCCESS"

        else:

            txn.status = "FAILED - Insufficient Balance"

        self.transactions.append(txn)

        return txn

    def show_transactions(self):

        if not self.transactions:
            print("\n❌ No Transactions Found")
            return

        print("\n📜 Transaction History:\n")

        for txn in self.transactions:
            print(txn)


class Transaction:

    def __init__(self, sender, receiver, amount):

        self.sender = sender.name
        self.receiver = receiver.name
        self.amount = amount
        self.status = "PENDING"

    def __str__(self):

        return f"{self.sender} -> {self.receiver} : ₹{self.amount} [{self.status}]"


class User:

    def __init__(self, name, pin):

        self.name = name
        self.wallet = Wallet(pin)


# ================= MAIN PROGRAM ================= #

u1 = User("Akshay", 1234)
u2 = User("Rahul", 5678)

while True:

    print("\n====== 💳 DIGITAL WALLET SYSTEM ======")
    print("1. Add Money")
    print("2. Send Money")
    print("3. Check Balance")
    print("4. Transaction History")
    print("5. Exit")

    choice = input("\nEnter Choice: ")

    # ADD MONEY
    if choice == "1":

        amount = int(input("Enter Amount: ₹"))

        u1.wallet.add_money(amount)

        print("✅ Money Added Successfully")

    # SEND MONEY
    elif choice == "2":

        amount = int(input("Enter Amount: ₹"))
        pin = int(input("Enter PIN: "))

        txn = u1.wallet.send_money(u1, u2, amount, pin)

        print(txn)

    # CHECK BALANCE
    elif choice == "3":

        print(f"\n💰 Current Balance: ₹{u1.wallet.get_balance()}")

    # TRANSACTION HISTORY
    elif choice == "4":

        u1.wallet.show_transactions()

    # EXIT
    elif choice == "5":

        print("\n👋 Exiting Wallet System...")
        break

    # INVALID CHOICE
    else:

        print("\n❌ Invalid Choice")