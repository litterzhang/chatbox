# -*- coding: utf-8 -*-

'Chat数据库'

__author__='litterzhang'

import os
import copy

from model.answer import Answer
from model.question import Question
from model.ans2que import Ans2Que

from WordSegment.segs import bmseg

import ChatUtils

answers = list()
questions = list()
ans2ques = list()
ids = list([0, 0])

def init_db(key):
	global answers, questions, ans2ques, ids

	ANSWER = os.path.join(os.path.dirname(__file__), 'data/answer_%s.json' % key)
	QUESTION = os.path.join(os.path.dirname(__file__), 'data/question_%s.json' % key)
	ANS2QUE = os.path.join(os.path.dirname(__file__), 'data/ans2que_%s.json' % key)
	IDS = os.path.join(os.path.dirname(__file__), 'data/ids_%s' % key)

	if os.path.exists(ANSWER):
		answers = Answer.load(ANSWER)
	if os.path.exists(QUESTION):
		questions = Question.load(QUESTION)
	if os.path.exists(ANS2QUE):
		ans2ques = Ans2Que.load(ANS2QUE)
	if os.path.exists(IDS):
		with open(IDS, 'r', encoding='utf-8') as fr:
			ids = [int(x) for x in fr.readline().strip().split()]
	
	print('\n----------Debug---------\n')
	for question in questions:
		print('question : %s ' % question.toString())
	for answer in answers:
		print('answer : %s ' % answer.toString())
	for ans2que in ans2ques:
		print('ans2que : %s ' % ans2que.toString())
	print('\n----------Debug---------\n')

def save_db(key):
	global answers, questions, ans2ques, ids

	ANSWER = os.path.join(os.path.dirname(__file__), 'data/answer_%s.json' % key)
	QUESTION = os.path.join(os.path.dirname(__file__), 'data/question_%s.json' % key)
	ANS2QUE = os.path.join(os.path.dirname(__file__), 'data/ans2que_%s.json' % key)
	IDS = os.path.join(os.path.dirname(__file__), 'data/ids_%s' % key)

	# print('\n----------Debug---------\n')
	# for question in questions:
	# 	print('question : %s ' % question.toString())
	# for answer in answers:
	# 	print('answer : %s ' % answer.toString())
	# for ans2que in ans2ques:
	# 	print('ans2que : %s ' % ans2que.toString())
	# print('\n----------Debug---------\n')

	Answer.dump(answers, ANSWER)
	Question.dump(questions, QUESTION)
	Ans2Que.dump(ans2ques, ANS2QUE)

	with open(IDS, 'w', encoding='utf-8') as fw:
		fw.write('%s %s' % (str(ids[0]), str(ids[1])))

def match_question(que_str):
	global answers, questions, ans2ques, ids

	# print('\n----------Debug---------\n')
	# for question in questions:
	# 	print('question : %s ' % question.toString())
	# for answer in answers:
	# 	print('answer : %s ' % answer.toString())
	# for ans2que in ans2ques:
	# 	print('ans2que : %s ' % ans2que.toString())
	# print('\n----------Debug---------\n')

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
	global answers, questions, ans2ques, ids

	ans2que = Ans2Que.get_ans_by_que(ans2ques, que.id)
	anss = list()
	if ans2que:
		for ans_id in ans2que.ans_ids:
			ans = Answer.get_ans_by_id(answers, ans_id['id'])
			if ans:
				anss.append({'ans' : ans, 'score' : ans_id['score']})
	return anss

def get_answer(que_str):
	global answers, questions, ans2ques, ids

	que, sim = match_question(que_str)
	if not que:
		return None, 0, list()
	anss = get_ans_by_que(que)

	# print('相似度: %s\n' % sim)
	return que, sim, anss

def que_new_id():
	global answers, questions, ans2ques, ids

	ids[0] += 1
	return ids[0]

def ans_new_id():
	global answers, questions, ans2ques, ids

	ids[1] += 1
	return ids[1]

def que_new(que_str, que_type=2):
	global answers, questions, ans2ques, ids

	que_id = que_new_id()
	que = Question(que_id, que_type, que_str, bmseg.seg(que_str))

	questions.append(que)

	# print('\n----------Debug---------\n')
	# for question in questions:
	# 	print('question : %s ' % question.toString())
	# for answer in answers:
	# 	print('answer : %s ' % answer.toString())
	# for ans2que in ans2ques:
	# 	print('ans2que : %s ' % ans2que.toString())
	# print('\n----------Debug---------\n')

	return que

def ans_new(ans_str, ans_type=2, ans_seed=-1, ans_deg=0):
	global answers, questions, ans2ques, ids

	ans_id = ans_new_id()
	ans = Answer(ans_id, ans_type, ans_seed, ans_deg, ans_str, bmseg.seg(ans_str))

	answers.append(ans)
	return ans

def ans_new_and_match_que(que_id, ans_str, ans_type=2, ans_seed=-1, ans_deg=0, score=10):
	global answers, questions, ans2ques, ids

	ans = ans_new(ans_str, ans_type, ans_seed, ans_deg)

	match = False
	for ans2que in ans2ques:
		if ans2que.que_id==que_id:
			ans2que.ans_ids.append({'id' : ans.id, 'score' : score})
			match = True
			break
	if not match:
		ans2ques.append(Ans2Que(que_id, [{'id' : ans.id, 'score' : score}, ]))

	# print('\n----------Debug---------\n')
	# for question in questions:
	# 	print('question : %s ' % question.toString())
	# for answer in answers:
	# 	print('answer : %s ' % answer.toString())
	# for ans2que in ans2ques:
	# 	print('ans2que : %s ' % ans2que.toString())
	# print('\n----------Debug---------\n')

def match_old_anss(que_new_id, que_old_id):
	global answers, questions, ans2ques, ids

	ans2que = Ans2Que.get_ans_by_que(ans2ques, que_old_id)

	if ans2que:
		ans2que_new = Ans2Que(que_new_id, copy.deepcopy(ans2que.ans_ids))
		ans2ques.append(ans2que_new)

	# print('\n----------Debug---------\n')
	# for question in questions:
	# 	print('question : %s ' % question.toString())
	# for answer in answers:
	# 	print('answer : %s ' % answer.toString())
	# for ans2que in ans2ques:
	# 	print('ans2que : %s ' % ans2que.toString())
	# print('\n----------Debug---------\n')

def change_score(que_id, ans_id, score):
	global answers, questions, ans2ques, ids

	if score!=0:
		for ans2que in ans2ques:
			if ans2que.que_id==que_id:
				print(ans2que.toString())
				for ans_score in ans2que.ans_ids:
					if ans_score['id']==ans_id:
						ans_score['score'] += score
						break
				break

	# print('\n----------Debug---------\n')
	# for question in questions:
	# 	print('question : %s ' % question.toString())
	# for answer in answers:
	# 	print('answer : %s ' % answer.toString())
	# for ans2que in ans2ques:
	# 	print('ans2que : %s ' % ans2que.toString())
	# print('\n----------Debug---------\n')

if __name__=='__main__':
	que, sim = match_question('吃了吗??')
	anss = get_ans_by_que(que)