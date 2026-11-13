| <br><br>HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG<br>KHOA VIỄN THÔNG<br>------------------------------<br>MÔN HỌC TRỰC QUAN HÓA DỮ LIỆU |
| --- |
| <br> |
| TÊN TIỂU LUẬN:<br>Phân tích xu hướng già hóa dân số Việt Nam trong mối liên hệ với phát triển kinh tế và lao động giai đoạn 1991–2023<br><br><br>Giảng viên bộ môn: TS.Vũ Thị Thúy Hà<br>Sinh viên thực hiện: Nguyễn Hoàng Long<br>Mã Sinh Viên: B23DCKD039<br><br><br><br><br><br><br>Hà Nội – 2026 |

MỤC LỤC

# DANH MỤC HÌNH

Hình 01 Cơ cấu tuổi của Việt Nam

Hình 02 Quy mô và tỷ trọng dân số cao tuổi

Hình 03 Phụ thuộc nhân khẩu học

Hình 04 Già hóa trong bức tranh toàn cầu

Hình 05 Mức già hóa và thay đổi đầu kỳ cuối kỳ

Hình 06 Tốc độ thay đổi qua các giai đoạn

Hình 07 Mức sinh như bối cảnh nhân khẩu học

Hình 08 Già hóa và mức phát triển kinh tế

Hình 09 Quỹ đạo GDP/người và già hóa

Hình 10 So sánh tại mốc già hóa 10 phần trăm

Hình 11 Cơ cấu tuổi và lao động ở Việt Nam

Hình 12 Quan hệ giữa cơ cấu tuổi và việc làm

# DANH MỤC ẢNH

Ảnh 01 Trang dữ liệu World Bank về dân số 65+ của Việt Nam

Ảnh 02 Quy trình thu thập và xử lý dữ liệu

Ảnh 03 Từ phản hồi API đến bản ghi dữ liệu chuẩn

Ảnh 04 Tính các chỉ số từ dữ liệu Việt Nam năm 2023

Ảnh 05 Bảng dữ liệu chuẩn master.csv trong Visual Studio Code

Ảnh 06 Dashboard trang Tổng quan

Ảnh 07 Dashboard trang Diễn biến già hóa

Ảnh 08 Dashboard trang Già hóa và kinh tế

Ảnh 09 Dashboard trang Cơ cấu tuổi và lao động

# DANH MỤC BẢNG

Bảng 1.1 Các chỉ tiêu nguồn

Bảng 1.2 Các cách so sánh dữ liệu

Bảng 2.1 Độ phủ dữ liệu

Bảng 2.2 Bản ghi dữ liệu chuẩn Việt Nam năm 2023

Bảng 3.1 Kiểm tra độ nhạy

Bảng 3.2 Nội dung dashboard

Bảng 3.3 Tổng hợp câu trả lời nghiên cứu

Ký hiệu: WDI là World Development Indicators; PPP là sức mua tương đương; LFPR là tỷ lệ tham gia lực lượng lao động; ILO là Tổ chức Lao động Quốc tế; n là cỡ mẫu nền kinh tế; CSV là tệp dữ liệu bảng. Nhóm 65+ gồm người từ 65 tuổi trở lên.

# LỜI MỞ ĐẦU

## Lý do chọn đề tài và mục tiêu

Già hóa dân số đang đặt ra những câu hỏi về chăm sóc sức khỏe, an sinh và việc làm tại Việt Nam. Các tài liệu của UNFPA và WHO cho thấy cần xem xét cả sự thay đổi cơ cấu tuổi lẫn điều kiện sống của người cao tuổi [14–15]. Vì vậy, đề tài được chọn để tìm hiểu Việt Nam đang già hóa như thế nào và đặt sự thay đổi này trong bối cảnh kinh tế, lao động và so sánh quốc tế.

Đề tài “Phân tích xu hướng già hóa dân số Việt Nam trong mối liên hệ với phát triển kinh tế và lao động giai đoạn 1991–2023” sử dụng nguồn số liệu công khai, chuỗi thời gian dài và nhiều trường hợp đối chiếu. Mục tiêu là làm rõ xu hướng già hóa của Việt Nam, đặt xu hướng này bên cạnh mức phát triển kinh tế và hoạt động lao động, đồng thời trình bày kết quả bằng biểu đồ và dashboard. Đây là phân tích mô tả; báo cáo không xây dựng mô hình dự báo hoặc xác định tác động nhân quả.

## Câu hỏi nghiên cứu

Báo cáo tìm hiểu bốn vấn đề: cơ cấu tuổi và quy mô người cao tuổi của Việt Nam thay đổi như thế nào; Việt Nam nằm ở đâu khi so sánh với các nền kinh tế khác; già hóa có liên hệ gì với GDP/người; và sự thay đổi cơ cấu tuổi có đi cùng diễn biến tham gia lao động, việc làm hay không. Những câu hỏi này quyết định loại biểu đồ và phạm vi dữ liệu sử dụng.

## Phạm vi và cấu trúc

Dữ liệu gồm 217 nền kinh tế trong giai đoạn 1991–2023, tương ứng 7.161 quan sát theo nền kinh tế và năm. Việt Nam là trường hợp nghiên cứu chính. Thái Lan, Indonesia, Nhật Bản và Hàn Quốc được chọn để đối chiếu các quỹ đạo khác nhau trong Đông Nam Á và Đông Á; nhóm này không đại diện cho toàn thế giới. Khi phân tích phân bố quốc tế, báo cáo sử dụng tất cả nền kinh tế có đủ biến cần thiết.

Phạm vi kết thúc ở năm 2023 nhằm giữ một khoảng thời gian thống nhất giữa các phân tích. Các kết quả trong báo cáo phản ánh bộ dữ liệu đã lưu vào tháng 9/2026. Chương 1 giới thiệu nguồn dữ liệu và cơ sở lý thuyết. Chương 2 trình bày việc thu thập, làm sạch và tạo bảng dữ liệu chuẩn. Chương 3 phân tích 12 biểu đồ và giới thiệu bốn trang dashboard, sau đó là kết luận và tài liệu tham khảo.

# CHƯƠNG I. LÝ THUYẾT VÀ TÌM HIỂU DỮ LIỆU

## 1.1 Nguồn dữ liệu và các chỉ tiêu nghiên cứu

Đề tài sử dụng bộ dữ liệu World Development Indicators (WDI) của World Bank [1]. Nguồn này tập hợp các thông tin về dân số, kinh tế và lao động, giúp theo dõi Việt Nam qua nhiều năm và đặt kết quả trong bối cảnh quốc tế. Dữ liệu dân số chủ yếu dựa trên nguồn của Liên Hợp Quốc; các chỉ tiêu lao động sử dụng ước tính của Tổ chức Lao động Quốc tế (ILO).

