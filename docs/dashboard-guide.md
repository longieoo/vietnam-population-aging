# Hướng dẫn dashboard web bốn trang

Mở `outputs/interactive/explorer.html` bằng trình duyệt. Plotly và dữ liệu được nhúng trong HTML; không cần mạng hay máy chủ để sử dụng. Các liên kết nguồn bên ngoài cần mạng. Dựng lại bằng `python src/explore.py` hoặc `python run.py build`; đóng gói bằng `python run.py package`.

## Nội dung và mục đích

| Trang | Câu hỏi và các góc nhìn |
|---|---|
| Tổng quan | Quy mô và cơ cấu tuổi của quốc gia trọng tâm; đối chiếu tỷ trọng 65+ với quốc gia đã chọn; 15 mức già hóa cao trong vùng |
| Diễn biến già hóa | Tỷ trọng/số người 65+/chỉ số già hóa; tốc độ tăng theo giai đoạn; thành phần phụ thuộc; heatmap thay đổi từng năm |
| Già hóa và kinh tế | Lát cắt GDP PPP–65+; quỹ đạo quốc gia; thu nhập tại lần vượt mốc 8/10/12%, kèm luồng loại mẫu |
| Cơ cấu tuổi và lao động | Lát cắt cơ cấu tuổi–việc làm; hai chuỗi lao động của quốc gia; đối chiếu tỷ trọng 15–64 |

Quốc gia trọng tâm mặc định Việt Nam. Bốn thẻ chỉ số và diễn giải thay đổi theo dữ liệu được chọn. Chuỗi đối chiếu mặc định gồm Việt Nam, Thái Lan, Indonesia, Nhật Bản và Hàn Quốc; thêm/bớt được, tối đa sáu quốc gia kể cả trọng tâm. Khi đổi quốc gia trọng tâm, quốc gia đó luôn được đưa vào đối chiếu; nếu đã đủ sáu, danh sách được giữ tối đa sáu và hiển thị bằng các nút trên trang.

## Quy tắc bộ lọc

- **Năm:** thẻ chỉ số/lát cắt dùng đúng năm; lịch sử dùng 1991 đến năm đó. Không cộng dân số qua các năm.
- **Vùng so sánh:** áp dụng benchmark, xếp mức cao, tốc độ vùng và mẫu mốc già hóa; không loại các quốc gia được người dùng chọn khỏi lịch sử. Phạm vi này hiển thị ngay dưới bộ lọc.
- **Đại lượng theo dõi:** tỷ trọng 65+, số người 65+ hoặc chỉ số già hóa; không trộn đơn vị trên cùng trục.
- **Benchmark:** trung vị nền kinh tế hoặc tổng hợp theo dân số, chỉ cho tỷ trọng 65+. Cỡ mẫu có thể đổi qua các năm và có trong CSV.
- **Năm đầu tốc độ:** chọn 1991, 2000 hoặc 2010. Tốc độ = thay đổi tỷ trọng / số năm; khi năm kết thúc không sau năm đầu thì không tạo số liệu tốc độ.
- **Ngưỡng 8/10/12%:** dùng toàn cửa sổ cố định 1991–2023 để giữ so sánh có ý nghĩa. Biểu đồ ghi rõ độc lập với năm đang chọn; vẫn lọc theo vùng.
- **Đặt lại:** trả các bộ lọc về mặc định trong trang hiện tại.

Bấm điểm scatter hoặc cột xếp mức cao/tốc độ/mốc thu nhập để mở chuỗi tỷ trọng 65+ của nền kinh tế đó. Đóng chi tiết để quay lại; thao tác này không đổi bộ lọc quốc gia trọng tâm.

## Định nghĩa và dữ liệu nguồn

Chỉ số già hóa = `age_65_plus / age_0_14 × 100`: người 65+ trên 100 trẻ em. Tỷ số hỗ trợ tiềm năng = `age_15_64 / age_65_plus`: người 15–64 trên một người 65+, không phải số người có việc làm hoặc thực sự đang nuôi người khác. Mẫu số không hợp lệ/thiếu tạo giá trị thiếu.

Các biến này nằm trong payload dashboard và CSV bổ trợ; bảng master gốc vẫn giữ nguyên để bảo toàn tái lập và notebook đã kiểm chứng. `dashboard_data.json` lưu toàn bộ dữ liệu đã nhúng, hash master, snapshot và kết quả ngưỡng. Vùng/nhóm thu nhập là metadata tại lúc tải, không phải phân loại lịch sử.

