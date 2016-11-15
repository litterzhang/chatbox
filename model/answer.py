#-*- coding:utf8 -*-

'问题模型'

__author__='litterzhang'

import json

# 答案定义
# id : 标识答案  
# type : 0 , 1 , 2。 0表示正向回答，1表示负向回答，2表示中立回答。  
# seed : 标识回答的中心。  
# deg : 标识回答的情绪程度
# content : 回答内容  
# words ： 回答关键词
class Answer(object):
	def __init__(self, _id, _type, _seed, _deg, _content, _words=[]):
		self.id = _id
		self.type = _type
		self.seed = _seed
		self.deg = _deg
		self.content = _content
		self.words = _words

	def answer2dict(answer):
		return {
			'id' : answer.id,
			'type' : answer.type,
			'seed' : answer.seed,
			'deg' : answer.deg,
			'content' : answer.content,
			'words' : answer.words
		}

	def toString(self):
		return {
			'id' : self.id,
			'type' : self.type,
			'seed' : self.seed,
			'deg' : self.deg,
			'content' : self.content,
			'words' : self.words
		}

	def dict2answer(dic):
		return Answer(dic['id'], int(dic['type']), int(dic['seed']), int(dic['deg']), dic['content'], _words=dic['words'])

	def load(fp):
		answers = list()
		with open(fp, 'r', encoding='utf-8') as fr:
			answers = json.load(fr, object_hook=Answer.dict2answer)
		return answers

	def dump(answers, fp):
		with open(fp, 'w', encoding='utf-8') as fw:
			answers_json = json.dumps(answers, ensure_ascii=False, default=Answer.answer2dict)
			fw.write(answers_json)

	def get_ans_by_id(answers, _id):
		for answer in answers:
			if answer.id == _id:
				return answer
		return None