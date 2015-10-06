import argparse
import os
import traceback
import time
import similarityMeasurer
from tf_idf import termCounter
import weightMeasurer
from preprocessor import preprocessing

__author__ = 'veren_000'

similarityMeasurer = similarityMeasurer.SimilarityMeasurer()
weightMeasurer = weightMeasurer.WeightMeasurer()


def preprocess(resultsDir):
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


def countTerms(artistsWithTerms):
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


def weightTerms(N, weightFunction, artistsWithTermsCount):
    artistsWithTermsWeight = {}

    try:
        for artist in artistsWithTermsCount.keys():
            for term in artistsWithTermsCount[artist].keys():

                # term occuring in the document of the artist
                f_dt = artistsWithTermsCount[artist][term]

                # term occuring in all documents
                f_t = termCounter.TermCounter.countDocumentsContainingTerm(term)

                # calls the function of weightMeasurer depending on the input arg weightFunction
                weight = getattr(weightMeasurer, weightFunction)(f_dt, N, f_t)

                if artist not in artistsWithTermsWeight:
                    artistsWithTermsWeight[artist] = {}

                artistsWithTermsWeight[artist][term] = weight

    except Exception as e:
        traceback.print_exc()

    return artistsWithTermsWeight


def measureSimilarity(similarityFunction, artistsWithTermsWeight):
    similarity = {}
    artistsHandled = []

    try:
        for artist1 in artistsWithTermsWeight.keys():
            for artist2 in artistsWithTermsWeight.keys():
                if artist2 not in artistsHandled:
                    if (artist1 == artist2):
                        res = 0
                    else:

                        # calls the function of similarityMeasurer depending on the input arg weightFunction
                        res = getattr(similarityMeasurer, similarityFunction)(artistsWithTermsWeight[artist1], artistsWithTermsWeight[artist2])

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

    return similarity


def main():
    start_time = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument('resultsDir')

    # optional arguments
    parser.add_argument('weightFunction', nargs='?', default='standard_tf_idf')
    parser.add_argument('similarityFunction', nargs='?', default='jaccard_measure')

    args = parser.parse_args()
    resultsDir = args.resultsDir
    weightFunction = args.weightFunction
    similarityFunction = args.similarityFunction

    preprocess(resultsDir)
    artistsWithTerms = preprocessing.Preprocessing.getArtistsWithTerms()

    # count terms for every artist
    countTerms(artistsWithTerms)
    artistsWithTermsCount = termCounter.TermCounter.getArtistsWithTermsCount()

    N = len(os.listdir(resultsDir))

    # weight the terms using tf_idf
    artistsWithTermsWeight = weightTerms(N, weightFunction, artistsWithTermsCount)

    # measure similarity for each pair of artists
    similarityMatrix = measureSimilarity(similarityFunction, artistsWithTermsWeight)

    print similarityMatrix

    end_time = time.time()
    elapsed = end_time - start_time
    minutes = int(elapsed / 60)
    seconds = int(elapsed % 60)

    print "--- execution time for %s artists: %sm%ss--- (for 1200 artists: %s min.)" % (N, minutes, seconds, str((float(1200/N)) * elapsed/60))


if __name__ == "__main__":
    main()
