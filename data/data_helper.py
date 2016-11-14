#-*- coding:utf8 -*-

'处理问题、回答、问题-回答'

__author__='litterzhang'

import os
import json

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))

from WordSegment.segs import bmseg

ANSWER = os.path.join(os.path.dirname(__file__), 'answer.json')
QUESTION = os.path.join(os.path.dirname(__file__), 'question.json')
ANS2OQUE = os.path.join(os.path.dirname(__file__), 'ans2que.json')

def ParseAnswer(fp):
	answers = list()
	if os.path.exists(ANSWER):
		with open(ANSWER, 'r', encoding='utf-8') as fr:
			answers = json.load(fr)

	with open(fp, 'r', encoding='utf-8') as fr:
		for line in fr:
			line_s = line.strip().split()

			ans = {
				'id' : line_s[0],
				'type' : line_s[1],
				'seed' : line_s[2],
				'deg' : line_s[3],
				'content' : line_s[4:],
				'words' : bmseg.seg(' '.join(line_s[4:]))
			}

			index = -1
			for i in range(0, len(answers)):
				if ans['content'] == answers[i]['content'] and ans['id'] == answers[i]['id']:
					index = i
					break
			if index != -1:
				answers[index] = ans
			else:
				answers.append(ans)
	if answers:
		with open(ANSWER, 'w', encoding='utf-8') as fw:
			fw.write(json.dumps(answers, ensure_ascii=False))

def ParseQuestion(fp):
	questions = list()
	if os.path.exists(QUESTION):
		with open(QUESTION, 'r', encoding='utf-8') as fr:
			questions = json.load(fr)

	with open(fp, 'r', encoding='utf-8') as fr:
		for line in fr:
			line_s = line.strip().split()
			que = {
				'id' : line_s[0],
				'type' : line_s[1],
				'content' : line_s[2:],
				'words' : bmseg.seg(' '.join(line_s[2:]))
			}

			index = -1
			for i in range(0, len(questions)):
				if que['content'] == questions[i]['content'] and que['id'] == questions[i]['id']:
					index = i
					break
			if index != -1:
				questions[index] = que
			else:
				questions.append(que)

	if questions:
		with open(QUESTION, 'w', encoding='utf-8') as fw:
			fw.write(json.dumps(questions, ensure_ascii=False))

def ParseAns2Que(fp):
	ans2ques = list()
	if os.path.exists(ANS2OQUE):
		with open(ANS2OQUE, 'r', encoding='utf-8') as fr:
			ans2ques = json.load(fr)

	with open(fp, 'r', encoding='utf-8') as fr:
		for line in fr:
			line_s = line.strip().split()
			ans2que = {
				'que_id' : line_s[0],
				'ans_ids' : line_s[1:],
			}

			index = -1
			for i in range(0, len(ans2ques)):
				if ans2que['que_id'] == ans2ques[i]['que_id']:
					index = i
					break
			if index != -1:
				ans2ques[index]['ans_ids'].extend(ans2que['ans_ids'])
				ans2ques[index]['ans_ids'] = list(set(ans2ques[index]['ans_ids']))
			else:
				ans2ques.append(ans2que)
	if ans2ques:
		with open(ANS2OQUE, 'w', encoding='utf-8') as fw:
			fw.write(json.dumps(ans2ques, ensure_ascii=False))

if __name__=='__main__':
	ParseAnswer(os.path.join(os.path.dirname(__file__), 'answer'))
	ParseQuestion(os.path.join(os.path.dirname(__file__), 'question'))
	ParseAns2Que(os.path.join(os.path.dirname(__file__), 'ans2que'))

