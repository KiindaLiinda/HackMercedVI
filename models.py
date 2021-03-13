from google.appengine.ext import ndb

#Example Code from My Previous Project: https://github.com/lindajgarcia323/cssi-final-project/blob/master/models.py
#class Event(ndb.Model):
#    name = ndb.StringProperty(required=True)
#    start_time = ndb.DateTimeProperty(required=True)
#    end_time = ndb.DateTimeProperty(required=True)
#    owner_id = ndb.StringProperty(required=True)

#-------------------------------------------------------------------
#Hack Merced Example
class ForumPost(ndb.Model):
    name = ndb.StringProperty(required=True)
    title = ndb.StringProperty(required=True)
    description = ndb.StringProperty(required=True)
    current_date = nbd.DateTimeProperty(required=True)
    owner_id = ndb.StringProperty(required=True)
