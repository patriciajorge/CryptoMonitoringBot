import requests
import logging
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
import schedule
from time import sleep
from datetime import datetime

load_dotenv()

# Variable to store the previous Bitcoin price for comparison
previous_bitcoin_price = None

def get_user_value():
    logging.info('Enter an amount and your email to receive notifications about the Bitcoin value.')
    value = int(input('Enter a value: '))
    email = input('Enter your email: ')
    logging.info(f"Monitoring Bitcoin price. Alerts will be sent if the price falls below ${value}. Notifications will be sent to {email}.")
    return value, email

def get_crypto_value_from_api():
    API_KEY = os.getenv('API_KEY')
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY
    }
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    params = {
        'start': '1',
        'limit': '1',
        'convert': 'USD'
    }
    logging.info('Fetching the latest Bitcoin price from the API...')
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        bitcoin_data = data['data'][0]['quote']['USD']
        bitcoin_price = bitcoin_data['price']
        volume_24h = bitcoin_data['volume_24h']  # Get 24h volume from the API
        return bitcoin_price, volume_24h
    else:
        logging.error(f"Error obtaining data from the API: {response.status_code}")
        return None, None

def calculate_variation(current_price):
    global previous_bitcoin_price
    if previous_bitcoin_price is None:
        previous_bitcoin_price = current_price
        return 0, 0  # No variation on the first run
    else:
        price_difference = current_price - previous_bitcoin_price
        percentage_change = (price_difference / previous_bitcoin_price) * 100
        previous_bitcoin_price = current_price
        return price_difference, percentage_change

def send_email(email, value, bitcoin_price, volume_24h, price_difference, percentage_change):
    logging.info('Creating a report to send to your email...')
    EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

    try:
        if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
            raise EnvironmentError("Environment variables EMAIL_ADDRESS and EMAIL_PASSWORD are not set.")
        
        mail = EmailMessage()
        mail['Subject'] = 'Bitcoin Price Monitoring Report'
        mail['From'] = EMAIL_ADDRESS
        mail['To'] = email

        trend_arrow = '⬆️' if price_difference > 0 else '⬇️'

        message = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Bitcoin Price Monitoring Report</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    color: #333;
                }}
                .container {{
                    max-width: 800px;
                    margin: 20px auto;
                    padding: 20px;
                    background: #fff;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }}
                h1 {{
                    color: #4caf50;
                    text-align: center;
                }}
                .price {{
                    font-size: 2em;
                    text-align: center;
                    margin: 20px 0;
                }}
                .stats {{
                    margin: 20px 0;
                }}
                .footer {{
                    text-align: center;
                    font-size: 0.8em;
                    color: #999;
                    margin-top: 20px;
                }}
            </style>
        </head>
        <body>
        <div class="container">
            <h1>Bitcoin Price Monitoring Report</h1>
            <div class="price">
                Current Bitcoin Price: ${bitcoin_price:.4f} {trend_arrow}
            </div>
            <div class="stats">
                <p>Price Change: ${price_difference:.2f} ({percentage_change:.2f}%)</p>
                <p>24h Trading Volume: ${volume_24h:,.2f}</p>
            </div>
            <div class="footer">
                &copy; 2024 Bitcoin Monitor. All rights reserved.
            </div>
        </div>
        </body>
        </html>
        '''

        mail.set_content(message, subtype='html')

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(mail)

        logging.info(f"Notification email sent to {email}.")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

def schedule_email(value, email):
    logging.info('Setting up the email notification schedule...')
    schedule.every(10).minutes.do(lambda: send_scheduled_email(value, email))

def send_scheduled_email(value, email):
    bitcoin_price, volume_24h = get_crypto_value_from_api()

    if bitcoin_price is not None:
        price_difference, percentage_change = calculate_variation(bitcoin_price)
        logging.info(f"Current Bitcoin Price: ${bitcoin_price:.2f} | 24h Volume: ${volume_24h:,.2f}")
        send_email(email, value, bitcoin_price, volume_24h, price_difference, percentage_change)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
    value, email = get_user_value()

    # Fetch the initial data and send the first report
    bitcoin_price, volume_24h = get_crypto_value_from_api()

    if bitcoin_price is not None:
        price_difference, percentage_change = calculate_variation(bitcoin_price)
        logging.info(f"Initial Bitcoin Price: ${bitcoin_price:.2f} | 24h Volume: ${volume_24h:,.2f}")
        send_email(email, value, bitcoin_price, volume_24h, price_difference, percentage_change)

    schedule_email(value, email)

    logging.info('Bitcoin price monitoring started.')
    while True:
        schedule.run_pending()
        sleep(1)