Trang World Bank cho phép chọn quốc gia, xem diễn biến chỉ tiêu và tải dữ liệu. Ảnh 01 giới thiệu trang tỷ trọng dân số 65+ của Việt Nam [1, 5].

Ảnh 01. Trang dữ liệu World Bank về dân số 65+ của Việt Nam

Nguồn: World Bank Open Data. Trang nguồn hiển thị đến năm 2025; dữ liệu phân tích trong báo cáo giới hạn ở 1991–2023.

Bảng 1.1 tóm tắt tám chỉ tiêu thuộc ba nhóm: nhân khẩu học, kinh tế và lao động. Mỗi chỉ tiêu bổ sung một góc nhìn cho câu hỏi nghiên cứu.

Bảng 1.1 Các chỉ tiêu nguồn

| Biến | Ý nghĩa trong nghiên cứu | Đơn vị / mẫu số |
| --- | --- | --- |
| Dân số | Quy mô dân số chung | Người, giữa năm |
| Tuổi 0–14 | Tỷ trọng trẻ em trong dân số | % tổng dân số |
| Tuổi 15–64 | Tỷ trọng nhóm 15–64 trong dân số | % tổng dân số |
| Tuổi 65+ | Mức già hóa dân số | % tổng dân số |
| Tổng tỷ suất sinh | Bối cảnh hình thành các thế hệ trẻ | Con/phụ nữ |
| GDP/người PPP | Bối cảnh phát triển kinh tế | Đô la quốc tế giá 2021/người |
| Tham gia lao động | Mức tham gia hoạt động lao động | % dân số 15+ |
| Có việc làm | Mức dân số có việc làm | % dân số 15+ |

Một phần số liệu là ước tính và có thể được nguồn điều chỉnh về sau [2–10]. Vì vậy, báo cáo sử dụng thống nhất bản dữ liệu lưu tháng 9/2026. Các con số phản ánh tình hình trong phạm vi này, chưa bao quát hoàn cảnh sống của từng người cao tuổi.

Bản đồ sử dụng ranh giới Natural Earth [11]; các tài liệu [13–17] bổ sung bối cảnh già hóa và cơ sở trình bày.

## 1.2 Các khái niệm dùng trong phân tích

### 1.2.1 Già hóa dân số và cơ cấu tuổi

Già hóa dân số là quá trình người cao tuổi chiếm tỷ trọng ngày càng lớn trong dân số. Báo cáo dùng nhóm từ 65 tuổi trở lên, gọi tắt là 65+, theo dữ liệu WDI [5]. Một số tài liệu tại Việt Nam dùng mốc 60 tuổi [13]; hai cách tính khác nhau nên không so sánh trực tiếp các tỷ trọng này.

Cơ cấu tuổi cho biết dân số trẻ hay già hơn, còn quy mô cho biết có bao nhiêu người trong mỗi nhóm. Chẳng hạn, tỷ trọng 65+ của Việt Nam tăng từ 5,49% lên 8,62%, trong khi số người thuộc nhóm này tăng từ 3,67 lên 8,65 triệu. Xem cả hai giúp hiểu rõ hơn mức thay đổi thay vì chỉ nhìn một tỷ lệ.

### 1.2.2 Phụ thuộc nhân khẩu học và hỗ trợ tiềm năng

Tỷ số phụ thuộc đặt trẻ em và người cao tuổi bên cạnh nhóm 15–64 tuổi. Tách hai nhóm giúp thấy cơ cấu dân số đang chuyển từ nhiều trẻ em sang nhiều người cao tuổi như thế nào. Chỉ số hỗ trợ tiềm năng cho biết có bao nhiêu người 15–64 tuổi trên một người 65+. Những chỉ số này mô tả cơ cấu tuổi, chưa cho biết ai thực sự làm việc hay chăm sóc người khác.

### 1.2.3 Mức sinh và GDP bình quân đầu người

Mức sinh cho biết trung bình một phụ nữ sẽ có bao nhiêu con nếu mức sinh theo tuổi của năm đang xét được duy trì suốt tuổi sinh đẻ [6]. Chỉ tiêu này giúp hiểu bối cảnh hình thành các thế hệ trẻ; nó không phải số con thực tế của từng phụ nữ.

GDP bình quân đầu người cho biết mức sản lượng kinh tế tính trên mỗi người. Quy đổi theo sức mua tương đương (PPP) giúp so sánh nơi có mức giá khác nhau; dùng cùng mặt bằng giá năm 2021 giúp theo dõi thay đổi qua thời gian [7]. GDP/người là bối cảnh kinh tế chung, chưa phản ánh riêng thu nhập hay mức sống của người cao tuổi.

### 1.2.4 Tham gia lao động và tỷ lệ có việc làm

Tỷ lệ tham gia lực lượng lao động cho biết bao nhiêu người từ 15 tuổi trở lên đang làm việc hoặc tìm việc; tỷ lệ có việc làm chỉ tính những người đang làm việc [8–10]. Hai chỉ tiêu giúp xem nguồn lực dân số có đi cùng hoạt động lao động hay không. Chúng khác với tỷ trọng nhóm 15–64 tuổi, vốn chỉ mô tả cơ cấu tuổi của toàn dân số.

## 1.3 Cơ sở trực quan hóa và so sánh dữ liệu

### 1.3.1 Biểu đồ và dashboard

Biểu đồ giúp nhận ra những thay đổi khó thấy khi đọc một bảng nhiều con số: xu hướng tăng giảm, thời điểm đổi chiều và khác biệt giữa các nước. Dashboard kết hợp các hình trong một giao diện, cho phép đổi năm hoặc trường hợp so sánh để tìm hiểu sâu hơn.

### 1.3.2 Cách so sánh và giới hạn diễn giải

Ba cách so sánh trong Bảng 1.2 bổ sung cho nhau. Theo dõi nhiều năm cho biết một nước đã thay đổi ra sao; so sánh cùng năm cho biết nước đó đang ở đâu; đối chiếu ở cùng mốc già hóa cho biết bối cảnh kinh tế khi tỷ trọng người cao tuổi đạt mức tương tự.

Bảng 1.2 Các cách so sánh dữ liệu

| Cách so sánh | Điều kiện chung | Nội dung xem xét |
| --- | --- | --- |
| Diễn biến theo thời gian | 1991–2023; cùng nền kinh tế | Xu hướng và nhịp thay đổi |
| Lát cắt giữa các nền kinh tế | Cùng năm 2023 | Vị trí và liên hệ giữa các biến |
| So sánh tại mốc già hóa | Cùng mốc 65+: 8%, 10% hoặc 12% | GDP/người tại lần vượt được quan sát |

Các mốc 8%, 10% và 12% chỉ phục vụ so sánh trong đề tài, không phải tiêu chuẩn xác định một nước đã già hay đã giàu. Khi nói đến trung vị, báo cáo dùng mức ở giữa của các nền kinh tế trong mẫu: một nửa có giá trị thấp hơn và một nửa cao hơn.

