from celery import task
import psycopg2



@task()
def add(x, y):
    return x + y

@task()
def multiply(x, y):
    return x * y

@task()
def dbtest():
    conn = None
    try:
        conn = psycopg2.connect("dbname='webupdownusersDB' user='postgres' host='localhost' password='3skateboard'")
    except:
        print "I am unable to connect to the database"

    cur = conn.cursor()
    cur.execute("""SELECT url FROM rssrecords_rssrecord""")
    rows = cur.fetchall()

    print "\nShow me the databases:\n"
    for row in rows:
        print "  ", row[0]
