import json
from math import sqrt

def _confidence(ups, downs):
    n = ups + downs

    if n == 0:
        return 0
    
    z = 1.0
    phat = float(ups) / n;
    return sqrt(abs( phat + z*z/(2*n) - z*( (phat*(1-phat) + z*z/(4*n))/n) ) /(1+z*z/n))
    
def confidence(ups, downs):
    if ups + downs == 0:
        return 0
    else:
        return _confidence(ups, downs)

rank_dict = {}

for line in open('data/ranking.dat', 'r').readlines():
    data = json.loads(line)
    dic = data.values()[0]
    #print dic
    #print dic.keys()
    #print dic.values()
    #for id in data.values()[0].keys():
    for key, value in dic.iteritems():
        #print dic[key]
        rating = int(value)
        rating = (rating - 50) / 100.0
        k = int(key)
        #print k, ":", rating
        if k not in rank_dict.keys():
            rank_dict[k] = {}
            rank_dict[k]['up'] = 0
            rank_dict[k]['down'] = 0
        elif rating >= 0:
            rank_dict[k]['up'] = rank_dict[k]['up'] + rating
        else:
            rank_dict[k]['down'] = rank_dict[k]['down'] + abs(rating)

#print rank_dict.keys()

for key, dic in rank_dict.iteritems():
    rank_dict[key]['con'] = confidence(rank_dict[key]['up'], rank_dict[key]['down'])
    #print key, ":", rank_dict[key]['con']*100;

for key in sorted(rank_dict, key= lambda x : rank_dict[x]['con']):
    print key, " - ", rank_dict[key]['con']*100