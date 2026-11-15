# Kịch bản thuyết trình — khoảng 20 phút

Theo [bộ slide Canva 20 trang](https://www.canva.com/d/DNbsAZLx2iAkTnS). Thời lượng dưới đây là phân bổ để luyện tập, không phải thời gian nói đã đo. Trang 18 dành khoảng một phút cho thao tác dashboard.

## Slide 1 — Già hóa dân số Việt Nam

Thời lượng mục tiêu: 30 giây. Em xin trình bày đề tài Phân tích xu hướng già hóa dân số Việt Nam trong mối liên hệ với phát triển kinh tế và lao động giai đoạn 1991–2023. Bài trình bày đi từ cách em thu thập và chuẩn hóa dữ liệu đến lựa chọn biểu đồ, kết quả phân tích và sản phẩm dashboard. Mục tiêu là thể hiện cả kết quả lẫn quy trình thực hiện. Nguồn kiểm chứng: báo cáo cuối của đề tài; data/processed/master.csv; outputs/tables. Dữ liệu WDI lưu tháng 9/2026, không bổ sung quan sát sau năm 2023.

## Slide 2 — Bốn câu hỏi dẫn dắt phân tích

Thời lượng mục tiêu: 45 giây. Em chọn đề tài vì quá trình già hóa thể hiện qua nhiều chỉ tiêu và khó nhận ra đầy đủ nếu chỉ đọc bảng. Có bốn câu hỏi: xu hướng trong nước, vị trí quốc tế, liên hệ kinh tế và liên hệ lao động. Câu hỏi nghiên cứu quyết định phép so sánh và loại biểu đồ. Bài thực hiện phân tích mô tả, không xây dựng mô hình dự báo hay xác định tác động nhân quả. Nguồn kiểm chứng: báo cáo cuối của đề tài; data/processed/master.csv; outputs/tables. Dữ liệu WDI lưu tháng 9/2026, không bổ sung quan sát sau năm 2023.

## Slide 3 — Quy trình thực hiện và sản phẩm

Thời lượng mục tiêu: 55 giây. Đây là phạm vi công việc em đã triển khai. Em lưu dữ liệu nguồn, xây dựng bảng chung thay vì làm từng biểu đồ từ những bảng rời rạc. Từ bảng này em tạo 12 hình, dashboard web và mô hình Power BI. Mã được chia theo bước: acquire thu thập, prepare xử lý, analyze tính toán, visualize vẽ hình. Notebook và các bảng số liệu giúp truy ngược kết quả. Nguồn kiểm chứng: báo cáo cuối của đề tài; data/processed/master.csv; outputs/tables. Dữ liệu WDI lưu tháng 9/2026, không bổ sung quan sát sau năm 2023.

## Slide 4 — Nguồn dữ liệu World Bank

Thời lượng mục tiêu: 55 giây. Em sử dụng World Development Indicators của World Bank. Dữ liệu dân số dựa trên các nguồn nhân khẩu học, trong đó có Liên Hợp Quốc; lao động sử dụng hai chỉ tiêu ILO mô hình. WDI tạo điều kiện dùng mã chỉ tiêu, định nghĩa và đơn vị thống nhất. Ảnh chụp giới thiệu nơi lấy dữ liệu, không phải là dữ liệu em nhập tay. Dù trang nguồn có các năm mới hơn, phạm vi phân tích cố định đến năm 2023. Nguồn kiểm chứng: báo cáo cuối của đề tài; data/processed/master.csv; outputs/tables. Dữ liệu WDI lưu tháng 9/2026, không bổ sung quan sát sau năm 2023.

## Slide 5 — Tám chỉ tiêu nguồn, ba nhóm nội dung

Thời lượng mục tiêu: 60 giây. Em dùng Python để gọi API World Bank, tải riêng từng chỉ tiêu và danh mục nền kinh tế. API trả về JSON có phân trang nên thư mục raw có nhiều tệp cho cùng một biến; chúng không phải các bộ dữ liệu trùng nhau. Biên nhận lưu thời điểm, địa chỉ nguồn và SHA256. Em kiểm tra đủ trang và số bản ghi trước khi ghép. Các dữ liệu và metadata được lưu ngày 21–22 tháng 9 năm 2026. Nguồn kiểm chứng: báo cáo cuối của đề tài; data/processed/master.csv; outputs/tables. Dữ liệu WDI lưu tháng 9/2026, không bổ sung quan sát sau năm 2023.

## Slide 6 — Làm sạch để bảo đảm tính nhất quán

Thời lượng mục tiêu: 65 giây. Bước đầu là dùng metadata để loại vùng hoặc nhóm thu nhập vì chúng có thể chồng lặp với các nền kinh tế thành viên. Sau đó kiểm tra khóa mã nền kinh tế và năm, kiểu dữ liệu, giới hạn tỷ lệ và tổng ba nhóm tuổi gần 100%. Dữ liệu thiếu được giữ trống, không tự nội suy. Em đánh dấu 182 trường hợp biến động mạnh giữa hai năm để rà soát, nhưng không tự xóa vì biến động lớn chưa đủ để coi là sai. Độ phủ nhân khẩu học tốt hơn kinh tế và lao động. Nguồn kiểm chứng: báo cáo cuối của đề tài; data/processed/master.csv; outputs/tables. Dữ liệu WDI lưu tháng 9/2026, không bổ sung quan sát sau năm 2023.

## Slide 7 — Ghép dữ liệu theo mã và năm

Thời lượng mục tiêu: 60 giây. Mỗi chỉ tiêu ban đầu nằm trong một tập phản hồi riêng. Em đưa mã nền kinh tế về iso3, năm về số nguyên và giá trị về kiểu số. Các bảng được nối ngoài theo hai khóa với kiểm tra một–một. Nếu GDP bị thiếu nhưng dân số còn thì dòng vẫn được giữ; biểu đồ GDP sẽ chọn mẫu đủ hai biến khi phân tích. Tên nước, vùng và nhóm thu nhập được bổ sung để lọc. Giá trị thiếu không làm mất những dữ liệu hợp lệ ở hình khác. Nguồn kiểm chứng: báo cáo cuối của đề tài; data/processed/master.csv; outputs/tables. Dữ liệu WDI lưu tháng 9/2026, không bổ sung quan sát sau năm 2023.

## Slide 8 — Bảng dữ liệu chuẩn sau xử lý

Thời lượng mục tiêu: 65 giây. Đây là năm dòng thực của Việt Nam trong master, không phải số minh họa tự tạo. Bảng gồm mã, năm, tên, vùng, nhóm thu nhập, tám chỉ tiêu nguồn và bốn biến dẫn xuất. Số người 65+ bằng dân số nhân tỷ trọng rồi chia 100. Phụ thuộc trẻ em, tuổi già và tổng tính trên nhóm 15–64. Các phép tính giữ độ chính xác nguồn; bảng trình bày mới làm tròn. Từ cùng bảng này em chọn các cột cần cho biểu đồ, web và Power BI. Nguồn kiểm chứng: báo cáo cuối của đề tài; data/processed/master.csv; outputs/tables. Dữ liệu WDI lưu tháng 9/2026, không bổ sung quan sát sau năm 2023.

## Slide 9 — Chọn biểu đồ theo câu hỏi nghiên cứu

Thời lượng mục tiêu: 55 giây. Ở môn Trực quan hóa dữ liệu, quyết định quan trọng là hình nào phù hợp với câu hỏi. Em tạo 12 biểu đồ PNG và SVG, kèm CSV từng hình. Hình diện tích dùng cho cơ cấu; đường cho lịch sử; phân tán cho liên hệ. Bản đồ giúp nhận diện vị trí địa lý nhưng diện tích lãnh thổ không phải trọng số thống kê. Không cố đưa cả 12 hình vào bài nói; em chọn những hình trả lời trực tiếp các câu hỏi chính. Nguồn kiểm chứng: báo cáo cuối của đề tài; data/processed/master.csv; outputs/tables. Dữ liệu WDI lưu tháng 9/2026, không bổ sung quan sát sau năm 2023.

## Slide 10 — Cơ cấu tuổi chuyển dần về nhóm lớn tuổi

Thời lượng mục tiêu: 60 giây. Hình diện tích cho thấy ba nhóm tuổi trong cùng tổng dân số. Vùng trẻ em thu hẹp, vùng cao tuổi mở rộng. Nhóm 15–64 tăng khi so hai đầu kỳ nhưng đã đạt đỉnh khoảng 69,90% năm 2012 rồi về 67,77% năm 2023. Điểm cần rút ra là cơ cấu đã đổi chiều trong hơn mười năm gần đây. Hình đo tỷ trọng, vì vậy cần xem thêm số người ở slide sau. Nguồn kiểm chứng: báo cáo cuối của đề tài; data/processed/master.csv; outputs/tables. Dữ liệu WDI lưu tháng 9/2026, không bổ sung quan sát sau năm 2023.

## Slide 11 — Quy mô cao tuổi tăng hơn gấp đôi

Thời lượng mục tiêu: 60 giây. Số người cao tuổi tăng hơn gấp đôi, trong khi tỷ trọng tăng 3,13 điểm phần trăm. Hai biểu đồ tách đơn vị triệu người và phần trăm để không nhầm quy mô với cơ cấu. Nhịp tăng tỷ trọng giai đoạn 2010–2023 lớn hơn trước 2010; khoảng 82,2% mức tăng toàn kỳ tập trung trong giai đoạn sau. Dữ liệu chỉ thể hiện quy mô nhóm dân số, chưa đo trực tiếp nhu cầu chăm sóc hay hoàn cảnh từng người. Nguồn kiểm chứng: báo cáo cuối của đề tài; data/processed/master.csv; outputs/tables. Dữ liệu WDI lưu tháng 9/2026, không bổ sung quan sát sau năm 2023.

## Slide 12 — Phụ thuộc tổng tăng lại sau năm 2012

Thời lượng mục tiêu: 60 giây. Phụ thuộc tổng giảm trong toàn kỳ nhưng chạm đáy năm 2012 rồi tăng lại. Nếu chỉ nêu giảm từ 77,28 xuống 47,55 sẽ bỏ qua đổi chiều này. Ba đường tách phần trẻ em và phần cao tuổi; phần tuổi già chiếm phần lớn mức tăng gần đây. Đây là một cách phân bổ số học theo nhóm tuổi, không chứng minh nguyên nhân hoặc gánh nặng tài chính thực tế. Nguồn kiểm chứng: báo cáo cuối của đề tài; data/processed/master.csv; outputs/tables. Dữ liệu WDI lưu tháng 9/2026, không bổ sung quan sát sau năm 2023.

## Slide 13 — Việt Nam trong so sánh quốc tế

Thời lượng mục tiêu: 60 giây. Hình trái so hai đầu kỳ của nhóm đối chiếu, hình phải xem phân bố mức thay đổi ở 217 nền kinh tế. Việt Nam có mức già hóa thấp hơn Thái Lan, Hàn Quốc, Nhật Bản nhưng cao hơn Indonesia trong năm 2023. Việt Nam gần trung vị quốc tế về mức hiện tại, còn nhịp tăng gần đây đã nhanh hơn giai đoạn trước. Năm nước được chọn có chủ đích, không đại diện cho mọi nền kinh tế. Báo cáo còn có bản đồ để bổ sung vị trí địa lý. Nguồn kiểm chứng: báo cáo cuối của đề tài; data/processed/master.csv; outputs/tables. Dữ liệu WDI lưu tháng 9/2026, không bổ sung quan sát sau năm 2023.

## Slide 14 — GDP/người và già hóa có liên hệ dương

Thời lượng mục tiêu: 65 giây. Mỗi điểm là một nền kinh tế có đủ GDP và tỷ trọng 65+ năm 2023. GDP/người là sản lượng bình quân quy đổi theo sức mua, không phải tiền thu nhập thực nhận của người cao tuổi. Thang log giúp đọc các giá trị chênh lệch lớn. Hệ số Pearson trên log GDP khoảng 0,72 cho thấy liên hệ dương. Các điểm vẫn phân tán, và GDP/người tăng cùng già hóa ở Việt Nam chưa đủ để kết luận tăng GDP gây già hóa hoặc ngược lại. Nguồn kiểm chứng: báo cáo cuối của đề tài; data/processed/master.csv; outputs/tables. Dữ liệu WDI lưu tháng 9/2026, không bổ sung quan sát sau năm 2023.

## Slide 15 — Đối chiếu GDP tại cùng mốc già hóa

Thời lượng mục tiêu: 60 giây. Phần này bổ sung góc nhìn so với lát cắt cùng năm: so GDP khi tỷ trọng cao tuổi ở mức tương đương. Việt Nam chưa đạt 10% trong cửa sổ quan sát nên không tự gán năm hay GDP tại mốc. Nhật Bản đã ở trên mốc ngay đầu chuỗi, không coi năm 1991 là năm vượt. Đổi sang 8% thì Việt Nam có lần vượt quan sát năm 2022, nhưng mốc 12% chưa đạt. Các ngưỡng là lựa chọn phân tích, chưa đủ để khẳng định già trước khi giàu. Nguồn kiểm chứng: báo cáo cuối của đề tài; data/processed/master.csv; outputs/tables. Dữ liệu WDI lưu tháng 9/2026, không bổ sung quan sát sau năm 2023.

## Slide 16 — Cơ cấu tuổi chưa đủ để giải thích việc làm

Thời lượng mục tiêu: 65 giây. Các điểm phân tán rộng nên cơ cấu tuổi tương tự có thể đi cùng mức việc làm khác nhau. Mẫu số của tỷ trọng 15–64 là tổng dân số, trong khi hai tỷ lệ lao động dùng dân số 15+. Do đó không cộng ba tỷ lệ và không lấy một trừ tỷ trọng tuổi lao động để tính thất nghiệp. Riêng Việt Nam, nhóm 15–64 giảm sau đỉnh 2012; giai đoạn 2019–2023 tỷ lệ tham gia và việc làm cùng giảm nhưng chưa quy được nguyên nhân cho già hóa. Chưa suy ra việc làm của riêng người cao tuổi. Nguồn kiểm chứng: báo cáo cuối của đề tài; data/processed/master.csv; outputs/tables. Dữ liệu WDI lưu tháng 9/2026, không bổ sung quan sát sau năm 2023.

## Slide 17 — Dashboard web để kiểm tra kết quả

Thời lượng mục tiêu: 75 giây. Đây là ảnh thật của dashboard web đã xây dựng từ cùng master. Trang Tổng quan hiển thị các chỉ số và cơ cấu tuổi. Trang Diễn biến già hóa đổi giữa tỷ trọng 65+, số người cao tuổi và chỉ số già hóa; còn có benchmark vùng và năm đầu tính tốc độ. Hai trang còn lại phân tích kinh tế và lao động. Mô hình tính trong dashboard_model.js, tương tác trong dashboard_app.js; explore.py đóng gói thành một tệp HTML mở ngoại tuyến. Khi đổi bộ lọc, cả nội dung biểu đồ và mẫu liên quan được tính lại. Nguồn kiểm chứng: báo cáo cuối của đề tài; data/processed/master.csv; outputs/tables. Dữ liệu WDI lưu tháng 9/2026, không bổ sung quan sát sau năm 2023.

## Slide 18 — Power BI và kịch bản trình diễn

Thời lượng mục tiêu: 100 giây. Ngoài web, em tạo bản Power BI gồm sáu trang với biểu đồ native, mô hình import và bộ lọc. PBIX đã nhúng dữ liệu; PBIP giữ mô hình và định nghĩa visual. CSV chính cùng các bảng tốc độ và lần vượt ngưỡng được dùng để import. Demo nên mở sẵn web giống ảnh: Việt Nam năm 2023 có 8,62% người 65+; đổi về 2000 còn khoảng 5,98%, chuỗi lịch sử dừng ở năm chọn. Đổi vùng thay mẫu so sánh quốc tế rồi đặt lại. Nếu demo Power BI, lưu ý thẻ tương quan GDP gốc khác với r trên log GDP ở báo cáo/web; không gọi hai hệ số là cùng một phép tính. Dùng dashboard web cho mạch thuyết trình này để nhất quán với các hình. Bản Power BI có cách bố trí riêng, không phải ảnh minh họa ở slide trước. Nguồn kiểm chứng: báo cáo cuối của đề tài; data/processed/master.csv; outputs/tables. Dữ liệu WDI lưu tháng 9/2026, không bổ sung quan sát sau năm 2023.

## Slide 19 — Kiểm chứng để kết quả có thể đối chiếu

Thời lượng mục tiêu: 65 giây. Để kết quả có thể kiểm tra, mỗi hình có CSV dữ liệu, notebook ghi snapshot và hash của master. Kiểm tra đối chiếu 57.288 ô của tám biến với nguồn và bốn công thức dẫn xuất. Có 16 giá trị kiểm tra nguồn ở Việt Nam, 21 kiểm thử Python, cùng kiểm tra logic JavaScript. Em đã chạy lại build ngoại tuyến trên bản sao và đối chiếu kết quả. Các kiểm tra này xác nhận tính nhất quán kỹ thuật, không chứng minh suy luận nhân quả. Thư mục nộp chia data, mã nguồn, dashboard và PDF để người xem tìm từng phần. Nguồn kiểm chứng: báo cáo cuối của đề tài; data/processed/master.csv; outputs/tables. Dữ liệu WDI lưu tháng 9/2026, không bổ sung quan sát sau năm 2023.

## Slide 20 — Kết quả chính và hướng phát triển

Thời lượng mục tiêu: 40 giây. Em chốt ba kết quả tương ứng tên đề tài. Già hóa tăng cả số người và tỷ trọng, đặc biệt rõ hơn sau 2010. Kinh tế và già hóa có liên hệ dương trong mẫu quốc tế, còn cơ cấu tuổi và việc làm liên hệ yếu. Về môn học, em đã thực hiện một quy trình từ thu thập đến sản phẩm trực quan có tương tác, kèm mã và dữ liệu để kiểm tra. Các kết quả giới hạn ở dữ liệu tổng hợp và phân tích mô tả; hướng mở rộng là dữ liệu theo tuổi, giới, địa phương và chất lượng việc làm. Em xin cảm ơn cô cùng các bạn và sẵn sàng trao đổi. Nguồn kiểm chứng: báo cáo cuối của đề tài; data/processed/master.csv; outputs/tables. Dữ liệu WDI lưu tháng 9/2026, không bổ sung quan sát sau năm 2023.
