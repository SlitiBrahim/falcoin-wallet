from pyfiglet import Figlet
import sys

def main():
    f = Figlet(font='doom')
    print(f.renderText("Falcoin Wallet"))

    def create_account():
        print('create account')

    def sign_in():
        print('sign in')

    def send_transaction():
        print('send transaction')

    def my_transactions():
        print('my transactions')

    def logout():
        print('logout')

    def exit_app():
        print('exit')
        sys.exit(0)

    # list of commands as (menu_item, func, must_be_connected)
    main_menu_items = [
        ('Create account', create_account, False),
        ('Sign in', sign_in, False),
        ('Send transaction', send_transaction, True),
        ('My transactions', my_transactions, True),
        ('Logout', logout, True),
        ('Exit', exit_app, False),
    ]

    def display_menu(menu_items, is_connected):
        for index, item in enumerate(menu_items):
            cmd_title, func, must_be_connected = item
            if must_be_connected and not is_connected:
                continue
            print("[{}] {}".format(index, cmd_title))

    connected = False

    while True:
        display_menu(main_menu_items, connected)
        choice = int(input('>> '))
        assert choice >= 0
        try:
            main_menu_items[choice][1]()
        except IndexError:
            print("You must issue a number available in the commands above.")
            print("If you want to quit program, select the Exit command.\n")


if __name__ == '__main__':
    main()
