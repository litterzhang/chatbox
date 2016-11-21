# -*- coding: utf-8 -*-

'web入口'

__author__='litterzhang'

import tornado.ioloop
import tornado.web

from settings import *

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))
import chatdb

import functools

class BaseHandler(tornado.web.RequestHandler):
	def initialize(self):
		self.name = None
		self.sim_new = sim_new_defalut
		self.sim_old = sim_old_defalut

def check_login(func):
	@functools.wraps(func)
	def wrapper(self):
		if not self.get_secure_cookie('name'):
			self.redirect('/login')
			return
		else:
			self.name = self.get_secure_cookie('name')
			if self.get_secure_cookie('sim_new'):
				self.sim_new = tofloat(self.get_secure_cookie('sim_new'), default=sim_new_defalut)
			if self.get_secure_cookie('sim_old'):
				self.sim_old = tofloat(self.get_secure_cookie('sim_old'), default=sim_old_defalut)
		return func(self)
	return wrapper

def check_not_login(func):
	@functools.wraps(func)
	def wrapper(self):
		if self.name or self.get_secure_cookie('name'):
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

class MainHandler(BaseHandler):
	@check_login
	def get(self):
		self.render('index.html', name=self.name, sim_new=self.sim_new, sim_old=self.sim_old)

class LoginHandler(BaseHandler):
	@check_not_login
	def get(self):
		self.render('login.html')

	@check_not_login
	def post(self):
		if self.get_argument('name'):
			self.set_secure_cookie('name', self.get_argument('name'))
			self.name = self.get_argument('name')
		if self.get_argument('sim_new'):
			self.set_secure_cookie('sim_new', self.get_argument('sim_new'))
			self.sim_new = tofloat(self.get_argument('sim_new'), default=sim_new_defalut)
		if self.get_argument('sim_old'):
			self.set_secure_cookie('sim_old', self.get_argument('sim_old'))
			self.sim_old = tofloat(self.get_argument('sim_old'), default=sim_old_defalut)

		chatdb.init_db(self.name)
		self.redirect('/')

class LogoutHandler(BaseHandler):
	@check_login
	def get(self):
		self.name = None
		self.sim_new = sim_new_defalut
		self.sim_old = sim_old_defalut
		self.set_secure_cookie('name', '')
		self.set_secure_cookie('sim_new', '')
		self.set_secure_cookie('sim_old', '')

		self.redirect('/login')

class QuestionHandler(BaseHandler):
	@check_login
	def post(self):
		
		
if __name__=='__main__':
    application = tornado.web.Application([
        (r'/', MainHandler),
        (r'/login', LoginHandler),
        (r'/logout', LogoutHandler),
        (r'/question', QuestionHandler)
    ], **app_settings)

    application.listen(3000)
    tornado.ioloop.IOLoop.current().start()