import zipfile
import re
import os

reAbbr = re.compile(r"(?:\s|^)([A-Z])")
reFlag = re.compile(r"<!--([a-z]+)-->")
reCount = re.compile(r"<!--(\d{1,3})-->")
reDropcap = re.compile(r"<p>(\w)")

container_xml = """<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf"
     media-type="application/oebps-package+xml" />
  </rootfiles>
</container>"""

content_opf = """<?xml version='1.0' encoding='utf-8'?>
<package xmlns="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/"unique-identifier="bookid" version="2.0">
  <metadata>
    <dc:title>Movie Plots</dc:title>
    <dc:creator>WikiPlot</dc:creator>
    <dc:identifier id="bookid">urn:uuid:0cc33cbd-94e2-49c1-909a-72ae16bc2658</dc:identifier>
    <dc:language>en-US</dc:language>
  </metadata>
  <manifest>
    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
    <item id="cover" href="title.html" media-type="application/xhtml+xml"/>
    <item id="css" href="styles.css" media-type="text/css"/>
    <!--manifest-->
  </manifest>
  <spine toc="ncx">
    <itemref idref="cover" linear="no"/>
    <!--spine-->
  </spine>
  <guide>
    <reference href="title.html" type="cover" title="Cover"/>
  </guide>
</package>"""

toc_ncx = """<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"
                 "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta name="dtb:uid" content="urn:uuid:0cc33cbd-94e2-49c1-909a-72ae16bc2658"/>
    <meta name="dtb:depth" content="1"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle>
    <text>Movie Plot</text>
  </docTitle>
  <navMap>
    <navPoint id="navpoint-1" playOrder="1">
      <navLabel>
        <text>Book cover</text>
      </navLabel>
      <content src="title.html"/>
    </navPoint>
    <!--toc-->
  </navMap>
</ncx>"""

title_html = """<!DOCTYPE html>
<html>
<head>
	<title>Title</title>
</head>
<body style = "text-align: center;">
	<h1>Movie Plots</h1>
	<p>WikiPlot</p>
</body>
</html>"""

styles_css = """
#dropcap {
	float : left;
	font-size : 250%;
}

p {
	text-indent: 7%;
}

"""

def filler(metadata={}):
	metadata['navpoint'] = metadata['count'] + 1

	manifest = '''<item id="movie-%(count)s" href="movie-%(count)s.html" media-type="application/xhtml+xml"/>
    <!--manifest-->
	<!--%(count)s-->''' % metadata

	spine = '''<itemref idref="movie-%(count)s"/>
	<!--spine-->''' % metadata

	toc = '''<navPoint id="navpoint-%(navpoint)s" playOrder="%(navpoint)s">
    <navLabel>
        <text>%(title)s</text>
    </navLabel>
    <content src="movie-%(count)s.html"/>
    </navPoint>
    <!--toc-->''' % metadata

	return {
    	"manifest" : manifest,
    	"spine" : spine,
    	"toc" : toc
    }


def printEpub(htmlcode="", metadata={}):
#	ttlAbr = "".join(re.findall(reAbbr, metadata['title']))
	global content_opf, toc_ncx
	epubin = zipfile.ZipFile('epubs/WikiPlots.epub', 'r')

	content_opf = epubin.read("OEBPS/content.opf")
	content_opf = re.sub(reFlag, r"%(\1)s", content_opf)
	toc_ncx = epubin.read("OEBPS/toc.ncx")
	toc_ncx = re.sub(reFlag, r"%(\1)s", toc_ncx)

	metadata['count'] = int(re.findall(reCount, content_opf)[0]) + 1
	content_opf = re.sub(reCount, "", content_opf)

	metadata.update(filler(metadata))

	content_opf = content_opf % metadata
	toc_ncx = toc_ncx % metadata


	epubout = zipfile.ZipFile('epubs/WikiPlots_new.epub', 'w')
	epubout.writestr("mimetype", "application/epub+zip")
	epubout.writestr("OEBPS/styles.css", styles_css)

	filenames = [i for i in epubin.namelist() if ".html" in i]

	for filename in filenames:
		epubout.writestr(filename, epubin.read(filename))

#	htmlcode = re.sub(reDropcap, r"<p><span id='dropcap'>\1</span>", htmlcode, count=1)

	epubout.writestr("OEBPS/content.opf", content_opf % metadata)
	epubout.writestr("META-INF/container.xml", container_xml)
	epubout.writestr("OEBPS/toc.ncx", toc_ncx)
	epubout.writestr("OEBPS/movie-%s.html" % metadata['count'], htmlcode)

	epubin.close()
	epubout.close()

#	os.remove("epubs/WikiPlots.epub")
	os.rename("epubs/WikiPlots_new.epub", "epubs/WikiPlots.epub")


def newEpub(htmlcode="", metadata={}):
	global content_opf, toc_ncx
	content_opf = re.sub(reFlag, r"%(\1)s", content_opf)
	toc_ncx = re.sub(reFlag, r"%(\1)s", toc_ncx)

	metadata['count'] = 1

	metadata.update(filler(metadata))

	content_opf = content_opf % metadata
	toc_ncx = toc_ncx % metadata

#	htmlcode = re.sub(reDropcap, r"<p><span id='dropcap'>\1</span>", htmlcode, count=1)

	epub = zipfile.ZipFile('epubs/WikiPlots.epub', 'w')
	epub.writestr("mimetype", "application/epub+zip")
	epub.writestr("OEBPS/movie-1.html", htmlcode)
	epub.writestr("OEBPS/content.opf", content_opf % metadata)
	epub.writestr("META-INF/container.xml", container_xml)
	epub.writestr("OEBPS/toc.ncx", toc_ncx % metadata)
	epub.writestr("OEBPS/title.html", title_html % metadata)
	epub.writestr("OEBPS/styles.css", styles_css)