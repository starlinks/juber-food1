#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import urllib

from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

DEFAULT_SUGGESTION_NAME = 'default_suggestion'

def suggestion_key(suggestion_name=DEFAULT_SUGGESTION_NAME):
    return ndb.Key('Suggestion', suggestion_name)

class Entry(ndb.Model):
    author = ndb.StringProperty(indexed=False)
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        suggestion_name = self.request.get('suggestion_name', DEFAULT_SUGGESTION_NAME)

        entries_query = Entry.query().order(-Entry.date)
        entries = entries_query.fetch(10)

        template_values = {
        'entries' : entries,
        'suggestion_name' : urllib.quote_plus(suggestion_name),
        }

        template = JINJA_ENVIRONMENT.get_template('templates/fridge.html')
        self.response.write(template.render(template_values))

class Suggestion(webapp2.RequestHandler):
    def get(self):

        template = JINJA_ENVIRONMENT.get_template('templates/suggestion.html')
        self.response.write(template.render())

    def post(self):
        '''suggestion_name = self.request.get('suggestion_name', DEFAULT_SUGGESTION_NAME)'''
        entry = Entry()

        entry.author = self.request.get('author')
        entry.content = self.request.get('content')
        entry.put()
        self.redirect('/')

class Countdown(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/countdown.html')
        self.response.write(template.render())

class Stash(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/stash.html')
        self.response.write(template.render())

class About(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/about.html')
        self.response.write(template.render())

class Circle(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/index.html')
        self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/suggestion', Suggestion),
    ('/countdown', Countdown),
    ('/circle', Circle),
    ('/stash', Stash),
    ('/about', About),
], debug=True)
