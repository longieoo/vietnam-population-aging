# Báo cáo chất lượng dữ liệu

{
  "snapshot_id": "f802111fa64f0c25",
  "economies": 217,
  "meaningful_rows": 7161,
  "complete_age_shares": 7161,
  "complete_demographic_rows": 7161,
  "aging_gdp_rows": 6412,
  "working_age_employment_rows": 6167,
  "labor_both_rows": 6167,
  "all_eight_complete_rows": 5780,
  "year_min": 1991,
  "year_max": 2023,
  "aggregate_entities_excluded": 78,
  "empty_eligible_entities": [],
  "age_sum_max_absolute_error_pp": 0.00014273642860018754,
  "age_sum_tolerance_pp": 0.15,
  "range_errors": [],
  "source_checks": 16,
  "price_base": 2021
}

Pipeline tải 98 phản hồi/tệp có dấu thời gian và SHA256, kiểm tra số trang và tổng số dòng theo header API. Bảng metadata loại 78 thực thể tổng hợp bằng trường region. Khóa iso3–year là duy nhất; các phép nối chỉ tiêu kiểm tra quan hệ một–một, nối metadata kiểm tra nhiều–một.

Tất cả 7161 dòng có đủ dân số, ba nhóm tuổi và mức sinh. GDP thiếu 749 dòng (10,46%); mỗi chuỗi lao động thiếu 994 dòng (13,88%). Không thay thiếu bằng 0, không nội suy và không xóa toàn bộ dòng chỉ vì thiếu GDP hoặc lao động. Số quan sát của từng hình vì vậy khác nhau.

Kiểm tra miền giá trị không phát hiện vi phạm trong bộ quy tắc đã đặt. Sai lệch lớn nhất của tổng ba tỷ trọng tuổi so với 100 là 0,000143 điểm phần trăm, nhỏ hơn dung sai 0,15. Tổng cộng 16 giá trị Việt Nam ở 1991/2023 được đối chiếu với truy vấn quốc gia riêng và khớp.

Có 182 biến động vượt ngưỡng rà soát; không có trường hợp của Việt Nam. Danh sách giữ nguyên để kiểm toán, không tự coi là lỗi hoặc loại ngoại lệ. Chưa có xác minh sự kiện riêng cho mọi cờ toàn cầu. Các kiểm tra độ nhạy của hai lát cắt đánh giá ảnh hưởng của đuôi phân bố mà không thay đổi bảng chính.

Chi tiết thiếu dữ liệu: outputs/tables/missingness_indicator.csv, missingness_iso3.csv, missingness_year.csv. Tỷ lệ thiếu tính trên các dòng có giá trị nguồn trong bảng chính.

Cờ biến động: tuổi 0–14 và 15–64 >2 đpt/năm; 65+ >1,5 đpt; lao động >5 đpt; mức sinh >0,5 con/phụ nữ; GDP thực/người >20%/năm. Đây là ngưỡng rà soát do dự án đặt, không phải kiểm định điểm gãy. Giữ nguyên mọi cờ; chưa xác minh nguyên nhân từng sự kiện.

Bản đồ: 47 nền kinh tế không có hình học phù hợp; xem map_data_without_geometry.csv. ISO_A3_EH được ưu tiên, fallback ADM0_A3 và KOS→XKX. Không gộp Đài Loan vào Trung Quốc hoặc tô giá trị thay thế cho lãnh thổ không có mã khớp.