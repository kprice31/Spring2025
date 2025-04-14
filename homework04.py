from functools import wraps
import time

# Initializing a simple database
atm_database = {}

# Implement decorators
# Decorators

# Logs the operation name
def log_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Performing operation: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

# Only allows 'admin' as the first argument
def authorization_decorator(func):
    @wraps(func)
    def wrapper(user, *args, **kwargs):
        if user != "admin":
            print("[AUTH] Access denied. Only admin can perform this operation.")
            return None
        return func(*args, **kwargs)
    return wrapper

# Measures operation duration
def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[TIME] Operation took {end - start:.4f} seconds.")
        return result
    return wrapper


# Validates that account_number is a string and amount is a number if given
def validation_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            account_number = args[1]
            if not isinstance(account_number, str):
                print("[VALIDATION] Account number must be a string.")
                return None  # <-- make sure to return early!
            if len(args) > 2:
                amount = args[2]
                if not isinstance(amount, (int, float)):
                    print("[VALIDATION] Amount must be a number.")
                    return None  # <-- this prevents the original function from running
            return func(*args, **kwargs)
        except IndexError:
            print("[VALIDATION] Missing arguments.")
            return None
    return wrapper


# ATM Functions 
@authorization_decorator
@log_decorator
def check_balance(account_number):
    return atm_database.get(account_number, "Account not found.")


@validation_decorator
@timing_decorator
@authorization_decorator
@log_decorator
def deposit(account_number, amount):
    if account_number in atm_database:
        atm_database[account_number] += amount
        print(f"Successfully deposited ${amount}. Current balance: ${atm_database[account_number]}")
    else:
        print("Account not found.")


@validation_decorator
@timing_decorator
@authorization_decorator
@log_decorator
def withdraw(account_number, amount):
    if account_number in atm_database:
        if atm_database[account_number] >= amount:
            atm_database[account_number] -= amount
            print(f"Successfully withdrew ${amount}. Current balance: ${atm_database[account_number]}")
        else:
            print("Insufficient balance.")
    else:
        print("Account not found.")


@validation_decorator
@timing_decorator
@authorization_decorator
@log_decorator
def delete_account(account_number):
    if account_number in atm_database:
        del atm_database[account_number]
        print(f"Account '{account_number}' deleted successfully.")
    else:
        print(f"'{account_number}' not found in the database.")


# Test cases
atm_database = {"123456": 1000, "654321": 500}  # Sample accounts

# Test for checking balance of existing account
# Expected output: 1000
print(check_balance("admin", "123456"))

# Test for deposit in an amount of 200 to admin account and update of current balance 
# Expected output: 1200
deposit("admin", "123456", 200)  # Valid deposit

# Test for deposit in an amount of two hundred in string form and update of current balance 
# Expected output: invalid input, amount must be a number
deposit("admin", "123456", "two hundred") 

# Test for withdrawal of 300 to the corresponding admin account and update of current balance
# Expected output: 900
withdraw("admin", "123456", 300)  

# Test for withdraw of 2000 from corresponding admin account and update
# Expected output: invalid operation and insufficient balance
withdraw("admin", "123456", 2000)  

# Test for checking the balance of the corresponding admin account
# Expected output: 900
print(check_balance("admin", "123456"))

# Test for deletion of corresponding admin account 
# Expected output: account deleted successfully 
delete_account("admin", "654321")

# Test for check the balance of the corresponding admin account
# Expected output: invalid since account was deleted 
print(check_balance("admin", "654321"))

# Test for deposit as a user of 100 dollars into the corresponding user account (authorization decorator)
# Expected output: access denied since only admin can perform this operation. 
deposit("user", "123456", 100)