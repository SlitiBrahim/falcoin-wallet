from pyfiglet import Figlet
import sys
import re
import crypto
import time
from User import User
from Repository import Repository
from ApiManager import ApiManager
from Transaction import Transaction

user = None
repository = None


def is_user_connected():
    global user

    return user is not None


def display_banner_keys(private_key, public_key):
    print()
    print('*' * 126)
    print('*' * 37 + " WARNING: SAVE YOUR PRIVATE KEY AND KEEP IT SECRET " + '*' * 37)
    print('*' * 37 + " IF YOU LOSE YOUR PRIVATE KEY YOU'LL LOSE YOUR COINS " + '*' * 37)
    print('*' * 20 + " YOU SHOULD ONY SHARE YOUR PUBLIC KEY SO PEOPLE CAN MAKE TRANSACTIONS TO YOUR ACCOUNT " + '*' * 20)
    print('*' * 37 + " Private key: {} ".format(private_key) + '*' * 37)
    print('*' * 37 + " Public key: {} ".format(public_key) + '*' * 37)
    print('*' * 126)
    print()


def display_tx_confirmation(tx, balance, tx_amount):
    print()
    print(('#' * 20) + "\tTRANSACTION CONFIRMATION\t" + '#' * 20)
    print("Your actual balance: {}".format(coins_amount_msg(balance)))
    print("Your balance after validation of transaction by miners: {}".format(coins_amount_msg(balance - tx_amount)))
    print('-' * 72)
    print('Transaction amount: {}'.format(coins_amount_msg(tx_amount)))
    print('Recipient: {}'.format(tx.get_outputs()[0].get_pubkey()))
    print('#' * 72)
    print()


def coins_amount_msg(amount):
    return "{} Falcoin{} (FLC)".format(amount, 's' if amount >= 2.0 else '')


def ask_for_validation(msg=None):
    default_msg = "> Do you want to validate ? "\
                  "\nEnter 'y' if yes, 'n' if you want to abort: "

    user_input = ""
    while user_input != 'y' and user_input != 'n':
        user_input = input(msg if msg is not None else default_msg)

    return user_input is 'y'


def create_account():
    global repository

    print(' [*] Creation of your account.')
    print(" [*] Generating key pair...")
    # faking load
    time.sleep(1)
    private_key, public_key = crypto.generate_key_pair()
    new_user = User(private_key, time.time())

    repository.save_user(new_user)

    display_banner_keys(private_key, public_key)

    return new_user


def sign_in():
    global user
    global repository

    print('[*] Signing in.')

    key_reg = r"^\w+$"
    user_input = ""
    is_valid_input = False
    has_retried = False
    while not is_valid_input:
        user_input = input('> Please enter {} private key: '.format("a valid" if has_retried else "your"))
        is_valid_input = re.match(key_reg, user_input)
        has_retried = not is_valid_input

    print('[*] Connection...')
    # fake connecting user
    time.sleep(1)
    user = repository.get_user(user_input)
    if user is not None:
        print("You are connected now.")
    else:
        print("Failed, this private key is not registered.")


def send_transaction():
    global user

    print('[*] Making transaction.')
    print("[*] Getting user balance...")
    time.sleep(0.5)
    balance = ApiManager.get_balance(user.get_public_key())
    print("User balance = {}.".format(coins_amount_msg(balance)))
    if balance == 0.0:
        print("You currently don't have any coin, you cannot make a transaction.")
        return

    while True:
        try:
            tx_amount = float(input("> Enter the amount of the transaction: "))
            break
        except ValueError:
            print('Please enter a float number.')

    # as asked in the project specs, txs are fee-less but it can be modified
    fees = Transaction.fees_default_amount
    if balance + fees < tx_amount:
        print("Transaction error:")
        if balance < tx_amount:
            print("Your balance ({}) is lower than the amount of "
                  "the transaction you want to create which is equals to {}."
                  .format(balance, tx_amount))
        elif balance + fees < tx_amount:
            print("Your balance ({}) + fees ({}) = {} is lower than the amount of "
                  "the transaction you want to create which is equals to {}."
                  .format(balance, fees, balance + fees, tx_amount))

        return

    key_reg = r"^\w+$"
    user_input = ""
    is_valid_input = re.match(key_reg, user_input)
    has_retried = False
    while not is_valid_input:
        user_input = input('> {}Please enter the public key of your recipient: '
                           .format("Public key is not valid. " if has_retried else ""))
        is_valid_input = re.match(key_reg, user_input)
        has_retried = not is_valid_input

    tx_pubkey = user_input

    transaction = Transaction.make_transaction(user, tx_amount, tx_pubkey, fees, ApiManager)

    display_tx_confirmation(transaction, balance, tx_amount)
    did_user_validates = ask_for_validation()

    if did_user_validates:
        # TODO: Send transaction to api

        print("Success ! The transaction has been sent to the blockchain. "
              "It is going to be validated by miners, please wait for confirmation.\n"
              "It may take some time to reflect changes on your account.")
    else:
        print("Transaction has been aborted.")


def my_transactions():
    global user

    user_txs = ApiManager.get_transactions(user.get_public_key())
    print("{} transactions.".format(len(user_txs)))
    # TODO: display transactions in table


def logout():
    global user

    print('[*] Logging out user...\n')
    time.sleep(0.3)
    user = None


def exit_app():
    print('[*] Exiting application.')
    sys.exit(0)


def display_menu(menu_items, is_connected):
    for index, item in enumerate(menu_items):
        cmd_title, func, must_be_connected, hide_if_connected = item
        if (must_be_connected and not is_connected) or (hide_if_connected and is_connected):
            continue
        print("[{}] {}".format(index, cmd_title))


def display_balance(user):
    balance = ApiManager.get_balance(user.get_public_key())
    print("\n== Balance: {} ==\n".format(coins_amount_msg(balance)))


def main():
    f = Figlet(font='doom')
    print(f.renderText("Falcoin Wallet"))

    # list of commands as (menu_item, func, must_be_connected, hide_if_connected)
    main_menu_items = [
        ('Create account', create_account, False, True),
        ('Sign in', sign_in, False, True),
        ('Send transaction', send_transaction, True, False),
        ('My transactions', my_transactions, True, False),
        ('Logout', logout, True, False),
        ('Exit', exit_app, False, False),
    ]

    global repository
    repository = Repository()
    repository.init_db()

    while True:
        if is_user_connected():
            display_balance(user)

        display_menu(main_menu_items, is_user_connected())
        choice = int(input('>> '))
        assert choice >= 0
        try:
            main_menu_items[choice][1]()
        except IndexError:
            print("You must issue a number available in the commands above.")
            print("If you want to quit program, select the Exit command.\n")


if __name__ == '__main__':
    main()
