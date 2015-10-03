from bs4 import BeautifulSoup
import re
import mechanize
import urllib

__author__ = 'mario'


class Spider(object):

    def fetchLinks(self, query):
        links = []
        # create a browser
        br = mechanize.Browser()

        # ignore restrictions for robots
        br.set_handle_robots(False)

        # fetch first page
        url = 'http://duckduckgo.com/html/?q=%s' % (query)

        try:
            response = br.open(url)
            links += self.parseLinks(response)

            # invoke form to fetch second page
            br.select_form(nr=2)
            response = br.submit()
            links += self.parseLinks(response)
        except:
            pass

        return links

    def parseLinks(self, response):
        links = []
        parsed = BeautifulSoup(response.read())

        for i in parsed.findAll('div', {'class': re.compile('links_main*')}):
            links.append(i.a['href'])

        return links

    '''
    Downloads all files given in 'urls' and concatenates them into one single output file.
    '''
    def download(slef, urls, out_file):
        myfile = open(out_file, "w")

        for url in urls:
            try:
                response = urllib.urlopen(url)
                html = response.read()
                myfile.write(html)
            except:
                pass

        myfile.close()