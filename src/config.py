"""Project paths, WDI indicators and shared display conventions."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDICATORS = {
    'population': 'SP.POP.TOTL',
    'age_0_14': 'SP.POP.0014.TO.ZS',
    'age_15_64': 'SP.POP.1564.TO.ZS',
    'age_65_plus': 'SP.POP.65UP.TO.ZS',
    'fertility': 'SP.DYN.TFRT.IN',
    'gdp_ppp': 'NY.GDP.PCAP.PP.KD',
    'lfpr': 'SL.TLF.CACT.ZS',
    'employment': 'SL.EMP.TOTL.SP.ZS',
}
FOCAL = {'VNM': 'Việt Nam', 'THA': 'Thái Lan', 'IDN': 'Indonesia', 'JPN': 'Nhật Bản', 'KOR': 'Hàn Quốc'}
COLORS = {'VNM': '#C54B27', 'THA': '#0072B2', 'IDN': '#009E73', 'JPN': '#8B62A6', 'KOR': '#AD7D00'}
YEARS = list(range(1991, 2024))

def ensure_dirs():
    for p in ['data/raw', 'data/metadata', 'data/processed', 'outputs/figures', 'outputs/tables', 'outputs/interactive', 'reports', 'slides', 'docs', 'notebooks', 'tests']:
        (ROOT / p).mkdir(parents=True, exist_ok=True)


def format_number(value, decimals=2):
    """Vietnamese display notation; calculation precision remains unchanged."""
    return f'{value:,.{decimals}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
