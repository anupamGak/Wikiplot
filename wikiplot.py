from lxml import html
import re
from urllib2 import urlopen
import sys
from pager import pager
import printepub

reAnchor = re.compile("<a.+?>")
reTable = re.compile("<table[\w\W]+<\/table>")

search = raw_input("Search :")

schpage = urlopen("https://www.wikipedia.org")
schpage = html.parse(schpage).getroot()

schpage.forms[0].fields['search'] = search

wiki = html.parse(html.submit_form(schpage.forms[0])).getroot()
print "Movie plot obtained"

#getting the movie title
ttlcode = wiki.xpath("//h1")[0]
soup = html.tostring(ttlcode)
try:
	title = ttlcode.xpath("i/text()")[0]
except IndexError:
	sys.exit("Error: No such movie found. Try adding '(film)' to the end.")

#Getting the plot paragraphs
renodes = wiki.xpath("//h2[span='Plot']/following-sibling::*")
for renode in renodes:
	if renode.tag != 'h2':
		soup += html.tostring(renode)
	else:
		break

htmlfrag = re.sub(reAnchor, "", soup)
htmlfrag = re.sub("</a>", "", htmlfrag)
htmlfrag = re.sub(reTable, "", htmlfrag)

ePage = pager(htmlfrag, title)

metadata = {
	"title" : title,
}

choice = raw_input("Add to existing ebook? [y/n] : ")

if choice == 'y':
	printepub.printEpub(ePage, metadata)
else:
	printepub.newEpub(ePage, metadata)

print "Success!"