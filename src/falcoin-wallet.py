from pyfiglet import Figlet
import sys
import re
import crypto
import time
from User import User

user = None


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


def create_account():
    print('create account')
    print("Generating key pair...")
    # faking load
    time.sleep(1)
    private_key, public_key = crypto.generate_key_pair()

    # TODO: Save user in db

    display_banner_keys(private_key, public_key)

    return User(private_key, time.time())


def sign_in():
    global user

    print('sign in')

    p_key_reg = r"^\w+$"
    user_input = ""
    is_valid_input = False
    has_retried = False
    while not is_valid_input:
        user_input = input('>> Please enter {} private key: '.format("a valid" if has_retried else "your"))
        is_valid_input = re.match(p_key_reg, user_input)
        has_retried = not is_valid_input
    print("Your private key:", user_input)
    # TODO: check if private key exists in db
    # TODO: if user exists, hydrate user obj
    user = User()

    if user is not None:
        print("You are connected now.")
    else:
        print("Invalid private key.")


def send_transaction():
    print('send transaction')


def my_transactions():
    print('my transactions')


def logout():
    global user

    print('logging out')
    user = None


def exit_app():
    print('exit')
    sys.exit(0)


def display_menu(menu_items, is_connected):
    for index, item in enumerate(menu_items):
        cmd_title, func, must_be_connected, hide_if_connected = item
        if (must_be_connected and not is_connected) or (hide_if_connected and is_connected):
            continue
        print("[{}] {}".format(index, cmd_title))


def display_balance(user):
    # TODO: Get user's balance from API
    print("\n== Balance: {} falcoins. ==\n".format(0.0))


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
