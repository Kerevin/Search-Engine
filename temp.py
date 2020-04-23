# -*- coding: utf-8 -*-
#!/usr/bin/python

import os, sys
import glob # Thư viện này dùng để import hết files vào đây
import math
import time
### Last updated: 4:23 PM - 29/03/2019 ###
start_time = time.time()
### Import hết file trong thư mục ###
file_path = "ChiNhan/20_newsgroups/*/*"
f = input("Nhập tên file muốn tìm kiếm. Để trống thì đường dẫn sẽ được mặc định: ")
if f == "":
	f = file_path
files = glob.glob(os.path.join(f)) 
#files = glob.glob(os.path.join("alt.atheism/*")) 
global file_length
file_length = len(files)
### Nhập files, lấy dữ liệu của các nội dung trong files ###
def import_file():
	# Nội dung trong tất cả các files sẽ được lưu dưới dạng dictionary
	# Key là tên file
	# Value là token của văn bản
	# Ví dụ: {'file1' : ['hello', 'world']}
	file_dicts = {}
	for file in files:		
		_list_ = [] # List tạm để lưu trữ dữ liệu trong file
		for sentence in open(file, encoding="utf-8", errors='ignore'): #sentece là các câu trong file
			_list_.extend( (sentence.lower().split()) )
		if len(_list_)== 0 :
			continue
		file_dicts.update({ file: _list_ })
	return file_dicts

File_Dicts = import_file() # Chứa các dữ liệu của file
### Tính TF  = số lần xuất hiện của 1 từ trong 1 file / số từ của 1 file ###
def term_frequency(input_data, file_dicts):
	# Lưu các thông số dưới dạng DICTIONARY
	# Key là tên file
	# Value là các TF của từ có trong input
	# Ví dụ : { file1: ["hello": 0.1, "world": 0,2]}
	# -----------------------------------------------------------------------------#
	# input_data là dữ liệu từ người dùng nhập vào
	# input_data có kiểu dữ liệu là một dictionary có key là từ, value là TF của từ
	tf_dict = {}
	for file_name in file_dicts.keys(): # Lấy từng file 
		#temp_dict = {}
		# for word in input_data.keys():
		# 	temp_dict.update({word: file_dicts[file_name].count(word)/(len(file_dicts[file_name] ))})
		temp_dict = ({word: file_dicts[file_name].count(word)/(len(file_dicts[file_name])) for word in input_data.keys()})
		tf_dict.update({file_name: temp_dict})
	return tf_dict

### Tính IDF = log(tổng số file / 1 + số file chứa từ ) ( + 1 vì mẫu có thể = 0) ###
def inverse_document_frequency(input_data, file_dicts):
	# IDF lưu kiểu DICTIONARY
	# Key là tên từ 
	# Value là giá trị IDF của từ
	# Ví dụ: {'hello': 6.230481447578482, 'world': 2.2414974010142075}

	length = len(file_dicts) # Tính số lượng files
	idf_dict = {}
	for word in input_data.keys():	# Xét từng từ trong dữ liệu input
		amount = 0
		for file_value in file_dicts.values(): # Lấy từng file 
			# Nếu file chứa từ trong input -> qua file mới, + 1 số lượng lên
			if word in file_value:
				amount +=1
				continue
		idf_dict.update({word: math.log(length/float((amount + 1)))})
	return idf_dict
 

### Tính TF * IDF của database ###
def TF_IDF(tf,idf,file_dicts):
	# TF_IDF được lưu theo kiểu Dictionary
	# Key là tên files
	# Value là một dictionary có chứa key là từ trong input, value của nó là giá trị TF_IDF
	# Ví dụ : { file1: {'hello': 0.01234, 'world': 0.06789},file2: {....} }
	tf_idf_dict = {}
	for file_name, tf_values in tf.items(): # Lấy ra tên file và giá trị TF của từng file trong dict tf
		temp_dict = {}
		for word in tf_values: # Lấy ra các từ trong giá trị value 
			### TF của từng từ trong file * IDF của từng từ ###
			temp_dict.update({word: idf[word] * tf_values[word]}) 
		#temp_dict = {word: idf[word] * tf_values[word] for word in tf_values}
		tf_idf_dict.update({file_name : temp_dict})
	#tf_idf_dict.update({file_name : {word : idf[word] * tf_values[word] for word in tf_values} for file_name, tf_values in tf.items()})
	return tf_idf_dict

#print(TF_IDF(test,test2,File_Dicts))

### Tính độ tương đồng ###
def Cosine_Similarity(tf_idf_file, tf_idf_input, file_dicts):
	# cosine(a,b) = Tích vô hướng / Tích độ dài
	similarity = {}
	query = 0.0
	query = math.sqrt(sum(value**2 for value in tf_idf_input.values()))
	for file_name, value in file_dicts.items(): # Lấy tên file và giá trị trong database
		tich_vo_huong = 0.0
		tich_do_dai = 0.0
		for name,value in tf_idf_file[file_name].items(): # Lấy từ ("name") và giá trị TF_IDF ("value")
			# TÍNH TÍCH VÔ HƯỚNG: Tổng của tích  idf của từng file với idf của input
			# TÍNH TÍCH ĐỘ DÀI:  Tổng của căn bậc 2 của tích idf của từng file với idf của input
			tich_vo_huong += (tf_idf_input[name] * value)
			tich_do_dai +=  (value ** 2)
		tich_do_dai = math.sqrt(tich_do_dai) * query
		similarity.update({file_name : tich_vo_huong/(tich_do_dai+0.1)})
	return similarity
	
#input_document = input("Nhap tu khoa tim kiem: ")
input_document = "How do cruiser riders with no or negligible helmets"

bowInput = (input_document.lower().split(" "))
wordDictInput = dict.fromkeys(bowInput,0)

for word in bowInput:
	wordDictInput[word] += 1
input_tf = {}
length_input = len(wordDictInput)

# Tính TF của input
for word,count in wordDictInput.items():
	input_tf[word] = count/length_input

idf = inverse_document_frequency(wordDictInput,File_Dicts) # IDF của input và của file 

## Tính TF-IDF của input
tf_idf_input = dict.fromkeys(bowInput,0)
for word in input_tf.keys():
	tf_idf_input[word] =  input_tf[word] * idf[word]


tuong_dong= Cosine_Similarity(TF_IDF(term_frequency(wordDictInput, File_Dicts), idf, File_Dicts), tf_idf_input, File_Dicts)
amount_of_files = 5

sorted_x = sorted(tuong_dong.items(), key=lambda kv: kv[1]) # Sắp xếp lại dictionary của tuong_duong
print("Du lieu tim kiem: ", input_document)
print("So files: ", len(File_Dicts))
print("Do tuong dong giam nhat trong %d file(s):"%amount_of_files)
for i in range(amount_of_files):
	print("...\\"+sorted_x[-1-i][0],"voi so tuong dong:", sorted_x[-1-i][1])
print("Xu ly sau ", (time.time()- start_time) , "giay")
input("Done")
