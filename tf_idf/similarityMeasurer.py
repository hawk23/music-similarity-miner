import math

__author__ = 'veren_000'

class SimilarityMeasurer(object):

    def cosine_measure(self, terms1, terms2):
        '''
        :param terms1: dict of the terms and its weights for one artist
        :param terms2: dict of the terms and its weights for one artist
        :return: cosine measure for the similarity
        '''

        if len(terms1) == 0 or len(terms2) == 0:
            return math.inf

        similarity = 0
        for i in terms1.keys():
            if i in terms2.keys():
                 similarity += (terms1[i] * terms2[i])

        # cosine normalization
        similarity /= len(terms1)*len(terms2)
        return similarity

    def jaccard_measure(self, terms1, terms2):
        '''
        :param terms1: dict of the terms and its weights for one artist
        :param terms2: dict of the terms and its weights for one artist
        :return: jaccard measure for the similarity
        '''

        if len(terms1) == 0 or len(terms2) == 0:
            return math.inf

        overlapping = 0
        for i in terms1.keys():
            if i in terms2.keys():
                 overlapping += (terms1[i] * terms2[i])

        similarity = overlapping / (len(terms1)**2 + len(terms2)**2 - overlapping)

        return similarity