Hai chỉ tiêu thay đổi cùng chiều chưa đủ để khẳng định chỉ tiêu này gây ra chỉ tiêu kia. Vì vậy, báo cáo dùng các liên hệ giữa dân số, GDP và lao động để nhận diện vấn đề cần tìm hiểu thêm, đồng thời kiểm tra xem nhận xét có thay đổi khi điều chỉnh mẫu so sánh hay không.

# CHƯƠNG II. THU THẬP LÀM SẠCH VÀ CHUẨN HÓA DỮ LIỆU

## 2.1 Thu thập và lưu dữ liệu nguồn

Đề tài thu thập tám chỉ tiêu WDI bằng Python qua cổng dữ liệu World Bank [1]. Số liệu và thông tin giải thích chỉ tiêu được lưu ngày 21–22/09/2026. Việc giữ cùng một bản dữ liệu giúp các bảng và biểu đồ trong báo cáo nhất quán với nhau.

Trước khi xử lý, dữ liệu tải về được kiểm tra về mức đầy đủ và lưu riêng để có thể đối chiếu khi cần. Mục đích của bước này là bảo đảm kết quả phân tích có căn cứ rõ ràng và có thể kiểm tra lại.

Ảnh 02 tóm tắt các bước từ dữ liệu nguồn đến bảng dùng chung cho biểu đồ và dashboard.

Ảnh 02. Quy trình thu thập và xử lý dữ liệu

Nguồn: Sơ đồ tổng hợp từ quy trình thu thập và xử lý của đề tài.

Dữ liệu gốc được giữ lại để đối chiếu những giá trị đáng chú ý sau xử lý. Bản đồ dùng ranh giới Natural Earth [11], còn các con số về dân số và kinh tế vẫn lấy từ WDI.

## 2.2 Làm sạch và kiểm tra chất lượng

Bước làm sạch giữ đúng phạm vi nghiên cứu: 217 nền kinh tế trong giai đoạn 1991–2023. Có 78 nhóm tổng hợp theo vùng hoặc thu nhập được loại khỏi danh sách so sánh để tránh tính lặp. Mỗi nền kinh tế chỉ có một dòng cho mỗi năm.

Các kiểm tra tập trung vào những điểm có thể làm sai biểu đồ: tỷ lệ vượt giới hạn, dân số hoặc GDP không hợp lệ và cơ cấu tuổi không cộng về gần 100%. Kết quả cho thấy ba nhóm tuổi khớp với tổng dân số, chỉ có sai lệch rất nhỏ do độ chính xác của số liệu.

Ô thiếu dữ liệu được giữ trống. Thay ô trống bằng 0 có thể khiến biểu đồ thể hiện một sự sụt giảm không có thật. Bảng 2.1 cho thấy mức đầy đủ của dữ liệu trong toàn bộ 33 năm.

Bảng 2.1 Độ phủ dữ liệu

| Tiêu chí | Số lượng |
| --- | --- |
| Nền kinh tế | 217 |
| Quốc gia–năm có giá trị nguồn | 7161 |
| Đủ 5 biến nhân khẩu học | 7161 |
| Đủ tỷ trọng 65+ và GDP | 6412 |
| Đủ hai chỉ tiêu lao động | 6167 |
| Đủ cả 8 chỉ tiêu | 5780 |

Toàn bộ 7.161 dòng có đủ dữ liệu nhân khẩu học, nhưng chỉ 5.780 dòng có đủ cả tám chỉ tiêu. Vì vậy, hình về dân số có phạm vi rộng hơn hình kết hợp GDP hoặc lao động. Năm 2023, so sánh già hóa với GDP có 197 nền kinh tế, còn so sánh cơ cấu tuổi với việc làm có 184.

Có 182 trường hợp biến động lớn giữa hai năm được đánh dấu để rà soát. Chúng vẫn được giữ lại vì thay đổi mạnh chưa có nghĩa là số liệu sai; nguyên nhân của từng trường hợp chưa được xác minh đầy đủ.

## 2.3 Chuẩn hóa và ghép các chỉ tiêu

Dữ liệu của tám chỉ tiêu được đưa về một bảng chung. Mỗi dòng gắn với một nền kinh tế và một năm, nhờ đó dân số, GDP và lao động được đặt cạnh nhau đúng thời điểm.

Ảnh 03 đối chiếu số liệu Việt Nam năm 2023 từ nguồn với bản ghi sau chuẩn hóa.

Ảnh 03. Từ phản hồi API đến bản ghi dữ liệu chuẩn

Nguồn: Trích phản hồi API đã lưu và bản ghi tương ứng trong master.csv; World Bank WDI.

Khi ghép bảng, dòng thiếu GDP vẫn được giữ nếu còn dữ liệu dân số. Cách làm này tránh mất những thông tin có ích cho các hình khác. Tên nền kinh tế, vùng và nhóm thu nhập được bổ sung để thuận tiện lựa chọn nhóm so sánh.

Chuẩn hóa giúp các giá trị được đọc theo cùng một cách: dân số tính bằng người, cơ cấu tuổi và lao động tính bằng phần trăm, GDP/người dùng cùng mặt bằng giá. Việc đổi sang triệu người và làm tròn chỉ diễn ra khi trình bày, để phép tính vẫn giữ độ chính xác của nguồn.

Bảng được sắp theo nền kinh tế và năm để dễ theo dõi lịch sử từng trường hợp. Nhờ đó, biểu đồ và dashboard cùng sử dụng một bộ số liệu đã thống nhất.

## 2.4 Tính các biến phục vụ trực quan hóa

Từ tổng dân số và cơ cấu tuổi, đề tài tính thêm số người 65+ và ba tỷ số phụ thuộc. Những chỉ số này làm rõ quy mô dân số cao tuổi và tương quan giữa các nhóm tuổi. Ảnh 04 trình bày ví dụ Việt Nam năm 2023.

Ảnh 04. Tính các chỉ số từ dữ liệu Việt Nam năm 2023

Nguồn: Bảng tính từ giá trị đầy đủ của bản ghi VNM–2023 trong master.csv; World Bank WDI.

Với Việt Nam năm 2023, số người 65+ ước tính là 8,65 triệu. Cứ 100 người thuộc nhóm 15–64 tuổi tương ứng khoảng 35 trẻ em và 13 người 65+. Ví dụ này giúp hình dung cơ cấu tuổi bằng các con số gần gũi hơn.

Dashboard còn bổ sung chỉ số già hóa và hỗ trợ tiềm năng để xem tương quan giữa người cao tuổi, trẻ em và nhóm 15–64 tuổi. Các chỉ số này chưa phản ánh số người thực tế đang làm việc hay trực tiếp chăm sóc người cao tuổi.

