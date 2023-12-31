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
def post_request(url, payload, **kwargs):
    print(url)
    print(payload)
    print(kwargs)
    try:
        response = requests.post(url, params=kwargs, json=payload)
    except Exception as e:
        print("Error" ,e)
    print("Status Code ", {response.status_code})
    data = json.loads(response.text)
    return data


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    dealers = get_request(url, **kwargs)
    for dealer in dealers["result"]["rows"]:
        dealer_obj = CarDealer(address=dealer.get("doc")["address"], city=dealer.get("doc")["city"], full_name=dealer.get("doc")["full_name"],
                                id=dealer.get("doc")["id"], lat=dealer.get("doc")["lat"], long=dealer.get("doc")["long"],
                                short_name=dealer.get("doc")["short_name"],
                                st=dealer.get("doc")["st"], state=dealer.get("doc")["state"], zip=dealer.get("doc")["zip"])
        results.append(dealer_obj)

    return results


#Get dealers by id
def get_dealer_name_by_id(url, dealer_id):
    results = []
    dealers = get_request(url, dealerId=dealer_id)
    
    for dealer in dealers["result"]["rows"]:
        if dealer.get("doc")["id"] == dealer_id:
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
def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    dealers = get_request(url, dealerId=dealer_id)
    
    for dealer in dealers["result"]["rows"]:
        doc = dealer.get("doc") #using this notation to avoid errors when certain parts of the review are not found
        if dealer.get("doc")["id"] == dealer_id:
            dealer_obj = DealerReview(id=doc.get("id"), name=doc.get("name"), 
                            dealership=doc.get("dealership"), purchase=doc.get("purchase"), 
                            review=doc.get("review"), purchase_date=doc.get("purchase_date", None), 
                            car_make=doc.get("car_make", None), car_model=doc.get("car_model", None),
                            car_year=doc.get("car_year", None), sentiment=analyze_review_sentiments(doc.get("review")))
            results.append(dealer_obj)
            
    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealer_review, **kwargs):
    API_KEY="uFrum6doAjnaVUDoKwNrYI3wmWKiL74tyNo4BUd2KY1B"
    NLU_URL='https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/0d7e1cd0-ff03-4c59-9475-560f3a7c857c'
    params = json.dumps({"text": dealer_review, "features": {"sentiment": {}}})
    response = requests.post(NLU_URL,data=params,headers={'Content-Type':'application/json'},auth=HTTPBasicAuth("apikey", API_KEY))
    
    #print(response.json())
    try:
        sentiment=response.json()['sentiment']['document']['label']
        return sentiment
    except:
        return "neutral"


