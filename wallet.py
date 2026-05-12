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
    
class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender.name
        self.receiver = receiver.name
        self.amount = amount
        self.status = "PENDING"

    def __str__(self):
        return f"{self.sender} -> {self.receiver} : {self.amount} [{self.status}]"

class User:
    def __init__(self, name, pin):
        self.name = name
        self.wallet = Wallet(pin)


u1 = User("Akshay", 1234)
u2 = User("Rahul", 5678)

u1.wallet.add_money(1000)

txn = u1.wallet.send_money(u1, u2, 300, 1234)

print(txn)

print("Akshay Balance:", u1.wallet.get_balance())
print("Rahul Balance:", u2.wallet.get_balance())