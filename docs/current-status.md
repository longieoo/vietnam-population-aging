# Trạng thái dự án — 15/11/2026

## Bản nâng cấp hiện hành

- Kiểm tra dữ liệu chuẩn trước khi phân tích: khóa `iso3/year`, kiểu dữ liệu, kỳ nghiên cứu, miền giá trị, số hữu hạn, tổng cơ cấu tuổi và bốn công thức dẫn xuất. Giá trị thiếu được giữ nguyên.
- Kiểm tra URL, kích thước, checksum và phân trang của cache nguồn; ghi cache nguyên tử để tránh để lại tệp dở dang.
- Dashboard có bảng nguồn phân trang, xuất CSV, thông báo mẫu trống, điều khiển tab bằng bàn phím và bố cục màn hình hẹp.
- Lệnh build chạy kiểm tra sản phẩm sau khi dựng; `verify-archive` kiểm tra lại gói ZIP. Manifest nằm trong ZIP, không làm thay đổi mã nguồn.
- Git giữ nguyên byte của snapshot; master dùng cùng định dạng xuống dòng trên Windows/Linux để bảo toàn provenance của notebook và PBIX.
- README và kịch bản nói đã đồng bộ với bộ Canva 20 slide. Không còn yêu cầu PPTX cũ trong kiểm tra mặc định.

## Kiểm tra tại máy — lần này

Môi trường Python 3.12.14 mới được tạo riêng; cài thành công các phiên bản trong requirements. `doctor` nhận đủ phụ thuộc. Lệnh `build` dựng lại dữ liệu, phân tích, 12 hình PNG/SVG, bảng minh chứng và dashboard, sau đó chạy kiểm thử và đối chiếu sản phẩm.

- **39 kiểm thử Python đạt**; bao gồm các trường hợp dữ liệu hỏng và archive sai checksum.
- Ruff không phát hiện lỗi cú pháp/tên chưa định nghĩa trong phạm vi cấu hình.
- Mô hình dashboard JavaScript đạt kiểm tra mẫu, ngưỡng, giá trị thiếu, trọng số, tương quan và CSV.
- Chromium qua Chrome headless: bốn trang hiển thị tại 1440×1000 và 390×844; kiểm tra bàn phím, phân trang, CSV, reset, quốc gia/vùng và khoảng tốc độ trống đạt. Không ghi nhận lỗi JavaScript trong các trạng thái đã thử.
- Notebook được chạy lại **7 ô mã** trong kernel mới; không dùng kết quả cache của kernel trước.
- Đối chiếu 98 tệp nguồn, 57.288 giá trị raw/master, bốn công thức dẫn xuất và mười chỉ số nhân khẩu học đạt. Master vẫn có 7.161 dòng và SHA256 `6a65ae1082c04fa4726874952853c01eae83b69e942c8ace5d792b961271f6a5`.
- Kiểm tra cấu trúc PBIP, sáu trang, các visual và CRC/hash của PBIX đạt. Đây là kiểm tra file, không phải chạy lại giao diện Power BI Desktop.

Biên nhận dựng tại `work/logs/` và ảnh kiểm tra tại `work/browser/` là tệp làm việc, không đưa vào gói bàn giao. Kết quả đối chiếu có thể đọc ở [delivery_validation.json](../outputs/tables/delivery_validation.json). Trạng thái Linux mới nhất nằm trong [GitHub Actions](https://github.com/longieoo/vietnam-population-aging/actions), không được suy từ kết quả Windows.

## Các sản phẩm đã biên tập

Báo cáo Word/PDF 35 trang và PBIX được giữ nguyên từ bản bàn giao trước. Kiểm tra định lượng đọc các giá trị chính của báo cáo Markdown và dữ liệu nhúng đã ghi nhận của PBIX; lần này không biên tập lại báo cáo, không xuất lại PDF và không tái kiểm tra mọi trang trong Word/Power BI Desktop.

Slide hiện hành là [Canva, 20 trang](https://www.canva.com/d/DNbsAZLx2iAkTnS). Kiểm tra cục bộ không xác nhận nội dung Canva. Nếu cập nhật dữ liệu, cần rà lại báo cáo, slide và Refresh/Save As PBIX thủ công.

## Giới hạn sử dụng

Khoảng nghiên cứu 1991–2023 và snapshot nguồn được giữ cố định. Không phải số liệu thời gian thực hoặc mô hình dự báo. Tương quan không xác định nhân quả; ngưỡng 8/10/12% là lựa chọn phân tích. Vùng/thu nhập là metadata lúc tải. Bản đồ có 47 nền kinh tế không có hình học. Power BI Desktop chưa xuất bản lên Service; các tổ hợp bộ lọc và trình duyệt chưa được thử hết.
