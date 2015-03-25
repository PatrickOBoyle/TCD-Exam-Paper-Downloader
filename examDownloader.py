# Created:       17/02/2015
# Last updated:  17/02/2015

import urllib2
import os
from HTMLParser import HTMLParser

# URLs for constructing the link to exam papers
base_url = "https://www.tcd.ie/Local/Exam_Papers/annual_search.cgi?"
exam_year = "&acyear="
course_year = "&Standing="
course_id = "Course=19"
end_url = "&annual_search.cgi=Search"
TCD_URL = "https://www.tcd.ie"

# Used to block downloads on data params after the initial name of the file
canDownload = True

# Sets both strings as empty initially
download_url = ""
file_name = ""


print("Enter the year of exams you want:")

user_exam_year = raw_input()
exam_year += user_exam_year

print("Enter your course year: (1 = JF, 2 = SF, 3 = JS, 4 = SS)")

user_year = raw_input()
course_year += user_year

# Creates the URL to the page the documents are linked on
complete_year = base_url + course_id + exam_year + course_year + end_url

# Dump the HTML from the page into a string
response = urllib2.urlopen(complete_year)
html = response.read()


def download_file(download_url, file_name):
    #Save the file in a folder based on year
    directory = user_exam_year
    if not os.path.exists(directory):
        os.makedirs(directory)
    response = urllib2.urlopen(download_url)
    file = open(directory+"/"+file_name, 'w')
    file.write(response.read())
    file.close
    print("Download completed.")

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        # Checks to see if the tag is an anchor tag
        if(tag == "a"):
            # Tests if the value of the tuple starts with a forward slash (start address of all exam paper URLs)
            if(attrs[0][1].startswith("/")):
                partial_url = attrs[0][1]
                global download_url
                download_url = TCD_URL + partial_url
                global canDownload
                canDownload = True


    def handle_data(self, data):
        # Skips over all data returns that are empty
        if(data != ""):
            global file_name
            file_name = data + ".pdf"

            # Block of tests to weed out static element on all the download pages, blocks downloading the same file under multiple names
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

                    # After a download occurs, block downloading another file until a new URL has been assigned
                    canDownload = False;

parser = MyHTMLParser()
parser.feed(html)