## 2.5 Bảng dữ liệu chuẩn sau xử lý

Sau xử lý, bảng dữ liệu chuẩn có 7.161 dòng và 17 cột. Mỗi dòng thể hiện tình hình của một nền kinh tế trong một năm, gồm thông tin nhận diện, tám chỉ tiêu nguồn và bốn chỉ số bổ sung. Đây là đầu vào chung cho toàn bộ hình và dashboard ở Chương 3.

Bảng 2.2 minh họa kết quả xử lý bằng số liệu Việt Nam năm 2023. Các chỉ tiêu dân số, kinh tế và lao động đã được đặt trong cùng một bản ghi, giúp đối chiếu dễ hơn so với các bảng nguồn riêng lẻ.

Bảng 2.2 Bản ghi dữ liệu chuẩn Việt Nam năm 2023

| Biến số | Đơn vị | Giá trị |
| --- | --- | --- |
| Tổng dân số | Người | 100.352.192 |
| Tỷ trọng 0–14 tuổi | % tổng dân số | 23,61 |
| Tỷ trọng 15–64 tuổi | % tổng dân số | 67,77 |
| Tỷ trọng 65+ | % tổng dân số | 8,62 |
| Tổng tỷ suất sinh | Con/phụ nữ | 1,913 |
| GDP/người PPP | Đô la quốc tế giá 2021 | 13.534,80 |
| Tham gia lực lượng lao động | % dân số 15+ | 73,55 |
| Tỷ lệ có việc làm | % dân số 15+ | 72,34 |
| Số người 65+ ước tính | Người | 8.651.529 |
| Phụ thuộc trẻ em | Trên 100 người 15–64 | 34,83 |
| Phụ thuộc tuổi già | Trên 100 người 15–64 | 12,72 |
| Phụ thuộc tổng | Trên 100 người 15–64 | 47,55 |

Nguồn: World Bank WDI và bảng dữ liệu chuẩn của đề tài.

Ảnh 05. Bảng dữ liệu chuẩn master.csv trong Visual Studio Code

Nguồn: Trích master.csv của đề tài, World Bank WDI

Ảnh 05 giới thiệu tệp master.csv được mở trong Visual Studio Code, với tên cột và các bản ghi theo nền kinh tế, năm. Đây là bảng dữ liệu chung dùng để chọn các chỉ tiêu cho từng biểu đồ và dashboard.

# CHƯƠNG III. BIỂU ĐỒ VÀ DASHBOARD TRỰC QUAN HÓA DỮ LIỆU

## 3.1 Lựa chọn biểu đồ và cách tổ chức trình bày

Các hình trong chương trả lời bốn câu hỏi: Việt Nam già hóa như thế nào, đang ở đâu trong bối cảnh quốc tế, già hóa đi cùng phát triển kinh tế ra sao và cơ cấu tuổi liên hệ với lao động đến mức nào. Mỗi loại biểu đồ được chọn để làm rõ một phần của câu trả lời [16].

Việt Nam được theo dõi xuyên suốt, đồng thời đối chiếu với bốn nền kinh tế trong khu vực. Tỷ trọng và số người được xem riêng để phân biệt mức già hóa với quy mô dân số cao tuổi. Nguồn, thời gian và đơn vị được ghi dưới hình để người đọc có thể kiểm tra.

## 3.2 Biểu đồ cơ cấu tuổi và diễn biến già hóa

### 3.2.1 Cơ cấu tuổi của Việt Nam

Hình 01. Cơ cấu tuổi của Việt Nam

Nguồn: World Bank WDI; tác giả tính toán, giai đoạn 1991–2023.

Từ năm 1991 đến năm 2023, tỷ trọng trẻ em giảm từ 38,10% xuống 23,61%, còn tỷ trọng người 65+ tăng từ 5,49% lên 8,62%. Nhóm 15–64 tuổi tăng trong phần lớn giai đoạn, đạt đỉnh 69,90% năm 2012 rồi giảm về 67,77% năm 2023.

Dân số Việt Nam đang chuyển dần sang cơ cấu lớn tuổi hơn. Điểm đáng chú ý là tỷ trọng nhóm 15–64 đã qua mức cao nhất trong chuỗi quan sát. Vì vậy, nhìn riêng chênh lệch năm đầu và năm cuối sẽ bỏ qua sự đổi chiều trong hơn mười năm gần đây.

### 3.2.2 Quy mô và tỷ trọng dân số cao tuổi

Hình 02. Quy mô và tỷ trọng dân số cao tuổi

Nguồn: World Bank WDI; tác giả tính toán, giai đoạn 1991–2023.

Số người 65+ tăng từ 3,67 triệu lên 8,65 triệu, tức hơn gấp đôi trong giai đoạn 1991–2023. Trong khi đó, tỷ trọng của nhóm này tăng 3,13 điểm phần trăm. Hai kết quả cho thấy quy mô dân số cao tuổi thay đổi mạnh hơn điều dễ hình dung nếu chỉ đọc tỷ lệ.

Mức tăng gần 5 triệu người 65+ gắn với cả tổng dân số lớn hơn và cơ cấu tuổi già hơn. Khi xem xét quy mô các dịch vụ hướng đến người cao tuổi, số người là thông tin cần đặt cạnh tỷ trọng. Dữ liệu tuổi chưa cho biết cụ thể ai cần chăm sóc, nhưng đã làm rõ nhóm dân số cần quan tâm ngày càng lớn.

### 3.2.3 Phụ thuộc nhân khẩu học

Hình 03. Phụ thuộc nhân khẩu học

Nguồn: World Bank WDI; tác giả tính toán, giai đoạn 1991–2023.

Tỷ số phụ thuộc tổng giảm từ 77,28 xuống 47,55 người trên 100 người 15–64 tuổi trong toàn kỳ. Tuy nhiên, chỉ số đã chạm mức thấp nhất 43,06 vào năm 2012 rồi tăng trở lại. Thành phần tuổi già chiếm khoảng 89% phần tăng từ năm 2012 đến năm 2023.

Sự thay đổi gần đây chủ yếu nằm ở nhóm cao tuổi. Điều này cho thấy bối cảnh cơ cấu dân số đã khác thời kỳ tỷ trọng trẻ em còn cao. Chỉ số tổng giảm so với năm 1991 không có nghĩa quá trình già hóa đang chậm lại; các tỷ số tuổi cũng chưa đo mức phụ thuộc kinh tế thực tế.

### 3.2.4 Già hóa trong bức tranh toàn cầu

Hình 04. Già hóa trong bức tranh toàn cầu

Nguồn: World Bank WDI; tác giả tính toán, năm 2023.

