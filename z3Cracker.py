#!/usr/bin/python
######################################################################
#
# Copyright (C) 2015
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
######################################################################
import sys
import struct
import string
from z3 import *
########### Functions Def
def Usage():
	print "###############################################################"
	print "Get password by z3!"
	# Please don't remove this. At least respect my rights!
	print "Auther: Lambda"
	print "Usage: {} <ciphertext> <password_len>".format(sys.argv[0])
	print "  ciphertext: password string that has been hashed "
	print "  password_len: a number between 8 to 40."
	print "Examples: "
	print "  {} bRbQyzcy9b 8".format(sys.argv[0])
	print "  {} bbddRdzb9 22".format(sys.argv[0])
	print "  {} cdcS9bcQc 8".format(sys.argv[0])
	print "  {} See9cb9y99 9".format(sys.argv[0])
	print "Special thanks to: Qing Chang,w-y"
	print "###############################################################"
	sys.exit(0)
def display_model(m):
	block = {}
	for x in m:
		if 'in' in str(x):
			block[int(str(x)[2:])] = int(str(m[x]))
	password = ''.join(map(chr, block.values()))
	print "find password: "+password
def get_models(F):
	s = Solver()
	s.add(F)
	while True:
		if s.check() == sat:
			m = s.model()
			display_model(m)
			block = []
			for d in m:
				if d.arity() > 0:
					raise Z3Exception("uninterpreted functions are not suppported")
				c = d()
				if is_array(c) or c.sort().kind() == Z3_UNINTERPRETED_SORT:
					raise Z3Exception("arrays and uninterpreted sorts are not supported")
				block.append(c != m[d])
			s.add(Or(block))
		else:
			print 'finish! if no result,please input other password_len'
			break
def strmap(cipstr):
	temp=[]
	dic={'R':'1','S':'2','b':'3','c':'4','d':'5','e':'6','y':'7','z':'8','9':'9','Q':'0'}
	for ch in cipstr:
		if ch in dic:
			temp.append(dic[ch])
		else:
			print "invalid ciphertext!:ciphertext can olny contain characters in {}".format(dic.keys())
			sys.exit(0)	
	return int(''.join(temp))
##################################################################### Main Start Here
if len(sys.argv) !=3 or sys.argv[1]=="-h":
	Usage()
password_len = sys.argv[2]
if int(password_len)< 8 or int(password_len)> 40:
	print "invalid password_len!:password_len must between 8 to 40"
	sys.exit(0)
out_num = strmap(sys.argv[1])
objs=[]
for i in range(int(password_len)):
	objs.append(BitVec("in"+str(i),64))
magic = BitVec('magic',64)
passwdInt = BitVec('passwdInt',64)	
F = [
	magic == 31695317,
	reduce(lambda x,y:And(x,y), map(lambda x: And(x >= ord('!'), x <= ord('~')) ,objs)),
	passwdInt == reduce(lambda x,y: x+y, map(lambda (n,x): ((x * (n+1))^(n+1)), enumerate(objs))),
	( (passwdInt * magic) & 0xffffffff) == out_num,
]
get_models(F)
