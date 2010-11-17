# -*- coding: utf-8 -*-
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
from google.appengine.ext.webapp import util
from views import *

import os
import sys
from google.appengine.ext.webapp import template

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.conf import settings
# Force Django to reload settings
settings._target = None

def main():
    application = webapp.WSGIApplication([('/', MainHandler),
                                          ('/initdb',initdbHandler),
                                          ('/saveResults',saveResultsHandler),
                                          ('/showMyResults',showMyResultsHandler),
                                          ('/changeLanguage',changeLanguageHandler),

                                          ],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
