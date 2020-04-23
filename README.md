## Nhập môn CNTT2 - Đại học Khoa Học Tự Nhiên TPHCM
### Tên nhóm: RESTUDY
18127158 - Lê Thành Nam		-	18127158@student.hcmus.edu.vn	   
18127121	- Nguyễn Đăng Khoa	- 18127121@student.hcmus.edu.vn	   
18127138	- Nguyễn Duy Long			- 18127138@student.hcmus.edu.vn	    
18127107	- Lý Đăng Huy			-  18127107@student.hcmus.edu.vn      
18127134	- Lê Huỳnh Long		-	18127134@student.hcmus.edu.vn      

# Project Search-Engine
Xây dựng một hệ thống tìm kiếm văn bản (Search Engine). 
## Ngôn ngữ: Python
## Mục tiêu
- Cho trước một tập văn bản D, người dùng sẽ nhập vào một văn bản đầu vào (Input
Document), nhiệm vụ của một hệ thống tìm kiếm văn bản là trả về các văn bản có độ tương
đồng giảm dần so với “Input Document”. 

## Thực hiện
- Bước 1: Vector hóa các văn bản trong D dưới một tập đặc trưng (Mô hình cơ bản: Bag-of-words và TF-IDF)
https://en.wikipedia.org/wiki/Bag-of-words_model https://en.wikipedia.org/wiki/Tf%E2%80%93idf
- Bước 2: Vector hóa “Input Document” bằng mô hình đã sử dụng ở bước 1
- Bước 3: Tính độ tương đồng (similarity measure) giữa vector đại diện cho “Input Document”
và vector đại diện cho từng văn bản trong D ( các phương pháp tính độ tương đồng giữa hai
vector văn bản: Euclidean, Cosine …)
https://en.wikipedia.org/wiki/Similarity_measure
- Bước 4: Chọn ra top k văn bản trong D tương đồng giảm dần với “Input Document”.
Tập dữ liệu: http://www.mediafire.com/file/njw6g524o506lav/ChiNhan.rar

### Xem file PDF để rõ hơn về yêu cầu.
