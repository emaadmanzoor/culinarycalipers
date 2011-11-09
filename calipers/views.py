from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response
from django.core.files import File
import urllib2
import json
import re
import time
from BeautifulSoup import BeautifulSoup

DEFAULT_RATING = 2.5

def weighted_average(data):
    """Calculates weighted average for data in form [ [weight, n], ...]"""
    weight_vector, rating_vector = zip(*data)
    average = 0
    #average = sum(x[0]*x[1] for x in data) / sum(weight_vector)
    for i in xrange(len(data)):
        average += weight_vector[i] * rating_vector[i]
    average /= round(float(sum(weight_vector)), 2)
    return average

def index(request):
    return render_to_response('index.html', locals())

def diff(request):
    restaurants = [0, 0, 0]
    ratings = [-1, -1, -1]
    loaded = False
    for k, v in request.GET.iteritems():
        index = re.search("\d+", k).group(0)
        if not "rest" in k:
            ratings[int(index) - 1] = v
            loaded = True
        else:
            url = "https://api.zomato.com/v1/restaurant.json/" + v
            request = urllib2.Request(url, None, {"X-Zomato-API-Key": "4eb0bc1d9f8015870256524eb0bc1d9f"})
            response = urllib2.urlopen(request)
            data = response.read()
            data_dic = json.loads(data)
            restaurants[int(index) - 1] = data_dic
            
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
            #print 'Soup-ed'
            
            user_review_data[data_dic["id"]] = []
            rating_dic = []

            if data_dic["userReviews"]["count"] >= 1:
                # Get list of review ids
                for i in range(data_dic["userReviews"]["count"]):
                    review_id = data_dic["userReviews"][str(i)]["review"]["id"]
                    #print review_id
                    tag = "review_item_" + review_id
                    # print tag
                    review = soup.find("article", {"class" : "userReviewItem", "id" : tag})
                    print review
                    num_reviews_string = review.findAll('p')[2].find('a').contents[0]
                    num_reviews = int(num_reviews_string.split()[0])
                    print num_reviews_string    
                    # Store lists of [number_of_reviews_by_this_user, rating]
                    rating_dic.append([num_reviews, data_dic["userReviews"][str(i)]["review"]["rating"]])
                    print rating_dic
                    user_review_data[data_dic["id"]] += rating_dic
                user_rating = weighted_average(rating_dic)
            else:
                user_rating = DEFAULT_RATING
            
            restaurants[int(index) - 1]["user_rating"] = user_rating
    return render_to_response('diff.html', {"data": zip(restaurants, ratings), "loaded": loaded})
    
def get_permalink(request):
    ids = [0, 0, 0]
    ratings = [-1, -1, -1]
    
    for k, v in request.GET.iteritems():
        index = re.search("\d+", k).group(0)
        if "rest" in k:
            ids[int(index) - 1] = v
        else:
            ratings[int(index) - 1] = v
    
    timestamp = str(int(time.time()))
    rankdata = {}
    rankdata[timestamp] = {}
    for id, rating in zip(ids, ratings):
        rankdata[timestamp][id] = rating
    
    rankfile = File(open('data/ranking.dat', 'a'))
    rankfile.write(json.dumps(rankdata) + "\n")
    rankfile.close()
    
    params = request.GET.urlencode()
    permalink = "http://" + request.get_host() + "/diff/?" + params
    return render_to_response('permalink.html', {"permalink" : permalink})