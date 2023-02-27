import requests
from datetime import datetime, timedelta
import time
import telebot
import logging

# Set up logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up the Hybrid-Analysis API credentials
api_key = 'YOUR_API_KEY'

# Set up the Telegram bot credentials
bot_token = 'YOUR_BOT_TOKEN'
chat_id = 'YOUR_CHAT_ID'
bot = telebot.TeleBot(bot_token)

try:
    # Set up the start and end times for the top 20 submissions
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=1)

    # Get the top 20 malicious files for the specified time period from the Hybrid-Analysis API
    response = requests.get(f'https://www.hybrid-analysis.com/api/v2/latest-submissions?start={start_time}&end={end_time}&sort=score&order=desc&size=20', headers={'api-key': api_key})
    response.raise_for_status()
    top_20 = []
    for submission in response.json()['data']:
        sha256 = submission['sha256']
        severity = submission['severity']
        top_20.append(f'{sha256} ({severity})')

    # Send the top 20 malicious files to the Telegram bot
    message = f'Top 20 Malicious Files for {start_time.date()}:\n\n' + '\n'.join(top_20)
    bot.send_message(chat_id, message)

except Exception as e:
    # Handle any errors that occur during the scraping or sending process
    logging.error(f'Error occurred: {e}')
    bot.send_message(chat_id, f'Error occurred while fetching top 20 malicious files: {e}')
