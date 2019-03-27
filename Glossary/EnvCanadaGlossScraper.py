# import libraries
import urllib2
from bs4 import BeautifulSoup

# specify the url
quote_page = 'http://climate.weather.gc.ca/glossary_f.html'

# query page
page = urllib2.urlopen(quote_page)

# Parse html
soup = BeautifulSoup(page, 'html.parser')

#html tags I want to collect
name_bowl = soup.findAll('h2', attrs= {'class': None})

#exporting it
with open('EnvCanadaGlossScraperf.txt', 'w') as f:
    for curr in name_bowl:
        name = curr.text.encode('utf-8').strip()
        print name
        f.write("%s\n" % name)
