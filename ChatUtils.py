# -*- coding: utf-8 -*-

'辅助类'

__author__='litterzhang'

def sim_calc(words_s, words_d):
	cnt_same = 0
	for word in words_s:
		if word in words_d:
			cnt_same += 1
	word_same = cnt_same/(len(words_s)+len(words_d)-cnt_same)

	return word_same