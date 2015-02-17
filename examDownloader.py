import urllib2
from HTMLParser import HTMLParser

base_url = "https://www.tcd.ie/Local/Exam_Papers/annual_search.cgi?"
exam_year = "&acyear="
course_year = "&Standing="
course_id = "Course=19"
end_url = "&annual_search.cgi=Search"
TCD_URL = "https://www.tcd.ie"

canDownload = True

download_url = ""
file_name = ""

print("Enter the year of exams you want:")

user_exam_year = raw_input()
exam_year += user_exam_year

print("Enter your course year: (1 = JF, 2 = SF, 3 = JS, 4 = SS)")

user_year = raw_input()
course_year += user_year

complete_year = base_url + course_id + exam_year + course_year + end_url

response = urllib2.urlopen(complete_year)
html = response.read()


def download_file(download_url, file_name):
	response = urllib2.urlopen(download_url)
	file = open(file_name, 'w')
	file.write(response.read())
	file.close
	print("Download completed.")

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if(tag == "a"):
        	if(attrs[0][1].startswith("/")):
        		partial_url = attrs[0][1]
        		global download_url
        		download_url = TCD_URL + partial_url
       			global canDownload
       			canDownload = True


    def handle_data(self, data):
    	if(data != ""):
    		global file_name
        	file_name = data + ".pdf"
        	if(file_name.startswith("T")):
        		file_name = ""
        	if(file_name.startswith("A")):
        		file_name = ""
        	if(file_name.startswith("Y")):
        		file_name = ""
        	if(download_url != ""):
        		global canDownload
        		if(canDownload == True):
        			download_file(download_url, file_name)
        			canDownload = False;

parser = MyHTMLParser()
parser.feed(html)