# -*- coding: utf-8 -*-

'用于控制对话的进行'

__author__='litterzhang'

import chatdb
import random

# 获取最佳答案
def best_ans(que, sim, anss, coms):
	i = random.randint(0, len(anss)-1)
	return anss[i]

# 聊天
def chat():
	coms = list()

	# 这里进行打招呼，暂时省略

	# 开始问答
	while True:
		que_str = input()
		
		if que_str=='end':
			break

		que, sim, anss = chatdb.get_answer(que_str)
		ans = best_ans(que, sim, anss, coms)

		print(sim)
		print(ans.content)

		# 记录回答
		coms.append({
			'que_str' : que_str,
			'que' : que,
			'que_sim' : sim,
			'ans' : ans
		})

if __name__=='__main__':
	chat()