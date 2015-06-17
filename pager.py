def pager(frag = "", title = ""):
	codeopen = """<!DOCTYPE html>
			  <html>
				<head>
				<title>Plot of %s</title>
				<link rel="stylesheet" href="styles.css" type="text/css"/>
			  </head>
			  <body>""" % title

	codeclose = """</body>
			   </html>"""

	code = codeopen + frag + codeclose
	return code