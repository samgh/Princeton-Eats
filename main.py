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
        entree = models.Entree.get_by_id(entreeID)
        params = { 'entree':entree }
        template = jinja.get_template('templates/pieces/entree.html')
        self.response.out.write(template.render(params))

class Home(webapp2.RequestHandler):
    def get(self):
        if (isMobile(self.request) == False):
            template = jinja.get_template('templates/homeMobile.html')
            self.response.out.write(template.render({})) 
            return
        template = jinja.get_template('templates/home.html')
        self.response.out.write(template.render({})) 

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
        
class Menus(webapp2.RequestHandler):
    def get(self):
        template = jinja.get_template('templates/pieces/menus.html')
        d = self.request.get('day')
        d = datetime.strptime(d, '%m/%d/%Y').date()
        meal = self.request.get('meal')
        params = {}
        params['menus'] = models.getMeals(d, meal)
        self.response.out.write(template.render(params)) 

class Search(webapp2.RequestHandler):
    def get(self):
        entrees = models.searchEntrees('enchilada')
        self.response.out.write(entrees) 
        
class Timeline(webapp2.RequestHandler):
    def get(self):
        template = jinja.get_template('templates/timeline.html')
        self.response.out.write(template.render({}))

app = webapp2.WSGIApplication([
    ('/entree', Entree),
    ('/load-data', LoadData),
    ('/menus', Menus),
    ('/search', Search),
    ('/timeline', Timeline),
    ('/', Home)
], debug=True)
