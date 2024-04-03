# 1. Start by importing the necessary libraries and setting up the API clients 
import requests
import json
import os
import threading
import subprocess
import re
# import credentials from creds.py
from creds import BOT_TOKEN, CHATBOT_HANDLE, CHAT_ID

# Function that sends a message to a specific telegram group
def telegram_bot_sendtext(bot_message,chat_id):
    data = {
        'chat_id': chat_id,
        'text': bot_message,
        'parse_mode':'MarkdownV2'
    }
    response = requests.post(
        'https://api.telegram.org/bot' + BOT_TOKEN + '/sendMessage',
        json=data,
        timeout=5
    )
    return response.json()

# 3b. Function that sends an image to a specific telegram group
def telegram_bot_sendimage(image_url, group_id):
    data = {
        'chat_id': group_id, 
        'photo': image_url
    }
    url = 'https://api.telegram.org/bot' + BOT_TOKEN + '/sendPhoto'
    
    response = requests.post(url, data=data, timeout=5)
    return response.json()

# Call 
def main():
    #output = subprocess.check_output('./PrettyPrintDiskUsage.sh',stderr=subprocess.STDOUT,shell=True)
    #telegram_bot_sendtext('```\n' + output.decode('utf-8') + '```',CHAT_ID)
    zpool_output = subprocess.check_output('zpool list',stderr=subprocess.STDOUT,shell=True).decode('utf-8')
    print(zpool_output)
    free_space_search = re.search('T  (([0-9]+)(\.[0-9])*)T',zpool_output)
    free_space = free_space_search.group(1)
    print(free_space)
# Run the main function
if __name__ == "__main__":
    main()
