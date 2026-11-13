# Cập nhật kiểm tra — 07/10/2026

Dashboard được dựng lại từ master giữ nguyên SHA256. 21 kiểm thử Python đạt; kiểm tra thêm JavaScript về mẫu, tương quan, ngưỡng, trọng số, giá trị thiếu và CSV. Payload được đối chiếu toàn bộ cột số với master; hai chỉ số mới và ba CSV dự phòng có kiểm tra riêng.

Đã thử bốn trang, năm đầu/cuối, vùng Đông Á–Thái Bình Dương, ngưỡng 8/10%, sáu quốc gia, đổi đại lượng, benchmark theo dân số, mở lịch sử Aruba và dữ liệu lao động thiếu. Mẫu 197 GDP, 184 lao động năm 2023, 187 lao động năm 1991 và ngưỡng 10% 45→39 khớp. Giao diện hẹp sau ổn định có clientWidth=scrollWidth=375px. Không thấy lỗi JavaScript ở trạng thái đã thử.

CSV GDP cố định tải trực tiếp qua liên kết và khớp SHA256 với tệp dự án. Tải CSV động qua Blob chưa được phần kiểm tra trình duyệt xác nhận hoàn tất; các tệp cố định dự phòng ghi rõ phạm vi. Chưa thử mọi tổ hợp/mọi trình duyệt. Bằng chứng: dashboard_validation.json. Bằng chứng kiểm tra định lượng nằm trong outputs/tables.

Xem [hướng dẫn dashboard](dashboard-guide.md) và [mục lục tài liệu](README.md).
# Kiểm tra Power BI — 09/10/2026

Đã mở và xem sáu trang trong Power BI Desktop, nhập bảng chuẩn 7.161 dòng và lưu PBIX với DataModel nhúng. Các giá trị Việt Nam 2023, mẫu GDP–65+ (197), mẫu cơ cấu tuổi–việc làm (184) và Pearson r GDP (0,603) khớp CSV. Kiểm tra bộ lọc 2023 → 2000 → 2023: tỷ trọng 65+ chuyển 8,62% → 5,98% → 8,62%, chuỗi thời gian dừng theo năm chọn; ma trận giai đoạn giữ cửa sổ cố định. Bản đồ tô màu quốc gia chạy bằng Shape map và TopoJSON Natural Earth nhúng. Các bảng dài có thanh cuộn.

21 kiểm thử Python và kiểm tra đồng bộ tài liệu đạt. PBIX kiểm tra ZIP CRC đạt; dữ liệu master giữ nguyên SHA256. Bằng chứng định lượng và phạm vi kiểm tra: `powerbi/validation.json`. Tệp là báo cáo Desktop, chưa xuất bản lên Service.


# Báo cáo cuối và gói bàn giao — 09/10/2026

Báo cáo Word/PDF hiện hành có 34 trang; toàn bộ trang đã được kiểm tra trực quan. PDF được sao chép từ bản xuất Word đã xác minh của cùng bản DOCX. 12 hình, 9 ảnh và 7 bảng; các bảng số liệu và dữ liệu master không thay đổi. Bằng chứng: `outputs/tables/submission_report_validation.json`. Bản báo cáo cũ, tài liệu lịch sử và tệp trung gian không nằm trong gói.
