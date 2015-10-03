import math

__author__ = 'veren_000'

def standard_tf_idf(f_dt, N, f_t):
    """
    :param f_dt: number of occurences of term t in document d (e.g. term "music" for artist Rihanna)
    :param N: number of documents (=artists)
    :param f_t: number of documents containing term t
    :return: standard tf_idf (TF_C * IDF_B2)
    """

    # adjustments to avoid division/log by 0
    if f_dt == 0:
        return 0
    if f_t == 0:
        f_t = 1

    tf_idf = (1 + math.log(f_dt)) * math.log(N / f_t)
    return tf_idf

def alternative_tf_idf(f_dt, N, f_t):
    """
    :param f_dt: number of occurences of term t in document d (e.g. term "music" for artist Rihanna)
    :param N: number of documents (=artists)
    :param f_t: number of documents containing term t
    :return: alternative tf_idf (TF_C2 * IDF_E)
    """

    # adjustments to avoid division by 0/ a negative result
    if f_t == 0:
        f_t = 1
    elif f_t > N/2:
        return 0

    tf_idf = (math.log(1 + f_dt)) * math.log((N - f_t) / f_t)
    return tf_idf


