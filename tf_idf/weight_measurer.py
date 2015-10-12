import math

__author__ = 'veren_000'


class WeightMeasurer(object):
    def standard_tf_idf(self, f_dt, n, f_t):
        '''
        :param f_dt: number of occurences of term t in document d
        :param n: number of documents (=artists)
        :param f_t: number of documents containing term t
        :return: standard tf_idf (TF_C * IDF_B2)
        '''

        # adjustments to avoid division/log by 0
        if f_dt == 0:
            return 0.0
        if f_t == 0:
            f_t = 1.0

        tf_idf = (1.0 + math.log(float(f_dt))) * math.log(n / float(f_t))
        return tf_idf

    def alternative_tf_idf(self, f_dt, n, f_t):
        '''
        :param f_dt: number of occurences of term t in document d
        :param n: number of documents (=artists)
        :param f_t: number of documents containing term t
        :return: alternative tf_idf (TF_C2 * IDF_E)
        '''

        # do not compute tf_idf if division / log by zero
        if f_t == 0:
            return 0.0

        # tf_idf (TF_C2 and IDF_C) formula
        tf_idf = (math.log(1.0 + float(f_dt))) * (1 / float(f_t))
        return tf_idf
