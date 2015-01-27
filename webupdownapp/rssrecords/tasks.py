import psycopg2
import feedparser
from random import randint
from random import choice
from lxml import html
import requests
from datetime import datetime
import time
from BeautifulSoup import BeautifulSoup
import urllib2
import re


def AllUpdate():
    try:
        TwitterUpdate()
        print "\nWaiting between checks\n"
        time.sleep(5)
    except:
        print "could not perform Twitter updates"

    try:
        GooglePlusUpdate()
        print "\nWaiting between checks\n"
        time.sleep(5)
    except:
        print "could not perform Twitter updates"

    try:
        RssUpdate()
        print "\nUpdates Complete\n"
    except:
        print "could not perform Twitter updates"


def TwitterUpdate():

    conn = None

    x = 0
    format = None
    todaysdate = datetime.now().timetuple()
    print todaysdate
    soup = None

    try:
        conn = psycopg2.connect("dbname='d20kid2g0f7d7a' user='aekxaxttfecntl' host='ec2-54-225-115-77.compute-1.amazonaws.com' password='dKNAV1_vFR0Q_fDBvKcATgdHzU'")
    except:
        print "I am unable to connect to the database\n"

    cur = conn.cursor()
    cur.execute("""SELECT url,uuid FROM rssrecords_rssrecord WHERE url LIKE '%twitter.com/%'""")
    rows = cur.fetchall()

    print "\nShow me the filtered Twitter URLs from the database:\n"
    for row in rows:
        print "  ", row[0]
    print "\n"

    # for row in rows:   #reads in a row at a time and appends it to holder list
    #     holder.append(row)



    for row in rows:
        try:

            headers = {'User-Agent': 'Mozilla/5 (Solaris 10) Gecko'}

            # page = requests.get(str(item).strip('[\'\']'), headers=headers)
            # page_content = page.content
            # soup = BeautifulSoup(page_content)
            # print soup

            print str(row[0]).strip('[\'\']')
            req = urllib2.Request(str(row[0]).strip('[\'\']'), headers=headers)
            page = urllib2.urlopen(req)
            soup = BeautifulSoup(page)
            soup.prettify()

            datecounter = 0
            dates = []

            for span in soup.findAll("span"):

                for date in span.findAll("a", href=re.compile("status")):
                    while datecounter < 1:
                        try:
                            #print "trying to come up with something"
                            #print date['title']
                            dates.append(date['title'])
                            datecounter += 1
                            print dates[0]
                        except:
                            print "nothing found or code is WRONG"

            time.sleep(randint(1,3)) # random wait period to slow down IP blocking

            try:

                format = '%I:%M %p - %d %b %Y'

                difference = time.mktime(todaysdate) - int(time.mktime(time.strptime(dates[0],format))) #calculates differences
                #in seconds from last RSS feed entry and the current date as of the start of this operation.
                if difference < 0:
                    print "RSS feed was last updated today"

                else:
                    print "RSS feed was last updated ",round(difference/86400, 1),"days ago""\n"  #takes difference in seconds and divides by
                    #24 hours x 60 minutes x 60 seconds = 86,400 seconds to give days difference. Rounds to first decimal place for
                    #ease of reading

            except:
                print str(row).strip('[\'\']'),": Cannot find date RSS was last updated. Feed or source may be down!""\n"  #if
                #there is an error above it means that there is no rss feed available at that url. In that case the site is
                #likely down

            try:
                id = row[1]
                cur.execute("""UPDATE rssrecords_rssrecord SET upordown = 'UP', last_checked = CURRENT_TIMESTAMP WHERE uuid = %s""", (id,))
                print "successfully updated database\n"
                conn.commit()
            except:
                print "unable to execute update to database\n"

        except:
            print str(row[0]),": Cannot find date RSS was last updated. Feed or source may be down!"
            try:
                id = row[1]
                cur.execute("""UPDATE rssrecords_rssrecord SET upordown = 'DOWN', last_checked = CURRENT_TIMESTAMP WHERE uuid = %s""", (id,))
                print "successfully updated database\n"
                conn.commit()
            except:
                print "unable to execute update to database\n"

    conn.close()

