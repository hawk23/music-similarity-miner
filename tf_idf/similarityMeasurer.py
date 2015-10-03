import math

__author__ = 'veren_000'

def cosine_measure(terms1, terms2):
    """
    :param terms1: dict of the terms and its weights for one artist
    :param terms2: dict of the terms and its weights for one artist
    :return: cosine measure for the similarity
    """

    if len(terms1) == 0 or len(terms2) == 0:
        return math.inf

    similarity = 0
    for i in terms1.keys():
        for j in terms2.keys():
            if i==j:
                similarity += (terms1[i] * terms2[j])

    # cosine normalization
    similarity /= len(terms1)*len(terms2)
    return similarity

def jaccard_measure(terms1, terms2):
    """
    :param terms1: dict of the terms and its weights for one artist
    :param terms2: dict of the terms and its weights for one artist
    :return: jaccard measure for the similarity
    """

    if len(terms1) == 0 or len(terms2) == 0:
        return math.inf

    similarity = 0
    overlapping = 0
    for i in terms1.keys():
        for j in terms2.keys():
            if i==j:
                overlapping += (terms1[i] * terms2[j])

    similarity = overlapping / (len(terms1)**2 + len(terms2)**2 - overlapping)

    return similarity

rihanna = {
    "music" : 0.4,
    "pop"   : 0.7,
    "reggae": 0.9,
}

mileyCyrus = {
    "tongue": 0.96,
    "music" : 0.2,
    "pop"   : 0.5,
    "drugs" : 0.3,
}

print cosine_measure(rihanna, mileyCyrus)
print jaccard_measure(rihanna, mileyCyrus)