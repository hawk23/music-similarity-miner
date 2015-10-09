import argparse
import json
import os
import traceback
import time
import similarity_measurer
from tf_idf import term_counter
import weight_measurer
from preprocessor import preprocessing
__author__ = 'veren_000'

weight_measurer = weight_measurer.WeightMeasurer()


def preprocess(results_dir):
    try:
        threads = []
        for file in os.listdir(results_dir):
            thread = preprocessing.Preprocessing(results_dir + os.sep + file)
            threads.append(thread)
            thread.start()

        # wait for all threads to finish
        for thread in threads:
            thread.join()
    except Exception as e:
        traceback.print_exc()


def count_terms(term_index, artists_with_terms):
    try:
        threads = []
        for artist in artists_with_terms.keys():
            thread = term_counter.TermCounter(artist, term_index, artists_with_terms)
            threads.append(thread)
            thread.start()

        # wait until threads are finished
        for thread in threads:
            thread.join()
    except Exception as e:
        traceback.print_exc()


def weight_terms(N, weight_function, artists_with_terms_count):
    artists_with_terms_weight = {}

    try:
        for artist in artists_with_terms_count.keys():
            for term in artists_with_terms_count[artist].keys():

                # term occuring in the document of the artist
                f_dt = artists_with_terms_count[artist][term]

                # term occuring in all documents
                f_t = term_counter.TermCounter.count_documents_containing_term(term)

                # calls the function of weightMeasurer depending on the input arg weightFunction
                weight = getattr(weight_measurer, weight_function)(f_dt, N, f_t)

                if artist not in artists_with_terms_weight:
                    artists_with_terms_weight[artist] = {}

                artists_with_terms_weight[artist][term] = weight

    except Exception as e:
        traceback.print_exc()

    return artists_with_terms_weight


def measure_similarity(similarity_function, artists_with_terms_weight):
    artists_handled = []
    threads = []

    try:
        for artist1 in artists_with_terms_weight.keys():
            for artist2 in artists_with_terms_weight.keys():
                if artist2 not in artists_handled:

                        # start thread for computing the similarity between artist1 and artist2
                        thread = similarity_measurer.SimilarityMeasurer(artist1, artist2, artists_with_terms_weight[artist1], artists_with_terms_weight[artist2], similarity_function)
                        threads.append(thread)
                        thread.start()

            # add to handled artists in order to avoid handling this pair again
            artists_handled.append(artist1)

        # wait until threads are finished
        for thread in threads:
            thread.join()
    except Exception as e:
        traceback.print_exc()

    similarity = similarity_measurer.SimilarityMeasurer.getSimilarity()
    return similarity


def main():
    start_time = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument('data_dir')

    # optional arguments
    parser.add_argument('weight_function', nargs='?', default='standard_tf_idf')
    parser.add_argument('similarity_function', nargs='?', default='jaccard_measure')

    args = parser.parse_args()
    results_dir = args.data_dir + os.sep + 'results'
    index_terms_file = args.data_dir + os.sep + 'index-terms' + os.sep + 'index-terms.txt'
    similarities_dir = args.data_dir + os.sep + 'similarities' + os.sep

    # preprocess artists
    print "Preprocessing artists and index terms"
    preprocess(results_dir)
    artists_with_terms = preprocessing.Preprocessing.get_artists_with_terms()

    # preprocess terms
    prep = preprocessing.Preprocessing()
    term_index = prep.pre_process(index_terms_file)

    # count terms contained in the termIndex for every artist
    count_terms(term_index, artists_with_terms)
    artists_with_terms_count = term_counter.TermCounter.get_artists_with_terms_count()

    # create similarity directory if it doesn't exist
    if not os.path.exists(similarities_dir):
        os.makedirs(similarities_dir)

    counts_file = open(similarities_dir + os.sep + 'counts', 'w+')
    json.dump(artists_with_terms_count, counts_file)
    counts_file.close()

    # weight the terms using tf_idf
    print "Weighting terms by using %s" % (args.weight_function)
    N = len(os.listdir(results_dir))
    artists_with_terms_weight = weight_terms(N, args.weight_function, artists_with_terms_count)

    weights_file = open(similarities_dir + os.sep + 'weights', 'w+')
    json.dump(artists_with_terms_weight, weights_file)
    weights_file.close()

    # measure similarity for each pair of artists
    print "Measuring distance between artists by using %s" % (args.similarity_function)
    similarity_matrix = measure_similarity(args.similarity_function, artists_with_terms_weight)

    end_time = time.time()
    elapsed = end_time - start_time
    minutes = int(elapsed / 60)
    seconds = int(elapsed % 60)

    print "Finished! --- execution time for %s artists: %sm%ss--- (for 224 artists: %s min.)" % (N, minutes, seconds, str((float(224/N)) * elapsed/60))

    similarity_file = open(similarities_dir + os.sep + 'similarities', 'w+')
    json.dump(similarity_matrix, similarity_file)
    similarity_file.close()

if __name__ == "__main__":
    main()