Mỗi biểu đồ có nút xem dữ liệu và tải CSV riêng. Bảng hiển thị tối đa 50 dòng, CSV gồm toàn bộ dữ liệu của biểu đồ. Chuỗi lịch sử giữ cả dòng thiếu để thể hiện khoảng trống; scatter chọn mẫu đủ hai biến. CSV benchmark có cột phân biệt chuỗi quốc gia/chuỗi tổng hợp. Heatmap giữ thiếu ở 1991 vì năm 1990 ngoài cửa sổ.

CSV động dùng Blob và giữ URL đủ lâu để trình duyệt xử lý. Công cụ trình duyệt tích hợp chưa trả được sự kiện hoàn tất tải Blob, nên không tuyên bố đã xác minh tải động trên mọi trình duyệt. Ba tệp dự phòng mở được trực tiếp:

- `dashboard_gdp_2023.csv`: 197 nền kinh tế, toàn mẫu GDP–65+ năm 2023.
- `dashboard_labor_2023.csv`: 184 nền kinh tế, toàn mẫu cơ cấu tuổi–việc làm năm 2023.
- `dashboard_aging_metrics.csv`: các chỉ số nhân khẩu học của 7.161 dòng.

Liên kết các tệp có trong mục nguồn trên dashboard; chúng dùng phạm vi cố định, không theo bộ lọc hiện tại. Tệp GDP đã tải thật qua liên kết và khớp SHA256 với tệp dự án.

## Kiểm tra và giới hạn

Đã thử bốn trang, năm 2023/1991, vùng Đông Á–Thái Bình Dương, ngưỡng 8/10%, thêm Pháp thành sáu quốc gia, chuyển chỉ số già hóa/benchmark theo dân số, mở lịch sử từ điểm Aruba và trường hợp Aruba thiếu lao động. Mẫu GDP 197, lao động 184/187 theo năm, ngưỡng 10% 45→39 khớp bảng đã kiểm chứng. Giao diện desktop và chiều rộng nội dung 375px đã xem; sau resize ổn định, scrollWidth bằng clientWidth. Không phát hiện lỗi JavaScript trong các trạng thái đã thử.

`tests/test_dashboard.py` kiểm tra toàn bộ cột số payload với master, hai chỉ số mới, giá trị thiếu, logic được nhúng đúng phiên bản và CSV dự phòng. `tests/dashboard_model_test.cjs` kiểm tra mẫu, tương quan, ngưỡng, trọng số, mẫu số thiếu và CSV; chạy bằng `node tests/dashboard_model_test.cjs`. Bộ Python đầy đủ hiện có 21 kiểm thử.

Phạm vi chưa bao gồm mọi tổ hợp bộ lọc, mọi trình duyệt, hoặc xác minh nguyên nhân từng biến động WDI. Chưa bổ sung dữ liệu tuổi–giới, nhóm 80+, dự báo 2050 hay Power BI; các phần này cần yêu cầu/phạm vi và nguồn riêng. Dự án hiện giữ đúng đề tài 1991–2023 đã đăng ký. Báo cáo 18 trang, 12 slide và notebook vẫn dùng dữ liệu đã kiểm chứng; dashboard là giao diện khám phá bổ sung, không thay thế giới hạn phân tích trong báo cáo.

## Mã nguồn

`explore.py` đóng gói dữ liệu bằng pandas và nhúng Plotly qua API xuất HTML chính thức. `dashboard_template.html` quản lý bố cục. `dashboard_model.js` chứa phép tính thuần dùng chung cho giao diện/kiểm tra Node. `dashboard_app.js` quản lý trạng thái, biểu đồ, nguồn và xuất CSV. Không bổ sung framework hoặc phụ thuộc Python mới.

## Bảng dữ liệu và bàn phím

Bảng nguồn chia trang 50 dòng; dùng Trước/Tiếp để xem toàn bộ mẫu, hoặc xuất CSV của biểu đồ. Đổi bộ lọc sẽ đưa bảng về trang đầu. Dùng Tab để tới nhóm trang, mũi tên trái/phải để chuyển trang, Home/End để tới trang đầu/cuối. Giá trị thiếu hiển thị trống hoặc dấu gạch; không được đổi thành 0. Khoảng tính tốc độ không hợp lệ có thông báo không có dữ liệu.
