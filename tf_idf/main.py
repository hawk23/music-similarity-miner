import argparse
import json
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


def countTerms(termIndex, artistsWithTerms):
    try:
        threads = []
        for artist in artistsWithTerms.keys():

            thread = termCounter.TermCounter(artist, termIndex, artistsWithTerms)
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
                        res = 1
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
    parser.add_argument('dataDir')

    # optional arguments
    parser.add_argument('weightFunction', nargs='?', default='standard_tf_idf')
    parser.add_argument('similarityFunction', nargs='?', default='jaccard_measure')

    args = parser.parse_args()
    results_dir = args.dataDir + os.sep + 'results'
    index_terms_file = args.dataDir + os.sep + 'index-terms' + os.sep + 'index-terms.txt'
    similarities_dir = args.dataDir + os.sep + 'similarities' + os.sep

    # preprocess artists
    preprocess(results_dir)
    artistsWithTerms = preprocessing.Preprocessing.getArtistsWithTerms()

    # preprocess terms
    prep = preprocessing.Preprocessing()
    termIndex = prep.pre_process(index_terms_file)

    # count terms contained in the termIndex for every artist
    countTerms(termIndex, artistsWithTerms)
    artistsWithTermsCount = termCounter.TermCounter.getArtistsWithTermsCount()

    counts_file = open(similarities_dir + os.sep + 'counts', 'w+')
    json.dump(artistsWithTermsCount, counts_file)
    counts_file.close()

    # weight the terms using tf_idf
    N = len(os.listdir(results_dir))
    artistsWithTermsWeight = weightTerms(N, args.weightFunction, artistsWithTermsCount)

    weights_file = open(similarities_dir + os.sep + 'weights', 'w+')
    json.dump(artistsWithTermsWeight, weights_file)
    weights_file.close()

    # measure similarity for each pair of artists
    similarityMatrix = measureSimilarity(args.similarityFunction, artistsWithTermsWeight)

    print similarityMatrix

    end_time = time.time()
    elapsed = end_time - start_time
    minutes = int(elapsed / 60)
    seconds = int(elapsed % 60)

    print "--- execution time for %s artists: %sm%ss--- (for 1200 artists: %s min.)" % (N, minutes, seconds, str((float(1200/N)) * elapsed/60))

    similarity_file = open(similarities_dir + os.sep + 'similarities', 'w+')
    json.dump(similarityMatrix, similarity_file)
    similarity_file.close()

if __name__ == "__main__":
    main()
