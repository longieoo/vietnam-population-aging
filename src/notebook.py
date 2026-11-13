"""Build and execute a clean-kernel notebook against the saved snapshot."""
import os
import sys
import json
import hashlib
from pathlib import Path
import nbformat as nbf
from nbclient import NotebookClient
from nbconvert import HTMLExporter
from config import ROOT

def main():
    n=nbf.v4.new_notebook()
    md=nbf.v4.new_markdown_cell;code=nbf.v4.new_code_cell
    n.cells=[md('# Già hóa dân số, kinh tế và lao động\n\nNotebook tái lập từ bản chụp World Bank WDI. Đơn vị quan sát là quốc gia/nền kinh tế–năm, 1991–2023. Không có lời gọi mạng trong notebook.'),md('## Dữ liệu và phương pháp\n\nLoại tổng hợp theo metadata chính thức. Giữ giá trị thiếu, dùng mẫu đủ biến cho từng câu hỏi. Ngưỡng 10% là mốc phân tích. Thay đổi tỷ trọng đo bằng điểm phần trăm.'),code("from pathlib import Path\nimport sys, json\nROOT = Path.cwd()\nif ROOT.name == 'notebooks': ROOT = ROOT.parent\nsys.path.insert(0, str(ROOT / 'src'))\nimport pandas as pd\nimport prepare, analyze, visualize\nfrom IPython.display import display, Image, Markdown\nmaster = prepare.main()"),md('## Kiểm tra bảng chính\n\nSố dòng chỉ tính những quốc gia–năm có ít nhất một giá trị nguồn. Bảng dưới cho biết độ phủ từng biến.'),code("assert not master.duplicated(['iso3','year']).any()\ndisplay(pd.read_csv(ROOT/'outputs/tables/missingness_indicator.csv'))"),md('## Kết quả phân tích\n\nTính kết quả từ bảng chính đã kiểm tra, sau đó tạo hình bằng mã nguồn đi kèm.'),code("summary = analyze.main()\nfigure_names = visualize.main()\ndisplay(pd.read_csv(ROOT/'outputs/tables/focal_series.csv').query('year == 2023')[['iso3','age_65_plus','gdp_ppp','lfpr','employment']])"),md('## Nhân khẩu học\n\nTỷ trọng và số người cao tuổi trả lời hai câu hỏi khác nhau. Tỷ số phụ thuộc chỉ là chỉ tiêu nhân khẩu học.'),code("display(Image(filename=str(ROOT/'outputs/figures'/f'{figure_names[1]}.png')))\ndisplay(Image(filename=str(ROOT/'outputs/figures'/f'{figure_names[4]}.png')))"),md('## Kinh tế và ngưỡng già hóa\n\nMẫu lát cắt cùng năm 2023. Ngưỡng chỉ được xác định chính xác trong chuỗi quan sát liền năm từ dưới lên trên.'),code("display(Image(filename=str(ROOT/'outputs/figures'/f'{figure_names[7]}.png')))\ndisplay(pd.read_csv(ROOT/'outputs/tables/threshold_crossings.csv').query(\"iso3 in ['VNM','THA','IDN','JPN','KOR'] and threshold == 10\"))"),md('## Lao động và độ nhạy\n\nKhông đồng nhất mẫu số 15+ của ILO với tỷ trọng dân số 15–64. Không dùng tương quan để suy luận nhân quả hoặc xếp hạng hiệu quả.'),code("display(Image(filename=str(ROOT/'outputs/figures'/f'{figure_names[11]}.png')))\ndisplay(pd.read_csv(ROOT/'outputs/tables/robustness.csv'))"),md('## Kết luận có thể kiểm chứng'),code("a=summary['vietnam_1991']; b=summary['vietnam_2023']\ndisplay(Markdown(f\"Tỷ trọng 65+ của Việt Nam tăng từ **{a['age_65_plus']:.2f}%** lên **{b['age_65_plus']:.2f}%**, tương đương **{summary['vietnam_old_share_change_pp']:.2f} điểm phần trăm**. GDP/người PPP tăng **{summary['vietnam_gdp_multiplier']:.2f} lần**. Đây là mô tả đồng thời, không phải quan hệ nhân quả.\"))")]
    n.metadata={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':sys.version.split()[0]}}
    # A pipeline build has already produced and checked these artifacts. A
    # standalone notebook execution still rebuilds from the snapshot by default.
    for cell in n.cells:
        if cell.cell_type == 'code':
            cell.source=cell.source.replace('master = prepare.main()',
                "import os\nreuse = os.environ.get('AGING_REUSE_RESULTS') == '1'\nprepare.verify_snapshot()\nmaster = pd.read_csv(ROOT/'data/processed/master.csv') if reuse else prepare.main()")
            cell.source=cell.source.replace('summary = analyze.main()\nfigure_names = visualize.main()',
                "summary = json.loads((ROOT/'outputs/tables/analysis_summary.json').read_text('utf-8')) if reuse else analyze.main()\nfigure_names = json.loads((ROOT/'outputs/figures/figure_index.json').read_text('utf-8')) if reuse else visualize.main()")
    n.cells[-1].source += "\nextra=summary['demographic_insights']\ndisplay(Markdown(f\"**Nhịp thay đổi gần đây:** {extra['recent_fraction_of_full_change_pct']:.1f}% mức tăng tỷ trọng 65+ toàn kỳ diễn ra trong 2010–2023. Sau đáy 2012, phụ thuộc tổng tăng {extra['dependency_increase_since_min']:.2f} người/100 người 15–64; tuổi già chiếm {extra['old_dependency_fraction_of_rebound_pct']:.1f}% mức tăng số học. Đây không phải phân rã nhân quả.\"))\ndisplay(pd.read_csv(ROOT/'outputs/tables/threshold_sample_funnel.csv'))"
    path=ROOT/'notebooks/analysis.ipynb'
    nbf.write(n,path)
    # A task-local kernel avoids installation in the user's home directory.
    kernel_root=Path(os.environ.get('PROJECT_WORK',ROOT/'work'))/'jupyter'
    specdir=kernel_root/'kernels/python3';specdir.mkdir(parents=True,exist_ok=True)
    (specdir/'kernel.json').write_text(json.dumps({'argv':[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}'],'display_name':'Python 3','language':'python','env':{'PYTHONPATH':os.environ.get('PYTHONPATH','')}}),'utf-8')
    extra_data=Path(nbf.__file__).resolve().parent.parent/'share/jupyter'
    os.environ['JUPYTER_PATH']=os.pathsep.join([str(kernel_root),str(extra_data)])
    client=NotebookClient(n,timeout=300,kernel_name='python3',resources={'metadata':{'path':str(ROOT)}},allow_errors=False)
    client.execute()
    n.metadata['aging_provenance']={
        'master_sha256':hashlib.sha256((ROOT/'data/processed/master.csv').read_bytes()).hexdigest(),
        'source_snapshot':json.loads((ROOT/'data/metadata/source_manifest.json').read_text('utf-8'))['snapshot_id'],
    }
    nbf.validate(n);nbf.write(n,path)
    html,_=HTMLExporter().from_notebook_node(n)
    (ROOT/'notebooks/analysis.html').write_text(html,'utf-8')
    print(f'Executed {sum(c.cell_type=="code" for c in n.cells)} cells from a clean kernel')

if __name__=='__main__':main()
