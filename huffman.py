#!/usr/local/bin/python3
from bitarray import bitarray
import sys
import argparse
import shutil


def encode(input_file, output_file):
	print("encoding ", input_file, output_file)

	# open th file to read data
	f = open(input_file,"r")
	dic = {}
	arr = []
	data = []
	data_str = ""

	# read byte by byte data from file
	i = 0
	while 1:
		char_data = f.read(1)
		if not char_data:
			break
		if not char_data in arr:
			dic[char_data] = i
			i += 1
			arr.append(char_data)
		data.append(char_data)
	f.close()


	# convert byte data to minimum possible bits and get bit string and then save that bit file
	dd = list(dic.keys())
	mask = ['00000000', '0000000', '000000', '00000', '0000', '000', '00', '0', '']
	length_str = str(len(dic))
	if len(length_str) == 1:
		data_str += mask[len(str(bin(ord('0'))[2:]))] + str(bin(ord('0'))[2:])
		data_str += mask[len(str(bin(ord('0'))[2:]))] + str(bin(ord('0'))[2:])
		data_str += mask[len(str(bin(ord(length_str[0]))[2:]))] + str(bin(ord(length_str[0]))[2:])
	elif len(length_str) == 2:
		data_str += mask[len(str(bin(ord('0'))[2:]))] + str(bin(ord('0'))[2:])
		data_str += mask[len(str(bin(ord(length_str[0]))[2:]))] + str(bin(ord(length_str[0]))[2:])
		data_str += mask[len(str(bin(ord(length_str[1]))[2:]))] + str(bin(ord(length_str[1]))[2:])
	else:
		data_str += mask[len(str(bin(ord(length_str[0]))[2:]))] + str(bin(ord(length_str[0]))[2:])
		data_str += mask[len(str(bin(ord(length_str[1]))[2:]))] + str(bin(ord(length_str[1]))[2:])
		data_str += mask[len(str(bin(ord(length_str[2]))[2:]))] + str(bin(ord(length_str[2]))[2:])

	for i in range(len(dic)):
		data_str += mask[len(str(bin(ord(dd[i]))[2:]))] + str(bin(ord(dd[i]))[2:])
		data_str += mask[len(str(bin(dic[dd[i]])[2:])) + 1] + str(bin(dic[dd[i]])[2:])

	for i in range(len(data)):
		data_str += mask[len(str(bin(dic[data[i]])[2:])) + 1] + str(bin(dic[data[i]])[2:])

	a = bitarray(data_str)
	with open(output_file, 'wb') as f:
		a.tofile(f)


def decode(input_file, output_file):
	print("decoding ", input_file, output_file)

	decode_data = bitarray()
	with open(input_file, 'rb') as f:
		decode_data.fromfile(f)
	temp = list(decode_data)

	str_data = ""
	for i in temp:
		if i:
			str_data += '1'
		else:
			str_data += '0'

	dic = {}
	data = ""

	length = 0 
	for i in range(3):
		length = length*10 + int(chr(int(str_data[i*8:i*8+8],2)))
	print(length)
	str_data = str_data[24:]
	for i in range(length):
		dic[int(str_data[i*15+8:i*15+15],2)] = chr(int(str_data[i*15:i*15+8],2))
	str_data = str_data[length*15:]
	i = 0
	num = len(str_data)//7
	for i in range(num):
		data += dic[int(str_data[i*7:i*7+7],2)] 

	f = open(output_file,"w")
	f.write(data)
	f.close


def get_options(args=sys.argv[1:]):
	parser = argparse.ArgumentParser(description="Huffman compression.")
	groups = parser.add_mutually_exclusive_group(required=True)
	groups.add_argument("-e", type=str, help="Encode files")
	groups.add_argument("-d", type=str, help="Decode files")
	parser.add_argument("-o", type=str, help="Write encoded/decoded file", required=True)
	options = parser.parse_args()
	return options


if __name__ == "__main__":
	options = get_options()
	if options.e is not None:
		encode(options.e, options.o)
	if options.d is not None:
		decode(options.d, options.o)
