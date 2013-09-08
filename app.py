import os
import random

from string import letters

import webapp2
import jinja2

from google.appengine.ext import db

import helpers
from databasemodels import *


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)



def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class Handler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)


class SignUp(Handler):
    def get(self):
        helpers.test()  
        self.render("signup.html")

    def post(self):
        name = self.request.get("name")
        email = self.request.get("email")
        pass1 = self.request.get("pass1")
        pass2 = self.request.get("pass2")

        messages = {}

        if not helpers.valid_username(name):
            messages['error_name'] = "Enter a valid name"
        if not helpers.valid_email(email):
            messages['error_email'] = "That's not a valid email"  
        if not helpers.valid_password(pass1):
            messages['error_pass1'] =  "Enter a valid password"
        if pass1 != pass2:
            messages['error_pass2'] = "password doesn't match"

        if len(messages):
            self.render("signup.html", **messages)
        else:
            self.render('signup.html', register="true")
            #user = User(name= name, email = email, password=pass1)
            #user.put()


class Login(Handler):
    def get(self):
        self.render("login.html")

    def post(self):
        email = self.request.get("email")
        pass1 = self.request.get("pass")

        #self.write(email +" "+ pass1)

        user = db.GqlQuery("select * from User where email = :email and password =:password",
                            email=email, password=pass1)

        for u in user:
            name = u.name

        if user.count():
            self.response.headers.add_header('Set-Cookie',"logged="+str(helpers.make_secure_val("true")))
            self.response.headers.add_header('Set-Cookie',"name="+str(name))
            self.redirect('/home')
        else:
            self.write("The user doesn't exist")

class Logout(Handler):
    def get(self):
        self.response.headers.add_header('Set-Cookie',"logged=true;Expires=Thu, 01-Jan-1970 00:00:00 GMT")
        self.response.headers.add_header('Set-Cookie',"name=")
        self.redirect("/login")


def check_login(self):
    logged = self.request.cookies.get("logged")
    if logged:
        return True

class Home(Handler):
    def get(self):
        if check_login(self):
            name = self.request.cookies.get("name")
            self.render("home.html", name=name)
        else:
            self.redirect("login", **messages)

class CreateGroup(Handler):
    def get(self):
        self.render("addGroup.html")

    def post(self):
        name = self.request.get("name")
        description = self.request.get("description")

        messages = {}
        if not name.strip():
            messages["error_name"] = "Enter a name"
        if not description.strip():
            messages["error_description"] = "Enter a description"

        if len(messages):
            self.render("addGroup.html", **messages)
        else:
            g = Group(name=name, description=description)
            g.put()
            self.render("addGroup.html", message="The group has been added")

class ViewGroup(Handler):
    def get(self, id=None):
        group_id = int(id)
        group = Group.get_by_id(group_id)
        posts = db.GqlQuery("select * from Post where group_id=:group_id order by created desc", group_id=group_id )
        #self.write(posts.count())

        self.render("singleGroup.html",
                    name= group.name, description=group.description,
                    group_id=group_id, posts=posts)

class AddPost(Handler):
    def get(self, id=None):
        self.render("addPost.html", group_id=int(id))

    def post(self, id=None):
        title = self.request.get("title").strip()
        content = self.request.get("content").strip()
        group_id = self.request.get("group_id").strip()


        if title and content:
            p = Post(title=title, content=content, user_id=1, group_id=int(group_id))
            self.write(p.put())
            self.redirect("/group/" + str(group_id))
        else:
            self.render("AddPost.html",group_id=int(id), message="Insert a title and content")
    
class ViewPost(Handler):
    def get(self, id=None):
        post_id = int(id)
        post = Post.get_by_id(post_id)
        self.render("post.html", post= post)

    def post(self, id=None):
        comment = self.request.get("comment").strip()
        post_id = self.request.get("postid").strip()

        if comment and post_id:
            c = Comment(comment=comment, user_id=1, post_id=post_id)
            c.put()
            self.redirect("/post/" + post_id)


class Index(Handler):   
    def get(self):
        #g = Group(name="javascript",description="dinamic prototypal language")
        #self.write(g.put())
        #self.write(helpers.make_secure_val("hello"))
        #self.response.headers.add_header('Set-Cookie',"logged=true")
        

        groups = db.GqlQuery("select * from Group order by created desc")
        self.render("index.html", groups=groups)

app = webapp2.WSGIApplication([('/signup', SignUp),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/home', Home),
                               ('/creategroup', CreateGroup),
                               ('/group/([0-9]+)', ViewGroup),
                               ('/addpost/([0-9]+)', AddPost),
                               ('/post/([0-9]+)', ViewPost),
                               ('/', Index)
                            ],
                            debug=True)

























