from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.views.decorators.csrf import csrf_exempt

from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments, post_review

# Get an instance of a logger
logger = logging.getLogger(__name__)

# ---------------- Cars ----------------
def get_cars(request): 
    """
    Return all car models and makes. Populate if empty.
    """
    count = CarMake.objects.filter().count() 
    if count == 0: 
        initiate() 
    car_models = CarModel.objects.select_related('car_make')
    cars = [] 
    for car_model in car_models: 
        cars.append({ 
            "CarModel": car_model.name, 
            "CarMake": car_model.car_make.name 
        }) 
    return JsonResponse({"CarModels": cars})

# ---------------- Authentication ----------------
@csrf_exempt
def login_user(request):
    """
    Authenticate and log in a user.
    """
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

def logout_request(request):
    """
    Log out the current user.
    """
    logout(request)
    return JsonResponse({"status": "Logged out"})

@csrf_exempt
def registration(request):
    """
    Register a new user.
    """
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    try:
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return JsonResponse({"status": "User created", "userName": username})
    except Exception as e:
        return JsonResponse({"status": "Error", "message": str(e)})

# ---------------- Dealerships ----------------
def get_dealerships(request, state="All"):
    """
    Get all dealerships or filter by state.
    """
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})

def get_dealer_details(request, dealer_id):
    """
    Get details for a specific dealer.
    """
    if dealer_id:
        endpoint = "/fetchDealer/" + str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

def get_dealer_reviews(request, dealer_id):
    """
    Get reviews for a dealer and analyze sentiment.
    """
    if dealer_id:
        endpoint = "/fetchReviews/dealer/" + str(dealer_id)
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            if response and 'sentiment' in response:
                review_detail['sentiment'] = response['sentiment']
            else:
                review_detail['sentiment'] = "unknown"
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

# ---------------- Reviews ----------------
@csrf_exempt
def add_review(request):
    """
    Add a new review for a dealer. Only authenticated users can post.
    """
    if request.method == "POST":
        if request.user.is_anonymous:
            return JsonResponse({"status": 403, "message": "Unauthorized"})
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse({"status": 200, "result": response})
        except Exception as e:
            return JsonResponse({"status": 401, "message": f"Error in posting review: {str(e)}"})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})
