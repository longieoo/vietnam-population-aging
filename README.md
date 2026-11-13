# Già hóa dân số, kinh tế và lao động, 1991–2023

Đồ án môn Trực quan hóa dữ liệu. Gói này chỉ giữ các sản phẩm hiện hành; dữ liệu nguồn và mã tái tạo được giữ để kiểm chứng kết quả.

## Mở các sản phẩm

| Sản phẩm | Đường dẫn |
|---|---|
| Báo cáo Word cuối, 35 trang gồm bìa | [report_submission.docx](reports/report_submission.docx) |
| PDF của cùng bản báo cáo | [report_submission.pdf](reports/report_submission.pdf) |
| Nội dung báo cáo để tra cứu | [report_submission.md](reports/report_submission.md) |
| Dashboard Power BI có dữ liệu nhúng | [PopulationAging.pbix](powerbi/PopulationAging.pbix) |
| Dự án Power BI chỉnh sửa được | [PopulationAging.pbip](powerbi/PopulationAging.pbip) |
| Dashboard web bốn trang, mở ngoại tuyến | [explorer.html](outputs/interactive/explorer.html) |
| Slide thuyết trình | [Slide Canva — 20 phút](https://www.canva.com/d/DNbsAZLx2iAkTnS) |
| Notebook phân tích và bản đọc ngay | [analysis.ipynb](notebooks/analysis.ipynb), [analysis.html](notebooks/analysis.html) |

Bản hiện hành đã có bìa do sinh viên cung cấp. Sau khi sửa Word, cập nhật mục lục và xuất lại PDF. PDF bàn giao hiện khớp bản Word cuối đã kiểm tra toàn bộ 35 trang.

Mở PBIX bằng Power BI Desktop để xem sáu trang tương tác. PBIX đã nhúng dữ liệu, không cần tải WDI khi mở. Để Refresh trên máy khác, đặt tham số `SourceRoot` thành đường dẫn tuyệt đối tới thư mục dự án đã giải nén. PBIP phải đi cùng hai thư mục `PopulationAging.Report` và `PopulationAging.SemanticModel`. Chi tiết ở [hướng dẫn Power BI](docs/powerbi-guide.md). Chưa xuất bản lên Power BI Service.

## Cấu trúc

- `reports/`: một bộ báo cáo cuối Word, PDF, Markdown và ảnh sử dụng trong bài.
- `powerbi/`: PBIX, PBIP, mô hình, định nghĩa visual và bằng chứng kiểm tra.
- `data/`: snapshot WDI gốc, metadata, biên nhận nguồn và bảng chuẩn `processed/master.csv`.
- `outputs/`: 12 hình PNG/SVG, CSV từng hình, bảng phân tích và dashboard web.
- `src/`: mã thu thập, xử lý, phân tích, trực quan hóa, dashboard và kiểm tra; xem `src/README.md`.
- `tests/`: kiểm thử; `notebooks/`: sản phẩm phân tích và trình bày.
- `docs/`: hướng dẫn hiện hành và định nghĩa dữ liệu.


## Dữ liệu và giới hạn

Snapshot `f802111fa64f0c25` dùng 217 nền kinh tế, 1991–2023, 7.161 dòng và 17 cột; có 5.780 dòng đủ tám chỉ tiêu nguồn. Giữ nguyên giá trị thiếu, không bù bằng 0 hoặc nội suy. Báo cáo mô tả liên hệ, không xác định nhân quả. GDP dùng đô la quốc tế giá cố định 2021; các chỉ tiêu lao động có mẫu số 15+, khác tỷ trọng tuổi 15–64 trên tổng dân số. Bản đồ khớp 170 hình học; 47 nền kinh tế còn lại vẫn có trong bảng.

Nguồn WDI và biên nhận tải nằm trong `data/metadata/source_manifest.json`. Natural Earth cung cấp ranh giới bản đồ. Không cần tải lại nguồn để đọc hoặc dựng phân tích.

## Tái tạo và kiểm tra

Python 3.12 trở lên; cài các phụ thuộc trong môi trường riêng:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe run.py doctor
.venv\Scripts\python.exe run.py check
```

| Lệnh | Chức năng |
|---|---|
| `python run.py build` | Dựng dữ liệu, bảng, hình và dashboard từ snapshot; giữ nguyên báo cáo Word đã biên tập |
| `python run.py build --notebook --pdf word` | Thêm notebook; cập nhật mục lục và xuất PDF bằng Microsoft Word trên Windows |
| `python run.py powerbi` | Dựng lại PBIP từ CSV; không ghi đè PBIX |
| `python run.py check` | Kiểm thử và đối chiếu dữ liệu giữa nguồn, bảng và sản phẩm |
| `python run.py package` | Kiểm tra, tạo ZIP và xác minh manifest/checksum |

`build` có thể ghi đè các tệp được sinh; lưu các chỉnh sửa tay trước khi chạy. Chỉ `--acquire` gọi bước thu thập. `--pdf none` là mặc định, giữ PDF đã có; nếu vừa chỉnh sửa Word, xuất PDF lại trước khi nộp. Đóng PBIP trong Desktop trước khi dựng lại; sau đó Refresh và Save As PBIX. Nhật ký và tài liệu trung gian nằm trong `work/`, không được đóng gói.

Xem [mục lục tài liệu](docs/README.md), [trạng thái bàn giao](docs/current-status.md) và [hướng dẫn mã](docs/code-guide.md).

Slide trình bày trên Canva gồm 20 trang, có ghi chú thuyết trình.

