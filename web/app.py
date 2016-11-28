# -*- coding: utf-8 -*-

'web入口'

__author__='litterzhang'

import tornado.ioloop
import tornado.web

from settings import *

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))
from chatjsonctl import Chat

import functools

chats = dict()

class BaseHandler(tornado.web.RequestHandler):
	@property
	def name(self):
		name_cookie = self.get_secure_cookie('name')
		name = None
		if name_cookie:
			name = bytes.decode(self.get_secure_cookie('name'))
		return name

	@property
	def chat(self):
		global chats

		chat = chats.get(self.name, None)
		if chat:
			chat = chat['chat']
		return chat

def check_login(func):
	@functools.wraps(func)
	def wrapper(self):
		if not self.name or not self.chat:
			self.redirect('/login')
			return
		return func(self)
	return wrapper

def check_not_login(func):
	@functools.wraps(func)
	def wrapper(self):
		if self.name:
			self.redirect('/')
			return
		return func(self)
	return wrapper


def tofloat(float_str, default=0):
	res = default
	try:
		res = float(float_str)
	except:
		pass
	return res

def toint(int_str, default=0):
	res = default
	try:
		res = int(int_str)
	except:
		pass
	return res

class MainHandler(BaseHandler):
	@check_login
	def get(self):
		global chats

		self.render('que_ask.html', chat=self.chat)

class LoginHandler(BaseHandler):
	@check_not_login
	def get(self):
		self.render('login.html')

	@check_not_login
	def post(self):
		global chats

		if self.get_argument('name'):
			self.set_secure_cookie('name', self.get_argument('name'))

			name = self.get_argument('name')
			sim_new = tofloat(self.get_argument('sim_new'), default=sim_new_defalut)
			sim_old = tofloat(self.get_argument('sim_old'), default=sim_old_defalut)
			chats[name] = {'name' : name, 'chat' : Chat(name, sim_new, sim_old)}

			self.redirect('/')
		else:
			self.redirect('/login')

class LogoutHandler(BaseHandler):
	@check_login
	def get(self):
		global chats

		del chats[self.name]['chat']
		del chats[self.name]

		self.set_secure_cookie('name', '')
		
		self.redirect('/login')

class QuestionAskHandler(BaseHandler):
	@check_login
	def post(self):
		if self.get_argument('que_content'):
			que, sim, anss = Chat.match_question(self.get_argument('que_content'))
			if not que or sim < self.chat.sim_new:
				self.render('que_add.html', chat=self.chat, que_content=self.get_argument('que_content'))
			else:
				self.chat.coms_add_que(self.get_argument('que_content'), que, sim)
				ans, score = self.chat.chat_ctl_answer(que, sim, anss)
				self.chat.coms_add_ans(ans, score)

				self.render('ans_add.html', chat=self.chat, que_id=que['id'])
		else:
			self.redirect('/')

class QuestionAddHandler(BaseHandler):
	@check_login
	def post(self):
		if self.get_argument('que_content'):
			que_type = toint(self.get_argument('que_type'), default=2)
			que, sim, anss = Chat.match_question(self.get_argument('que_content'))
			que, sim, anss = self.chat.chat_ctl_question(self.get_argument('que_content'), que, sim, anss, que_type)
			self.chat.coms_add_que(self.get_argument('que_content'), que, sim)
			ans, score = self.chat.chat_ctl_answer(que, sim, anss)
			self.chat.coms_add_ans(ans, score)

			print(que)
			self.render('ans_add.html', chat=self.chat, que_id=que['id'])
		else:
			self.redirect('/')

class AnswerAddHandler(BaseHandler):
	@check_login
	def post(self):
		if self.get_argument('que_id') and self.get_argument('ans_content'):
			que_id = toint(self.get_argument('que_id'))
			ans_content = self.get_argument('ans_content')
			ans_type = toint(self.get_argument('ans_type'), default=2)
			# ans_seed = toint(self.get_argument('ans_seed'), default=-1)
			ans_seed = -1
			ans_deg = toint(self.get_argument('ans_deg'), default=0)
			ans_score = toint(self.get_argument('ans_score'), default=10)

			Chat.add_answer(que_id, ans_content, ans_type, ans_seed, ans_deg, ans_score)
			print(que_id)
			
			self.render('ans_add.html', chat=self.chat, que_id=que_id)
		else:
			self.redirect('/')

if __name__=='__main__':
    application = tornado.web.Application([
        (r'/', MainHandler),
        (r'/login', LoginHandler),
        (r'/logout', LogoutHandler),
        (r'/que_ask', QuestionAskHandler),
        (r'/que_add', QuestionAddHandler),
        (r'/ans_add', AnswerAddHandler),
    ], **app_settings)

    application.listen(3000)
    tornado.ioloop.IOLoop.current().start()