def GooglePlusUpdate():
    conn = None
    x = 0
    format = None
    todaysdate = datetime.now().timetuple()
    print todaysdate

    try:
        conn = psycopg2.connect("dbname='d20kid2g0f7d7a' user='aekxaxttfecntl' host='ec2-54-225-115-77.compute-1.amazonaws.com' password='dKNAV1_vFR0Q_fDBvKcATgdHzU'")
    except:
        print "I am unable to connect to the database\n"

    cur = conn.cursor()
    cur.execute("""SELECT url,uuid FROM rssrecords_rssrecord WHERE url LIKE '%plus.google%'""")
    rows = cur.fetchall()

    print "\nShow me the filtered Google Plus URLs from the database:\n"
    for row in rows:
        print "  ", row[0]
    print "\n"

    # for row in rows:   #reads in a row at a time and appends it to holder list
    #     holder.append(row)
    #     #print"this is item #:", x, " - ", row[0]
    #     ++x



    for row in rows:
        try:

            headers = {'User-Agent':'Mozilla/5 (Solaris 10) Gecko'}
            proxies = ['http://adamproxy:dog@173.0.57.198:80']
            rand_proxy = choice(proxies)

            page = requests.get(str(row[0]).strip('[\'\']'), headers = headers, allow_redirects = True, timeout = 5, proxies = proxies)
            print "page request returned with status: ", page.status_code
            tree = html.fromstring(page.text)

            dates = tree.xpath('//a[@class="o-U-s FI Rg"]/text()')

            print dates[0]
            time.sleep(randint(10,20)) # random wait period to slow down IP blocking

            try:

                format = '%Y-%m-%d'

                difference = time.mktime(todaysdate) - int(time.mktime(time.strptime(dates[0],format))) #calculates differences
                #in seconds from last RSS feed entry and the current date as of the start of this operation.
                if difference < 0:
                    print "RSS feed was last updated today"

                else:
                    print "RSS feed was last updated ",round(difference/86400, 1),"days ago""\n"  #takes difference in seconds and divides by
                    #24 hours x 60 minutes x 60 seconds = 86,400 seconds to give days difference. Rounds to first decimal place for
                    #ease of reading

            except:
                print str(row).strip('[\'\']'),": Cannot find date RSS was last updated. Feed or source may be down! Error 1""\n"  #if
                #there is an error above it means that there is no rss feed available at that url. In that case the site is
                #likely down

            try:
                id = row[1]
                cur.execute("""UPDATE rssrecords_rssrecord SET upordown = 'UP', last_checked = CURRENT_TIMESTAMP WHERE uuid = %s""", (id,))
                print "successfully updated database\n"
                conn.commit()
            except:
                print "unable to execute update to database Error 2\n"

        except:
            print str(row[0]),": Cannot find date RSS was last updated. Feed or source may be down! Error 3"
            try:
                id = row[1]
                cur.execute("""UPDATE rssrecords_rssrecord SET upordown = 'DOWN', last_checked = CURRENT_TIMESTAMP WHERE uuid = %s""", (id,))
                print "successfully updated database\n"
                conn.commit()
            except:
                print "unable to execute update to database\n"

    conn.close()