Tỷ trọng 65+ của Việt Nam là 8,62%, gần mức trung vị 8,01% của 217 nền kinh tế. Việt Nam chưa thuộc nhóm có tỷ trọng cao tuổi cao nhất, trong khi bản đồ cho thấy già hóa diễn ra với mức độ rất khác nhau giữa các nơi.

Đặt Việt Nam trong bối cảnh rộng hơn giúp tránh chỉ so với những nước già hóa cao như Nhật Bản. Vị trí gần giữa phân bố cho biết mức hiện tại, chưa nói hết tốc độ thay đổi của Việt Nam. Bởi vậy, cần xem thêm so sánh theo thời gian ở hai hình tiếp theo.

### 3.2.5 Mức già hóa và thay đổi đầu kỳ cuối kỳ

Hình 05. Mức già hóa và thay đổi đầu kỳ cuối kỳ

Nguồn: World Bank WDI; tác giả tính toán, giai đoạn 1991–2023.

Năm 2023, tỷ trọng 65+ của Việt Nam (8,62%) cao hơn Indonesia (7,05%), nhưng thấp hơn Thái Lan (14,72%), Hàn Quốc (18,34%) và Nhật Bản (29,56%). Trong toàn kỳ, Việt Nam tăng 3,13 điểm phần trăm, trong khi tỷ trọng 65+ tính trên dân số toàn bộ mẫu tăng từ 6,14% lên 9,96%.

Những nước trong cùng khu vực có thể đang ở các giai đoạn rất khác nhau. Nhật Bản giúp hình dung một cơ cấu dân số già hơn, còn Thái Lan và Indonesia tạo thêm các đối chứng gần Việt Nam. Không nên lấy riêng năm nước này để đại diện cho toàn bộ thế giới.

### 3.2.6 Tốc độ thay đổi qua các giai đoạn

Hình 06. Tốc độ thay đổi qua các giai đoạn

Nguồn: World Bank WDI; tác giả tính toán, giai đoạn 1991–2023.

Giai đoạn 2010–2023, tỷ trọng 65+ của Việt Nam tăng bình quân 0,198 điểm phần trăm mỗi năm, cao hơn rõ rệt mức 0,029 của giai đoạn 1991–2010. Hơn 82% mức tăng của cả chuỗi tập trung sau năm 2010. Nhịp tăng gần đây cũng cao hơn trung vị 0,160 của 217 nền kinh tế.

Mức già hóa hiện tại còn tương đối gần giữa phân bố, nhưng tốc độ đã nhanh hơn trước. Đây là phát hiện cần đặt cạnh Hình 04 và Hình 05: tỷ trọng chưa cao không đồng nghĩa sự chuyển dịch đang chậm. Kết quả chưa cho biết nhịp tăng sẽ tiếp tục như thế nào sau năm 2023.

### 3.2.7 Mức sinh như bối cảnh nhân khẩu học

Hình 07. Mức sinh như bối cảnh nhân khẩu học

Nguồn: World Bank WDI; tác giả tính toán, giai đoạn 1991–2023.

Mức sinh của Việt Nam giảm từ 3,52 xuống 1,91 con/phụ nữ trong giai đoạn nghiên cứu. Năm 2023, mức này cao hơn Thái Lan, Nhật Bản và Hàn Quốc, nhưng thấp hơn Indonesia. Các nước đối chiếu cho thấy mức sinh thấp xuất hiện trong những bối cảnh già hóa khác nhau.

Mức sinh giảm giúp hiểu bối cảnh tỷ trọng trẻ em thu hẹp trong dài hạn. Tuy nhiên, việc sinh ít con trong một năm không lập tức làm tăng số người trên 65 tuổi. Quy mô các thế hệ trước, tuổi thọ và di cư cũng liên quan; hình chưa tách được vai trò riêng của từng yếu tố.

### 3.2.8 Đọc các chỉ số già hóa bổ sung

Chỉ số già hóa của Việt Nam tăng từ 14,40 lên 36,52 người 65+ trên 100 trẻ em trong so sánh 1991–2023. Tỷ số hỗ trợ tiềm năng giảm từ 10,28 xuống 7,86 người 15–64 trên một người 65+. Hai cách đo bổ sung cho tỷ trọng 65+ bằng việc đặt nhóm cao tuổi tương quan với trẻ em hoặc với nhóm 15–64.

Các chỉ số được tính từ cùng bảng dữ liệu chuẩn. “Hỗ trợ tiềm năng” chỉ so nhóm tuổi, không đo số người thực sự làm việc, đóng góp quỹ hưu trí hay chăm sóc người khác.

## 3.3 Biểu đồ già hóa và mức phát triển kinh tế

### 3.3.1 Già hóa và mức phát triển kinh tế

Hình 08. Già hóa và mức phát triển kinh tế

Nguồn: World Bank WDI; tác giả tính toán, năm 2023.

Trong 197 nền kinh tế có đủ dữ liệu năm 2023, GDP/người cao thường đi cùng tỷ trọng 65+ cao hơn. Hệ số tương quan khoảng 0,72 trên thang log GDP/người phản ánh xu hướng cùng chiều khá rõ. Việt Nam có GDP/người PPP khoảng 13.535 đô la quốc tế giá 2021 và tỷ trọng 65+ là 8,62%.

Các điểm vẫn phân tán, nên cùng một mức phát triển kinh tế có thể đi kèm những cơ cấu tuổi khác nhau. Hình cho thấy già hóa cần được xem trong bối cảnh phát triển, nhưng chưa chứng minh tăng GDP gây già hóa. GDP bình quân cũng chưa phản ánh thu nhập hay mức bảo đảm đời sống của riêng người cao tuổi [7].

### 3.3.2 Quỹ đạo GDP/người và già hóa

Hình 09. Quỹ đạo GDP/người và già hóa

Nguồn: World Bank WDI; tác giả tính toán, giai đoạn 1991–2023.

GDP/người PPP của Việt Nam tăng từ khoảng 2.561 lên 13.535 đô la quốc tế giá 2021, tương đương 5,29 lần. Trong cùng thời gian, tỷ trọng 65+ tăng 3,13 điểm phần trăm. Quỹ đạo cho thấy phát triển kinh tế và chuyển dịch cơ cấu tuổi diễn ra đồng thời.

Các nước không bắt đầu từ cùng một vị trí: Nhật Bản đã có mức già hóa cao hơn Việt Nam, Thái Lan và Hàn Quốc ngay đầu kỳ. Vì vậy, so sánh GDP cùng năm chỉ cho thấy một phần bối cảnh. Hình tiếp theo đặt các trường hợp cạnh nhau khi tỷ trọng cao tuổi đạt cùng một mốc để bổ sung góc nhìn.

### 3.3.3 So sánh tại mốc già hóa 10 phần trăm

Hình 10. So sánh tại mốc già hóa 10%

Nguồn: World Bank WDI; tác giả tính toán, giai đoạn 1991–2023.

