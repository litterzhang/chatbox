# -*- coding: utf-8 -*-

'用于控制对话的进行'

__author__='litterzhang'

import chatdb
import random
import ChatUtils

# 获取最佳答案
def best_ans(que_str, que, sim, anss, coms):

	ans = ChatUtils.default_ans()
	score = 0
	
	if sim < 0.2:
		ans = ChatUtils.blur_ans()
	else:
		# 查找之前相同的问题
		times = 0
		last_ans = None
		for com in coms:
			if com['que_sim']>=0.2 and que.id==com['que'].id:
				times += 1
				last_ans = com['ans']

		# 匹配固定的回答
		if que.type==0:
			ans_seed = -1
			ans_type = -1
			if last_ans:
				ans_seed = last_ans.seed
				ans_type = last_ans.type
			ans, score = ChatUtils.search_ans(anss, times=times, ans_seed=ans_seed, ans_type=ans_type)
		elif que.type==1:
			ans, score = ChatUtils.search_ans(anss, times=times)
		else:
			ans, score = ChatUtils.search_ans(anss, times=times)		

	# 记录本次回答
	coms.append({
		'que_str' : que_str,
		'que' : que,
		'que_sim' : sim,
		'ans' : ans,
		'ans_score' : score
	})

	return ans, score

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

# 新增1或n个答案
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
		
		chatdb.ans_new_and_match_que(que_id, ans_str, ans_type, ans_seed, ans_deg, ans_score)

# 聊天从这里开始————训练模式
def chat():
	# 记录对话的进行
	coms = list()
	
	# 这里开始对话，初始化对话问答库
	man_name = input('What\'s your name? ')

	# 这里输入新建问题相似度阈值，及匹配旧问题相似度阈值
	sim_new = input_float('新问题阈值sim_new ? ', default=0.7)
	sim_old = input_float('旧问题阈值sim_old ? ', default=0.2)
	
	# 加载问答库	
	chatdb.init_db(man_name)

	print('----------开始问答----------\n')

	# 开始问答
	while True:
		que_str = input('--------------------\nMr. %s: ' % man_name)
		
		if que_str=='end':
			chatdb.save_db(man_name)
			break

		# 进行问题匹配
		que, sim, anss = chatdb.get_answer(que_str)

		# 创建新问题
		if sim < sim_new:
			# 输入新问题类型
			que_new_type = input_int(input_tip='\n这是一个新问题输入问题类型新问题类型: ', default=2)
			que_new = chatdb.que_new(que_str, que_new_type)
			
			# 匹配旧问题答案
			if sim > sim_old:
				chatdb.match_old_anss(que_new.id, que.id)
			else:
				anss = list()
			que = que_new
			sim = 1.0

		#这里进行答案匹配
		ans, score = best_ans(que_str, que, sim, anss, coms)
		print('Mr. Bot: %s' % ans.content)
		print('Answer type : %s\nAnswer seed : %s\nAnswer deg : %s\nAnswer score : %s\n' % (ans.type, ans.seed, ans.deg, score))
		
		# 默认答案，要求新增1或n个答案
		if ans.id <= 0:
			create_anss(que.id)
		else:
			# 打分
			ans_score = input_int(input_tip='给答案打分 : ', default=0)
			chatdb.change_score(que.id, ans.id, ans_score)

			create_anss(que.id)

		print('--------------------\n')

if __name__=='__main__':
	chat()