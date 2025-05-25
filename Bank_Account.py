import json
from datetime import datetime
import time
file_location = 'Bank Simulator/accounts.json'


class BankAccount:
 
    def __init__(self, account_holder, account_number, account_balance):
        self.account_holder = account_holder
        self.account_number = account_number
        self.account_balance = account_balance
        self.transactions = []

    def add_account(self):

        with open(file_location, 'r') as accounts_dataFile:
            try:
                accounts_info = json.load(accounts_dataFile)
                for account_info in accounts_info:
                    # this loop goes through enitre list of accounts in dictionary form. if it comes out of this loop
                    if account_info.get('account holder', '').lower() == self.account_holder.lower():
                        # succesfully (cuz it didnt come at return) , this means account dne!
                        print('Account already exists')
                        return

                new_account = {
                    "account holder": self.account_holder,
                    "account number": self.account_number,
                    "account balance": self.account_balance,
                    "transactions": []

                }
                # added new account to the account_info list
                accounts_info.append(new_account)
                print(
                    f"\nAccount created successfully by the name of {self.account_holder}")
                with open(file_location, 'w') as f:
                    json.dump(accounts_info, f, indent=2)

            except json.JSONDecodeError:
                accounts_info = []
                with open(file_location, 'w') as f:
                    json.dump(accounts_info, f, indent=2)

    def view_account_info(self):
        display_message = f"""
    📄 Bank Account Summary
    ------------------------
    🧑 Account Holder : {self.account_holder}
    🏦 Account Number : {self.account_number}
    💰 Account Balance: ${self.account_balance:.2f}
    """
        print(f"\n{display_message.strip()}")

    def deposit_money(self, amount):
        with open(file_location, 'r') as f:
            accounts = json.load(f)  # list of all accounts
            for account in accounts:
                if account.get('account holder').lower() == self.account_holder.lower():

                    # Use current balance from JSON instead of self.account_balance
                    current_balance = account.get('account balance', 0)
                    new_balance = current_balance + amount
                    account['account balance'] = new_balance
                    self.account_balance = new_balance  # Sync back to self
                    print(f'\nSuccesfully deposited {amount}')

                    # calculating day and time of deposit
                    now = datetime.now()
                    date_str = now.strftime("%d/%m/%Y")
                    time_str = now.strftime("%H:%M:%S")
                    time = f"{date_str} {time_str}"

                    # Appending to the transaction history
                    transaction_details = {
                        "type": "deposit",
                        "amount_deposited": amount,
                        "time of deposit": time
                    }
                    # list of history of transactions
                    transaction_history = account['transactions']
                    transaction_history.append(transaction_details)
                    # writing the changes to accounts.json

                    with open(file_location, 'w') as file:
                        json.dump(accounts, file , indent=1)

                    print(f'\nEvaluating account details after depositing {amount}...\n')
                    self.view_account_info()

    def withdraw_money(self, amount):
        with open(file_location, 'r') as f:
            accounts = json.load(f)  # list of all accounts
            for account in accounts:
                if account['account holder'].lower() == self.account_holder.lower():
                    if amount > account.get('account balance'):
                        print(f'\nYou do not have enough balance to withdraw {amount}')
                        return
                     # Use current balance from JSON instead of self.account_balance
                    current_balance = account.get('account balance', 0)
                    new_balance = current_balance - amount
                    account['account balance'] = new_balance
                    self.account_balance = new_balance  # Sync back to self
                    print(f'\nSuccesfully withdrawn {amount}')

                    now = datetime.now()
                    date_str = now.strftime("%d/%m/%Y")
                    time_str = now.strftime("%H:%M:%S")
                    time = f"{date_str} {time_str}"
                    transaction_info = {
                        "type": "withdraw",
                        "amount": amount,
                        "time": time
                    }
                    transaction_list = account['transactions']
                    transaction_list.append(transaction_info)
                    with open(file_location, 'w') as file:
                        json.dump(accounts, file , indent = 1)

                    print(f'Evaluating account details after withdrawing {amount}...\n')
                    self.view_account_info()

    def view_transaction_history(self):

        with open(file_location, 'r') as f:
            accounts = json.load(f)
            print('\nLooking for transaction history \n')
            time.sleep(1)
            for account in accounts:
                if account.get('account holder').lower() == self.account_holder.lower():
                    transactions = account.get('transactions')
                    for transaction in transactions:
                        prettier_transaction = json.dumps(transaction , indent = 2)
                        print(prettier_transaction + '\n')
    
    def transfer_money(self , receiver_account_holder , amount):

        
        with open (file_location , 'r') as f:
            accounts = json.load(f)

            # Checking if receiver_account_holder exists or not. 
            # If it does , store the reciever account in a variable
            for account in accounts:
                if account.get('account holder').lower() == receiver_account_holder.lower():
                    receiver_account = account
                    break
            else:
                print(f'No account exists by the name of {receiver_account_holder}')

            # Storing the senders account in a variable
            for account in accounts:
                if account.get('account holder').lower() == self.account_holder.lower():
                    sender_account = account            

            # Check if you have enough money
            current_sender_balance = sender_account.get('account balance')
            if current_sender_balance < amount:
                print(f'You do not have enough money to transfer {amount}')
                return
            
            # If you've made it till here , this means you have enough balance and also
            # the recivers acccount exists

            # Changing senders account details
            new_sender_balance = current_sender_balance - amount
            sender_account['account balance'] = new_sender_balance
            self.account_balance = new_sender_balance
            transaction_history = sender_account.get('transactions')
            transaction_details = {
                "type": "transfer", 
                "amount": amount,
                "trasnferred_to": receiver_account_holder,
            }
            transaction_history.append(transaction_details)
            
            # Changing receivers account details
            current_receiver_balance = receiver_account.get('account balance')
            new_receiver_balance = current_receiver_balance + amount
            receiver_account['account balance'] = new_receiver_balance

            with open (file_location , 'w') as file:
                json.dump(accounts , file , indent = 1)




new_account1 = BankAccount('Abdul Ahad', 19900, 21000)
new_account2 = BankAccount('Alice', 19900, 50000)
#new_account1.add_account()
#new_account2.add_account()
#new_account1.view_account_info()
#new_account2.view_account_info()
#new_account1.deposit_money(4000)
#new_account1.withdraw_money(5000)
#new_account1.view_transaction_history()
#new_account1.view_transaction_history()
