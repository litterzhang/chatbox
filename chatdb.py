# -*- coding: utf-8 -*-

'Chat数据库'

__author__='litterzhang'

import os

from model.answer import Answer
from model.question import Question
from model.ans2que import Ans2Que

from WordSegment.segs import bmseg

import ChatUtils

ANSWER = os.path.join(os.path.dirname(__file__), 'data/answer.json')
QUESTION = os.path.join(os.path.dirname(__file__), 'data/question.json')
ANS2QUE = os.path.join(os.path.dirname(__file__), 'data/ans2que.json')

answers = Answer.load(ANSWER)
questions = Question.load(QUESTION)
ans2ques = Ans2Que.load(ANS2QUE)

def match_question(que_str):
	sims = list()
	
	que_words = [list(x) for x in bmseg.seg(que_str)]
	que_words = list(filter(lambda x: x[2]!='bd', que_words))

	for que in questions:
		sims.append(ChatUtils.sim_calc(que_words, que.words))

	sim_max = max(sims)
	que_mat = questions[sims.index(sim_max)]

	return que_mat, sim_max

def get_ans_by_que(que):
	ans2que = Ans2Que.get_ans_by_que(ans2ques, que.id)
	anss = list()
	if ans2que:
		for ans_id in ans2que.ans_ids:
			ans = Answer.get_ans_by_id(answers, ans_id)
			if ans:
				anss.append(ans)
	return anss

def get_answer(que_str):
	que, sim = match_question(que_str)
	anss = get_ans_by_que(que)
	return que, sim, anss
	 
if __name__=='__main__':
	que, sim = match_question('吃了吗??')
	anss = get_ans_by_que(que)