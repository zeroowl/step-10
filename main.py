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
        self.question(u"Подтвердил ли я вновь сегодня свою веру в любящего, заботливого Бога? ","bool").save()
        self.question(u"Увидел ли я сегодня, что моя Высшая Сила сопровождала меня? В чем именно? ","text").save()
        self.question(u"Что я сделал полезного для Бога и окружающих меня людей? ","text").save()
        self.question(u"Дал ли Бог мне что-нибудь такое, за что я мог бы быть благодарен сегодняшнему дню? ","bool_text").save()
        self.question(u"Верю ли я, что моя Высшая Сила может научить меня жить и следовать ее воле?","bool").save()
        self.question(u"Замечаю ли я какие-то “старые шаблоны” в моей жизни сегодня? ","text").save()
        self.question(u"Был ли я обидчив, эгоистичен, нечестен или труслив? ","bool").save()
        self.question(u"Не обманул ли я сам себя в своих ожиданиях? ","bool_text").save()
        self.question(u"Был ли я добрым и любящим ко всем?","bool_text").save()
        self.question(u"Испытывал ли я беспокойство о вчерашнем или завтрашнем дне?","bool").save()
        self.question(u"Позволил ли я какой-либо навязчивой идее завладеть мною? ","bool").save()
        self.question(u"Позволил ли я себе быть слишком голодным, злым, унылым или усталым? ","text").save()
        self.question(u"Не воспринимаю ли я себя слишком серьезно в отношении какой-то стороны моей жизни?","text").save()
        self.question(u"Не страдаю ли я от каких-то физических, умственных или духовных проблем?","text").save()
        self.question(u"Не умолчал ли я о чем-либо таком, о чем непременно должен был посоветоваться со спонсором?","text").save()
        self.question(u"Были ли у меня сегодня какие-то экстремальные ощущения? Что это были за ощущения и из-за чего? ","text").save()
        self.question(u"Какие проблемы существуют в моей сегодняшней жизни? ","text").save()
        self.question(u"Какие из моих недостатков проявились в моей сегодняшней жизни? Как именно? ","text").save()
        self.question(u"Был ли страх в моей сегодняшней жизни? ","text").save()
        self.question(u"Что я сделал сегодня такого, что было противно моим желаниям? ","text").save()
        self.question(u"Что я сегодня не сделал из того, что хотелось бы?","text").save()
        self.question(u"Готов ли я к изменениям? ","text").save()
        self.question(u"Были ли у меня сегодня с кем-то конфликты? Какие именно?","text").save()
        self.question(u"Поддерживаю ли я собственную честность в отношениях с другими людьми?","text").save()
        self.question(u"Не навредил ли я сегодня себе самому или кому-то другому прямо или косвенно? В чем именно?","text").save()
        self.question(u"Нет ли за мной каких-то невыполненных обещаний или клятв? ","text").save()
        self.question(u"В чем я ошибся? Если бы все вернуть назад, что бы я сделал по-другому? Что именно я смогу сделать лучше в следующий раз? ","text").save()
        self.question(u"Оставался ли я сегодня чистым? ","text").save()
        self.question(u"Оставался ли я сегодня чистым? ","text").save()
        self.question(u"Что это были за чувства, которые я испытывал сегодня? Обращал ли я на них внимание, действуя в соответствии с определенными принципами? ","text").save()
        self.question(u"Что я сделал сегодня такого, что принесло пользу другим? ","text").save()
        self.question(u"Что я сделал сегодня такого, о чем мне приятно вспомнить? ","text").save()
        self.question(u"Что принесло мне удовлетворение сегодня?","text").save()
        self.question(u"Что я делал сегодня такого, что мне обязательно захочется повторить? ","text").save()
        self.question(u"Ходил ли я сегодня на собрание или разговаривал ли я сегодня с другими выздоравливающими наркоманами?","text").save()
        self.question(u"За что я благодарен сегодняшнему дню?","text").save()

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
