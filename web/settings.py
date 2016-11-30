# -*- coding: utf-8 -*-

'web 配置'

__author__='litterzhang'

import os

app_settings = {
	'cookie_secret' : 'litterzhang',
	'login_url' : '/login',
	'xsrf_cookies' : False,
	'template_path' : os.path.join(os.path.dirname(__file__), 'templates'),
	'static_path' : os.path.join(os.path.dirname(__file__), 'static') 
}

sim_new_defalut = 0.7
sim_old_defalut = 0.2