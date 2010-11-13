# -*- coding: utf-8 -*-

from models import *
import os
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp

class saveResultsHandler(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()

        # Where is the new syntax :(
        # vals = [ x: self.request.get(x) for x in self.request.arguments()]
        vals = []
        elements_to_save = []
        # Create answer set and save it
        answerSet = AnswerSet()
        answerSet.author = user
        db.save(answerSet)

        real_answer_count = 0
        # iterate over all the parameters and make SavedResults
        for arg in self.request.arguments():
            answer = self.request.get(arg)
            elem = {'arg':arg,'val':answer}
            vals.append(elem)
            if answer != None and answer.strip() !="":
                real_answer_count +=1
            savedAnswer =self.createSavedResult(answerSet,arg,answer)
            elements_to_save.append(savedAnswer)

        answerSet.count = real_answer_count
        db.save(answerSet)
        db.save(elements_to_save)

        self.redirect("/")

        # for debug show what is saved
#        template_values = {'user':user,
#                           'arguments':self.request.arguments(),
#                           'values': vals,
#                           'request': self.request
#        }
        #path = os.path.join(os.path.dirname(__file__), 'templates/saveResults.html')
        #self.response.out.write(template.render(path, template_values))

    def createSavedResult(self,answer_set,questionId,answerText):
        answer  = SavedAnswer()
        answer.answer_set = answer_set
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

class showMyResultsHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect("/")

        answerSets = db.GqlQuery("SELECT * FROM AnswerSet")
        template_values = {'user':user,
                            'answerSets':answerSets,
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/showmyresults.html')
        self.response.out.write(template.render(path, template_values))



class initdbHandler(webapp.RequestHandler):
    def get(self):
        #print "initdbHandler"
        user = users.get_current_user()
        if user.email() != "zeroowl@gmail.com":
            #print("You should be logined as Admdin")
            self.redirect("/")
            return
        # clean old data
        print "Deleting all questions"
        questions = db.GqlQuery("SELECT * FROM Question")
        for question in questions:
            question.delete()

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
        self.question(u"Позволил ли я какой-либо навязчивой идее завладеть мною? ","bool_text").save()
        self.question(u"Позволил ли я себе быть слишком голодным, злым, унылым или усталым? ","text").save()
        self.question(u"Не воспринимаю ли я себя слишком серьезно в отношении какой-то стороны моей жизни?","text").save()
        self.question(u"Не страдаю ли я от каких-то физических, умственных или духовных проблем?","text").save()
        self.question(u"Не умолчал ли я о чем-либо таком, о чем непременно должен был посоветоваться со спонсором?","text").save()
        self.question(u"Были ли у меня сегодня какие-то экстремальные ощущения? Что это были за ощущения и из-за чего? ","text").save()
        self.question(u"Какие проблемы существуют в моей сегодняшней жизни? ","text").save()
        self.question(u"Какие из моих недостатков проявились в моей сегодняшней жизни? Как именно? ","text").save()
        self.question(u"Был ли страх в моей сегодняшней жизни? ","bool_text").save()
        self.question(u"Что я сделал сегодня такого, что было противно моим желаниям? ","text").save()
        self.question(u"Что я сегодня не сделал из того, что хотелось бы?","text").save()
        self.question(u"Готов ли я к изменениям? ","bool_text").save()
        self.question(u"Были ли у меня сегодня с кем-то конфликты? Какие именно?","bool_text").save()
        self.question(u"Поддерживаю ли я собственную честность в отношениях с другими людьми?","text").save()
        self.question(u"Не навредил ли я сегодня себе самому или кому-то другому прямо или косвенно? В чем именно?","text").save()
        self.question(u"Нет ли за мной каких-то невыполненных обещаний или клятв? ","text").save()
        self.question(u"В чем я ошибся? Если бы все вернуть назад, что бы я сделал по-другому? Что именно я смогу сделать лучше в следующий раз? ","text").save()
        self.question(u"Оставался ли я сегодня чистым? ","bool").save()
        self.question(u"Что это были за чувства, которые я испытывал сегодня? Обращал ли я на них внимание, действуя в соответствии с определенными принципами? ","text").save()
        self.question(u"Что я сделал сегодня такого, что принесло пользу другим? ","text").save()
        self.question(u"Что я сделал сегодня такого, о чем мне приятно вспомнить? ","text").save()
        self.question(u"Что принесло мне удовлетворение сегодня?","text").save()
        self.question(u"Что я делал сегодня такого, что мне обязательно захочется повторить? ","text").save()
        self.question(u"Ходил ли я сегодня на собрание или разговаривал ли я сегодня с другими выздоравливающими наркоманами?","bool").save()
        self.question(u"За что я благодарен сегодняшнему дню?","text").save()
        print "All elements are saved"
        self.redirect("/")

    def question(self,text,type):
        question = Question()
        question.text = text
        question.type = type
        return question



__author__ = 'zeroowl'
  