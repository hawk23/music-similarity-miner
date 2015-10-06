import argparse
import os
import traceback
import time
import similarityMeasurer
from tf_idf import termCounter
import weightMeasurer
from preprocessor import preprocessing

__author__ = 'veren_000'

start_time = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("resultsDir")
args = parser.parse_args()
resultsDir = args.resultsDir

# preprocess html documents
try:
    threads = []
    for file in os.listdir(resultsDir):

        thread = preprocessing.Preprocessing(resultsDir + os.sep + file)
        threads.append(thread)
        thread.start()

    # wait for all threads to finish
    for thread in threads:
        thread.join()
except Exception as e:
    traceback.print_exc()

artistsWithTerms = preprocessing.Preprocessing.getArtistsWithTerms()

# count terms for every artist
try:
    threads = []
    for artist in artistsWithTerms.keys():

        thread = termCounter.TermCounter(artist, artistsWithTerms)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
except Exception as e:
    traceback.print_exc()

artistsWithTermsCount = termCounter.TermCounter.getArtistsWithTermsCount()

# weight the terms using tf_idf
weightMeasurer = weightMeasurer.WeightMeasurer()
N = len(os.listdir(resultsDir))
artistsWithTermsWeight = {}
try:
    for artist in artistsWithTermsCount.keys():
        for term in artistsWithTermsCount[artist].keys():

            # term occuring in the document of the artist
            f_dt = artistsWithTermsCount[artist][term]

            # term occuring in all documents
            f_t = termCounter.TermCounter.countDocumentsContainingTerm(term)

            weight = weightMeasurer.standard_tf_idf(f_dt, N, f_t)

            if artist not in artistsWithTermsWeight:
                artistsWithTermsWeight[artist] = {}

            artistsWithTermsWeight[artist][term] = weight

except Exception as e:
    traceback.print_exc()

# use cosine and jaccard similarity measure
similarityMeasurer = similarityMeasurer.SimilarityMeasurer()
similarity = {}

artistsHandled = []
try:
    for artist1 in artistsWithTermsWeight.keys():
        for artist2 in artistsWithTermsWeight.keys():
            if artist2 not in artistsHandled:
                if (artist1 == artist2):
                    res = 0
                else:
                    res = similarityMeasurer.cosine_measure(artistsWithTermsWeight[artist1], artistsWithTermsWeight[artist2])

                if artist1 not in similarity:
                    similarity[artist1] = {}
                if artist2 not in similarity:
                    similarity[artist2] = {}

                # save in similarity matrix
                similarity[artist1][artist2] = res
                similarity[artist2][artist1] = res

        artistsHandled.append(artist1)

except Exception as e:
    traceback.print_exc()

print similarity

end_time = time.time()
elapsed = end_time - start_time
minutes = int(elapsed / 60)
seconds = int(elapsed % 60)

print "--- execution time for %s artists: %sm%ss--- (for 1200 artists: %s min.)" % (N, minutes, seconds, str((float(1200/N)) * elapsed/60))
