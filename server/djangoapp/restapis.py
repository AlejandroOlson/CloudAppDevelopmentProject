import requests
import json
from .models import CarDealer, DealerReview 
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    data = {}
    try:
        if "apikey" in kwargs:
            response = requests.get(url, headers={'Content-Type':'application/json'}, params=kwargs, auth=HTTPBasicAuth("apikey", kwargs["apikey"]))
        else:
            response = requests.get(url, headers={'Content-Type':'application/json'}, params=kwargs)

        data = json.loads(response.text)
    except Exception as e:
        print(e)
    
    return data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    dealers = get_request(url, **kwargs)
    for dealer in dealers["result"]["rows"]:
        # print(dealer.get("doc")["address"])
        dealer_obj = CarDealer(address=dealer.get("doc")["address"], city=dealer.get("doc")["city"], full_name=dealer.get("doc")["full_name"],
                                id=dealer.get("doc")["id"], lat=dealer.get("doc")["lat"], long=dealer.get("doc")["long"],
                                short_name=dealer.get("doc")["short_name"],
                                st=dealer.get("doc")["st"], state=dealer.get("doc")["state"], zip=dealer.get("doc")["zip"])
        results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_by_id_from_cf(url, dealerId):
    results = []
    dealers = get_request(url, dealerId)
    for dealer in dealers["result"]["rows"]:
        
        if dealer.get("doc")["id"] == dealerId:
            dealer_obj = CarDealer(address=dealer.get("doc")["address"], city=dealer.get("doc")["city"], full_name=dealer.get("doc")["full_name"],
                                id=dealer.get("doc")["id"], lat=dealer.get("doc")["lat"], long=dealer.get("doc")["long"],
                                short_name=dealer.get("doc")["short_name"],
                                st=dealer.get("doc")["st"], state=dealer.get("doc")["state"], zip=dealer.get("doc")["zip"])
            results.append(dealer_obj)
            
    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



