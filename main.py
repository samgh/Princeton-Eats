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
from datetime import datetime, date, time
from detectmobile import isMobile
from google.appengine.api import taskqueue

import menuparser
import loadData
import menuscraper
import models

jinja = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Entree(webapp2.RequestHandler):
    def get(self):
        entreeID = self.request.get('id')
        entreeID = int(float(entreeID))
        ip = self.request.remote_addr
        entree = models.getEntreeById(entreeID, ip)
        params = { 'entree':entree }
        template = jinja.get_template('templates/pieces/entree.html')
        self.response.out.write(template.render(params))
    def post(self):
        # Get vars
        entreeID = self.request.get('id')
        entreeID = int(float(entreeID))
        ip = self.request.remote_addr
        vote = self.request.get('vote')
        vote = int(float(vote))
        
        # Add vote
        models.addEntreeVote(entreeID, ip, vote)

class Hall(webapp2.RequestHandler):
    def get(self):
        template = jinja.get_template('templates/pieces/hall.html')
        hall = self.request.get('hall')
        d = self.request.get('day')
        d = datetime.strptime(d, '%m/%d/%Y').date()
        params = {}
        params['meals'] = models.getHallMeals(d, hall)
        self.response.out.write(template.render(params))         

class Home(webapp2.RequestHandler):
    def get(self):
        if (isMobile(self.request)):
        #if (True):
            template = jinja.get_template('templates/homeMobile.html')
            self.response.out.write(template.render({})) 
            return
        template = jinja.get_template('templates/home.html')
        self.response.out.write(template.render({})) 

class Load(webapp2.RequestHandler):
    def get(self):
        for i in range(0, 7):
            url_to_do = "/load-data"
            taskqueue.add(url=url_to_do, params={'offset':i}, method = 'GET')

class LoadData(webapp2.RequestHandler):
    def get(self):
        offset = self.request.get('offset')
        if offset == '':
            offset = 0
        offset = int(float(offset))
        (meals, entrees) = loadData.load(offset)
        #(meals, entrees) = models.getMealsAndEntrees()
        #menus = models.getHomeMenus()
        #self.response.out.write(menus)
        
        for m in meals:
            self.response.out.write(m.html_string())
        for e in entrees:
            self.response.out.write(e.html_string())
        
class Delete(webapp2.RequestHandler):
    def get(self):
        models.delOutdatedEntries()

class Menus(webapp2.RequestHandler):
    def get(self):
        template = jinja.get_template('templates/pieces/menus.html')
        d = self.request.get('day')
        d = datetime.strptime(d, '%m/%d/%Y').date()
        meal = self.request.get('meal')
        params = {}
        params['menus'] = models.getMeals(d, meal)
        self.response.out.write(template.render(params)) 

class MobileSearch(webapp2.RequestHandler):
    def get(self):
        q = self.request.get('q')
        ip = self.request.remote_addr
        params = { 
            'entrees':models.searchEntrees(q, ip),
            'q':q 
        }
        template = jinja.get_template('templates/mobileSearch.html')
        self.response.out.write(template.render(params))

class Search(webapp2.RequestHandler):
    def get(self):
        q = self.request.get('q')
        ip = self.request.remote_addr
        params = { 
            'entrees':models.searchEntrees(q, ip),
            'q':q 
        }
        template = jinja.get_template('templates/search.html')
        self.response.out.write(template.render(params))

class Timeline(webapp2.RequestHandler):
    def get(self):
        template = jinja.get_template('templates/timeline.html')
        self.response.out.write(template.render({}))

app = webapp2.WSGIApplication([
    ('/entree', Entree),
    ('/hall', Hall),
    ('/load-data', LoadData),
    ('/queue-load', Load),
    ('/del-data', Delete),
    ('/menus', Menus),
    ('/mobile-search', MobileSearch),
    ('/search', Search),
    ('/timeline', Timeline),
    ('/', Home)
], debug=True)
