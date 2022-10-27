#!/usr/bin/env python
# coding: utf-8

# I am using python for web scraping
# Here we are using requests library from python for web scraping
# and BeautifulSoup library for better parsing of the scraped data

# At the time of writing this code, only 10 jobs are available on the Coursera portal/website and running my code gives the details and saves the details of all the 10 jobs. If in future more jobs are added
# to the portal, my code will show their details as well. So in this example it is showing details of 10 jobs instead of 11 as only 10 jobs were available on the website instead of 11.
# Note: One of the jobs which was Sr Software Engineer - Application Architecture did not have a job description

# First we will import both libraries into our Python code
from bs4 import BeautifulSoup
import requests

url="https://boards.greenhouse.io/embed/job_board?for=coursera" # Here we are defining the url of the page containing details of jobs

r=requests.get(url) # Here we are using requests library to call GET API and save it in object r
soup=BeautifulSoup(r.content,"html.parser") # Now we are using Beautiful Soup library for parsing the contents of r and storing it in a bs4 object which we have called soup

# Advantage of using Beautiful soup is that now, we can easily see the elements of the object 'soup' and search it.

jobs = soup.findAll(attrs = {"class": "opening"}) # Since all the jobs titles and details and their urls are in a div with the attribute, class=opening, I have used this to filter those divs.

# The object 'jobs' saves all those divs (10 in this case), containing Job title, Location and URL of each job's web page

maincount=1 # Maincount is the total number of Jobs available in the platform. It is used as a counter and for displaying

mainlist=[] # Mainlist is the list in which all the details of all the jobs are stored. 
# Here mainlist is a list in which each job position is a dictionary which has attributes like Job Title, Location, Job Overview, Responsibilities, Basic Qualifications, Preferred Qualifications etc. 
# Each Job is a dictionary with these items details and each of these Job Profiles is an entry in the mainlist

