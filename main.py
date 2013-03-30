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
import cgi
import webapp2

import jinja2
import os

import george
import models
import will

jinja = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class George(webapp2.RequestHandler):
    def get(self):
        data = george.getData()
        self.response.write(data)

class Home(webapp2.RequestHandler):
    def get(self):
        template = jinja.get_template('templates/home.html')
        params = {}
        params['menu'] = 'test'
        self.response.out.write(template.render(params)) 

class Timeline(webapp2.RequestHandler):
    def get(self):
        template = jinja.get_template('templates/timeline.html')
        self.response.out.write(template.render({}))

class Will(webapp2.RequestHandler):
    def get(self):
        data = will.getData()
        self.response.write(data.html_string())

app = webapp2.WSGIApplication([
    ('/george', George),
    ('/will', Will),
    ('/timeline', Timeline),
    ('/', Home)
], debug=True)