from bs4 import BeautifulSoup
import re
import mechanize

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