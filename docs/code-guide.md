# Mã nguồn phân tích và trực quan hóa

Chạy lệnh từ thư mục dự án chứa `run.py`, không chạy từ bên trong `src/`.

| Tệp | Vai trò |
|---|---|
| `config.py` | Đường dẫn dự án, tám chỉ tiêu WDI, năm, quốc gia và định dạng số |
| `acquire.py` | Thu thập nguồn WDI, phân trang, cache và biên nhận SHA256 |
| `prepare.py` | Kiểm tra nguồn, làm sạch, ghép chỉ tiêu và tạo master.csv |
| `analyze.py` | Tính bảng kết quả, liên hệ mô tả, tốc độ và lần vượt ngưỡng |
| `visualize.py` | Tạo 12 biểu đồ PNG/SVG và CSV tương ứng |
| `export_evidence.py` | Xuất bảng phát hiện, nguồn dữ liệu, cỡ mẫu và giới hạn |
| `explore.py` | Đóng gói dashboard web ngoại tuyến từ dữ liệu đã lưu |
| `dashboard_template.html` | Bố cục và bộ lọc của dashboard web |
| `dashboard_app.js` | Trạng thái giao diện, biểu đồ, tương tác và xuất CSV |
| `dashboard_model.js` | Các phép tính, lựa chọn mẫu và chỉ số của dashboard |
| `build_powerbi.py` | Tạo bộ PBIP, mô hình và các trang Power BI từ CSV |
| `powerbi_template/` | Cấu trúc Power BI nền; cần giữ khi dựng lại PBIP |
| `notebook.py` | Tạo và chạy notebook, xuất HTML và ghi nguồn dữ liệu |
| `verify_delivery.py` | Đối chiếu dữ liệu gốc, bảng kết quả, notebook và biểu đồ slide |
| `pipeline.py` | Điều phối các bước, ghi nhật ký và dừng khi có lỗi |
| `package_delivery.py` | Tạo ZIP, manifest và kiểm tra CRC/SHA256 |
| `export_word_pdf.ps1` | Cập nhật mục lục và xuất bản Word hiện có sang PDF |
| `export_slides.ps1` | Xuất ảnh slide bằng PowerPoint để kiểm tra |

## Các lệnh

```powershell
python run.py doctor
python run.py build
python run.py check
python run.py powerbi
python run.py package
```

`build` dùng snapshot đã lưu, tạo lại dữ liệu, bảng, hình, minh chứng và dashboard web. Chỉ `build --acquire` gọi bước thu thập. Báo cáo Word, nội dung Markdown, bìa và kết luận đã biên tập được giữ nguyên. `build --pdf word` xuất PDF từ Word hiện có trên Windows; `build --notebook` chạy thêm notebook.

Lệnh `powerbi` tạo lại PBIP và có thể ghi đè chỉnh sửa tay trong PBIP; đóng dự án trong Desktop trước khi chạy. PBIX đã nhập dữ liệu được giữ nguyên, cập nhật bằng Refresh và Save As trong Power BI Desktop. PowerPoint chỉnh sửa trực tiếp; sau khi đổi số liệu cần cập nhật slide rồi chạy `check`.

Để chạy lại sau khi giải nén, giữ nguyên cấu trúc `src/`, `data/`, `outputs/`, `notebooks/`, `slides/`, `reports/`, `tests/` và `run.py`. `src/` riêng lẻ không chứa dữ liệu nguồn. Nhật ký nằm trong `work/` và không đưa vào ZIP.
