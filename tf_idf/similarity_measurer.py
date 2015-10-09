import threading
import traceback

__author__ = 'veren_000'

# max threads
threadLimiter = threading.BoundedSemaphore(8)
lock = threading.RLock()

similarity = {}


class SimilarityMeasurer(threading.Thread):

    @staticmethod
    def getSimilarity():
        return similarity

    def __init__(self, artist1, artist2, terms_weight1, terms_weight2, similarity_function):
        threading.Thread.__init__(self)
        self.artist1 = artist1
        self.artist2 = artist2
        self.terms_weight1 = terms_weight1
        self.terms_weight2 = terms_weight2
        self.similarity_function = similarity_function
    
    def run(self):

        threadLimiter.acquire()

        try:
            if (self.artist1 == self.artist2):
                res = 1
            else:
                # calls the function of similarityMeasurer depending on the input arg weightFunction
                res = getattr(self, self.similarity_function)(self.terms_weight1, self.terms_weight2)

            # lock similarity and save in similarity matrix
            lock.acquire()
            if self.artist1 not in similarity:
                similarity[self.artist1] = {}
            if self.artist2 not in similarity:
                similarity[self.artist2] = {}

            similarity[self.artist1][self.artist2] = res
            similarity[self.artist2][self.artist1] = res
        except Exception as ex:
            traceback.print_exc()
        finally:
            lock.release()

        threadLimiter.release()


    def cosine_measure(self, terms1, terms2):
        '''
        :param terms1: dict of the terms and its weights for one artist
        :param terms2: dict of the terms and its weights for one artist
        :return: cosine measure for the similarity
        '''

        similarity = 0.0
        for i in terms1.keys():
            similarity += (terms1[i] * terms2[i])

        # cosine normalization
        similarity /= (len(terms1) * len(terms2))

        print "My: " + similarity
        # print "Cosine" + scidist.cosine(terms1, terms2)
        return similarity

    def jaccard_measure(self, terms1, terms2):
        '''
        :param terms1: dict of the terms and its weights for one artist
        :param terms2: dict of the terms and its weights for one artist
        :return: jaccard measure for the similarity
        '''

        overlapping = 0.0
        for i in terms1.keys():
            overlapping += (terms1[i] * terms2[i])

        similarity = overlapping / (len(terms1) ** 2 + len(terms2) ** 2 - overlapping)

        return similarity