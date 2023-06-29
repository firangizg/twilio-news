import os
from dotenv import load_dotenv
import requests
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

# Load environment variables from .env file
load_dotenv()

# Fetch environment variables
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

app = Flask(__name__)

def fetch_news(api_key, keywords):
    url = 'https://newsapi.org/v2/everything?'  
    parameters = {
        'q': keywords,  
        'apiKey': api_key,
    }
    response = requests.get(url, params=parameters)
    news = response.json()
    if 'articles' in news and len(news['articles']) > 0:
        first_article = news['articles'][0]
        return f"{first_article['title']}\n{first_article['description']}\n{first_article['url']}"
    else:
        return "No news found."

def send_sms(news, account_sid, auth_token, twilio_number, user_number):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=news,  
        from_=twilio_number,
        to=user_number
    )
    return message.sid  

@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)

    # Start our TwiML response
    resp = MessagingResponse()

    # Fetch news about the keyword the user texted
    news = fetch_news(api_key=NEWSAPI_KEY, keywords=body)  

    # Add a message to the response
    resp.message(news)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
