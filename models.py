# -*- coding: utf-8 -*-
from google.appengine.ext import db


class Question(db.Model):
#  author = db.UserProperty()
  text = db.StringProperty()
  type = db.StringProperty(choices=['text','bool','text_bool','bool_text'])

class AnswerSet(db.Model):
    date = db.DateTimeProperty(auto_now_add=True)
    author = db.UserProperty()
    count  = db.IntegerProperty()

class SavedAnswer(db.Model):
  answer_set = db.ReferenceProperty(AnswerSet,
                                   collection_name='saved_answers')
  question = db.ReferenceProperty(reference_class=Question)
  answer = db.StringProperty()


__author__ = 'zeroowl'
  