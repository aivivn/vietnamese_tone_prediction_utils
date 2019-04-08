Các hàm hỗ trợ cho cuộc thi [Thêm dấu tiếng Việt].

## Hàm bỏ dấu của toàn bộ file

Hàm `utils.remove_tone_file(in_path, out_path)` giúp loại bỏ dấu tiếng Việt của file `in_path` và lưu vào file `out_path`.

## Hàm chuyển từ tiếng Việt có dấu sang dạng VNI chuẩn hóa

Hàm `convert_to_submission_file(in_path, out_path)` giúp chuyển một file dự đoán với mã dòng và tiếng Việt có dấu thành một file `.csv`. File này là dạng đã được chuẩn hóa sang dạng mã VNI với dấu ở cuối mỗi từ.


![Bảng mã VNI](https://cdn.trangcongnghe.com/uploads/posts/2018-08/c225ch-g245-tieng-viet-c243-dau-khi-d249ng-kieu-g245-telex-vni-v224-viqr_1.jpg)

(Nguồn: https://trangcongnghe.com/thu-thuat/145092-c225ch-g245-tieng-viet-c243-dau-khi-d249ng-kieu-g245-telex-vni-v224-viqr.html)

Xem thêm các file trong thư mục `./data` để thấy các ví dụ mẫu.





