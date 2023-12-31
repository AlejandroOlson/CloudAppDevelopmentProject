from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import CarDealer, DealerReview, CarModel, CarMake
# from .restapis import related methods
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request, get_dealer_name_by_id
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstName']
        last_name = request.POST['lastName']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))
            
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
            login(request, user)
            return redirect('djangoapp:index')
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://us-east.functions.appdomain.cloud/api/v1/web/fad374cf-c18a-41c6-982d-ee443d8ccb92/api/dealership.json"
        apikey = "1Wq08to7Fxiz5LZplhhZOvvRqpR8KRc3vuXNJbu3PjDw"
        dealerships = get_dealers_from_cf(url)
        context["dealership_list"]=dealerships
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    url = "https://us-east.functions.appdomain.cloud/api/v1/web/fad374cf-c18a-41c6-982d-ee443d8ccb92/api/review.json"
    name_url = "https://us-east.functions.appdomain.cloud/api/v1/web/fad374cf-c18a-41c6-982d-ee443d8ccb92/api/dealership.json"
    apikey = "1Wq08to7Fxiz5LZplhhZOvvRqpR8KRc3vuXNJbu3PjDw"
    dealer_details = get_dealer_reviews_from_cf(url, dealer_id)
    context["dealer_id"] = dealer_id
    context["reviews"] = dealer_details
    
    dealer_name = get_dealer_name_by_id(name_url, dealer_id)
    context["dealers"] = dealer_name
    # print(dealer_name[0].full_name)
    return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {}
    if request.method == 'GET':
        url = "https://us-east.functions.appdomain.cloud/api/v1/web/fad374cf-c18a-41c6-982d-ee443d8ccb92/api/dealership.json"

        context = {
            "dealer_id": dealer_id,
            "dealer_name": get_dealers_from_cf(url)[dealer_id-1].full_name,
            "cars": CarModel.objects.all()
        }
        
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        if (request.user.is_authenticated):
            review = dict()
            review["id"]=0 #will change automatically
            review["name"]=request.POST["name"]
            review["dealership"]=dealer_id
            review["review"]=request.POST["review"]
            if ("check" in request.POST):
                review["purchase"]=True
            else:
                review["purchase"]=False
            if review["purchase"] == True:
                car_parts=request.POST["car"].split("|")
                review["purchase_date"]=request.POST["purchase_date"] 
                review["car_make"]=car_parts[0]
                review["car_model"]=car_parts[1]
                review["car_year"]=car_parts[2]

            else:
                review["purchase_date"]=None
                review["car_make"]=None
                review["car_model"]=None
                review["car_year"]=None
            
            try:
                json_result = post_request("https://us-east.functions.cloud.ibm.com/api/v1/namespaces/fad374cf-c18a-41c6-982d-ee443d8ccb92/actions/api/add-review.json", review, dealerId=dealer_id)
            except:
                print("Your review was not submitted, an error occurred.")
                
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
    

