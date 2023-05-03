from colorama import Back, Fore, Style, init
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError
import configparser
import sys
import csv
import time

init(autoreset=True)
SLEEP_TIME = 30


class main():
    def banner():
        print(Back.LIGHTBLUE_EX + Fore.BLACK + "TELEGRAM SPAM BOT SCRIPT" + Style.RESET_ALL + "\n" +
              Back.LIGHTMAGENTA_EX + Fore.BLACK + "BY WANPAKU_SQUAD")

    def send_sms():
        try:
            config = configparser.RawConfigParser()
            config.read('config.data')
            api_id = config['data']['api_id']
            api_hash = config['data']['api_hash']
            phone = config['data']['phone_number']
        except KeyError:
            main.banner()
            print("\n\n" + Back.LIGHTRED_EX + Fore.BLACK + "ERROR: FILL CONFIG.DATA FIRST")
            sys.exit(1)

        client = TelegramClient(phone, api_id, api_hash, device_model="tg_tools")

        client.connect()
        if not client.is_user_authorized():
            client.send_code_request(phone)
            main.banner()
            client.sign_in(phone,
                           input("\n\n" + Back.BLUE + Fore.BLACK + "Enter code from telegram:"))

        main.banner()
        input_file = "members.csv"
        users = []
        with open(input_file, encoding='UTF-8') as f:
            rows = csv.reader(f, delimiter=",", lineterminator="\n")
            next(rows, None)
            for row in rows:
                user = {
                    'username': row[0],
                    'id': int(row[1]),
                    'access_hash': int(row[2]),
                    'name': row[3]
                }
                users.append(user)
        print("\n" + Back.LIGHTBLACK_EX + Fore.LIGHTWHITE_EX + "SELECT MODE:")
        print(Back.BLUE + Fore.BLACK + "[1] " + "Send message by user ID" + Style.RESET_ALL + "\n" +
              Back.BLUE + Fore.BLACK + "[2] " + "Send message by username")
        mode = int(input(Back.GREEN + Fore.BLACK + "Enter number:" + Style.RESET_ALL + " "))

        message = input(Back.GREEN + Fore.BLACK + "Enter Your Message:" + Style.RESET_ALL + " ")
        print("\n")

        for user in users:
            if mode == 2:
                if user['username'] == "":
                    continue
                receiver = client.get_input_entity(user['username'])
            elif mode == 1:
                receiver = InputPeerUser(user['id'], user['access_hash'])
            else:
                print(Back.LIGHTRED_EX + Fore.BLACK + "Invalid Mode. Exiting.")
                client.disconnect()
                sys.exit()
            try:
                print(Back.LIGHTBLACK_EX + Fore.LIGHTWHITE_EX + "Sending Message to:", user['name'])
                client.send_message(receiver, message.format(user['name']))
                print(Back.LIGHTBLACK_EX + Fore.LIGHTWHITE_EX + "Waiting {} seconds".format(SLEEP_TIME))
                time.sleep(SLEEP_TIME)
            except PeerFloodError:
                print(
                    Back.LIGHTRED_EX + Fore.BLACK + "Getting Flood Error from telegram" + Style.RESET_ALL + "\n" +
                    Back.LIGHTRED_EX + Fore.BLACK + "Script is stopping now" + Style.RESET_ALL + "\n" +
                    Back.LIGHTRED_EX + Fore.BLACK + "Please try again after some time")
                client.disconnect()
                sys.exit()
            except Exception as e:
                print(Back.LIGHTRED_EX + Fore.BLACK + "Error:" + e)
                print(Back.LIGHTRED_EX + Fore.BLACK + "Trying to continue...")
                continue
        client.disconnect()
        print(Back.LIGHTGREEN_EX + Fore.BLACK + "Done. Message sent to all users.")


main.send_sms()
