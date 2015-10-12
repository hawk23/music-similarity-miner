import argparse
import json
import operator

__author__ = 'mario'

parser = argparse.ArgumentParser()
parser.add_argument("artist") # the artist to classify the genre for
args = parser.parse_args()

k = 3
genres = dict()

def main():
    global genres

    artist = args.artist

    # prepare list of artists and genres
    genres = loadGenresFromFile()

    # get the similarities for the given artist
    similarities_file = open("./../data/similarities/similarities", "r")
    similarity_matrix = json.load(similarities_file)

    if artist in similarity_matrix.keys():
        similarity_artist = similarity_matrix[artist]

    # get a list of tuples (artist, similarity) sorted by descending similarity
    sorted_list = sorted(similarity_artist.items(), key=operator.itemgetter(1))
    sorted_list.reverse()

    # remove tuple of given artist
    sorted_list = [(name, similarity) for name, similarity in sorted_list if name != artist]

    # get the n most similar artist for the given artist
    result_genre = knearestclass(sorted_list[:k])

    print("%s most similar artists: %s" % (k,sorted_list[:k]))
    print("predicted genre: %s, correct genre: %s" % (result_genre, getGenre(artist)))

def knearestclass(list):
    genreCounts = dict()

    for artist in list:
        genre = getGenre(artist[0])

        if genre in genreCounts.keys():
            genreCounts[genre] += artist[1]
        else:
            genreCounts[genre] = artist[1]

    sorted_list = sorted(genreCounts.items(), key=operator.itemgetter(1))
    return sorted_list[-1][0]



def getGenre(artistName):
    global genres

    artist_prep = "".join(artistName.split()).lower()

    if artist_prep in genres.keys():
        return genres[artist_prep]
    else:
        return None

def loadGenresFromFile():
    genres_file = open("./../data/C224a_genre.txt", "r")
    list = dict()

    for line in genres_file:
        genre = line.split(":")[0]
        artist = line.split(":")[1].rstrip()
        list[artist] = genre

    return list

if __name__ == "__main__":
    main()