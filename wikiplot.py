from lxml import html
import re
from urllib2 import urlopen
import sys
import printepub
import argparse
from pager import pager

parser = argparse.ArgumentParser(description="Extract the plot of a movie from its Wikipedia page")
option = parser.add_mutually_exclusive_group()

parser.add_argument("movie", type=str)
option.add_argument("-n", "--new", action="store_true", help="Store the plot in a new epub file")
option.add_argument("-a", "--app", action="store_true", help="Append to an existing epub file")
args = parser.parse_args()

reAnchor = re.compile("<a.+?>")
reTable = re.compile("<table[\w\W]+<\/table>")

schpage = urlopen("https://www.wikipedia.org")
schpage = html.parse(schpage).getroot()

schpage.forms[0].fields['search'] = args.movie

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

if args.app:
	printepub.printEpub(ePage, metadata)
elif arg.new:
	printepub.newEpub(ePage, metadata)

print "Success!"