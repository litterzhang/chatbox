# -*- coding: utf-8 -*-

'双向最大匹配算法'

__author__='litterzhang'

import os
import re

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))

from utils import load_dict
from functools import reduce

# 分词标准流程
def seg(sen_str, dict_load=None, word_max=5):
	# 加载词典
	if not dict_load:
		dict_path = os.path.join(os.path.dirname(__file__), '../dict/dict_small.txt')
		dict_load = load_dict(dict_path)

	# 处理标点符号，根据标点符号，将句子分割为多个子句
	punc = ' ~!@#$%^&*()_+-=[]{}|\\\'\";:?/.>,<~！@#￥%……&（）|【】、‘“”’：；？。》《，'
	r = re.compile(r'[\s{}]+'.format(re.escape(punc)))
	sen_sub_strs = r.split(sen_str)

	# 词袋
	words = list()
	sen_proc_len = 0

	# 对每个子句分词
	for sen_sub_str in sen_sub_strs:
		words_mm = mmseg(sen_sub_str, dict_load=dict_load, word_max=word_max)
		words_rmm = rmmseg(sen_sub_str, dict_load=dict_load, word_max=word_max)

		if len(words_mm)>len(words_rmm):
			words.extend(words_rmm[::-1])
		elif len(words_rmm)>len(words_mm):
			words.extend(words_mm)
		else:
			dis_mm = len(list(filter(lambda x: x[2]=='wz', words_mm)))
			dis_rmm = len(list(filter(lambda x: x[2]=='wz', words_rmm)))

			if dis_mm > dis_rmm:
				words.extend(words_rmm[::-1])
			elif dis_rmm > dis_mm:
				words.extend(words_mm)
			else:
				cnt_mm = reduce(lambda x, y: len(y[2])**2+x, words_mm, 0)
				cnt_rmm = reduce(lambda x, y: len(y[2])**2+x, words_rmm, 0)

				if cnt_mm > cnt_rmm:
					words.extend(words_mm)
				else:
					words.extend(words_rmm[::-1])

		# 将标点加入分词结果
		sen_proc_len += len(sen_sub_str)
		while sen_proc_len<len(sen_str) and sen_str[sen_proc_len] in punc:
			words.append((sen_str[sen_proc_len], '0', 'bd'))
			sen_proc_len += 1
	return words


# 正向最大匹配算法
def mmseg(sen_str, dict_load=None, word_max=5):
	# 词袋
	words = list()

	# 处理每个字据	
	while sen_str:
		cut_tmp = sen_str[:word_max]
		cut_tmp_len = len(cut_tmp)

		while cut_tmp:
			if cut_tmp in dict_load:
				# 加入word
				words.append((cut_tmp, dict_load[cut_tmp][0], dict_load[cut_tmp][1]))
				sen_str = sen_str[cut_tmp_len:]
				break

			if cut_tmp_len==1:
				words.append((cut_tmp, 0, 'wz'))
				sen_str = sen_str[cut_tmp_len:]
				break

			cut_tmp = cut_tmp[:-1]
			cut_tmp_len -= 1
	return words

# 正向最大匹配算法
def rmmseg(sen_str, dict_load=None, word_max=5):
	# 词袋
	words = list()

	# 处理每个字据	
	while sen_str:
		cut_tmp = sen_str[-word_max:]
		cut_tmp_len = len(cut_tmp)

		while cut_tmp:
			if cut_tmp in dict_load:
				# 加入word
				words.append((cut_tmp, dict_load[cut_tmp][0], dict_load[cut_tmp][1]))
				sen_str = sen_str[:-cut_tmp_len]
				break

			if cut_tmp_len==1:
				words.append((cut_tmp, 0, 'wz'))
				sen_str = sen_str[:-cut_tmp_len]
				break

			cut_tmp = cut_tmp[1:]
			cut_tmp_len -= 1
	return words

if __name__=='__main__':
	print(seg('长春市长春药店'))
