#-*- coding:utf8 -*-

'处理问题、回答、问题-回答'

__author__='litterzhang'

import os
import json

from WordSegment.segs import bmseg

from model.answer import Answer

ANSWER = os.path.join(os.path.dirname(__file__), 'answer.json')
QUESTION = os.path.join(os.path.dirname(__file__), 'question.json')
ANSTOQUE = os.path.join(os.path.dirname(__file__), 'anstoque.json')

def ParseAnswer(fp):
	answers = list()
	if os.path.exists(ANSWER):
		answers = json.load(ANSWER)

	with open(fp, 'r', encoding='utf-8') as fr:
		for line in fr:
			pass

