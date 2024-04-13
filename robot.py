# 1. Start by importing the necessary libraries and setting up the API clients 
import requests
import json
import os
import threading
import subprocess
import re
# import credentials from creds.py
from creds import BOT_TOKEN, CHATBOT_HANDLE, CHAT_ID, TAUTULLI_API_KEY, TAUTULLI_LOCATION

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
    #print(response.json())
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

def get_tautulli_stats():
    response = requests.post("http://" + TAUTULLI_LOCATION + "/api/v2?apikey=" + TAUTULLI_API_KEY + "&cmd=get_home_stats&time_range=7").json()
    #print(response['response']['data'])
    stats= "Most Popular Movie of last week: " + response['response']['data'][1]['rows'][0]['title'] + " (" + str(response['response']['data'][1]['rows'][0]['users_watched']) + " Users)"
    stats+= "\nMost Popular TV Show of last week: " + response['response']['data'][3]['rows'][0]['title'] + " (" + str(response['response']['data'][3]['rows'][0]['users_watched']) + " Users)"
    if(len(response['response']['data'][9]['rows']) > 0):
      stats+= "\nMost Popular Artist of last week: " + response['response']['data'][9]['rows'][0]['title'] + " (" + str(response['response']['data'][9]['rows'][0]['total_plays']) + " Plays)"

    #print(stats)
    return stats

# Call 
def main():
    output = subprocess.check_output('./PrettyPrintDiskUsage.sh',stderr=subprocess.STDOUT,shell=True)
    result = telegram_bot_sendtext('```\n' + output.decode('utf-8') + '```',CHAT_ID)
    print(result)
    zpool_output = subprocess.check_output('zfs list',stderr=subprocess.STDOUT,shell=True).decode('utf-8')
    #print(zpool_output)
    free_space_search = re.search('castor\/media.*T  (([0-9]+)(\.[0-9])*)T',zpool_output)
    free_space = float(free_space_search.group(1))
    last_week_file = open('lastweek', 'r')
    lines = last_week_file.readlines()
    last_week_file.close()
    last_week=float(lines[0].strip())
    #print("Last week's space remaining " + str(last_week) + "TB")
    burn_rate = (last_week - free_space)/7
    tautulli_stats = get_tautulli_stats()
    #have to escape . in the below re.escape() is the easiest way
    telegram_bot_sendtext(re.escape("Free space remaining: " + str(free_space) + "TB\n"+"Current burn rate: {:.3f}TB per day, {:.1f} days of storage remaining\n{}".format(burn_rate,free_space/burn_rate,tautulli_stats)),CHAT_ID)
    last_week_file = open('lastweek','w')
    last_week_file.writelines([str(free_space)])
    last_week_file.close()

    # Run the main function
if __name__ == "__main__":
    main()
