#-*- coding:utf8 -*-

'回答模型'

__author__='litterzhang'

import json

# 问题定义
# id : 标识问题  
# type : 0 , 1 , 2。 0表示会话确定问题，在一次会话中，答案唯一；1表示会话发散问题，在一次会话中，答案可以有多种；2表示未知问题  
# content : 问题内容  
# words : 问题分词 
class Question(object):
	def __init__(self, _id, _type, _content, _words=[]):
		self.id = _id
		self.type = _type
		self.content = _content
		self.words = _words

	def question2dict(question):
		return {
			'id' : question.id,
			'type' : question.type,
			'content' : question.content,
			'words' : question.words
		}

	def dict2questiuon(dic):
		return Question(dic['id'], int(dic['type']), dic['content'], _words=dic['words'])

	def load(fp):
		questions = list()
		with open(fp, 'r', encoding='utf-8') as fr:
			questions = json.load(fr, object_hook=Question.dict2questiuon)
		return questions