# -*- coding: utf-8 -*-

'Chat数据库'

__author__='litterzhang'

import os
import functools

from tinydb import TinyDB, Query

import ChatUtils
from WordSegment.segs import bmseg

answer_db = None
question_db = None
ans2que_db = None

# 返回结果类封装
class Result:
	def __init__(self, success=True, message=None, content=dict()):
		self.success = success
		self.message = message
		self.content = content

	def __str__(self):
		return str({'success' : self.success, 'message' : self.message, 'content' : self.content})

	__repr__ = __str__


# 检查数据库是否初始化
def check_db(func):
	global answer_db, question_db, ans2que_db

	@functools.wraps(func)
	def wrapper(*args, **kw):
		if answer_db==None or question_db==None or ans2que_db==None:
			return Result(success=False, message='数据库未初始化!')
		return func(*args, **kw)
	return wrapper

# 使用key数据化数据库
def init_db(key):
	global answer_db, question_db, ans2que_db
	
	ANSWER = os.path.join(os.path.dirname(__file__), 'data/answer_%s.json' % key)
	QUESTION = os.path.join(os.path.dirname(__file__), 'data/question_%s.json' % key)
	ANS2QUE = os.path.join(os.path.dirname(__file__), 'data/ans2que_%s.json' % key)

	answer_db = TinyDB(ANSWER)
	question_db = TinyDB(QUESTION)
	ans2que_db = TinyDB(ANS2QUE)

# 匹配问题
@check_db
def match_question(que_str):
	global answer_db, question_db, ans2que_db

	sim_max = -1
	que_res = None

	que_words = [list(x) for x in bmseg.seg(que_str)]
	que_words = list(filter(lambda x: x[2]!='bd', que_words))

	for que in question_db.all():
		sim = ChatUtils.sim_calc(que_words, que['words'])
		if sim > sim_max:
			sim_max = sim
			que_res = que

	if que_res:
		que_res['id'] = que_res.eid
	return Result(content=dict({'que' : que_res, 'sim' : sim_max}))

# 新建问题
@check_db
def create_question(que_str, que_type=2):
	global answer_db, question_db, ans2que_db
	que_id = question_db.insert({'type' : que_type, 'content' : que_str, 'words' : bmseg.seg(que_str)})

	return Result(success=True, content=dict({'que' : {'id' : que_id, 'type' : que_type, 'content' : que_str, 'words' : bmseg.seg(que_str)}}))

# 新建答案
@check_db
def create_answer(ans_str, ans_type=2, ans_seed=-1, ans_deg=0):
	global answer_db, question_db, ans2que_db
	ans_id = answer_db.insert({'type' : ans_type, 'seed' : ans_seed, 'deg' : ans_deg, 'content' : ans_str, 'words' : bmseg.seg(ans_str)})

	return Result(success=True, content=dict({'id' : ans_id}))

# 更新问题-答案
@check_db
def create_ans2que(que_id, ans_id, score=10):
	global answer_db, question_db, ans2que_db
	
	X = Query()
	ans2que_db.remove((X.que_id==que_id) & (X.ans_id==ans_id))
	ans2que_id = ans2que_db.insert({'que_id' : que_id, 'ans_id' : ans_id, 'score' : score})
	return Result()

# 更新问题-答案
@check_db
def update_ans2que(que_id, ans_id, score=0):
	global answer_db, question_db, ans2que_db

	X = Query()
	ans2que_old = ans2que_db.get((X.que_id==que_id) & (X.ans_id==ans_id))
	if ans2que_old:
		ans2que_db.update({'score' : ans2que_old['score']+score}, (X.que_id==que_id) & (X.ans_id==ans_id))
	else:
		ans2que_db.insert({'que_id' : que_id, 'ans_id' : ans_id, 'score' : 10+score})

# 为问题添加答案
@check_db
def add_ans_for_que(que_id, ans_str, ans_type=2, ans_seed=-1, ans_deg=0, score=10):
	global answer_db, question_db, ans2que_db

	res = create_answer(ans_str, ans_type, ans_seed, ans_deg)
	if res.success:
		ans_id = res.content.get('id', -1)
		if ans_id == -1:
			return Result(success=False, message='新建答案失败')
		create_ans2que(que_id, ans_id, score)
		return Result()
	else:
		return Result(success=False, message='新建答案失败')

# 根据问题查找答案
@check_db
def get_ans2que_by_que(que_id):
	global answer_db, question_db, ans2que_db

	X = Query()
	ans2ques = ans2que_db.search(X.que_id==que_id)
	return Result(content=dict({'ans2ques' : ans2ques}))

# 为问题匹配旧答案
@check_db
def match_old_anss(que_new_id, que_old_id):
	global answer_db, question_db, ans2que_db

	res = get_ans2que_by_que(que_old_id)

	if res.success:
		ans2ques = res.content.get('ans2ques', None)
		if ans2ques:
			for ans2que in ans2ques:
				ans2que_db.insert({'que_id' : que_new_id, 'ans_id' : ans2que['ans_id'], 'score' : ans2que['score']})
	return Result()

# 根据问题查找答案
def get_answers_by_que(que_id):
	global answer_db, question_db, ans2que_db

	answers = list()

	X = Query()
	ans2ques = ans2que_db.search(X.que_id==que_id)
	for ans2que in ans2ques:
		ans_id = ans2que['ans_id']
		ans_score = ans2que['score']

		ans = answer_db.get(eid=ans_id)

		ans['id'] = ans_id
		answers.append({'ans' : ans, 'score' : ans_score})
	return Result(content=dict({'answers' : answers}))

# 根据问题匹配答案
def get_answers(que_str):
	global answer_db, question_db, ans2que_db

	res = match_question(que_str)
	if res.success:
		que = res.content.get('que', None)
		sim = res.content.get('sim', -1)

		if not que:
			return Result(success=False, message='未能匹配到问题！')
		res_anss = get_answers_by_que(que.eid)
		anss = list()
		if res_anss.success:
			anss = res_anss.content.get('answers', list())

		que['id'] = que.eid
		return Result(content=dict({'que' : que, 'sim' : sim, 'anss' : anss}))
	else:
		return Result(success=False, message='未能匹配到问题！')