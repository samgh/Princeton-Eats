import datetime

from google.appengine.ext import db

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