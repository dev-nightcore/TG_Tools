from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import os, sys, configparser, csv, time

from colorama import Fore, Back, Style, init

init(autoreset=True)


def banner():
    print(Back.BLUE + Fore.BLACK + "TELEGRAM PARSING SCRIPT" + Style.RESET_ALL + "\n" +
          Back.MAGENTA + Fore.BLACK + "BY WANPAKU_SQUAD")


config = configparser.RawConfigParser()
config.read('config.data')

try:
    api_id = config['data']['api_id']
    api_hash = config['data']['api_hash']
    phone = config['data']['phone_number']
    client = TelegramClient(phone, api_id, api_hash, device_model="parsing")
except KeyError as e:
    banner()
    print("\n\n" + Back.LIGHTRED_EX + Fore.BLACK + "ERROR: FILL CONFIG.DATA FIRST")
    sys.exit(1)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    banner()
    client.sign_in(phone, input("\n\n" + Back.BLUE + Fore.BLACK + "Enter code from telegram:"))
banner()
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
target_group = groups[int(g_index)]

print("\n" + Back.CYAN + Fore.BLACK + "Fetching Members...")
time.sleep(1)
all_participants = []
all_participants = client.get_participants(target_group, aggressive=True)

print(Back.CYAN + Fore.BLACK + "Saving In file...")
time.sleep(1)
with open("members.csv", "w", encoding='UTF-8') as f:
    writer = csv.writer(f, delimiter=",", lineterminator="\n")
    writer.writerow(['username', 'user id', 'access hash', 'name'])
    for user in all_participants:
        if user.username:
            username = user.username
        else:
            username = ""
        if user.first_name:
            first_name = user.first_name
        else:
            first_name = ""
        if user.last_name:
            last_name = user.last_name
        else:
            last_name = ""
        name = (first_name + ' ' + last_name).strip()
        writer.writerow([username, user.id, user.access_hash, name])

print("\n" + Back.LIGHTGREEN_EX + Fore.BLACK + "Members scraped successfully")
