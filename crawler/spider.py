__author__ = 'mario'

import sys
import argparse
import urllib
import simplejson
import downloader

parser = argparse.ArgumentParser()
parser.add_argument("resultCount")
parser.add_argument("query")
parser.add_argument("output")

def search(query, index, offset, min_count, quiet=False, rs=[]):
    url = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&rsz=large&%s&start=%s" % (query, offset)
    result = urllib.urlopen(url)
    json = simplejson.loads(result.read())
    status = json["responseStatus"]
    if status == 200:
        results = json["responseData"]["results"]
        cursor = json["responseData"]["cursor"]
        pages = cursor["pages"]
        for r in results:
            i = results.index(r) + (index -1) * len(results) + 1
            u = r["unescapedUrl"]
            rs.append(u)
            if not quiet:
                print("%3d. %s" % (i, u))
        next_index  = None
        next_offset = None
        for p in pages:
            if p["label"] == index:
                i = pages.index(p)
                if i < len(pages) - 1:
                    next_index  = pages[i+1]["label"]
                    next_offset = pages[i+1]["start"]
                break
        if next_index != None and next_offset != None:
            if int(next_offset) < min_count:
                search(query, next_index, next_offset, min_count, quiet, rs)
    return rs

def main():
    args = parser.parse_args()
    query = urllib.urlencode({"q" : args.query})
    rs = search(query, 1, "0", args.resultCount)

    downloader.download(rs, args.output)

if __name__ == "__main__":
    main()