def RssUpdate():
    conn = None
    holder = []
    RSSfeed = None
    id = None
    todaysdate = datetime.now().timetuple()
    print todaysdate

    try:
        conn = psycopg2.connect("dbname='d20kid2g0f7d7a' user='aekxaxttfecntl' host='ec2-54-225-115-77.compute-1.amazonaws.com' password='dKNAV1_vFR0Q_fDBvKcATgdHzU'")
    except:
        print "I am unable to connect to the database"

    cur = conn.cursor()
    cur.execute("""SELECT url,uuid FROM rssrecords_rssrecord WHERE url LIKE '%/feed%' OR url LIKE '%/rss%'
        OR url LIKE '%uploads?orderby' OR url LIKE '%.xml%' OR url LIKE '%format=atom%' OR url LIKE '%.rss%'""")
    rows = cur.fetchall()

    print "\nShow me the filtered RSS URLs from the database:\n"
    for row in rows:
        print "  ", row[0]
    print "\n"

    for row in rows:
        try:

            RSSfeed = feedparser.parse(row[0])
            print RSSfeed['feed']['title'], " Feed appears to be up! @: ", row[0]
            print "with UUID: ", row[1]
            time.sleep(randint(1,3)) # random wait period to slow down IP blocking
            try:
                #print RSSfeed['feed']['title'],":", str(row).strip('[\'\']')
                #print RSSfeed.entries[0].published_parsed
                #var2 = RSSfeed.entries[0].published_parsed
                #print var2
                #rsspub = time.mktime(var2)
                #print "seconds since epoch rss feed: ", time.mktime(RSSfeed.entries[0].published_parsed)
                #print "seconds since epoch today: ", time.mktime(todaysdate)
                #print todaysdate
                difference = time.mktime(todaysdate) - time.mktime(RSSfeed.entries[0].published_parsed) #calculates differences
                #in seconds from last RSS feed entry and the current date as of the start of this operation.
                if difference < 0:
                    print "RSS feed was last updated today"

                else:
                    print "RSS feed was last updated ",round(difference/86400, 1),"days ago""\n"  #takes difference in seconds and divides by
                    #24 hours x 60 minutes x 60 seconds = 86,400 seconds to give days difference. Rounds to first decimal place for
                    #ease of reading

            except:
                print str(row).strip('[\'\']'),": Cannot find date RSS was last updated. Feed or source may be down!""\n"  #if
                #there is an error above it means that there is no rss feed available at that url. In that case the site is
                #likely down

            try:
                id = row[1]
                cur.execute("""UPDATE rssrecords_rssrecord SET upordown = 'UP', last_checked = CURRENT_TIMESTAMP WHERE uuid = %s""", (id,))
                print "successfully updated database\n"
                conn.commit()
            except:
                print "unable to execute update to database\n"

        except:
            print str(row[0]),": Cannot find date RSS was last updated. Feed or source may be down!"
            try:
                id = row[1]
                cur.execute("""UPDATE rssrecords_rssrecord SET upordown = 'DOWN', last_checked = CURRENT_TIMESTAMP WHERE uuid = %s""", (id,))
                print "successfully updated database\n"
                conn.commit()
            except:
                print "unable to execute update to database\n"

    conn.close()


def dbtest():
    conn = None
    holder = []
    RSSfeed = None
    id = None

    try:
        conn = psycopg2.connect("dbname='d20kid2g0f7d7a' user='aekxaxttfecntl' host='ec2-54-225-115-77.compute-1.amazonaws.com' password='dKNAV1_vFR0Q_fDBvKcATgdHzU'")
        # change host back to 'localhostl' for use on local machine. also, that host can change, use ENV VAR to call host from heroku
        #dbname='webupdownusersDB' user='postgres' password='3skateboard'
    except:
        print "I am unable to connect to the database"

    cur = conn.cursor()
    cur.execute("""SELECT url,uuid FROM rssrecords_rssrecord""")
    rows = cur.fetchall()


    print "\nShow me the URLs from the database:\n"
    for row in rows:
        print "  ", row[0]
    print "\n"

    for row in rows:
        try:
            RSSfeed = feedparser.parse(row[0])
            print RSSfeed['feed']['title'], " Feed appears to be up! @: ", row[0]
            print "with UUID: ", row[1]

            try:
                id = row[1]
                cur.execute("""UPDATE rssrecords_rssrecord SET upordown = 'UP', last_checked = CURRENT_TIMESTAMP WHERE uuid = %s""", (id,))
                print "successfully updated database\n"
                conn.commit()
            except:
                print "unable to execute update to database\n"

        except:
            print str(row[0]),": Cannot find date RSS was last updated. Feed or source may be down!"
            #print str(row).strip('[\'\']'),": Cannot find date RSS was last updated. Feed or source may be down!""\n"  #if
            #there is an error above it means that there is no rss feed available at that url. In that case the site is
            #likely down
            try:
                id = row[1]
                cur.execute("""UPDATE rssrecords_rssrecord SET upordown = 'DOWN', last_checked = CURRENT_TIMESTAMP WHERE uuid = %s""", (id,))
                print "successfully updated database\n"
                conn.commit()
            except:
                print "unable to execute update to database\n"

    conn.close()
