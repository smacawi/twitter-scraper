# import libraries
import urllib2
from bs4 import BeautifulSoup

# specify the url
quote_page = "https://www.canada.ca/en/environment-climate-change/services/weather-general-tools-resources/subscribe-to-twitter-alerts.html"

# query page
page = urllib2.urlopen(quote_page)

# Parse html
soup = BeautifulSoup(page, 'html.parser')

#html tags i want to collect
name_bowl = soup.findAll('a')

#exporting it
with open('ECCCtwitteraccount.txt', 'w') as f:
    for curr in name_bowl:
        name = curr.text.encode('utf-8').strip()
        print name
        f.write("%s\n" % name)