Tại lần đầu quan sát tỷ trọng 65+ đạt hoặc vượt 10%, Hàn Quốc đạt vào năm 2008 với GDP/người PPP khoảng 37.064 đô la quốc tế, còn Thái Lan đạt năm 2015 với khoảng 18.814. Việt Nam chưa đạt mốc này đến năm 2023. Nhật Bản đã ở trên mốc khi chuỗi bắt đầu, nên không có lần vượt để so sánh trong giai đoạn nghiên cứu.

Cùng mốc già hóa có thể đi kèm mức GDP rất khác nhau. Việt Nam vượt mốc 8% năm 2022 với GDP/người khoảng 12.980, cung cấp thêm một điểm đối chiếu nhưng chưa đủ để kết luận “già trước khi giàu”. Các mốc của đề tài là lựa chọn phân tích, và các lần vượt xảy ra trong những năm lịch khác nhau.

### 3.3.4 Độ nhạy của các liên hệ mô tả

Bảng 3.1 Kiểm tra độ nhạy của hai lát cắt năm 2023

| Phân tích và mẫu | n | Pearson | Spearman |
| --- | --- | --- | --- |
| GDP và già hóa; mẫu gốc | 197 | 0,722 | 0,750 |
| GDP và già hóa; cắt hai đuôi 5% | 162 | 0,758 | 0,763 |
| GDP và già hóa; dân số từ 1 triệu | 153 | 0,732 | 0,747 |
| Cơ cấu tuổi và việc làm; mẫu gốc | 184 | 0,081 | 0,067 |
| Cơ cấu tuổi và việc làm; cắt hai đuôi 5% | 148 | 0,016 | 0,067 |
| Cơ cấu tuổi và việc làm; dân số từ 1 triệu | 156 | 0,048 | 0,020 |

Bảng 3.1 cho thấy nhận xét chính vẫn giữ nguyên khi thay đổi cách chọn mẫu: GDP/người có liên hệ cùng chiều khá rõ với già hóa, còn cơ cấu tuổi và việc làm có liên hệ yếu. Điều này làm các nhận xét vững hơn trước những trường hợp quá khác biệt. Hệ số Pearson ở phần GDP được tính trên log GDP/người; các hệ số chỉ mô tả liên hệ, chưa xác định nguyên nhân.

## 3.4 Biểu đồ cơ cấu tuổi và lao động

### 3.4.1 Diễn biến tại Việt Nam

Hình 11. Cơ cấu tuổi và lao động ở Việt Nam

Nguồn: World Bank WDI; tác giả tính toán, giai đoạn 1991–2023.

Tỷ trọng 15–64 tuổi giảm 2,13 điểm phần trăm từ đỉnh năm 2012 đến năm 2023. Riêng giai đoạn 2019–2023, tỷ lệ tham gia lao động giảm 3,07 điểm phần trăm và tỷ lệ có việc làm giảm 2,99 điểm phần trăm. Hai chỉ tiêu lao động không giảm liên tục trong toàn bộ chuỗi.

Cơ cấu tuổi và hoạt động lao động có diễn biến riêng, nên không thể dùng tỷ trọng 15–64 để thay thế cho mức tham gia hay việc làm. Hình gợi ý cần xem thêm ai đang đi học, ai tham gia lao động và công việc thuộc nhóm nào. Dữ liệu hiện có chưa xác định biến động việc làm của riêng người cao tuổi.

### 3.4.2 Lát cắt giữa các nền kinh tế

Hình 12. Quan hệ giữa cơ cấu tuổi và việc làm

Nguồn: World Bank WDI; tác giả tính toán, năm 2023.

Trong 184 nền kinh tế năm 2023, tỷ trọng 15–64 và tỷ lệ có việc làm chỉ có liên hệ rất yếu, với hệ số tương quan khoảng 0,08. Các điểm phân tán rộng: cơ cấu tuổi tương tự vẫn có thể đi cùng mức việc làm khác nhau. Nhận xét này giữ nguyên trong các mẫu kiểm tra ở Bảng 3.1.

Nguồn lực dân số chưa tự động trở thành nguồn lực lao động được sử dụng. Muốn hiểu khác biệt việc làm, cần bổ sung thông tin về trình độ, giới, cơ cấu kinh tế và chất lượng công việc. Hình phục vụ tìm hiểu mối liên hệ, không dùng các ước tính mô hình để xếp hạng thành tích quốc gia [10].

## 3.5 Xây dựng và sử dụng dashboard

Dashboard web gồm bốn trang, sử dụng chung bộ lọc quốc gia, năm và vùng so sánh. Các ảnh dưới đây ghi nhận giao diện với Việt Nam năm 2023. Phần này trình bày thao tác và phản hồi của biểu đồ; bản Power BI sử dụng cùng nguồn dữ liệu được bàn giao trong dự án.

### 3.5.1 Trang Tổng quan

Trên trang Tổng quan, chọn “Quốc gia trọng tâm” để chuyển các thẻ chỉ số và biểu đồ cơ cấu tuổi sang quốc gia cần xem.

Ảnh 06. Dashboard trang Tổng quan

Nguồn: Dashboard web của đề tài; Việt Nam, năm 2023, tất cả vùng.

Kéo thanh “Năm” từ 2023 về 2000: các thẻ chuyển sang giá trị năm 2000, còn biểu đồ cơ cấu tuổi kết thúc ở năm đó. Với Việt Nam, thẻ tỷ trọng 65+ đổi từ 8,62% sang khoảng 5,98%. Thêm hoặc bỏ quốc gia trong nhóm đối chiếu sẽ thêm hoặc bỏ đường ở biểu đồ so sánh phía dưới. Chọn “Vùng so sánh” làm thay mẫu tham chiếu và danh sách 15 nền kinh tế có tỷ trọng 65+ cao trong vùng, đồng thời giữ chuỗi lịch sử quốc gia đã chọn.

### 3.5.2 Trang Diễn biến già hóa

Trang Diễn biến già hóa có thêm các bộ chọn đại lượng, đường so sánh và năm đầu tính tốc độ.

Ảnh 07. Dashboard trang Diễn biến già hóa

Nguồn: Dashboard web của đề tài; Việt Nam, năm 2023, tất cả vùng.

Đổi “Đại lượng theo dõi” từ tỷ trọng 65+ sang số người 65+ hoặc chỉ số già hóa sẽ thay giá trị và đơn vị trên biểu đồ đường. Khi xem tỷ trọng 65+, có thể đổi đường tham chiếu giữa trung vị các nền kinh tế và mức tổng hợp theo dân số; đường nét đứt được tính lại theo vùng chọn. Đổi “Năm đầu tính tốc độ” từ 2010 về 2000 làm biểu đồ tốc độ phía dưới tính lại khoảng 2000 đến năm kết thúc. Nếu năm kết thúc không sau năm đầu, phần này chưa có tốc độ để hiển thị.

