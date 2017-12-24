# "Database code" for the DB Forum.

import psycopg2
import bleach

#POSTS = [("This is the first post.", datetime.datetime.now())]
DBNAME="forum"
def get_posts():
  """Return all posts from the 'database', most recent first."""
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  c.execute("select content, time from posts order by time desc")
  result = c.fetchall()
  db.close()
  return result

def add_post(content):
  """Add a post to the 'database' with the current timestamp."""
  #POSTS.append((content, datetime.datetime.now()))
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  #c.execute("delete from posts;")
  
  c.execute("update posts set content = 'cheese' where content like 'spam%'")
  c.execute("insert into posts (content) values (%s)", (content,))
  db.commit()
  db.close()

