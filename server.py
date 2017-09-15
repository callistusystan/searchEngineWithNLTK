import json
from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer
from collections import defaultdict
from interest_career_mapper import InterestCareerMapper, ID, NAME, DESC, INTERESTS
from flask import Flask, request

app = Flask(__name__)

icm = InterestCareerMapper()
print(icm.interestContextToCareer)

@app.route('/search', methods=['GET'])
def search():
    terms = request.args.getlist('term')
    response = {}
    seenIds = set()
    results = []
    from queue import Queue
    distanceOfssName = {}
    q = Queue()
    # loop through terms given by user
    for term in terms:
        term = term.lower()
        if " " in term:
            term = term.replace(" ", "_")
        print(term)

        ssTerms = wn.synsets(term)
        if ssTerms is None:
            continue
        # put ssTerms in queue
        for ssTerm in ssTerms:
            q.put(ssTerm)
            distanceOfssName[ssTerm.name()] = 0

    # do BFS
    while not q.empty():
        curSS = q.get()
        curSSName = curSS.name()
        print(curSSName)
        curDist = distanceOfssName[curSSName]
        if curDist >= 3:
            break
        if curSSName in icm.interestContextToCareer.keys():
            for careerId in icm.interestContextToCareer[curSSName]:
                if careerId not in seenIds:
                    results.append(icm.careers[careerId])
                    seenIds.add(careerId)
        # add synonyms, hyponyms, hypernyms
        for nextSS in curSS.hypernyms():
            nextSSName = nextSS.name()
            if nextSSName not in distanceOfssName or distanceOfssName[nextSSName] < curDist + 1:
                distanceOfssName[nextSSName] = curDist + 1
                q.put(nextSS)
        for nextSS in curSS.hyponyms():
            nextSSName = nextSS.name()
            if nextSSName not in distanceOfssName or distanceOfssName[nextSSName] < curDist + 1:
                distanceOfssName[nextSSName] = curDist + 1
                q.put(nextSS)

    # for ssName in icm.interestContextToCareer.keys():
    #     ssInterest = wn.synset(ssName)
    #     print(ssTerm, ssInterest)
    #     print(ssTerm.wup_similarity(ssInterest))
    #     if ssTerm.wup_similarity(ssInterest) is not None and ssTerm.wup_similarity(ssInterest) >= 0.7:
    #         for careerId in icm.interestContextToCareer[ssName]:
    #             if careerId not in seenIds:
    #                 print(icm.careers[careerId])
    #                 results.append(icm.careers[careerId])
    #                 seenIds.add(careerId)
    response["data"] = results
    return json.dumps(response)
