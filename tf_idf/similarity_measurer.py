import threading
import math

__author__ = 'veren_000'

class SimilarityMeasurer(threading.Thread):

    def cosine_measure(self, terms1, terms2):
        '''
        :param terms1: dict of the terms and its weights for one artist
        :param terms2: dict of the terms and its weights for one artist
        :return: cosine measure for the similarity
        '''

        norm1 = 0.0
        norm2 = 0.0
        similarity = 0.0
        for i in terms1.keys():
            similarity += (terms1[i] * terms2[i])
            norm1 += terms1[i] ** 2
            norm2 += terms2[i] ** 2

        # cosine normalization
        normalization = math.sqrt(norm1) * math.sqrt(norm2)

        # to avoid division by 0
        if (normalization == 0):
            return 0

        similarity /= normalization

        return similarity



    def jaccard_measure(self, terms1, terms2):
        '''
        :param terms1: dict of the terms and its weights for one artist
        :param terms2: dict of the terms and its weights for one artist
        :return: jaccard measure for the similarity
        '''

        norm1 = 0.0
        norm2 = 0.0
        overlapping = 0.0

        for i in terms1.keys():
            # if both terms are not 0 then add to intersection and union
            if (terms1[i] != 0 and terms2[i] != 0):
                overlapping += 1
                norm1 += 1
                norm2 += 1
            # else add only to the corresponding normalization vector
            elif (terms1[i] != 0):
                norm1 += 1
            elif (terms2[i] != 0):
                norm2 += 1

        # union
        norm = norm1 + norm2

        # to avoid division by 0
        if (norm == 0):
            return 0
        similarity = overlapping / norm

        return similarity