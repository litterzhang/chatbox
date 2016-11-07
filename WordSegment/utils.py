# -*- coding: utf-8 -*-

'分词中用到的通用方法'

__author__='litterzhang'

# 加载词典
# 返回dict
def load_dict(fp, encoding='utf-8'):
	# 使用dict保存詞典信息
	dict_load = dict()

	# 打开文件
	with open(fp, 'r', encoding=encoding) as fr:
		for line in fr:
			word_inf = line.strip().split()
			word_inf_len = len(word_inf)

			if word_inf_len is 1:
				dict_load[word_inf[0]] = (0, 'wz')
			elif word_inf_len is 2:
				try:
					dict_load[word_inf[0]] = (int(word_inf[1]), 'wz')
				except:
					dict_load[word_inf[0]] = (0, word_inf[1])
			elif word_inf_len > 2:
				try:
					dict_load[word_inf[0]] = (int(word_inf[1]), word_inf[2])
				except:
					dict_load[word_inf[0]] = (0, word_inf[1])
			else:
				pass
	return dict_load

# hash表结构定义
class hash_dict:
	def __init__(self, dict_len=1000000):
		# 1000为最小长度
		dict_len = 1000 if dict_len < 1000 else dict_len
		self.dict_len = dict_len
		self.hash_list = [None for i in range(dict_len)]

	# 增加值
	def add(self, key, value):
		# 获取key的hash值
		hash_key = hash(key) & 0x7FFFFFFF
		hash_key_list = hash_key%self.dict_len

		if not self.hash_list[hash_key_list]:
			self.hash_list[hash_key_list] = (hash_key, key, value, None)
		else:
			tmp = self.hash_list[hash_key_list]
			self.hash_list[hash_key_list] = (hash_key, key, value, tmp)

	# 查询值
	def get(self, key):
		# 获取key的hash值
		hash_key = hash(key) & 0x7FFFFFFF
		hash_key_list = hash_key%self.dict_len

		tmp = self.hash_list[hash_key_list]
		while tmp:
			if tmp[0] == hash_key:
				return tmp[2]
			tmp = tmp[3]
		return None

	# 删除值
	def remove(self, key):
		# 获取key的hash值
		hash_key = hash(key) & 0x7FFFFFFF
		hash_key_list = hash_key%self.dict_len

		tmp = self.hash_list[hash_key_list]
		new_head = None
		new_now = None
		while tmp:
			if tmp[0] != hash_key:
				if not new_head:

					new_head = tmp
					new_now = new_head
				else:
					new_now[3] = tmp
					new_now = new_now[3]
			tmp = tmp[3]
		if new_now:
			new_now[3] = None

		self.hash_list[hash_key_list] = new_head

# 加载字典
# 返回hash表
def load_dict_hash(fp, encoding='utf-8'):
	# 使用hash表存储词典信息
	dict_load = hash_dict()

	# 打开文件
	with open(fp, 'r', encoding=encoding) as fr:
		for line in fr:
			word_inf = line.strip().split()
			word_inf_len = len(word_inf)

			if word_inf_len is 1:
				dict_load.add(word_inf[0], (0, 'wz'))
			elif word_inf_len is 2:
				try:
					dict_load.add(word_inf[0], (int(word_inf[1]), 'wz'))
				except:
					dict_load.add(word_inf[0], (0, word_inf[1]))
			elif word_inf_len > 2:
				try:
					dict_load.add(word_inf[0], (int(word_inf[1]), word_inf[2]))
				except:
					dict_load.add(word_inf[0], (0, word_inf[1]))
			else:
				pass
	return dict_load

# 测试
if __name__=='__main__':
	import time
	s = time.time()
	d = load_dict_hash('./dict/dict_small.txt')
	with open('./dict/dict_small.txt', 'r', encoding='utf-8') as fr:
		for line in fr:
			d.get(line.strip().split()[0])
	e = time.time()
	print(e-s)

	s = time.time()
	d = load_dict('./dict/dict_small.txt')
	with open('./dict/dict_small.txt', 'r', encoding='utf-8') as fr:
		for line in fr:
			d.get(line.strip().split()[0])
	e = time.time()
	print(e-s)

