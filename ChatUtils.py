# -*- coding: utf-8 -*-

'辅助类'

__author__='litterzhang'

import random
from model.answer import Answer

# 模糊回答，先写死，之后写入文件，多种模糊回答
__blur_anss = [
	{
		'id' : 0,
		'type' : 0,
		'seed' : 0,
		'deg' : 0,
		'content' : '完全听不懂你在说什么~',
	},
	{
		'id' : 0,
		'type' : 0,
		'seed' : 0,
		'deg' : 0,
		'content' : '一脸懵逼~',
	},
	{
		'id' : 0,
		'type' : 0,
		'seed' : 0,
		'deg' : 0,
		'content' : '来啊！互相伤害啊！',
	},
	{
		'id' : 0,
		'type' : 0,
		'seed' : 0,
		'deg' : 0,
		'content' : '不明觉厉！！',
	},
]

# 默认回答
def default_ans():
	ans = Answer(-1, 0, 0, 0, '欢迎！小伙子们在火炉旁挤挤，留个位子出来~')
	return ans

# 计算相似度
def sim_calc(words_s, words_d):
	cnt_same = 0
	for word in words_s:
		if word in words_d:
			cnt_same += 1
	word_same = cnt_same/(len(words_s)+len(words_d)-cnt_same)

	return word_same

# 获取一个模糊回答
def blur_ans():
	index = random.randint(0, len(__blur_anss)-1)
	_ans = __blur_anss[index]
	ans = Answer(_ans.get('id', 0), _ans.get('type', 0), _ans.get('seed', 0), _ans.get('deg', 0), _ans.get('content', 'oh no！我的系统出故障了！'))
	return ans

# 搜索匹配的答案
def search_ans(anss, times=-1, ans_seed=-1, ans_type=-1):
	# 第一次回答问题，尝试打乱数组，达到随机回答的目的
	# if times==0:
	random.shuffle(anss)
	anss = sorted(anss, key=lambda x: x['ans'].deg)

	ans_res = default_ans
	for _ans in anss:
		ans = _ans['ans']
		if ans_seed==-1 and ans_type==-1:
			ans_res = ans
			if ans.deg>=times:
				break
		elif ans_seed==-1:
			if ans.type==ans_type:
				ans_res = ans
				if ans.deg>=times:
					break
		elif ans_type==-1:
			if ans.seed==ans_seed:
				ans_res = ans
				if ans.deg>=times:
					break
		else:
			if ans.type==ans_type and ans.seed==ans_seed:
				ans_res = ans
				if ans.deg>=times:
					break
	return ans_res