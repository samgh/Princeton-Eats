import datetime

from google.appengine.ext import db

class Entree(db.Model):
    allergens = db.StringListProperty()
    ingredients = db.StringListProperty()
    name = db.StringProperty()

class Meal(db.Model):
    date = db.DateTimeProperty()
    diningHall = db.StringProperty()
    entreeKeys = db.StringListProperty()
    name = db.StringProperty()
    
# Sample model for timeline posts (ended up using Tumblr)
class TimelinePost(db.Model):
    title = db.StringProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)
    
def insertTimelinePost(request):
    post = TimelinePost()
    post.title = request.get('title')
    post.content = request.get('content')
    post.put()
    
def getTimelinePosts():
    q = TimelinePost.all()
    posts = []
    for post in q.run():
        posts.append(post)
    return posts