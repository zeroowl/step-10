# -*- coding: Windows-1251 -*- #
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
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
import os
from google.appengine.ext.webapp import template
from google.appengine.ext import db

class Question(db.Model):
#  author = db.UserProperty()
  text = db.StringProperty()
  type = db.StringProperty(choices=['text','bool','text_bool','bool_text'])

class SavedAnswer(db.Model):
  author = db.UserProperty()
  question = db.ReferenceProperty(reference_class=Question)
  date = db.DateTimeProperty(auto_now_add=True)
  answer = db.StringProperty()



class saveResults(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()

        # Where is the new syntax :(
        # vals = [ x: self.request.get(x) for x in self.request.arguments()]
        vals = []
        elements_to_save = []
        for arg in self.request.arguments():
            answer = self.request.get(arg)
            elem = {'arg':arg,'val':answer}
            vals.append(elem)
            savedAnswer =self.createSavedResult(user,arg,answer)
            elements_to_save.append(savedAnswer)
        template_values = {'user':user,
                           'arguments':self.request.arguments(),
                           'values': vals,
                           'request': self.request
        }
        db.save(elements_to_save)
        path = os.path.join(os.path.dirname(__file__), 'templates/saveResults.html')
        self.response.out.write(template.render(path, template_values))

    def createSavedResult(self,user,questionId,answerText):
        answer  = SavedAnswer()
        answer.author = user
        answer.question = db.get(questionId)
        answer.answer = answerText
        return answer

class MainHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()

        questions = db.GqlQuery("SELECT * FROM Question")
        template_values = {'user':user,
                            'questions':questions,
                            'loginurl':  users.create_login_url(self.request.uri),
                            'logouturl' : users.create_logout_url(self.request.uri)
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/main.html')
        self.response.out.write(template.render(path, template_values))


class initdbHandler(webapp.RequestHandler):
    def get(self):
        self.question(u"���������� �� � ����� ������� ���� ���� � ��������, ����������� ����? ","bool").save()
        self.question(u"������ �� � �������, ��� ��� ������ ���� ������������ ����? � ��� ������? ","text").save()
        self.question(u"��� � ������ ��������� ��� ���� � ���������� ���� �����? ","text").save()
        self.question(u"��� �� ��� ��� ���-������ �����, �� ��� � ��� �� ���� ���������� ������������ ���? ","bool_text").save()
        self.question(u"���� �� �, ��� ��� ������ ���� ����� ������� ���� ���� � ��������� �� ����?","bool").save()
        self.question(u"������� �� � �����-�� ������� �������� � ���� ����� �������? ","text").save()
        self.question(u"��� �� � �������, ����������, �������� ��� �������? ","bool").save()
        self.question(u"�� ������� �� � ��� ���� � ����� ���������? ","bool_text").save()
        self.question(u"��� �� � ������ � ������� �� ����?","bool_text").save()
        self.question(u"��������� �� � ������������ � ��������� ��� ���������� ���?","bool").save()
        self.question(u"�������� �� � �����-���� ���������� ���� ��������� ����? ","bool").save()
        self.question(u"�������� �� � ���� ���� ������� ��������, ����, ������ ��� �������? ","text").save()
        self.question(u"�� ����������� �� � ���� ������� �������� � ��������� �����-�� ������� ���� �����?","text").save()
        self.question(u"�� ������� �� � �� �����-�� ����������, ���������� ��� �������� �������?","text").save()
        self.question(u"�� ������� �� � � ���-���� �����, � ��� ���������� ������ ��� �������������� �� ���������?","text").save()
        self.question(u"���� �� � ���� ������� �����-�� ������������� ��������? ��� ��� ���� �� �������� � ��-�� ����? ","text").save()
        self.question(u"����� �������� ���������� � ���� ����������� �����? ","text").save()
        self.question(u"����� �� ���� ����������� ���������� � ���� ����������� �����? ��� ������? ","text").save()
        self.question(u"��� �� ����� � ���� ����������� �����? ","text").save()
        self.question(u"��� � ������ ������� ������, ��� ���� �������� ���� ��������? ","text").save()
        self.question(u"��� � ������� �� ������ �� ����, ��� �������� ��?","text").save()
        self.question(u"����� �� � � ����������? ","text").save()
        self.question(u"���� �� � ���� ������� � ���-�� ���������? ����� ������?","text").save()
        self.question(u"����������� �� � ����������� ��������� � ���������� � ������� ������?","text").save()
        self.question(u"�� �������� �� � ������� ���� ������ ��� ����-�� ������� ����� ��� ��������? � ��� ������?","text").save()
        self.question(u"��� �� �� ���� �����-�� ������������� �������� ��� �����? ","text").save()
        self.question(u"� ��� � ������? ���� �� ��� ������� �����, ��� �� � ������ ��-�������? ��� ������ � ����� ������� ����� � ��������� ���? ","text").save()
        self.question(u"��������� �� � ������� ������? ","text").save()
        self.question(u"��������� �� � ������� ������? ","text").save()
        self.question(u"��� ��� ���� �� �������, ������� � ��������� �������? ������� �� � �� ��� ��������, �������� � ������������ � ������������� ����������? ","text").save()
        self.question(u"��� � ������ ������� ������, ��� �������� ������ ������? ","text").save()
        self.question(u"��� � ������ ������� ������, � ��� ��� ������� ���������? ","text").save()
        self.question(u"��� �������� ��� �������������� �������?","text").save()
        self.question(u"��� � ����� ������� ������, ��� ��� ����������� ��������� ���������? ","text").save()
        self.question(u"����� �� � ������� �� �������� ��� ������������ �� � ������� � ������� ����������������� �����������?","text").save()
        self.question(u"�� ��� � ���������� ������������ ���?","text").save()

    def question(self,text,type):
        question = Question()
        question.text = text
        question.type = type
        return question

def main():
    application = webapp.WSGIApplication([('/', MainHandler),
                                          ('/initdb',initdbHandler),
                                          ('/saveResults',saveResults)
                                          ],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
