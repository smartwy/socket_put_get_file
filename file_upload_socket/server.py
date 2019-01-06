#!/usr/bin/python3
# -*- coding:utf-8 -*-
#Name:     
#Descripton:
#Author:    smartwy
#Date:     
#Version:

from socket import *
import os

Basedir = 'E:\\python_project_dir\\python_test\\练习文件\\file_upload_socket\\server_file\\'

def send_file(csock, filename):
	fp = os.path.join(Basedir, filename)
	if not os.path.exists(fp):
		csock.send("error".encode('utf-8'))
	else:
		f_size = os.path.getsize(fp)
		csock.send(str(f_size).encode('utf-8'))
		with open(fp, 'rb') as f:
			print('start send file size is {}'.format(f_size))
			r_data = bytes()
			while True:
				data = f.read(4096)
				r_data += data
				if len(r_data) == int(f_size):
					csock.send(r_data)
					print('\033[31mSend file ok !\033[0m')
					return

	return

def recv_file(csock, filename):
	fp = os.path.join(Basedir, filename)
	csock.send('start_upload'.encode('utf-8'))
	fsize = csock.recv(1024)
	sumsize = fsize.decode('utf-8')
	if len(sumsize) > 0:
		with open(fp, 'wb') as f:
			print('start save file :', fp)
			r_data = bytes()
			while True:
				# print(sumsize)
				ndata = csock.recv(4096)
				r_data += ndata
				# print(r_data)
				if len(r_data) == int(sumsize):
					f.write(r_data)
					print('save file ok')
					break
	return

def sls_fun():
	list_data = os.listdir(Basedir)
	return list_data
def accept_write(ssock):
	csockfd, addres = ssock.accept()
	print('connect client \033[31m{}\033[0m...'.format(addres))
	while True:
		data = csockfd.recv(1024)
		ndata = data.decode('utf-8')
		ndata = ndata.split()
		# print(ndata,type(ndata))
		if ndata[0] == 'close':
			break
		elif ndata[0] == 'sls':
			list2 = sls_fun()
			csockfd.send(str(list2).encode('utf-8'))
		elif ndata[0] == 'put':
			recv_file(csockfd, ndata[1])
		elif ndata[0] == 'get':
			send_file(csockfd, ndata[1])
		else:
			break

if __name__ == '__main__':
	sock = socket(AF_INET, SOCK_STREAM)
	sock.bind(('192.168.10.241', 8008))
	sock.listen(5)
	print('waiting connect ...')
	accept_write(sock)




