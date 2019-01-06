#!/usr/bin/python3
# -*- coding:utf-8 -*-
#Name:     
#Descripton:
#Author:    smartwy
#Date:     
#Version:


from socket import *
import os, time
Basedir = 'E:\\python_project_dir\\python_test\\练习文件\\file_upload_socket\\client_file\\'

def put_file(csock, filename, ncmd):
	file_path = os.path.join(Basedir, filename)
	if not os.path.exists(file_path):
		print('本地没有该文件！')
		return
	else:
		csock.send(ncmd.encode('utf-8'))
		result = csock.recv(1024)
		if result.decode('utf-8') == 'start_upload':
			f_size = os.path.getsize(file_path)
			csock.send(str(f_size).encode('utf-8'))
			with open(file_path, 'rb') as f:
				print('start put file...')
				r_data = bytes()
				while True:
					data = f.read(4096)
					r_data += data
					if len(r_data) == int(f_size):
						csock.send(r_data)
						print('put file ok {}'.format(len(r_data)))
						break
	return

def get_file(csock, filename, ncmd):
	csock.send(ncmd.encode('utf-8'))
	data = csock.recv(1024)
	if data.decode('utf-8') == 'error':
		print('file not found!')
	elif int(data.decode('utf-8')) > 0:
		sumsize = data.decode('utf-8')
		fp = os.path.join(Basedir, filename)
		print('start get file')
		with open(fp, 'wb') as f:
			rdata = bytes()
			while True:
				ndata = csock.recv(4096)
				rdata += ndata
				if len(rdata) == int(sumsize):
					f.write(rdata)
					print('\033[31mGet file ok !\033[0m')
					break
		return

def ls_fun():
	ls_data = os.listdir(Basedir)
	return ls_data
def conn_s(csock):
	csock.connect(('192.168.10.241', 8008))
	print('connect server ...')
	print("Please input command:")
	print("ls :列出客户端文件。")
	print("sls:列出服务端文件。")
	print("put fn:上传‘fn’文件。")
	print("get fn:下载‘fn’文件。")
	while True:
		ncmd = input('>>>')
		cmd = ncmd.split()
		if not cmd or cmd[0] == 'ls':
			list1 = ls_fun()
			print(list1)
		elif cmd[0] == 'sls':
			csock.send(cmd[0].encode('utf-8'))
			sdata = csock.recv(4096)
			print(sdata.decode('utf-8'))
		elif cmd[0] == 'put' and cmd[1]:
			put_file(csock, str(cmd[1]), ncmd)
		elif cmd[0] == 'get' and cmd[1]:
			get_file(csock, str(cmd[1]), ncmd)
		elif cmd[0] == 'del' and cmd[1]:
			csock.send(cmd[0].encode('utf-8'))
		elif cmd[0] == 'sdel' and cmd[1]:
			csock.send(cmd[0].encode('utf-8'))
		elif cmd[0] == 'close':
			csock.send(cmd[0].encode('utf-8'))
			break
		else:
			pass

if __name__ == '__main__':
	csock = socket(AF_INET, SOCK_STREAM)
	conn_s(csock)


