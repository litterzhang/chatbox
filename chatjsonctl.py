# -*- coding: utf-8 -*-

'用于控制对话的进行'

__author__='litterzhang'

import os
import datetime
import json

import chatjsondb
import ChatUtils

name = None
sim_new = 0.7
sim_old = 0.2

coms = None

# 初始化对话
def init_chat(_name, _sim_new=0.7, _sim_old=0.2):
	global name, sim_new, sim_old, coms

	name = _name
	sim_new = _sim_new
	sim_old = _sim_old

	chatjsondb.init_db(name)

	coms = list()

# 结束对话
def stop_chat():
	global name, sim_new, sim_old, coms

	COMS = os.path.join(os.path.dirname(__file__), 'coms')
	with open(os.path.join(COMS, '%s_%s' % (name, datetime.datetime.now().strftime("%Y%m%d %H%M%S"))), 'w', encoding='utf-8') as fw:
		coms_str = json.dumps(coms, ensure_ascii=False)
		fw.write(coms_str)

# 创建新的问题
def create_question(que_str, que_type=2):
	res = chatjsondb.create_question(que_str, que_type=que_type)
	if res.success:
		que = res.content.get('que', None)
		que_id = res.content.get('id', -1)

		if que:
			que['id'] = que_id
		return que
	else:
		return None

# 匹配问题
def match_question(que_str):
	res = chatjsondb.get_answers(que_str)

	que = None
	sim = -1
	anss = list()
	if res.success:
		que = res.content.get('que', None)
		sim = res.content.get('sim', -1)
		anss = res.content.get('anss', list())

	return que, sim, anss

# 进行问题控制
def chat_ctl_question(que_str, que, sim, anss, que_type=2):
	global name, sim_new, sim_old, coms
	
	que_new = create_question(que_str, que_type)

	if que and sim > sim_old:
		chatjsondb.match_old_anss(que_new['id'], que['id'])
	else:
		anss = list()
	que = que_new
	sim = 1
	return que, sim, anss

# 进行回答控制
def chat_ctl_answer(que, sim, anss):
	global name, sim_new, sim_old, coms

	ans = ChatUtils.default_ans_json()
	score = 0
	
	if sim < 0.2:
		ans = ChatUtils.blur_ans_json()
	else:
		# 查找之前相同的问题
		times = 0
		last_ans = None
		for com in coms:
			if com['que_sim']>=0.2 and que['id']==com['que']['id']:
				times += 1
				last_ans = com['ans']

		# 匹配固定的回答
		if que['type']==0:
			ans_seed = -1
			ans_type = -1
			if last_ans:
				ans_seed = last_ans['seed']
				ans_type = last_ans['type']
			ans, score = ChatUtils.search_ans_json(anss, times=times, ans_seed=ans_seed, ans_type=ans_type)
		elif que['type']==1:
			ans, score = ChatUtils.search_ans_json(anss, times=times)
		else:
			ans, score = ChatUtils.search_ans_json(anss, times=times)		

	# 记录本次回答
	coms.append({
		'que' : que,
		'que_sim' : sim,
		'ans' : ans,
		'ans_score' : score
	})

	return ans, score

# 创建新的答案
def create_answer(ans_str, ans_type=2, ans_seed=-1, ans_deg=0):
	res = chatjsondb.create_answer(ans_str, ans_type, ans_seed, ans_deg)
	ans_id = -1
	if res.success:
		ans_id = res.content.get('id', -1)
	return ans_id

# 为问题创建答案
def add_answer(que_id, ans_str, ans_type=2, ans_seed=-1, ans_deg=0, score=10):
	res = chatjsondb.add_ans_for_que(que_id, ans_str, ans_type, ans_seed, ans_deg, score)
	return res.success

# 更改答案打分
def change_score(que_id, ans_id, score=0):
	chatjsondb.update_ans2que(que_id, ans_id, score)

# 输入int值
def input_int(input_tip='', default=0):
	res = default
	try:
		res = int(input(input_tip))
	except:
		pass
	return res

# 输入float值
def input_float(input_tip='', default=0.0):
	res = default
	try:
		res = float(input(input_tip))
	except:
		pass
	return res

# 添加答案
def create_anss(que_id):
	while True:
		print('添加答案，按回车退出\n')
		ans_str = input('新增答案内容 : ')
		if not ans_str:
			break
		ans_type = input_int(input_tip='答案类型 : ', default=2)
		ans_seed = input_int(input_tip='答案中心 : ', default=-1)
		ans_deg = input_int(input_tip='答案语气 : ', default=0)
		ans_score = input_int(input_tip='答案打分 : ', default=10)
		
		add_answer(que_id, ans_str, ans_type, ans_seed, ans_deg, ans_score)

# 训练模式
def chat_ex():
	# 这里开始对话，初始化对话问答库
	man_name = input('What\'s your name ? ')

	# 这里输入新建问题相似度阈值，及匹配旧问题相似度阈值
	sim_new = input_float('新问题阈值sim_new ? ', default=0.7)
	sim_old = input_float('旧问题阈值sim_old ? ', default=0.2)
	
	# 加载问答库	
	init_chat(man_name, sim_new, sim_old)

	print('----------开始问答----------\n')

	# 开始问答
	while True:
		que_str = input('--------------------\nMr. %s: ' % man_name)
		
		if que_str=='end':
			stop_chat()
			break

		# 进行问题匹配
		que, sim, anss = match_question(que_str)
		if not que or sim < sim_new:
			que_new_type = input_int(input_tip='\n这是一个新问题, 输入问题类型: ', default=2)

			que, sim, anss = chat_ctl_question(que_str, que, sim, anss, que_new_type)

		#这里进行答案匹配
		ans, score = chat_ctl_answer(que, sim, anss)

		print('Mr. Bot: %s\n' % ans['content'])
		print('Answer type : %s\nAnswer seed : %s\nAnswer deg : %s\nAnswer score : %s\n' % (ans['type'], ans['seed'], ans['deg'], score))
		
		if ans['id']<=0:
			create_anss(que['id'])
		else:
			ans_score = input_int(input_tip='给答案打分 : ', default=0)
			change_score(que['id'], ans['id'], ans_score)
			
			create_anss(que['id'])

# 对话模式
def chat():
	# 这里开始对话，初始化对话问答库
	man_name = input('What\'s your name ? ')
	
	# 加载问答库	
	init_chat(man_name)

	print('----------开始问答----------\n')

	# 开始问答
	while True:
		que_str = input('--------------------\nMr. %s: ' % man_name)
		
		if que_str=='end':
			stop_chat()
			break
		# 进行问题匹配
		que, sim, anss = match_question(que_str)
		#这里进行答案匹配
		ans, score = chat_ctl_answer(que, sim, anss)

		print('Mr. Bot: %s\n' % ans['content'])
		

if __name__=='__main__':
	chat()
	