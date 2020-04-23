# -*- coding: utf-8 -*-
#!/usr/bin/python
from tkinter import *
from tkinter import messagebox
import time
import glob
import os,sys
import math
import re

class GUI(Tk):
	def __init__(self):
		super().__init__() # Kế thừa hàm __init__ của tkinter
		self._canvas_ = Canvas(self,width = 1500, height = 8000)
		self._canvas_.pack()
		#self.img1=PhotoImage(file='download.png')
		#self.img1_tiny=self.img1.subsample(10, 10)
		#self._canvas_.configure(bg='red')
		self.title("Natural Language Processing ~ Restudy from HCMUS - 18CLC5")
		self.Xu_Ly()

	def input(self):	
		self.start_time = time.time()
		self.content = self.box_input.get()

		self.amount = (self.amount_files.get())
		if self.amount.isdigit():
			self.amount = int(self.amount)
		else:
			messagebox.showinfo("Lỗi định dạng", "Số lượng file phải là một số")
			return
		self.input_data = (re.findall(r"[\w]+",self.content))
		wordDictInput = dict.fromkeys(self.input_data,0)
		for word in self.input_data:
			wordDictInput[word] += 1
		self.input_tf = {}
		length_input = len(wordDictInput)
		# Tính TF của input
		for word,count in wordDictInput.items():
			self.input_tf[word] = count/length_input

		self.import_file()
		self.Inverse_Document_Frequency()

		## Tính TF-IDF của input
		self.tf_idf_input = dict.fromkeys(self.input_data,0)
		for word in self.input_tf.keys():
			self.tf_idf_input[word] =  self.input_tf[word] * self.idf_dict[word]
		self.Show_Content()

	def Xoa(self):
		for widget in self.winfo_children():
			if widget == self._canvas_:
				continue
			widget.destroy()
		self._canvas_.delete("all")
		
	### Nhận dữ liệu từ folder ###
	def import_file(self):
		# Nội dung trong tất cả các files sẽ được lưu dưới dạng dictionary
		# Key là tên file
		# Value là token của văn bản
		# Ví dụ: {'file' : ['hello', 'world']}
		files = glob.glob(os.path.join("ChiNhan/20_newsgroups/*/*")) 
		#files = glob.glob(os.path.join("ChiNhan/20_newsgroups/*/*")) 
		self.File_Dicts = {}
		for file in files:		
			_list_ = [] # List tạm để lưu trữ dữ liệu trong file
			for sentence in open(file, encoding="utf-8", errors="ignore"): #sentece là các câu trong file
				_list_.extend(re.findall(r"[\w']+",sentence))
			# Nếu file rỗng thì bỏ qua thui
			if len(_list_)== 0 :
				continue 
			self.File_Dicts.update({ file: _list_ })

	### Tính TF  = số lần xuất hiện của 1 từ trong 1 file / số từ của 1 file ###
	def Term_Frequency(self):
		# Lưu các thông số dưới dạng DICTIONARY
		# Key là tên file
		# Value là các TF của từ có trong input
		# Ví dụ : { file: ["hello": 0.1, "world": 0,2]}
		# -----------------------------------------------------------------------------#
		# input_data là dữ liệu từ người dùng nhập vào
		# input_data có kiểu dữ liệu là một dictionary có key là từ, value là TF của từ
		self.tf_dict_file = {}
		for file_name in self.File_Dicts.keys(): # Lấy từng file 
			length = len(self.File_Dicts[file_name])
			temp_dict = {}
			for word in self.input_tf.keys():
				temp_dict.update({word: self.File_Dicts[file_name].count(word)/(length)})
			self.tf_dict_file.update({file_name: temp_dict})
			#print(length, file_name, temp_dict)
		#print(self.tf_dict_file)

	### Tính IDF = log(tổng số file / 1 + số file chứa từ ) ( + 1 vì mẫu có thể = 0) ###
	def Inverse_Document_Frequency(self):
		# IDF lưu kiểu DICTIONARY
		# Key là tên từ 
		# Value là giá trị IDF của từ
		# Ví dụ: {'hello': 6.230481447578482, 'world': 2.2414974010142075}
		self.Term_Frequency()
		length = len(self.File_Dicts) # Tính số lượng files
		self.idf_dict = {}
		for word in self.input_tf.keys():	# Xét từng từ trong dữ liệu input
			amount = 0
			for file_value in self.File_Dicts.values(): # Lấy từng file 
				# Nếu file chứa từ trong input -> qua file mới, + 1 số lượng lên
				if word in file_value:
					amount +=1
					continue
			self.idf_dict.update({word: 1 +  math.log((length+1)/float((amount + 1)))})
 
	### Tính TF * IDF của database ###
	def TF_IDF(self):
		# TF_IDF được lưu theo kiểu Dictionary
		# Key là tên files
		# Value là một dictionary có chứa key là từ trong input, value của nó là giá trị TF_IDF
		# Ví dụ : { file: {'hello': 0.01234, 'world': 0.06789},file2: {....} }
		self.tf_idf_dict_file = {}
		for file_name, tf_values in self.tf_dict_file.items(): # Lấy ra tên file và giá trị TF của từng file trong dict tf
			temp_dict = {}
			for word in tf_values: # Lấy ra các từ trong giá trị value 
				### TF của từng từ trong file * IDF của từng từ ###
				temp_dict.update({word: self.idf_dict[word] * tf_values[word]}) 
			self.tf_idf_dict_file.update({file_name : temp_dict})
		#print(self.tf_idf_dict_file)
	### Tính độ tương đồng ###
	def Cosine_Similarity(self):
		self.TF_IDF()
		### cosine(a,b) = Tích vô hướng / Tích độ dài ###
		self.similarity = {}
		### căn bậc 2 của tổng bình phương tf_idf của input ###
		query = 0.0
		query = sum(value**2 for value in self.tf_idf_input.values())
		query = math.sqrt(query)
		for file_name, value in self.File_Dicts.items(): # Lấy tên file và giá trị trong database
			tich_vo_huong = 0.0
			tich_do_dai = 0.0
			for name,value in self.tf_idf_dict_file[file_name].items(): # Lấy từ ("name") và giá trị TF_IDF ("value")
				# TÍNH TÍCH VÔ HƯỚNG: Tổng của tích tf_idf của từng file với tf_idf của input
				# TÍNH TÍCH ĐỘ DÀI:  Tích của căn bậc 2 của tổng bình phương tf_idf của từng file với căn bậc 2 của tổng bình phương tf_idf của input
				tich_vo_huong += (self.tf_idf_input[name] * value)
				tich_do_dai +=  (value ** 2)
			self.similarity.update( {file_name : tich_vo_huong/(math.sqrt(tich_do_dai) * query + 0.1)})

	def Create_Scroll_Bar(self):
		# Tạo một scroll bar để sử dụng #
		self.scroll_box = Scrollbar(self, orient= "vertical")
		self.scroll_box.config(command = self.yview)
		self.scroll_box.place(x=1110, y= 200, height = 380)

	def Create_Scroll_Text(self):
		# Tạo một cái bảng để in ra kết quả đã tìm được #
		# Có thể scroll được #
		self.Create_Scroll_Bar()
		# Tạo một khung chứa tên file #
		self.scroll_text = Listbox(self,   font = ("Helvetica", 15), borderwidth=0)
		self.scroll_text.place(x= 50,y = 200, width= 1000, height= 380)
		# Tạo một khung chứa số tương đồng #
		self.similarity_box = Listbox(self,font = ("Helvetica", 15), justify = "right", borderwidth = 0)
		self.similarity_box.place(x= 1000, y = 200, width = 150, height = 380)
		# Tạo khả năng scroll #
		self.scroll_text.configure(yscrollcommand= self.scroll_box.set)
		self.similarity_box.configure(yscrollcommand = self.scroll_box.set)
		# Nút lên-xuống để scholl #
		self.Up_Down_Scrolling()
		# Lăn chuột để scroll #
		self.Wheel_Scrolling()
		# Tinh chỉnh #
		self.scroll_text.focus_set()  #set up listbox1 for immediate scrolling
		self.scroll_text.activate(0)  #first scrolling will scroll away from listbox item #1  

	def Wheel_Scrolling(self):
		# Lăn chuột để scroll #
		self.similarity_box.bind('<MouseWheel>',self.OnMouseWheel)
		self.scroll_text.bind('<MouseWheel>',self.OnMouseWheel)

	def Up_Down_Scrolling(self):
		# Ấn nút lên và xuống để scroll #
		self.scroll_text.bind('<Up>', lambda event: self.scroll_listboxes(-1))
		self.similarity_box.bind('<Up>', lambda event: self.scroll_listboxes(-1))
		self.scroll_text.bind('<Down>', lambda event: self.scroll_listboxes(1))
		self.similarity_box.bind('<Down>', lambda event: self.scroll_listboxes(1))

	def scroll_listboxes(self, yFactor):
        # Canh lại góc nhìn khi boxes đã được click vào và nút lên-xuống được ấn #
		self.scroll_text.yview_scroll(yFactor, "units")
		self.similarity_box.yview_scroll(yFactor, "units")

	def yview(self, *args):
        # Cho 2 cái boxes chung 1 góc nhìn #
		self.scroll_text.yview(*args)
		self.similarity_box.yview(*args)

	def OnMouseWheel(self, event):
		# Khi kéo lên-xuống thì 2 cái boxes sẽ di chuyển cùng nhau #
		if event.num == 5 or event.delta == -120:
			yFactor = 1
		else:
			yFactor = -1
		self.scroll_text.yview("scroll", yFactor, "units")
		self.similarity_box.yview("scroll", yFactor, "units")
		return "break"
        # this prevents default bindings from firing, which
        # would end up scrolling the widget twice

	def Create_Text(self, content, x, y, length):
		# Tạo một bảng text bất kỳ #
		scroll = Scrollbar(self)
		if (length > 900): 
			length = 900
		new_Text  = Listbox(self,font=("Helvetica",14), xscrollcommand = scroll.set)
		new_Text.place(x =x,y=y, width= length, height= 30)
		new_Text.insert(END,content)
		new_Text.configure(justify = CENTER)
		scroll.config(command=new_Text.xview)

	def Show_Content(self):
		# Hàm này dùng để hiện kết quả đã tìm kiếm #
		# ---------------------------------------- #
		self.Xoa()
		self.unbind('<Enter>')

		self.Create_Text("Dữ liệu đã nhập:", 50, 50, 200)
		self.Create_Text(self.content, 250, 50,len(self.input_data) * 60)

		self.Cosine_Similarity()
		sorted_result = sorted(self.similarity.items(), key=lambda kv: kv[1]) # Sort từ bé đến lớn #
		num = 0
		self.Create_Scroll_Text()

		# Tính thời gian chạy thuật toán #
		self.Create_Text("Thời gian xử lý: ", 50, 100, 200)
		time_end = time.time() - self.start_time
		self.Create_Text("%f"%time_end, 250, 100, 200)

		self.Create_Text("Tên file", 75, 150, 900)
		self.Create_Text("Độ tương đồng", 1000, 150, 150)
		path_name = (os.path.dirname(os.path.realpath(__file__))).replace("\\","/")
		if len(sorted_result) > 0:
			for i in range(self.amount):
				if sorted_result[-1-i][1] < 0.0000000000000000001:
					continue
				num += 1
				self.scroll_text.insert(END, "%s/%s " % (path_name, (sorted_result[-1-i][0]).replace("\\","/") ))
				self.similarity_box.insert(END, "%f\n" % sorted_result[-1-i][1])

		if num == 0:
			self.scroll_text.insert(END, "Không có file nào chứa nội dung bạn tìm :( ")

		self.back_btt = Button(self,text="Back",command=self.Xu_Ly).place(x=10,y=10)

	def Pre_Click(self,event):
		self.bind('<Button-1>',self.Input_Click)

	def Input_Click(self,event): 
		# Khi click vào widget Entry thì hoạt động #
		# Hàm này dùng để xóa chữ trong ô Entry khi ta click vào Entry đó #
		number = event.widget.winfo_name()
		if event.widget.winfo_class() =="Entry": 
			# Tại sao có dòng này? #
			# Vì tkinter khi tạo lại một widget thì sẽ đặt tên khác :D 
			# Khi xóa widget cũ ở hàm Xoa() thì nó sẽ tạo widget mới tên là !entry3 và !entry4 :( 
			# Nên ta cần cái dòng này để set nó lại như cũ 
			if (number[-1].isnumeric()):
				if (int(number[-1]) % 2 == 0):
					number = "!entry2"
				else:
					number = "!entry"
		if number == '!entry': # Nếu là ô nhập input_document
			content = self.box_input.get()	
			if content == '' or content.isspace():
				self.box_input.insert(1,"Nhập gì đó!")
			else:
				self.box_input.delete(0,END)	

		elif number == '!entry2': # Nếu là ô nhập số files
			amount = self.amount_files.get()
			if amount == '' or amount.isspace():
				self.amount_files.insert(1,"Nhập số files muốn tìm!")
			else:
				self.amount_files.delete(0,END)

	def Get_Input_Document(self):
		self.box_input = Entry(self, font = '100',width=50, justify = "center", cursor="plus")
		self.box_input.insert(0, "Nhập gì đó!")
		self.box_input.place(x=100, y=100, height = 50)

	def Get_Amount_Files(self):
		self.amount_files = Entry(self, font = '100',justify = "center", cursor="plus")	
		self.amount_files.place(x=100, y=175,height = 25)
		self.amount_files.insert(0, "Nhập số files muốn tìm!")

	def Xu_Ly(self):
		self.Xoa()
		self.Get_Input_Document()
		self.Get_Amount_Files()
		self.bt_ok = Button(self,text="Enter",command=self.input).place(x=600, y=100, width= 100,height=50)
		self.bind('<Enter>',self.Pre_Click)	
app = GUI()
app.maxsize(1200,600)
app.mainloop()
