import time
import os
import getpass
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colorama to add color styling in terminal output
init(autoreset=True)

class ATM:
    def __init__(self):
        # Simulating a predefined card and user details for the ATM
        self.card_number = '1234'
        self.pin = '5472'
        self.balance = 1000.0  # Default account balance
        self.max_pin_attempts = 3  # Maximum number of allowed PIN attempts
        self.pin_attempts = 0  # Counter for incorrect PIN attempts
        self.transaction_history = []  # To store the history of transactions

    def clear_screen(self):
        """Clear the console screen for a cleaner user experience."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def validate_pin(self, pin):
        """
        Validate the user-entered PIN.
        Tracks incorrect attempts and blocks the card after 3 incorrect attempts.
        """
        if self.pin_attempts >= self.max_pin_attempts:
            print(Fore.RED + "Card blocked. Too many incorrect attempts.")
            return False
        
        if pin == self.pin:
            self.pin_attempts = 0  # Reset attempts on successful validation
            return True
        
        self.pin_attempts += 1
        print(Fore.RED + f"Incorrect PIN. {self.max_pin_attempts - self.pin_attempts} attempts remaining.")
        return False

    def check_balance(self):
        """Return the current account balance."""
        return self.balance

    def deposit(self, amount):
        """
        Deposit money into the account.
        Updates the balance and records the transaction.
        """
        if amount > 0:
            self.balance += amount
            self._record_transaction('Deposit', amount)
            return True
        return False

    def withdraw(self, amount):
        """
        Withdraw money from the account.
        Ensures sufficient balance before proceeding.
        """
        if 0 < amount <= self.balance:
            self.balance -= amount
            self._record_transaction('Withdrawal', -amount)
            return True
        return False

    def transfer(self, amount, target_account):
        """
        Transfer money to another account.
        Requires sufficient balance to complete.
        """
        if 0 < amount <= self.balance:
            self.balance -= amount
            self._record_transaction(f'Transfer to {target_account}', -amount)
            return True
        return False

    def change_pin(self, new_pin):
        """
        Change the account PIN.
        Ensures the new PIN is a 4-digit numeric value.
        """
        if len(new_pin) == 4 and new_pin.isdigit():
            self.pin = new_pin
            self._record_transaction('PIN Change', 0)
            return True
        return False

    def _record_transaction(self, transaction_type, amount):
        """Record a transaction in the transaction history."""
        transaction = {
            'type': transaction_type,
            'amount': amount,
            'balance': self.balance,
            'timestamp': datetime.now()
        }
        self.transaction_history.append(transaction)

    def print_mini_statement(self):
        """
        Display the last 5 transactions in a concise format.
        Includes timestamp, type, amount, and balance.
        """
        print(Fore.YELLOW + "\n--- Mini Statement ---")
        for transaction in self.transaction_history[-5:]:
            print(Fore.GREEN + f"{transaction['timestamp'].strftime('%Y-%m-%d %H:%M')} | "
                  f"{transaction['type']}: ${abs(transaction['amount']):.2f} | "
                  f"Balance: ${transaction['balance']:.2f}")

def get_valid_float_input(prompt):
    """Prompt the user for a numeric input and validate it."""
    while True:
        try:
            amount = float(input(Fore.WHITE + prompt))
            return amount
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a number.")

def display_main_menu():
    """Display the main menu with various ATM service options."""
    print(Fore.YELLOW + "=" * 40)
    print(Fore.CYAN + "ATM SERVICES".center(40))
    print(Fore.YELLOW + "=" * 40)
    print(Fore.GREEN + "  1. Check Balance")
    print(Fore.GREEN + "  2. Deposit")
    print(Fore.GREEN + "  3. Withdraw")
    print(Fore.GREEN + "  4. Transfer")
    print(Fore.GREEN + "  5. Change PIN")
    print(Fore.GREEN + "  6. Mini Statement")
    print(Fore.GREEN + "  7. Exit")
    print(Fore.YELLOW + "=" * 40)

def main():
    """Main function to simulate the ATM's operations."""
    atm = ATM()  # Instantiate the ATM object
    atm.clear_screen()
    
    print(Fore.GREEN + "INSERT YOUR CARD".center(60))
    time.sleep(3)  # Simulate a delay for inserting the card
    
    while True:
        # Prompt the user to enter their PIN securely
        pin = getpass.getpass(Fore.WHITE + "ENTER THE PIN: ")
        
        if atm.validate_pin(pin):  # Validate the entered PIN
            while True:
                atm.clear_screen()
                display_main_menu()  # Show the ATM menu
                
                option = input(Fore.WHITE + "Choose option: ")
                
                if option == '1':  # Check balance
                    balance = atm.check_balance()
                    print(Fore.GREEN + f"Balance: ${balance:.2f}")
                    input(Fore.YELLOW + "Press Enter to continue...")
                
                elif option == '2':  # Deposit money
                    amount = get_valid_float_input("Deposit amount: $")
                    if atm.deposit(amount):
                        print(Fore.GREEN + "Deposit successful!")
                    input(Fore.YELLOW + "Press Enter to continue...")
                
                elif option == '3':  # Withdraw money
                    amount = get_valid_float_input("Withdrawal amount: $")
                    if atm.withdraw(amount):
                        print(Fore.GREEN + "Withdrawal successful!")
                    else:
                        print(Fore.RED + "Insufficient funds.")
                    input(Fore.YELLOW + "Press Enter to continue...")
                
                elif option == '4':  # Transfer money
                    target_account = input(Fore.WHITE + "Enter target account: ")
                    amount = get_valid_float_input("Transfer amount: $")
                    if atm.transfer(amount, target_account):
                        print(Fore.GREEN + "Transfer successful!")
                    else:
                        print(Fore.RED + "Transfer failed.")
                    input(Fore.YELLOW + "Press Enter to continue...")
                
                elif option == '5':  # Change PIN
                    new_pin = input(Fore.WHITE + "Enter new 4-digit PIN: ")
                    if atm.change_pin(new_pin):
                        print(Fore.GREEN + "PIN changed successfully!")
                    else:
                        print(Fore.RED + "Invalid PIN format.")
                    input(Fore.YELLOW + "Press Enter to continue...")
                
                elif option == '6':  # Print mini statement
                    atm.print_mini_statement()
                    input(Fore.YELLOW + "Press Enter to continue...")
                
                elif option == '7':  # Exit the application
                    print(Fore.GREEN + "Thank you for using our ATM.")
                    break
                
                else:
                    print(Fore.RED + "Invalid option. Please try again.")
                    input(Fore.YELLOW + "Press Enter to continue...")
            break
        
        if atm.pin_attempts >= 3:  # Block the card after 3 failed attempts
            print(Fore.RED + "Card blocked. Please contact customer support.")
            break

if __name__ == "__main__":
    main()