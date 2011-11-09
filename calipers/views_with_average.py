from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response

from BeautifulSoup import BeautifulSoup
import urllib2
import json

API_KEY = "4eb54150bcca33283792984eb54150bc"
DEFAULT_RATING = 2.5

def weighted_average(data):
    """Calculates weighted average for data in form [ [weight, n], ...]"""
    weight_vector, rating_vector = zip(*data)
    #average = sum(x[0]*x[1] for x in data) / sum(weight_vector)
    for i in xrange(len(data)):
        average += weight_vector[i] * rating_vector[i]
    average /= sum(weight_vector)
    return average

def index(request):
    return render_to_response('index.html', locals())

def diff(request):
    restaurants = []
    for k, v in request.GET.iteritems():
        url = "https://api.zomato.com/v1/restaurant.json/" + v
        request = urllib2.Request(url, None, {"X-Zomato-API-Key": API_KEY})
        response = urllib2.urlopen(request)
        data = response.read()
        data_dic = json.loads(data)

        # Average Editor Rating
        try:
            editor_rating = sum(data_dic["editorRating"].values()) / float(len(data_dic["editorRating"]))
        except ZeroDivisionError:
            editor_rating = DEFAULT_RATING

        # Average User Rating
        review_id_list = []
        user_review_data = {}
        stream = urllib2.urlopen(data_dic["url"]).read()
        soup = BeautifulSoup(stream)
        print 'Soup-ed'

        if data_dic["userReviews"]["count"] >= 1:
            # Get list of review ids
            for i in range(data_dic["userReviews"]["count"]):
                review_id = data_dic["userReviews"][str(i)]["review"]["id"]
                # print review_id
                tag = "review_item_" + review_id
                # print tag
                review = soup.find("article", {"class" : "userReviewItem", "id" : tag})
                num_reviews_string = review.findAll('p')[2].find('a').getString()
                num_reviews = int(num_reviews_string.split()[0])
                # print num_reviews
                # Store lists of [number_of_reviews_by_this_user, rating]
                rating_dic = { "num_review" : num_reviews,
                               "rating" : data_dic["userReviews"][str(i)]["review"]["rating"],
                             }
                user_review_data[data_dic["id"]] = rating_dic
        else:
            user_rating = DEFAULT_RATING

        print user_review_data
        restaurants.append(data_dic)

    return render_to_response('diff.html', {"data": restaurants})