### 3.5.3 Trang Già hóa và kinh tế

Trang Già hóa và kinh tế cho phép xem mối liên hệ GDP–già hóa tại một năm và đối chiếu GDP khi đạt mốc già hóa.

Ảnh 08. Dashboard trang Già hóa và kinh tế

Nguồn: Dashboard web của đề tài; Việt Nam, năm 2023, tất cả vùng.

Đổi năm sẽ cập nhật các điểm của biểu đồ phân tán, cỡ mẫu và các thẻ chỉ số; quỹ đạo quốc gia phía dưới kết thúc ở năm vừa chọn. Đổi vùng sẽ giới hạn các điểm vào mẫu của vùng đó. Bấm một điểm để mở lịch sử tỷ trọng 65+ của nền kinh tế tương ứng. Bộ chọn mốc 8%, 10% hoặc 12% làm thay mẫu và GDP tại lần vượt ngưỡng ở phần dưới. Riêng biểu đồ tại mốc luôn dùng giai đoạn 1991–2023, nên không thay đổi chỉ vì kéo thanh năm.

### 3.5.4 Trang Cơ cấu tuổi và lao động

Trang Cơ cấu tuổi và lao động kết hợp biểu đồ phân tán với các chuỗi tham gia lao động, việc làm và tỷ trọng 15–64 tuổi.

Ảnh 09. Dashboard trang Cơ cấu tuổi và lao động

Nguồn: Dashboard web của đề tài; Việt Nam, năm 2023, tất cả vùng.

Chọn quốc gia khác sẽ cập nhật các thẻ chỉ số và hai đường lao động của quốc gia đó. Đổi năm làm biểu đồ phân tán chuyển sang lát cắt mới, còn các chuỗi lịch sử kết thúc ở năm chọn. Đổi vùng làm thay tập điểm và cỡ mẫu trên biểu đồ phân tán; các quốc gia đã chọn để đối chiếu vẫn giữ lịch sử riêng. Thêm hoặc bỏ quốc gia làm thay số đường trên biểu đồ tỷ trọng 15–64 phía dưới. Bấm một điểm để mở lịch sử 65+ của trường hợp đó.

### 3.5.5 Thao tác chung và khôi phục lựa chọn

Nút “Đặt lại” đưa các bộ lọc về Việt Nam, năm 2023, tất cả vùng và nhóm đối chiếu ban đầu gồm Việt Nam, Thái Lan, Indonesia, Nhật Bản, Hàn Quốc. Các bộ chọn riêng trở về tỷ trọng 65+, đường trung vị, năm đầu 2010 và mốc 10%. Trang đang xem được giữ nguyên.

Đưa con trỏ lên đường hoặc điểm để xem giá trị của trường hợp đang xét. Nút “Xem dữ liệu biểu đồ” mở bảng tương ứng với hình và trạng thái bộ lọc hiện tại. Nhờ đó, người xem có thể đối chiếu một nhận xét trên biểu đồ với các giá trị nguồn.

Bảng 3.2 Nội dung dashboard bốn trang

| Trang | Nội dung chính |
| --- | --- |
| Tổng quan | Đổi quốc gia và năm để cập nhật thẻ, cơ cấu tuổi; thêm quốc gia để đổi nhóm đường đối chiếu |
| Diễn biến già hóa | Đổi đại lượng để thay nội dung đường; đổi đường tham chiếu và năm đầu để tính lại so sánh |
| Già hóa và kinh tế | Đổi năm, vùng để cập nhật tập điểm; đổi mốc để tính lại mẫu vượt ngưỡng |
| Cơ cấu tuổi và lao động | Đổi quốc gia để cập nhật chuỗi lao động; đổi năm, vùng để thay lát cắt việc làm |

## 3.6 Diễn giải kết quả và giới hạn trực quan

Bảng 3.3 Câu hỏi nghiên cứu, bằng chứng và ý nghĩa của kết quả

| Câu hỏi | Bằng chứng chính | Ý nghĩa |
| --- | --- | --- |
| Cơ cấu và quy mô đổi ra sao? | 65+ tăng 3,13 điểm phần trăm và 4,98 triệu người; phụ thuộc tăng lại sau 2012. Hình 01–03. | Già hóa thể hiện ở cả cơ cấu và số người; toàn kỳ có thể che xu hướng gần đây. |
| Việt Nam ở đâu? | 8,62% so với trung vị 8,01%; tốc độ 2010–2023 là 0,198 so với trung vị 0,160 điểm phần trăm/năm. Hình 04–06. | Mức hiện tại gần giữa phân bố nhưng nhịp tăng gần đây cao hơn trung vị mẫu. |
| Liên hệ với kinh tế? | GDP/người tăng 5,29 lần; tương quan lát cắt 0,72, n=197. Hình 08–10, Bảng 3.1. | Có liên hệ mô tả dương; chưa chứng minh tăng trưởng gây già hóa hoặc ngược lại. |
| Liên hệ với lao động? | Tương quan cơ cấu tuổi–việc làm 0,08, n=184; mẫu phụ vẫn yếu. Hình 11–12. | Tỷ trọng 15–64 không đủ để suy ra mức huy động lao động hoặc việc làm người cao tuổi. |

Bảng 3.3 tổng hợp các kết quả đã phân tích ở từng hình. Điểm đáng chú ý là mức già hóa và tốc độ già hóa trả lời hai câu hỏi khác nhau: Việt Nam chưa thuộc nhóm có tỷ trọng 65+ cao trong phân bố năm 2023, nhưng nhịp tăng sau 2010 đã rõ hơn giai đoạn trước. Tương tự, tỷ trọng dân số trong tuổi lao động không đủ để giải thích riêng mức tham gia lao động hoặc việc làm.

### 3.6.1 Giới hạn và cách sử dụng kết quả

Dữ liệu tổng hợp theo nền kinh tế chưa cho phép xem xét khác biệt theo giới, địa phương, nghề và sức khỏe. Vì vậy, một tỷ trọng 65+ cao không tự nó xác định mức chi phí y tế, hưu trí hay nhu cầu chăm sóc. WHO cũng nhấn mạnh sự khác nhau về sức khỏe và khả năng hoạt động ở tuổi cao [15]. Các phát hiện trong báo cáo có thể gợi ý câu hỏi cần nghiên cứu thêm, nhưng chưa đủ làm căn cứ cho một quyết định chính sách cụ thể.

Dữ liệu được giới hạn ở giai đoạn 1991–2023 và phiên bản đã lưu. Cỡ mẫu kinh tế, lao động thay đổi theo mức đầy đủ của số liệu; bản đồ chưa hiển thị được 47 nền kinh tế thiếu ranh giới phù hợp. Các giới hạn này cần được cân nhắc khi khái quát kết quả.

