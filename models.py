from google.appengine.ext import ndb

#Example Code from My Previous Project: https://github.com/lindajgarcia323/cssi-final-project/blob/master/models.py
class Event(ndb.Model):
    name = ndb.StringProperty(required=True)
    start_time = ndb.DateTimeProperty(required=True)
    end_time = ndb.DateTimeProperty(required=True)
    owner_id = ndb.StringProperty(required=True)
