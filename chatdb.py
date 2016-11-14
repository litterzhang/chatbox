# -*- coding: utf-8 -*-

'Chat数据库'

__author__='litterzhang'

import os

from model.answer import Answer
from model.question import Question
from model.ans2que import Ans2Que

from WordSegment.segs import bmseg

import ChatUtils

answers = list()
questions = list()
ans2ques = list()

def init_db(key):
	ANSWER = os.path.join(os.path.dirname(__file__), 'data/answer_%s.json' % key)
	QUESTION = os.path.join(os.path.dirname(__file__), 'data/question_%s.json' % key)
	ANS2QUE = os.path.join(os.path.dirname(__file__), 'data/ans2que_%s.json' % key)

	if os.path.exists(ANSWER):
		answers = Answer.load(ANSWER)
	if os.path.exists(QUESTION):
		questions = Question.load(QUESTION)
	if os.path.exists(ANS2QUE):
		ans2ques = Ans2Que.load(ANS2QUE)

def match_question(que_str):
	sims = list()
	
	que_words = [list(x) for x in bmseg.seg(que_str)]
	que_words = list(filter(lambda x: x[2]!='bd', que_words))

	for que in questions:
		sims.append(ChatUtils.sim_calc(que_words, que.words))

	if not sims:
		return None, 0

	sim_max = max(sims)
	que_mat = questions[sims.index(sim_max)]

	return que_mat, sim_max

def get_ans_by_que(que):
	ans2que = Ans2Que.get_ans_by_que(ans2ques, que.id)
	anss = list()
	if ans2que:
		for ans_id in ans2que.ans_ids:
			ans = Answer.get_ans_by_id(answers, ans_id['id'])
			if ans:
				anss.append({'ans' : ans, 'score' : ans_id['score']})
	return anss

def get_answer(que_str):
	que, sim = match_question(que_str)
	if not que:
		return None, 0, list()
	anss = get_ans_by_que(que)
	return que, sim, anss
	 
if __name__=='__main__':
	que, sim = match_question('吃了吗??')
	anss = get_ans_by_que(que)