
import json
import jinja2
import datetime
import os
import webapp2

from datetime import datetime
from datetime import timedelta
from google.appengine.api import users
from google.appengine.ext import ndb

from models import Event
#remember, you can get this by searching for jinja2 google app engine
jinja_current_dir = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
#-------------------------------------------------------------------

#Create Post Handlers
class CreatePostHandler(webapp2.RequestHandler):
    def get(self):
        start_template = jinja_current_dir.get_template("html/Forum.html")
        self.response.write(start_template.render())
    def post(self):
        

#-------------------------------------------------------------------
#Homepage Handler
class HomepageHandler(webapp2.RequestHandler):
    def get(self):
        start_template = jinja_current_dir.get_template("html/index.html")
        self.response.write(start_template.render())

#Dashboard Handler
class DashboardHandler(webapp2.RequestHandler):
    def get(self):
        start_template = jinja_current_dir.get_template("html/dashboard.html")
        self.response.write(start_template.render())
#Creating a new event
class NewEventHandler(webapp2.RequestHandler):
    def get(self):
        start_template = jinja_current_dir.get_template("html/newevent.html")
        self.response.write(start_template.render())

    def post(self):
        logged_in_user = users.get_current_user()
        event_name = self.request.get('event-name')
        start_string = self.request.get('start-time')
        end_string = self.request.get('end-time')
        if start_string and end_string and event_name:
            start_date = datetime.strptime(start_string, "%Y-%m-%dT%H:%M")
            end_utc = datetime.strptime(end_string, "%Y-%m-%dT%H:%M")
            start_utc = start_date + timedelta(hours=7)

            calendar_url = "http://www.google.com/calendar/event?action=TEMPLATE&text=%s&dates=%s/%s"
            calendar_start = start_utc.strftime("%Y%m%dT%H%M00Z")
            calendar_end = end_utc.strftime("%Y%m%dT%H%M00Z")

            calendar_link = calendar_url % (event_name, calendar_start, calendar_end)
            new_event = Event(name=event_name, start_time=start_utc,
                              end_time=end_utc, owner_id=logged_in_user.user_id())
            new_event.put()
            calendar_html = "<html><body><a target='_blank' href='%s'>Test Event Link</a></body></html>"
            self.response.write(calendar_html % calendar_link)
        else:
            self.redirect('/newevent')

class AllEventsHandler(webapp2.RequestHandler):
   def get(self):
       start_template = jinja_current_dir.get_template("html/myevents.html")
       logged_in_user = users.get_current_user()
       events = Event.query().filter(Event.owner_id == logged_in_user.user_id()).fetch()
       self.response.write(start_template.render({'my_events': events}))

class ComingSoonHandler(webapp2.RequestHandler):
   def get(self):
       start_template = jinja_current_dir.get_template("html/comingsoon.html")
       self.response.write(start_template.render())

app = webapp2.WSGIApplication([
    ('/', HomepageHandler),
    ('/dashboard', DashboardHandler),
    ('/newevent', NewEventHandler),
    ('/myevents', AllEventsHandler),
    ('/comingsoon', ComingSoonHandler),
], debug=True)
