# Nhật ký quyết định làm sạch

1. Chỉ dùng WDI source=2; tám mã trong config.py. Không trộn national estimates và modeled ILO estimates.
2. Dùng region.id=NA hoặc region.value=Aggregates trong metadata để loại tổng hợp. Không suy đoán bằng độ dài mã.
3. Ép năm thành số nguyên và giá trị thành số; lỗi kiểu dữ liệu dừng pipeline. Khóa quốc gia–năm duy nhất.
4. Nối ngoài các chỉ tiêu với validate=one_to_one; bỏ dòng chỉ khi cả tám giá trị nguồn đều thiếu. Không tạo Cartesian grid để tăng số dòng.
5. Không bù thiếu, không thay bằng 0, không xóa ngoại lệ. Mẫu đủ biến riêng cho từng phép phân tích.
6. Dung sai tổng cơ cấu tuổi 0,15 điểm phần trăm. Giữ nguyên độ chính xác nguồn trong tính toán; chỉ làm tròn khi hiển thị.
7. Lần vượt ngưỡng chỉ khẳng định khi chuỗi quan sát trước đó liền năm. Đầu chuỗi đã trên ngưỡng không được gọi là năm vượt.
8. Hình 06 dùng tốc độ điểm phần trăm/năm thay cho tổng thay đổi vì ba giai đoạn dài khác nhau. Hình 05 thêm histogram toàn cầu. Hình 10 mở rộng toàn cầu do chỉ hai nước trọng tâm vượt 10% trong cửa sổ.
9. Các cờ biến động được giữ trong abrupt_changes.csv. Không có bằng chứng đủ để sửa dữ liệu nguồn; không mặc định cờ là lỗi. Phần kiểm tra độ nhạy là phân tích bổ sung, không làm sạch bằng cắt ngoại lệ.
10. Phân trang đối chiếu tổng số dòng; SHA256 kiểm tra cache trước khi tái lập. Chỉ acquire.py có quyền tải mới theo thao tác rõ ràng. Các bước phân tích và báo cáo đọc snapshot đã lưu.
