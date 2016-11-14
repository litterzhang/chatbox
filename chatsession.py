# -*- coding: utf-8 -*-

'用于控制对话的进行'

__author__='litterzhang'

import chatdb
import random
import ChatUtils

# 获取最佳答案
def best_ans(que_str, coms):
	que, sim, anss = chatdb.get_answer(que_str)

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
		'ans' : ans
	})

	return ans, score

# 聊天从这里开始————训练模式
def chat():
	coms = list()
	# 这里进行打招呼，暂时省略
	man_name = input('What\'s your name? ')
	chatdb.init_db(man_name)

	# 开始问答
	while True:
		que_str = input('--------------------\nMr. %s: ' % man_name)
		
		if que_str=='end':
			break

		ans, score = best_ans(que_str, coms)

		print('Mr. Bot: %s' % ans.content)
		print('Answer type : %s\nAnswer seed : %s\nAnswer deg : %s\nAnswer score : %s\n--------------------\n' % (ans.type, ans.seed, ans.deg, score))

if __name__=='__main__':
	chat()