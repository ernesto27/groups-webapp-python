from google.appengine.ext import db

class Group(db.Model):
    name = db.StringProperty(required=True)
    description = db.StringProperty(required=True)
    avatar = db.BlobProperty()
    created = db.DateTimeProperty(auto_now = True)


class User(db.Model):
    name = db.StringProperty(required=True)
    email = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    avatar = db.BlobProperty()


class Post(db.Model):
    title = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    user_id = db.IntegerProperty()
    group_id = db.IntegerProperty()
    created = db.DateTimeProperty(auto_now = True)
    likes = db.IntegerProperty(default= 0)


class Comment(db.Model):
    comment = db.TextProperty(required=True)
    user_id = db.IntegerProperty()
    post_id = db.IntegerProperty()
    created = db.DateTimeProperty(auto_now = True)
    likes = db.IntegerProperty(default= 0)
