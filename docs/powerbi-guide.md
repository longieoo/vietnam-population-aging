# Báo cáo Power BI của đồ án

## Tệp và nguồn dữ liệu

Mở `powerbi/PopulationAging.pbix` bằng Power BI Desktop để xem và chỉnh sửa báo cáo đã nhập dữ liệu. Bản mã nguồn chỉnh sửa được gồm `PopulationAging.pbip`, thư mục `.Report` và `.SemanticModel`. Báo cáo dùng **biểu đồ Power BI native**, không dùng ảnh chụp biểu đồ làm dashboard.

Mô hình Import đọc ba CSV đã kiểm chứng trong dự án: `data/processed/master.csv`, `outputs/tables/period_changes.csv` và `outputs/tables/threshold_crossings.csv`. Bảng chính có 7.161 dòng, 217 nền kinh tế, 1991–2023. Không tải lại WDI khi mở báo cáo. PBIX chứa dữ liệu đã nhập; để Refresh trên máy khác, vào **Transform data → Edit parameters** và đặt `SourceRoot` thành đường dẫn tuyệt đối đến thư mục `population-aging` đã giải nén. Nếu mở PBIP không có cache, bấm Refresh sau khi đặt đường dẫn.

## Các trang

| Trang | Nội dung | Đối chiếu hình trong báo cáo |
|---|---|---|
| 01 · Tổng quan | Cơ cấu tuổi; quy mô và tỷ trọng 65+; ba tỷ số phụ thuộc | 01–03 |
| 02 · Diễn biến già hóa | Chuỗi 65+ của nhóm đối chiếu; mức sinh; ma trận màu tốc độ; tỷ trọng 15–64 | 05–07 và đối chiếu lao động |
| 03 · Già hóa và kinh tế | Scatter GDP–65+ với trục GDP log; quỹ đạo theo năm; GDP tại ngưỡng và bảng trạng thái | 08–10 |
| 04 · Cơ cấu tuổi và lao động | Scatter cơ cấu tuổi–việc làm; lịch sử cơ cấu tuổi, tham gia lao động và việc làm | 11–12 |
| 05 · Phân bố quốc tế | Bản đồ Shape map tô màu tỷ trọng 65+; bảng số liệu quốc tế | 04 |
| 06 · Hướng dẫn và nguồn | Thao tác, định nghĩa chỉ số, nguồn và giới hạn diễn giải | Thông tin bổ trợ |

Bản đồ dùng ranh giới Natural Earth 1:110m lưu trong dự án và khóa ISO3 đã sửa như hình gốc: 170 nền kinh tế khớp hình học, 47 trường hợp không khớp vẫn có trong bảng. TopoJSON được nhúng trong báo cáo. Không phụ thuộc geocoding Azure Maps; Azure Maps ở tài khoản tổ chức hiện có yêu cầu quản trị viên cho phép xử lý dữ liệu ngoài vùng. Shape map giữ cách mã hóa bằng màu của bài.

## Bộ lọc và cách đọc

- Quốc gia trọng tâm mặc định Việt Nam; các thẻ và chuỗi riêng giữ độc lập với vùng/thu nhập của mẫu quốc tế.
- Năm hiện trạng mặc định 2023. Chuỗi thời gian hiển thị 1991 đến năm chọn, thay vì bị lọc thành một điểm.
- Nhóm đối chiếu mặc định Việt Nam, Thái Lan, Indonesia, Nhật Bản, Hàn Quốc. Trang 02 và 03 có bộ chọn nhóm.
- Vùng và nhóm thu nhập lọc mẫu quốc tế. Phân loại thu nhập là metadata tại thời điểm lưu nguồn, không phải lịch sử từng năm.
- Trang 03 chọn ngưỡng 8%, 10%, 12%. Mốc vượt ngưỡng và tốc độ theo ba giai đoạn luôn dùng cửa sổ cố định 1991–2023.
- Có thể chọn điểm hoặc dòng bảng để lọc chéo, di chuột để xem số liệu, dùng dấu `...` để xem/xuất dữ liệu. Nút chọn quốc gia có tìm kiếm khi danh sách dài.

## Quy tắc tính

Tỷ lệ tuổi tổng hợp dùng trọng số dân số. Các chỉ số GDP/người, mức sinh, tham gia lao động và việc làm chỉ trả số tại cấp một quốc gia–một năm; không cộng các tỷ lệ hoặc dân số qua nhiều năm. Điểm thiếu biến giữ trống và bị loại khỏi scatter. Hai thẻ số quan sát tính lại theo năm/vùng/thu nhập; năm 2023, tất cả vùng có n=197 cho GDP–65+ và n=184 cho cơ cấu tuổi–việc làm.

Pearson r tính trên GDP gốc, dù trục hiển thị dùng log; không diễn giải tương quan như nhân quả. Quỹ đạo gồm một điểm cho mỗi năm, có năm trong tooltip. Thẻ dân số hiển thị số người chính xác và thẻ tỷ lệ hiển thị hai chữ số thập phân. Tỷ lệ cơ cấu tuổi và chỉ tiêu lao động có mẫu số khác nhau, đã ghi ngay trên trang 04.

Biểu đồ GDP tại ngưỡng chỉ hiển thị `observed` và có GDP. Bảng trạng thái giữ các trường hợp đã ở trên ngưỡng năm 1991/chưa đạt năm 2023. Việt Nam chưa đạt ngưỡng phân tích 10% đến 2023 nên không có cột GDP tại ngưỡng 10%. Các ngưỡng là mốc phân tích của đồ án, không tự coi là phân loại chính thức.

## Dựng lại

Đóng PBIP trong Desktop trước khi chạy `python run.py powerbi`. Lệnh tạo lại PBIP, 10 bảng, 78 measure DAX và 6 trang từ CSV hiện có; có thể ghi đè thay đổi đã chỉnh tay trong PBIP. Lệnh không ghi đè PBIX đã bàn giao. Sau khi dựng lại, mở PBIP, Refresh và Save As PBIX để cập nhật bản có dữ liệu nhúng. Cần thư viện `pyshp` (`shapefile`) có sẵn trong requirements của dự án.

Mã tạo: `src/build_powerbi.py`; nền cấu trúc native: `src/powerbi_template/`; danh sách visual: `powerbi/visual_inventory.json`. Cache `.pbi` không đưa vào gói bàn giao. Chỉ cập nhật nguồn CSV thông qua pipeline của dự án để giữ đồng bộ bảng và hình.

Định dạng dự án theo [Microsoft PBIP](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview); bản đồ theo [Microsoft Shape map](https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-shape-map).

## Phạm vi bàn giao

Đây là báo cáo tương tác nhiều trang trong Power BI Desktop. Chưa đăng lên Power BI Service hoặc tạo dashboard ghim trong workspace trực tuyến. Việc đó cần workspace đích và quyền xuất bản của tài khoản đang đăng nhập; file PBIX có thể dùng để xuất bản sau.
