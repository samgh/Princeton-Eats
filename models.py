import datetime

from google.appengine.ext import db

# Entree data type, keyed by name
class Entree(db.Model):
    allergens = db.StringListProperty()
    ingredients = db.StringListProperty()
    name = db.StringProperty()
    def html_string(self):
        html = '<div>'
        html = html + '<p><b>%s</b></p>' % self.name
        html = html + '<p>%s</p>' % self.allergens
        html = html + '<p>%s</p>' % self.ingredients
        html = html + '</div>'
        return html

# Meal data type
class Meal(db.Model):
    date = db.StringProperty()
    entreeKeys = db.StringListProperty()
    hall = db.StringProperty()
    type = db.StringProperty()
    def html_string(self):
        html = '<div>'
        html = html + '<p><b>%s, %s, %s</b></p>' % (self.hall, self.type, self.date)
        html = html + '<p>%s</p>' % self.entreeKeys
        html = html + '</div>'
        return html
    
# Return data for the homepage
def getHomeData():
    meals = Meal.all().run()
    entrees = Entree.all().run()
    return (meals, entrees)

# Sample model for timeline posts (ended up using Tumblr)
class TimelinePost(db.Model):
    title = db.StringProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)
    def html_string(self):
        return '%s, %s' % (self.title, self.content)
    
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