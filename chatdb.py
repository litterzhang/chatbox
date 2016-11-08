# -*- coding: utf-8 -*-

'Chat数据库'

__author__='litterzhang'

import os

from model.answer import Answer
from model.question import Question
from model.ans2que import Ans2Que

ANSWER = os.path.join(os.path.dirname(__file__), 'data/answer.json')
QUESTION = os.path.join(os.path.dirname(__file__), 'data/question.json')
ANS2QUE = os.path.join(os.path.dirname(__file__), 'data/ans2que.json')

answers = Answer.load(ANSWER)
questions = Question.load(QUESTION)
ans2ques = Ans2Que.load(ANS2QUE)

def match_question(que_str):
	pass