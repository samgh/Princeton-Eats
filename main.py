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

import menuparser
import loadData
import menuscraper
import models

jinja = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class George(webapp2.RequestHandler):
    def get(self):
        data = menuparser.getData()
        self.response.write(data)
 
class Home(webapp2.RequestHandler):
    def get(self):
        template = jinja.get_template('templates/home.html')
        params = {}
        params['menus'] = models.getHomeMenus()
        self.response.out.write(template.render(params)) 

class LoadData(webapp2.RequestHandler):
    def get(self):
        (meals, entrees) = loadData.load()
        #(meals, entrees) = models.getMealsAndEntrees()
        #menus = models.getHomeMenus()
        #self.response.out.write(menus)
        for m in meals:
            self.response.out.write(m.html_string())
        for e in entrees:
            self.response.out.write(e.html_string())
        
class Timeline(webapp2.RequestHandler):
    def get(self):
        template = jinja.get_template('templates/timeline.html')
        self.response.out.write(template.render({}))

class Will(webapp2.RequestHandler):
    def get(self):
        data = menuscraper.getData()
        self.response.write(data.html_string())

app = webapp2.WSGIApplication([
    ('/george', George),
    ('/load-data', LoadData),
    ('/timeline', Timeline),
    ('/will', Will),
    ('/', Home)
], debug=True)
