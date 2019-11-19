```
#!/usr/bin/env python3
from concurrent.futures import ThreadPoolExecutor
from random import randint
from time import sleep
import threading

class Account():
    def __init__(self, balance = 0):
        self._balance = balance
        lock = threading.Lock()
        self._condition = threading.Condition(lock)
    
    def deposit(self, money):
        with self._condition:
            new_balance = self._balance + money
            sleep(0.01)
            self._balance = new_balance
            self._condition.notify_all()
    
    def withdraw(self, money):
        with self._condition:
            while money > self._balance:
                self._condition.wait()
            
            new_balance = self._balance - money
            sleep(0.05)
            self._balance = new_balance

def add_money(account):
    while True:
        money = randint(5,8)
        account.deposit(money)        
        print(threading.current_thread().name, ":", money, "=====>", account._balance)


def sub_money(account):
    while True:
        money = randint(30,50)
        account.withdraw(money)        
        print(threading.current_thread().name, ":", money, "<=====", account._balance)

def main():
    account = Account()
    with ThreadPoolExecutor(max_workers=10) as pool:
        for _ in  range(5):
            pool.submit(add_money, account)
            pool.submit(sub_money, account)

if __name__ == "__main__":
    main()
```

