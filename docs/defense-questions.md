# 15 câu hỏi bảo vệ và gợi ý trả lời

## 1. Vì sao chọn WDI thay vì ghép nhiều website?

WDI cung cấp mã chỉ tiêu ổn định, metadata, phân trang và nguồn gốc rõ. Dự án vẫn ghi tổ chức sản xuất dữ liệu như UN, ICP và ILO. Ưu điểm là tái lập cùng snapshot; không có nghĩa mọi chỉ tiêu có cùng phương pháp.

## 2. 7.161 quan sát có phải là 7.161 người?

Không. Một quan sát là một nền kinh tế–năm. Có 217 nền kinh tế × 33 năm, tất cả có giá trị nguồn. Không tính lại dữ liệu dạng dài, không tính tổng hợp vùng hay dòng rỗng. Xem quality_summary.json.

## 3. Tại sao không dùng chỉ các dòng đủ tám biến?

Làm vậy chỉ còn 5.780 dòng và bỏ thông tin nhân khẩu học hợp lệ. Bảng chính giữ 7.161 dòng; từng hình chọn theo các biến cần thiết. Lát cắt GDP 2023 có 197 nước, lao động có 184.

## 4. GDP PPP đang dùng năm giá nào?

Metadata NY.GDP.PCAP.PP.KD xác nhận giá cố định 2021. Mã chuẩn bị dữ liệu trích năm từ tên chính thức và dừng nếu không xác định được. Không dùng GDP hiện hành hay tỷ giá danh nghĩa để thay thế.

## 5. Tăng 3,13 điểm phần trăm khác tăng 3,13% thế nào?

Điểm phần trăm là 8,62 trừ 5,49. Phần trăm tăng tương đối là (8,62/5,49−1)×100 nếu tính từ các số làm tròn. Khi cần số chính xác, dùng giá trị chưa làm tròn trong focal_series.csv.

## 6. Tỷ số phụ thuộc có đo gánh nặng tài chính không?

Không trực tiếp. Công thức chia nhóm tuổi 0–14 và 65+ cho nhóm 15–64. Một người ngoài nhóm 15–64 vẫn có thể làm việc, và một người trong nhóm này có thể không có việc.

## 7. Vì sao mốc chính là 10%?

Đây là mốc phân tích do đề tài yêu cầu để so sánh ở mức già hóa tương đương, không phải quy định pháp lý. Kiểm tra 8% và 12% cho thấy thay mốc làm thay mẫu và khả năng đưa Việt Nam vào so sánh.

## 8. Việt Nam đạt 10% khi nào?

Không quan sát được trong giai đoạn 1991–2023; năm 2023 là 8,62%. Dự án không dự báo năm đạt và không lấy số liệu 2024–2025 để kéo dài ngầm phạm vi.

## 9. Tại sao không ghi Nhật Bản vượt ngưỡng năm 1991?

Nhật Bản đã trên 10% ở đầu chuỗi. Gọi 1991 là lần vượt sẽ nhầm kiểm duyệt trái với một sự kiện quan sát được. Trạng thái đúng là already_above.

## 10. Có thể kết luận Việt Nam già trước khi giàu không?

Chưa từ mốc chính. Việt Nam chưa đạt 10%, và “giàu” cũng cần một chuẩn rõ. Ở mốc 8%, GDP của Việt Nam thấp hơn trung vị nhóm vượt ngưỡng, nhưng đây là kết quả phụ thuộc mốc, mẫu và năm lịch.

## 11. Vì sao tương quan kinh tế dùng log GDP?

GDP/người trải trên khoảng rộng. Log làm các tỷ lệ tương đương có khoảng cách tương đương, giảm sự lấn át thị giác của thu nhập rất cao. Pearson trên log GDP và Spearman đều được báo cáo; không dùng làm chứng cứ nhân quả.

## 12. 15–64 và 15+ có thể so trực tiếp như cùng mẫu số không?

Không. Tỷ trọng 15–64 chia tổng dân số, LFPR và tỷ lệ có việc làm chia dân số 15+. Hình chỉ đặt cạnh để khám phá và luôn ghi mẫu số. Không lấy 100 trừ tỷ trọng 15–64 để suy ra tỷ lệ thất nghiệp.

## 13. Các điểm cực trị có quyết định kết luận không?

Trong lát cắt GDP, Pearson từ 0,72 thành 0,76 khi cắt 5% hai đuôi ở cả hai biến. Với lao động từ 0,08 thành 0,02. Đây là kiểm tra mô tả riêng; bảng gốc không xóa điểm. Xem robustness.csv.

## 14. Mức sinh giảm có lập tức làm già hóa không?

Không thể kết luận vậy. Người 65+ hiện tại thuộc các thế hệ sinh trước đó nhiều thập kỷ. Sinh, tử vong và di cư cùng liên quan đến cơ cấu tuổi. Dự án không phân rã các cơ chế.

## 15. Làm sao tái lập và hạn chế lớn nhất là gì?

Chạy python run.py build --notebook từ gốc dự án, rồi python run.py check. Xem python run.py doctor để kiểm tra thư viện. Mã SHA256 bảo vệ đầu vào. Hạn chế lớn là dữ liệu tổng hợp/ước tính, không có phân tổ lao động theo tuổi, và không thiết kế nhân quả; bản bàn giao được xuất và kiểm tra bằng Word; vẫn nên kiểm tra phông trên máy nộp bài.