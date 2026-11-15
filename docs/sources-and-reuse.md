# Nguồn và cách sử dụng lại

## Dữ liệu

Nguồn chính là **World Development Indicators (WDI), World Bank, source 2**. Các chỉ tiêu dân số có nguồn gốc từ UN Population Division và cơ quan thống kê quốc gia; chỉ tiêu lao động là ước tính mô hình của ILO. Tên, mã, mẫu số và đơn vị từng chỉ tiêu nằm trong [từ điển dữ liệu](data-dictionary.md).

- [World Bank — điều khoản dữ liệu](https://data.worldbank.org/summary-terms-of-use): CC BY 4.0 kèm các điều kiện và ngoại lệ của nguồn. Kiểm tra metadata từng chỉ tiêu khi sử dụng lại.
- [Natural Earth — điều khoản sử dụng](https://www.naturalearthdata.com/about/terms-of-use/): ranh giới bản đồ thuộc public domain. Ranh giới chỉ phục vụ trực quan hóa, không thể hiện quan điểm về chủ quyền.
- [Plotly.js — MIT](https://github.com/plotly/plotly.js/blob/master/LICENSE): thư viện JavaScript nhúng trong dashboard ngoại tuyến; giữ thông báo bản quyền đi kèm khi phân phối.

Biên nhận tại `data/metadata/source_manifest.json` ghi URL, thời điểm tải và SHA256 của từng tệp nguồn. Đây là **snapshot của đồ án**, không phải dữ liệu cập nhật trực tiếp. Khoảng phân tích cố định là 1991–2023; một số tệp raw có các năm ngoài khoảng này để giữ nguyên phản hồi của nguồn.

Khi dẫn dữ liệu, ghi World Bank WDI, mã chỉ tiêu, giai đoạn và snapshot `f802111fa64f0c25`. Khi dùng kết quả tính toán, dẫn thêm dự án và commit đã sử dụng. Không gán kết quả tính toán của đồ án thành kết luận chính thức của World Bank hoặc ILO.

## Sản phẩm

Mã nguồn, báo cáo, notebook và cấu hình Power BI được lưu để đọc, kiểm chứng và tái tạo đồ án. Các điều khoản của dữ liệu và thư viện bên thứ ba vẫn áp dụng riêng; việc có mã công khai không thay thế các điều khoản đó.