for job in jobs:        # Here we are iterating through each of the jobs
    print("\n\n\nJob Number", maincount)        #Here we are just printing the variable 'maincount' which is a counter for numbering which starts at 1, so that in the end we can know how many jobs were being offered in the portal/website  
    data=job.find("a",attrs={"data-mapped":"true"})     # Each of the job on the main web page is an anchor <a> in html with the attribute data-mapped=true, so here 'data' stores the job position title
    name=data.text      # data.text has the Job Position title, so we are saving the Job Position Name in the variable 'name' 
    link=data["href"]   # Since gref has the link, so we are storing it in the variable 'link'
    job_id=link[-10:]   # The Job ID is a 10 digit number in coursera website and it is the last 10 digits of the link which we have saved via slicing in python in the variable 'job_id'
    data2=job.find("span",attrs={"class":"location"})       #The location of the Job is stored in span with attributes class=location and we are saving that in the variable 'data2'
    location=data2.text     # The location of the job is in data2.text and we save it in the variable 'location'
    link="https://boards.greenhouse.io/embed/job_app?for=coursera&token={}".format(job_id)    #This is the actual link of each of the job and we put in job ID of each job to get the specific URL of that job's webpage
    print("\nJob Title: ", name, "\nLink: ", link, "\nLocation: ",location, "\nJob ID: ", job_id)    #Here we are just printing the details of the job that we have obtained till now which include 
    # Job Name i.e. Job Title, Job Link i.e. link to the webpage of job details which we will be using in the next steps, Job Location, and Job ID
    
    r2=requests.get(link)       #Now we are making a GET API call to the web page of each particular job using the requests python library
    soup2=BeautifulSoup(r2.content,"html.parser")    #The data from the API call is stored in a Beautiful soup object called 'soup2' which we will be using to get details like responsibilities, qualifications etc. 
    
    # Now we are in the detailed web page of the job and can extract/scrap all the important details

    overview=soup2.findAll('p')     #All the Job overviews were in a <p> paragraoh, so we are creating a variable overview which saves all the <p> and their content found in the web page 

    job_overview=[]         # job_overview is an empty list which will store all the sentences present in the Job Overview section of the page
    # All the content of the Job overview Comes after the <p>Job Overview and before the <p>Responsibilities, so instead of just saving the text of the second <p> always (as that was saving wrong content sometimes Eg- About Coursera
    #  content was also getting saved in it sometimes), what we have done here is that we have put a flag called overview_counter=0 in the beginning and we are iterating over all <p> in overview and if Job Overview is in that <p>, we 
    # make the flag 1 and continue the loop, but if <p> has Responsibilities and also had <strong> in it, then it means Job Overview has ended and Responsibilities portion has started, so we make the flag 0 again.
    # If flag is 1, then we save the text in the job_overview list and thus, all the details of the Job Overview are saved in the list job_overview
    
    overview_count=0         
    for p in overview:
            if ("Job Overview" in p.text):         
                overview_count=1
                continue
            if ("Responsibilities" in p.text):
                for strong in p:
                    overview_count=0
                break
            if (overview_count==1):
                job_overview.append(p.text.replace('\xa0', ' '))
            

    print("\nJob Overview: ", job_overview)     #Printing the list job_overview
    
    #Here we have declared 3 empty lists responsibilities, basic and preferred to store the details of Responsibilities, Basic Qualifications and Preferred Qualifications in these lists from the web page of each individual job
    responsibilities=[]
    basic=[]
    preferred=[]
    
    count=0     #Here we have defined a variable 'count' as 0, which will be used as a counter
    # All 3 - Responsibilities, Basic Qualifications and Preferred Qualifications are Unordered lists <ul> with many list items <li> in each of them
    
    job_details = soup2.findAll('ul')       # job_details variable stores all the <ul> unordered lists and their contents
    
    for ul in job_details:          # Now we are iterating over each unordered list and saving each of the list's items. We only need to go over the first 3 unordered lists as the first 3 unordered lists are Responsibilities, 
                                    # Basic Qualifications and Preferred Qualifications. After that the unordered lists are not of any use to us
        count=count+1               # We increased the count to 1. Count 1 means Responsibilities, count 2 means Basic Qualifications and count 3 means Preferred Qualifications
        for li in ul:               # We are iterating over all the list items <li> in a single <ul> unordered list
            if (li != '\n'):        # I did this because "\n" was being saved twice - both before and after every <li> in the list and we only needed the text
                if (count == 1):    # If count=1, we will append the list items <li> to the list responsibilities
                    responsibilities.append(li.text.replace('\xa0', ' '))
                if (count == 2):    # If count=2, we will append the list items <li> to the list basic (qualifications)
                    basic.append(li.text.replace('\xa0', ' '))
                if (count == 3):    # If count=3, we will append the list items <li> to the list preferred (qualifications)
                    preferred.append(li.text.replace('\xa0', ' '))
                if (count > 3):     #  If count is >3, it means we have saved all the Responsibilities, Basic Qualifications and the Preferred Qualifications and so we can wend the loop
                    break
    # I have added .replace('\xa0', ' ')) because \xa0 is an empty space in Latin1 (a different encoding) and is not recognised in UTF-8. It is useless, so it is replaced by space ' ', which it originally stands for

    #Here we are printing all the Responsibilities, Basic Qualifications and the Preferred Qualifications
    print ("\nResponsibilities: ",responsibilities)
    print ("\nBasic Qualifications: ",basic)
    print ("\nPreferred Qualifications: ",preferred)

    # Now I have created a dictionary variable called 'dict' and in it I am storing all the details of a single Job as a Key-Value Pair like Job Title, Job Number, Location, Job ID, Link, Responsibilities, Basic Qualifications and Preferred Qualifications
    dict={"Job Number":maincount, "Job Title": name, "Location":location, "Job ID": job_id, "Link": link, "Job Overview": job_overview, "Responsibilities": responsibilities, "Basic Qualifications": basic, "Preferred Qualifications": preferred}
    mainlist.append(dict)       # This dict is appended to the list MainList and thus 1 entry in the mainlist corresponds to all the details of 1 job. We then iterate over the loop and save details of all jobs one by one. 
    maincount=maincount+1       # Each entry in the list called mainlist corresponds to a dictionary containing all the details of 1 job position

#Thus all the details of all the jobs are being stored in the list called mainlist and we can uncomment the below 2 lines to view the mainlist as well.
#print("\n\n\n")
#print("MAINLIST\n", mainlist)