# KẾT LUẬN

Kết quả phân tích cho thấy Việt Nam đang chuyển sang cơ cấu dân số lớn tuổi hơn, trong khi GDP bình quân đầu người tăng và hoạt động lao động có diễn biến riêng. Ba kết quả này làm rõ nội dung của đề tài trong phạm vi dữ liệu 1991–2023.

Về xu hướng già hóa, tỷ trọng dân số 65+ tăng từ 5,49% lên 8,62%, còn quy mô tăng từ 3,67 lên 8,65 triệu người. Nhịp tăng rõ hơn sau năm 2010, với bình quân 0,198 điểm phần trăm mỗi năm trong giai đoạn 2010–2023. Mức già hóa năm 2023 của Việt Nam gần trung vị quốc tế, nhưng tốc độ gần đây cao hơn trung vị. Vì vậy, cần xem cả mức hiện tại và tốc độ thay đổi để nhận diện xu hướng.

Về kinh tế, GDP/người PPP giá cố định 2021 của Việt Nam tăng từ khoảng 2.561 lên 13.535 đô la quốc tế, tương đương 5,29 lần. Trong lát cắt 197 nền kinh tế năm 2023, log GDP/người và tỷ trọng 65+ có tương quan dương khoảng 0,72. Già hóa và phát triển kinh tế diễn ra đồng thời ở Việt Nam, nhưng kết quả này chưa chứng minh tăng GDP gây già hóa và chưa đủ để kết luận “già trước khi giàu”.

Về lao động, tỷ trọng dân số 15–64 đạt đỉnh 69,90% năm 2012 rồi giảm còn 67,77% năm 2023. Tỷ lệ tham gia lao động và có việc làm không giảm liên tục trong toàn kỳ. Lát cắt 184 nền kinh tế năm 2023 cho thấy tỷ trọng 15–64 và tỷ lệ có việc làm chỉ có tương quan rất yếu, khoảng 0,08. Cơ cấu tuổi vì vậy chưa đủ để giải thích mức sử dụng lao động; dữ liệu hiện có cũng chưa xác định biến động việc làm của riêng người cao tuổi.

Đề tài đã xây dựng bảng dữ liệu chuẩn và thể hiện các kết quả trên 12 biểu đồ cùng dashboard tương tác. Các hình giúp nhận ra xu hướng, thời điểm đổi chiều và khác biệt giữa các nền kinh tế; bộ lọc cho phép kiểm tra lại kết quả theo năm và nhóm so sánh. Qua đó, báo cáo đáp ứng mục tiêu phân tích của đề tài và yêu cầu trình bày trực quan của môn học. Các kết luận vẫn giới hạn ở dữ liệu tổng hợp và mối liên hệ mô tả.

## Hướng phát triển

Hướng mở rộng phù hợp là bổ sung dữ liệu theo giới, địa phương và nhóm tuổi chi tiết, đồng thời kiểm tra khả năng tiếp cận của dashboard. Những thông tin này giúp tìm hiểu sâu hơn sự khác nhau bên trong Việt Nam và hoàn cảnh của người cao tuổi.

# TÀI LIỆU THAM KHẢO

Dữ liệu WDI được lưu ngày 21–22/09/2026. Các nguồn bổ trợ [13–17] được dùng để làm rõ định nghĩa, bối cảnh và cách trình bày; không ghép số liệu từ các nguồn này vào chuỗi phân tích.

[1] World Bank. World Development Indicators và User Guide to WDI Resources. https://datatopics.worldbank.org/world-development-indicators/user-guide.html

[2] World Bank. Population total. Chỉ tiêu SP.POP.TOTL. https://data.worldbank.org/indicator/SP.POP.TOTL

[3] World Bank. Population ages 0–14 as a percentage of total population. Chỉ tiêu SP.POP.0014.TO.ZS. https://data.worldbank.org/indicator/SP.POP.0014.TO.ZS

[4] World Bank. Population ages 15–64 as a percentage of total population. Chỉ tiêu SP.POP.1564.TO.ZS. https://data.worldbank.org/indicator/SP.POP.1564.TO.ZS

[5] World Bank. Population ages 65 and above as a percentage of total population. Chỉ tiêu SP.POP.65UP.TO.ZS. https://data.worldbank.org/indicator/SP.POP.65UP.TO.ZS

[6] World Bank. Fertility rate total. Chỉ tiêu SP.DYN.TFRT.IN. https://data.worldbank.org/indicator/SP.DYN.TFRT.IN

[7] World Bank. GDP per capita PPP in constant 2021 international dollars. Chỉ tiêu NY.GDP.PCAP.PP.KD. https://data.worldbank.org/indicator/NY.GDP.PCAP.PP.KD

[8] World Bank. Labor force participation rate total ages 15 and above modeled ILO estimate. Chỉ tiêu SL.TLF.CACT.ZS. https://data.worldbank.org/indicator/SL.TLF.CACT.ZS

[9] World Bank. Employment to population ratio ages 15 and above modeled ILO estimate. Chỉ tiêu SL.EMP.TOTL.SP.ZS. https://data.worldbank.org/indicator/SL.EMP.TOTL.SP.ZS

[10] World Bank. Metadata Glossary for employment to population ratio. https://databank.worldbank.org/metadataglossary/world-development-indicators/series/SL.EMP.TOTL.SP.ZS

[11] Natural Earth. Admin 0 Countries scale 1 to 110 million. https://www.naturalearthdata.com/downloads/110m-cultural-vectors/110m-admin-0-countries/ ; điều khoản: https://www.naturalearthdata.com/about/terms-of-use/

[12] World Bank. Summary terms of use. https://data.worldbank.org/summary-terms-of-use

[13] VNCA, với hỗ trợ UNFPA (2019). Towards a Comprehensive National Policy for an Ageing Viet Nam. Hà Nội, tháng 3; tr. 6, 14–22. https://vietnam.un.org/sites/default/files/2019-08/Toward%20a%20comprehensive%20ageing%20policy_ENG_0.pdf

[14] UNFPA Việt Nam (2021). Population Ageing & Projections of Older Population. Dựa trên Tổng điều tra dân số và nhà ở 2019; công bố 01/11/2021. https://vietnam.unfpa.org/en/publications/population-ageing-projections-older-population

[15] WHO (2025). Ageing and health. Fact sheet, 01/10/2025. https://www.who.int/news-room/fact-sheets/detail/ageing-and-health

[16] Government Analysis Function (2022). Data visualisation: charts. https://analysisfunction.civilservice.gov.uk/policy-store/data-visualisation-charts/

[17] Government Analysis Function (2026). Data visualisation: testing dashboards for design and accessibility. Công bố 06/02/2026. https://analysisfunction.civilservice.gov.uk/policy-store/data-visualisation-testing-dashboards-for-design-and-accessibility/
