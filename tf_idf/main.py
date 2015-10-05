import argparse
import os
import traceback
import similarityMeasurer
import weightMeasurer

from preprocessor import preprocessing

__author__ = 'veren_000'

parser = argparse.ArgumentParser()
parser.add_argument("resultsDir")
args = parser.parse_args()
resultsDir = args.resultsDir

artist_files = args.resultsDir

similarityMeasurer = similarityMeasurer.SimilarityMeasurer()
weightMeasurer = weightMeasurer.WeightMeasurer()

try:
    threads = []
    for file in os.listdir(resultsDir):

        # start thread to preprocess and to count terms for one artist
        thread = preprocessing.Preprocessing(resultsDir + os.sep + file)
        threads.append(thread)
        thread.start()

    # wait for all threads to finish
    for thread in threads:
        thread.join()
except Exception as e:
    traceback.print_exc()

N = len(os.listdir(resultsDir))
artistsWithTerms = preprocessing.Preprocessing.getArtistsWithTerms()
