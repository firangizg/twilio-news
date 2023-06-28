import os
from dotenv import load_dotenv
import requests
from twilio.rest import Client
from flask import Flask, request

# Load environment variables from .env file
load_dotenv()

# Fetch environment variables
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

def fetch_news(api_key, keywords):
    url = 'https://newsapi.org/v2/everything?'  # Use the correct endpoint for your news API
    parameters = {
        'q': keywords,  # search query
        'apiKey': api_key,
    }
    response = requests.get(url, params=parameters)
    news = response.json()
    # For simplicity, we'll just return the first news article's title and description
    first_article = news['articles'][0]
    return f"{first_article['title']}\n{first_article['description']}"

def send_sms(news, account_sid, auth_token, twilio_number, user_number):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=news,  # Text of the message
        from_=twilio_number,
        to=user_number
    )
    return message.sid  # This is the ID of the message, useful for tracking

if __name__ == "__main__":
    news = fetch_news(api_key=NEWSAPI_KEY, keywords='artificial intelligence')  # Fetch news about AI
    send_sms(news=news, account_sid=TWILIO_ACCOUNT_SID, auth_token=TWILIO_AUTH_TOKEN, twilio_number=TWILIO_PHONE, user_number='+17852264968')  