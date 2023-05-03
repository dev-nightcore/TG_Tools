from colorama import Back, Fore, Style, init
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import configparser
import os, sys
import csv
import traceback
import time
import random

init(autoreset=True)


def banner():
    print(Back.BLUE + Fore.BLACK + "TELEGRAM PARSING SCRIPT" + Style.RESET_ALL + "\n" +
          Back.MAGENTA + Fore.BLACK + "BY WANPAKU_SQUAD")


try:
    config = configparser.RawConfigParser()
    config.read('config.data')
    api_id = config['data']['api_id']
    api_hash = config['data']['api_hash']
    phone = config['data']['phone_number']
    client = TelegramClient(phone, api_id, api_hash, device_model="vx_370Custom")
except KeyError:
    banner()
    print("\n\n" + Back.LIGHTRED_EX + Fore.BLACK + "ERROR: FILL CONFIG.DATA FIRST")
    sys.exit(1)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    banner()
    client.sign_in(phone, input("\n\n" + Back.BLUE + Fore.BLACK + "Enter code from telegram:"))

banner()
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

chats = []
last_date = None
chunk_size = 200
groups = []

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup == True:
            groups.append(chat)
    except:
        continue

print("\n\n" + Back.GREEN + Fore.BLACK + "Choose a group to scrape members:")

i = 0
for g in groups:
    print(Back.BLUE + Fore.BLACK + " " + str(i) + " " + Style.RESET_ALL + ' - ' + g.title)
    i += 1

g_index = input("\n" + Back.BLUE + Fore.BLACK + "Enter a Number:" + " ")
try:
    target_group = groups[int(g_index)]
except IndexError:
    print(Back.LIGHTRED_EX + Fore.BLACK + "No groups founded with this index")
    print(Back.LIGHTRED_EX + Fore.BLACK + "Stopping script")
    sys.exit(1)

target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)

print("\n" + Back.LIGHTBLACK_EX + Fore.LIGHTWHITE_EX + "SELECT MODE:")
print(Back.BLUE + Fore.BLACK + "[1] " + "Add member by user ID" + Style.RESET_ALL + "\n" +
      Back.BLUE + Fore.BLACK + "[2] " + "Add member by username")

mode = int(input(Back.GREEN + Fore.BLACK + "Enter number:" + Style.RESET_ALL + " "))

n = 0
print(users)
print('before for')
for user in users:
    n += 1
    if 1 == 1:
        time.sleep(1)
        try:
            print(Back.LIGHTWHITE_EX + Fore.BLACK + "Adding {}".format(user['id']))
            if mode == 1:
                if user['username'] == "":
                    continue
                user_to_add = client.get_input_entity(user['username'])
            elif mode == 2:
                user_to_add = InputPeerUser(user['id'], user['access_hash'])
            else:
                sys.exit(Back.LIGHTRED_EX + Fore.BLACK + "Invalid Mode Selected. Please Try Again.")
            client(InviteToChannelRequest(target_group_entity, [user_to_add]))
            print(Back.GREEN + Fore.BLACK + "Waiting for 20-30 Seconds...")
            time.sleep(random.randrange(20, 30))
        except PeerFloodError:
            print(
                Back.LIGHTRED_EX + Fore.BLACK + "Getting Flood Error from telegram" + Style.RESET_ALL + "\n" +
                Back.LIGHTRED_EX + Fore.BLACK + "Script is stopping now" + Style.RESET_ALL + "\n" +
                Back.LIGHTRED_EX + Fore.BLACK + "Please try again after some time")
        except UserPrivacyRestrictedError:
            print(Back.LIGHTRED_EX + Fore.BLACK + "The user's privacy settings do not allow you to do this. Skipping.")
        except:
            traceback.print_exc()
            print(Back.LIGHTRED_EX + Fore.BLACK + "Unexpected Error")
            continue
