import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Backend and Sentiment Analyzer URLs
backend_url = os.getenv('backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', default="http://localhost:5050/")

def get_request(endpoint, **kwargs):
    """
    Perform a GET request to the backend with optional query parameters.
    """
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params += key + "=" + str(value) + "&"
    request_url = backend_url + endpoint + "?" + params
    print("GET from {} ".format(request_url))
    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as e:
        print("Network exception occurred:", e)
        return None

def analyze_review_sentiments(text):
    """
    Call the sentiment analyzer microservice to analyze review text.
    """
    request_url = sentiment_analyzer_url + "analyze/" + text
    print("Analyzing sentiment from {} ".format(request_url))
    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")
        return None

def post_review(data_dict):
    """
    Submit a review to the backend via POST request.
    """
    request_url = backend_url + "/insert_review"
    print("POST to {} ".format(request_url))
    try:
        response = requests.post(request_url, json=data_dict)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")
        return None
