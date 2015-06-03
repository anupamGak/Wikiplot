from lxml import html
import urllib2
import re
import sys
from pager import pager
import printepub

reAnchor = re.compile("<a.+?>")
reTable = re.compile("<table[\w\W]+<\/table>")

search = raw_input("Search :")
search += " (film)"

schpage = html.parse("http://www.wikipedia.org").getroot()

schpage.forms[0].fields['search'] = search

wiki = html.parse(html.submit_form(schpage.forms[0])).getroot()

#getting the movie title
ttlcode = wiki.xpath("//h1")[0]
soup = html.tostring(ttlcode)
try:
	title = ttlcode.xpath("i/text()")[0]
except IndexError:
	sys.exit("Error: No such movie found.")

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

author = raw_input("Author :")
ePage = pager(htmlfrag, title)

metadata = {
	"title" : title,
	"author" : author
}

printepub.printEpub(ePage, metadata)


with open('plots/plot%s.htm' % title, 'w') as f:
	f.write(ePage)
print "Done!"