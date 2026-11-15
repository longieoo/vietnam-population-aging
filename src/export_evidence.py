"""Export seven findings with their source tables and analytical limits."""
import json
import pandas as pd
from config import ROOT, format_number as f
from prepare import require

def main():
    table=ROOT/'outputs/tables'
    s=json.loads((table/'analysis_summary.json').read_text('utf-8'))
    a,b=s['vietnam_1991'],s['vietnam_2023']
    focal=pd.read_csv(table/'focal_series.csv'); end=focal[focal.year.eq(2023)].set_index('iso3')
    vn=focal[focal.iso3.eq('VNM')].set_index('year')
    crossings=pd.read_csv(table/'threshold_crossings.csv')
    # Select by semantic keys so harmless table sorting cannot swap findings.
    indexed = {(row['analysis'], row['restriction']): row for row in s['robustness']}
    require(len(indexed) == len(s['robustness']), 'Duplicate robustness sample keys')
    r = [indexed[(analysis, restriction)]
         for analysis in ['gdp_aging_2023', 'labor_2023']
         for restriction in ['all', 'trim_5_95', 'exclude_population_under_1m']]
    # Findings retain their period, sample, source tables and limitations.
    insights=[
      {'id':'I1','finding':f'Tỷ trọng 65+ của Việt Nam tăng từ {f(a["age_65_plus"])}% lên {f(b["age_65_plus"])}%, tăng {f(s["vietnam_old_share_change_pp"])} điểm phần trăm; số người 65+ tăng từ {f(a["population_65_plus"]/1e6)} lên {f(b["population_65_plus"]/1e6)} triệu.', 'scope':'Việt Nam, 1991 và 2023','sample':'Hai năm đủ dân số và cơ cấu tuổi','tables':'focal_series.csv; analysis_summary.json','figures':'01, 02','interpretation':'Tăng quy mô dân số và thay đổi cơ cấu cùng làm tăng số người cao tuổi.','limitation':'Số người 65+ được suy ra từ hai chỉ tiêu WDI, không phải số đếm độc lập.','implication':'Cần xem đồng thời tỷ trọng và quy mô khi thảo luận nhu cầu chăm sóc.'},
      {'id':'I2','finding':f'Tỷ số phụ thuộc trẻ em giảm từ {f(a["child_dependency"])} xuống {f(b["child_dependency"])}; phụ thuộc tuổi già tăng từ {f(a["old_dependency"])} lên {f(b["old_dependency"])} người trên 100 người 15–64. Tỷ trọng 15–64 đạt đỉnh quan sát năm {s["vietnam_working_age_peak_year"]}.','scope':'Việt Nam, 1991–2023','sample':'33 năm đủ ba nhóm tuổi','tables':'focal_series.csv; analysis_summary.json','figures':'03, 11','interpretation':'Hai thành phần phụ thuộc chuyển động ngược chiều, làm chỉ số tổng cộng che khuất sự thay đổi cơ cấu.','limitation':'Nhóm tuổi không đồng nghĩa với người thực sự phụ thuộc tài chính hoặc đang làm việc.','implication':'Theo dõi riêng phụ thuộc trẻ em và tuổi già thay vì chỉ nhìn tổng số.'},
      {'id':'I3','finding':f'Năm 2023, tỷ trọng 65+ là {f(end.loc["IDN","age_65_plus"])}% ở Indonesia, {f(end.loc["VNM","age_65_plus"])}% ở Việt Nam, {f(end.loc["THA","age_65_plus"])}% ở Thái Lan, {f(end.loc["KOR","age_65_plus"])}% ở Hàn Quốc và {f(end.loc["JPN","age_65_plus"])}% ở Nhật Bản.','scope':'Năm quốc gia, 2023; phân bố toàn cầu 1991/2023','sample':'217 nền kinh tế có đủ hai đầu kỳ cho phân bố','tables':'endpoints.csv; global_distribution.csv','figures':'04, 05, 06','interpretation':'Việt Nam có mức già hóa thấp hơn ba nước Đông Á/Thái Lan trong nhóm đối chiếu, nhưng điều này không loại trừ tốc độ tăng gần đây.','limitation':'Năm nước được chọn có chủ đích và không đại diện cho mọi nền kinh tế.','implication':'Tách mức hiện tại khỏi tốc độ thay đổi khi lựa chọn đối chứng.'},
      {'id':'I4','finding':f'Trong {r[0]["n"]} nền kinh tế năm 2023, tương quan mô tả giữa log GDP/người và tỷ trọng 65+ là {f(r[0]["pearson"])}; sau cắt hai đuôi 5% ở cả hai biến còn {r[1]["n"]} nền kinh tế và hệ số {f(r[1]["pearson"])}.','scope':'Toàn cầu, 2023','sample':'Đủ GDP PPP và tỷ trọng 65+; không trọng số','tables':'gdp_aging_2023.csv; robustness.csv','figures':'08, 09','interpretation':'Liên hệ dương không chỉ xuất hiện do vài điểm cực trị trong lát cắt này.','limitation':'Quan hệ giữa các quốc gia không xác định cơ chế hay tác động nhân quả, và không phải quỹ đạo tất yếu của một nước.','implication':'Dùng kết quả làm bối cảnh so sánh, tiếp tục phân tích lịch sử từng quốc gia.'},
      {'id':'I5','finding':f'Việt Nam chưa đạt 10% đến năm 2023. Ở mốc 8%, lần vượt được quan sát năm 2022 tại GDP/người PPP {f(s["benchmark_sensitivity"][0]["vietnam_gdp"],0)} đô la quốc tế giá 2021; mốc 10% có {s["benchmark_sensitivity"][1]["n"]} nền kinh tế toàn cầu đủ điều kiện so sánh.','scope':'Chuỗi 1991–2023; các mốc 8%, 10%, 12%','sample':'Chỉ lần vượt quan sát từ dưới ngưỡng, không thiếu năm trước đó, có GDP cùng năm','tables':'threshold_crossings.csv; analysis_summary.json','figures':'09, 10','interpretation':'Khả năng so sánh Việt Nam ở cùng mức già hóa phụ thuộc vào mốc được chọn và cửa sổ quan sát.','limitation':'Nhật Bản đã vượt trước đầu chuỗi; GDP tại ngưỡng của Việt Nam ở 10% và 12% chưa quan sát được.','implication':'Không kết luận cứng “già trước khi giàu” từ mốc 10% trong bộ dữ liệu này.'},
      {'id':'I6','finding':f'Tại Việt Nam, tỷ trọng 15–64 giảm từ {f(vn.loc[2012,"age_15_64"])}% năm 2012 xuống {f(b["age_15_64"])}% năm 2023. LFPR giảm từ {f(a["lfpr"])}% năm 1991 xuống {f(b["lfpr"])}%, còn tỷ lệ có việc làm từ {f(a["employment"])}% xuống {f(b["employment"])}%.','scope':'Việt Nam, 1991–2023','sample':'33 năm; hai tỷ lệ lao động cùng chuỗi ILO mô hình','tables':'focal_series.csv','figures':'11','interpretation':'Cơ cấu tuổi và mức tham gia lao động cùng thay đổi, nhưng ba tỷ lệ có mẫu số khác nhau.','limitation':'Không có phân tổ tuổi, giới hoặc chất lượng việc làm để quy nguyên nhân.','implication':'Bước nghiên cứu tiếp theo nên dùng dữ liệu lao động theo tuổi và giới.'},
      {'id':'I7','finding':f'Năm 2023, tương quan giữa tỷ trọng 15–64 và tỷ lệ có việc làm 15+ chỉ là {f(r[3]["pearson"])} (n={r[3]["n"]}); cắt hai đuôi còn {f(r[4]["pearson"])} (n={r[4]["n"]}).','scope':'Toàn cầu, 2023','sample':'Đủ tỷ trọng 15–64 và tỷ lệ có việc làm; không trọng số','tables':'labor_2023.csv; robustness.csv','figures':'12','interpretation':'Lát cắt không cho thấy quan hệ tuyến tính mạnh giữa hai tỷ lệ tổng hợp.','limitation':'Ước tính ILO có bất định và khác biệt đo lường; quan hệ yếu không chứng minh không có cơ chế nhân quả.','implication':'Không suy ra một tỷ trọng dân số trong tuổi lao động cao sẽ tự động tạo tỷ lệ có việc làm cao.'}
    ]
    extra=s['demographic_insights']
    insights[1].update({
      'finding':f'Sau đáy năm 2012, tỷ số phụ thuộc tổng tăng {f(extra["dependency_increase_since_min"])} người trên 100 người 15–64 đến 2023. Thành phần tuổi già tăng {f(extra["old_dependency_increase_since_peak"])} và trẻ em tăng {f(extra["child_dependency_increase_since_peak"])}; tuổi già chiếm {f(extra["old_dependency_fraction_of_rebound_pct"],1)}% mức tăng số học.',
      'interpretation':'Cả hai thành phần tăng trong 2012–2023, khác với hai hướng đối lập khi so 1991 với 2023.',
      'tables':'focal_series.csv; demographic_insights.json'})
    insights[2].update({
      'finding':f'Việt Nam tăng bình quân {f(extra["recent_annual_change_pp"],3)} điểm phần trăm tỷ trọng 65+ mỗi năm trong 2010–2023, so với {f(extra["earlier_annual_change_pp"],3)} trong 1991–2010. Giai đoạn sau 2010 chiếm {f(extra["recent_fraction_of_full_change_pct"],1)}% mức tăng toàn kỳ.',
      'scope':'Việt Nam 1991–2010 và 2010–2023; đối chiếu toàn cầu 2010–2023',
      'interpretation':f'Nhịp tăng mạnh hơn lịch sử của chính Việt Nam; trung vị gần đây của {extra["global_recent_economies"]} nền kinh tế là {f(extra["global_recent_median_annual_change_pp"],3)} điểm phần trăm/năm. Không có căn cứ gọi Việt Nam nhanh nhất thế giới.',
      'limitation':'Mốc 2010 được chọn để mô tả; không phải điểm gãy ước lượng. Tốc độ bình quân không phải dự báo.',
      'tables':'period_changes.csv; demographic_insights.json'})
    insights[5]['finding']=f'Tỷ trọng 15–64 của Việt Nam giảm {f(abs(extra["working_age_decline_since_peak_pp"]))} điểm phần trăm từ đỉnh 2012 đến 2023. Hai tỷ lệ lao động không giảm liên tục trong cả chuỗi; riêng 2019–2023, LFPR giảm {f(abs(extra["lfpr_change_2019_2023_pp"]))} và tỷ lệ có việc làm giảm {f(abs(extra["employment_change_2019_2023_pp"]))} điểm phần trăm.'
    insights[5]['tables']='focal_series.csv; demographic_insights.json'
    pd.DataFrame(insights).to_csv(table/'evidence_table.csv',index=False)
    (table/'evidence_table.json').write_text(json.dumps(insights,ensure_ascii=False,indent=2),'utf-8')
    print(f'Exported {len(insights)} findings to outputs/tables/evidence_table.csv and .json')
    return insights

if __name__ == '__main__':
    main()
