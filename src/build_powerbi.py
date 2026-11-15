"""Build an editable native Power BI project from the retained project data.

The PBIP contains native visuals and import partitions; no chart screenshots.
Open it in Desktop, refresh, and save a PBIX to embed the imported data.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "powerbi"
NAME = "PopulationAging"
SEED = ROOT / "src/powerbi_template"
REPORT = DEST / f"{NAME}.Report"
MODEL = DEST / f"{NAME}.SemanticModel"
COLORS = ["#C54B27", "#0072B2", "#009E73", "#8B62A6", "#AD7D00", "#516575"]
FOCAL = ["VNM", "THA", "IDN", "JPN", "KOR"]
VI = dict(zip(FOCAL, ["Việt Nam", "Thái Lan", "Indonesia", "Nhật Bản", "Hàn Quốc"]))


def write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def tquote(s):
    return "'" + s.replace("'", "''") + "'"


tables = {}
measures = {}


def table(name, columns, m, hidden=False):
    tables[name] = columns
    lines = [f"table {tquote(name)}"]
    if hidden:
        lines.append("\tisHidden")
    for col, typ in columns.items():
        lines.extend([f"\tcolumn {tquote(col)}", f"\t\tdataType: {typ}",
                      "\t\tsummarizeBy: none", f"\t\tsourceColumn: {col}"])
        if col in {"year", "threshold"}:
            lines.append("\t\tformatString: 0")
        if col == "country":
            lines.append("\t\tdataCategory: Country")
        lines.append("")
    lines.extend([f"\tpartition {tquote(name)} = m", "\t\tmode: import", "\t\tsource ="])
    lines.extend("\t\t\t" + x for x in m.splitlines())
    path = MODEL / "definition/tables" / f"{name}.tmdl"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def csv_m(relative, cols):
    mtypes = {"string": "type text", "double": "type number", "int64": "Int64.Type"}
    pairs = ", ".join('{"' + c + '", ' + mtypes[t] + "}" for c, t in cols.items())
    return f'''let
    Source = Csv.Document(File.Contents(SourceRoot & "/{relative}"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Headers, {{{pairs}}}, "en-US")
in
    Typed'''


def measure(name, dax, fmt="0.00", folder="Chỉ số"):
    dax = dax.replace("Thresholds[", "'Thresholds'[")
    measures[name] = (dax, fmt, folder)


def generate_model():
    shutil.copytree(SEED / "Seed.SemanticModel", MODEL, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns(".pbi", ".platform"))
    cols = {c: ("string" if c in {"iso3", "country", "region", "income_group"} else
                 "int64" if c in {"year", "population"} else "double")
            for c in next(csv.reader((ROOT / "data/processed/master.csv").open(encoding="utf-8")))}
    table("Master", cols, csv_m("data/processed/master.csv", cols), hidden=True)
    countries = {"iso3": "string", "country": "string", "region": "string", "income_group": "string", "Quốc gia": "string"}
    mapping = " ".join(f'else if [iso3] = "{iso}" then "{label}"' for iso, label in VI.items())
    country_m = f'''let
    Source = Table.Distinct(Table.SelectColumns(Master, {{"iso3", "country", "region", "income_group"}})),
    Named = Table.AddColumn(Source, "Quốc gia", each if false then "" {mapping} else [country], type text)
in
    Named'''
    table("DimCountry", countries, country_m)
    table("FocusCountry", countries, "DimCountry")
    table("ComparisonCountry", countries, "DimCountry")
    table("DimYear", {"year": "int64"}, 'Table.FromColumns({{1991..2023}}, type table [year=Int64.Type])')
    table("SelectedYear", {"year": "int64"}, "DimYear")
    pc = {"iso3": "string", "period": "string", "change_pp": "double", "annual_change_pp": "double"}
    table("PeriodChanges", pc, csv_m("outputs/tables/period_changes.csv", pc), hidden=True)
    tc = {"iso3": "string", "country": "string", "threshold": "int64", "status": "string",
          "year": "double", "previous_year": "double", "gdp_ppp": "double", "share": "double"}
    table("Thresholds", tc, csv_m("outputs/tables/threshold_crossings.csv", tc), hidden=True)
    table("ThresholdSelect", {"threshold": "int64"}, 'Table.FromColumns({{8,10,12}}, type table [threshold=Int64.Type])')
    measure("Năm đang xem", 'SELECTEDVALUE(SelectedYear[year], 2023)', "0", "Bộ lọc")
    measure("ISO quốc gia trọng tâm", 'SELECTEDVALUE(FocusCountry[iso3], "VNM")', "", "Bộ lọc")
    measure("Quốc gia trọng tâm", 'SELECTEDVALUE(FocusCountry[Quốc gia], "Việt Nam")', "", "Bộ lọc")
    measure("Dân số", 'IF(HASONEVALUE(DimYear[year]), SUM(Master[population]))', '#,0', "Gốc")
    measure("Dân số 65+", 'IF(HASONEVALUE(DimYear[year]), SUM(Master[population_65_plus]))', '#,0', "Gốc")
    for name, col in [("0–14 tuổi (%)", "age_0_14"), ("15–64 tuổi (%)", "age_15_64"), ("65+ tuổi (%)", "age_65_plus")]:
        measure(name, f'IF(HASONEVALUE(DimYear[year]), DIVIDE(SUMX(Master, Master[population] * Master[{col}]), SUM(Master[population])))', '0.00"%"', "Gốc")
    for name, col, fmt in [("Mức sinh", "fertility", "0.00"), ("GDP PPP/người", "gdp_ppp", '#,0.00'),
                           ("Tham gia lao động (%)", "lfpr", '0.00"%"'), ("Có việc làm (%)", "employment", '0.00"%"')]:
        measure(name, f'IF(HASONEVALUE(DimCountry[iso3]) && HASONEVALUE(DimYear[year]), AVERAGE(Master[{col}]))', fmt, "Gốc")
    measure("Phụ thuộc trẻ", '100 * DIVIDE([0–14 tuổi (%)], [15–64 tuổi (%)])', "0.00", "Gốc")
    measure("Phụ thuộc già", '100 * DIVIDE([65+ tuổi (%)], [15–64 tuổi (%)])', "0.00", "Gốc")
    measure("Tổng phụ thuộc", '[Phụ thuộc trẻ] + [Phụ thuộc già]', "0.00", "Gốc")
    measure("Chỉ số già hóa", '100 * DIVIDE([65+ tuổi (%)], [0–14 tuổi (%)])', "0.00", "Gốc")
    base_names = list(measures)
    for base in base_names:
        if measures[base][2] != "Gốc":
            continue
        fmt = measures[base][1]
        measure("Trọng tâm · " + base,
                f'VAR c = [ISO quốc gia trọng tâm] VAR y = [Năm đang xem] RETURN CALCULATE([{base}], REMOVEFILTERS(DimCountry), REMOVEFILTERS(DimYear), TREATAS({{c}}, DimCountry[iso3]), TREATAS({{y}}, DimYear[year]))', fmt, "Tổng quan")
        measure("Lịch sử · " + base,
                f'VAR c = [ISO quốc gia trọng tâm] RETURN IF(MAX(DimYear[year]) <= [Năm đang xem], CALCULATE([{base}], REMOVEFILTERS(DimCountry), TREATAS({{c}}, DimCountry[iso3])))', fmt, "Lịch sử")
        measure("So sánh · " + base,
                f'VAR c = SELECTEDVALUE(DimCountry[iso3]) RETURN IF(c IN VALUES(ComparisonCountry[iso3]) && MAX(DimYear[year]) <= [Năm đang xem], [{base}])', fmt, "So sánh")
        measure("Hiện trạng · " + base,
                f'VAR y = [Năm đang xem] RETURN CALCULATE([{base}], REMOVEFILTERS(DimYear), TREATAS({{y}}, DimYear[year]))', fmt, "Hiện trạng")
    measure("Tốc độ già hóa (đpt/năm)", 'VAR c = SELECTEDVALUE(DimCountry[iso3]) RETURN IF(c IN VALUES(ComparisonCountry[iso3]) && HASONEVALUE(PeriodChanges[period]), AVERAGE(PeriodChanges[annual_change_pp]))', "0.000", "So sánh")
    measure("Màu tốc độ", 'VAR v = [Tốc độ già hóa (đpt/năm)] RETURN IF(ISBLANK(v), BLANK(), SWITCH(TRUE(), v < 0, "#D9E9F2", v < 0.10, "#FBE6D7", v < 0.25, "#F7C6A2", v < 0.40, "#E98B55", "#C54B27"))', "", "So sánh")
    measure("GDP tại ngưỡng", 'VAR t = SELECTEDVALUE(ThresholdSelect[threshold], 10) VAR c = SELECTEDVALUE(DimCountry[iso3]) RETURN IF(c IN VALUES(ComparisonCountry[iso3]), CALCULATE(AVERAGE(Thresholds[gdp_ppp]), Thresholds[status] = "observed", TREATAS({t}, Thresholds[threshold])))', '#,0', "Ngưỡng")
    measure("Năm đầu quan sát tại ngưỡng", 'VAR t = SELECTEDVALUE(ThresholdSelect[threshold], 10) VAR c = SELECTEDVALUE(DimCountry[iso3]) RETURN IF(c IN VALUES(ComparisonCountry[iso3]), CALCULATE(MAX(Thresholds[year]), Thresholds[status] = "observed", TREATAS({t}, Thresholds[threshold])))', "0", "Ngưỡng")
    measure("Trạng thái ngưỡng", 'VAR t = SELECTEDVALUE(ThresholdSelect[threshold], 10) VAR c = SELECTEDVALUE(DimCountry[iso3]) VAR s = CALCULATE(SELECTEDVALUE(Thresholds[status]), TREATAS({t}, Thresholds[threshold])) RETURN IF(c IN VALUES(ComparisonCountry[iso3]), SWITCH(s, "observed", "Quan sát được", "already_above", "Đã ở trên ngưỡng năm 1991", "not_reached", "Chưa đạt đến năm 2023", "gap_uncertain", "Khoảng trống dữ liệu", s))', "", "Ngưỡng")
    for label, mx, my in [("GDP", "Hiện trạng · GDP PPP/người", "Hiện trạng · 65+ tuổi (%)"),
                          ("lao động", "Hiện trạng · 15–64 tuổi (%)", "Hiện trạng · Có việc làm (%)")]:
        pts = f'FILTER(ADDCOLUMNS(ALLSELECTED(DimCountry[iso3]), "_x", [{mx}], "_y", [{my}]), NOT ISBLANK([_x]) && NOT ISBLANK([_y]))'
        measure("Số quan sát · " + label, 'COUNTROWS(' + pts + ')', '0', "Mẫu")
        measure("Pearson r · " + label, f'VAR pts = {pts} VAR ax = AVERAGEX(pts, [_x]) VAR ay = AVERAGEX(pts, [_y]) RETURN DIVIDE(SUMX(pts, ([_x]-ax)*([_y]-ay)), SQRT(SUMX(pts, ([_x]-ax)^2)*SUMX(pts, ([_y]-ay)^2)))', "0.000", "Mẫu")
    measure("Số nền kinh tế", 'COUNTROWS(VALUES(DimCountry[iso3]))', "0", "Mẫu")
    lines = ["table Metrics", "\tisHidden: false"]
    for name, (dax, fmt, folder) in measures.items():
        lines.append(f"\tmeasure {tquote(name)} = {dax}")
        if fmt:
            lines.append(f"\t\tformatString: {fmt}")
        lines.extend([f"\t\tdisplayFolder: {folder}", ""])
    lines.extend(["\tcolumn Value", "\t\tdataType: int64", "\t\tisHidden", "\t\tsourceColumn: Value", "\t\tsummarizeBy: none", "", "\tpartition Metrics = m", "\t\tmode: import", "\t\tsource = #table(type table [Value=Int64.Type], {{1}})"])
    (MODEL / "definition/tables/Metrics.tmdl").write_text("\n".join(lines) + "\n", encoding="utf-8")
    tables["Metrics"] = {"Value": "int64"}
    relations = []
    for fact, key, dim, dkey in [("Master", "iso3", "DimCountry", "iso3"), ("Master", "year", "DimYear", "year"),
                                 ("PeriodChanges", "iso3", "DimCountry", "iso3"), ("Thresholds", "iso3", "DimCountry", "iso3")]:
        rid = hashlib.md5((fact + key).encode()).hexdigest()
        relations.extend([f"relationship {rid}", f"\tfromColumn: {fact}.{key}", f"\ttoColumn: {dim}.{dkey}", ""])
    (MODEL / "definition/relationships.tmdl").write_text("\n".join(relations), encoding="utf-8")
    (MODEL / "definition/expressions.tmdl").write_text(
        'expression SourceRoot = "' + ROOT.as_posix() + '" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]\n\tlineageTag: ' + hashlib.md5(b'SourceRoot').hexdigest() + '\n', encoding="utf-8")
    model = (MODEL / "definition/model.tmdl").read_text(encoding="utf-8")
    model += "\nref expression SourceRoot\n" + "\n".join(f"ref table {tquote(t)}" for t in tables) + "\n"
    (MODEL / "definition/model.tmdl").write_text(model, encoding="utf-8")


def literal(value):
    if isinstance(value, bool):
        value = str(value).lower()
    elif isinstance(value, (int, float)):
        value = f"{value}D"
    else:
        value = "'" + str(value).replace("'", "''") + "'"
    return {"expr": {"Literal": {"Value": value}}}


def color(value):
    return {"solid": {"color": literal(value)}}


def props(**kw):
    return [{"properties": {k: literal(v) for k, v in kw.items()}}]


def field(table_name, column, is_measure=False):
    kind = "Measure" if is_measure else "Column"
    return {kind: {"Expression": {"SourceRef": {"Entity": table_name}}, "Property": column}}


def col(t, c, label=None):
    return {"field": field(t, c), "queryRef": f"{t}.{c}", "nativeQueryRef": c, "displayName": label or c, "active": True}


def ms(c, label=None):
    return {"field": field("Metrics", c, True), "queryRef": f"Metrics.{c}", "nativeQueryRef": c, "displayName": label or c.replace("Hiện trạng · ", "").replace("Lịch sử · ", "").replace("So sánh · ", ""), "active": True}


def condition(t, c, values):
    def val(v):
        return {"Literal": {"Value": f"{v}L" if isinstance(v, int) else "'" + v.replace("'", "''") + "'"}}
    return {"Version": 2, "From": [{"Name": "d", "Entity": t, "Type": 0}],
            "Where": [{"Condition": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "d"}}, "Property": c}}], "Values": [[val(v)] for v in values]}}}]}


page_names = []
visual_inventory = []


def visual(page, name, typ, xywh, roles=None, title=None, objects=None):
    vid = hashlib.md5((page + name).encode()).hexdigest()[:20]
    x, y, w, h = xywh
    v = {"visualType": typ, "objects": objects or {}, "visualContainerObjects": {
        "padding": props(top=8, bottom=8, left=12, right=12),
        "background": [{"properties": {"show": literal(True), "color": color("#FFFFFF"), "transparency": literal(0)}}],
        "border": props(show=False),
        "visualHeader": props(show=True),
        "subTitle": props(show=False),
    }}
    if roles:
        v["query"] = {"queryState": {k: {"projections": val} for k, val in roles.items()}}
    if title:
        v["visualContainerObjects"]["title"] = [{"properties": {"show": literal(True), "text": literal(title), "fontSize": literal(14), "fontColor": color("#203444"), "bold": literal(True), "titleWrap": literal(True)}}]
    obj = {"$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.4.0/schema.json",
           "name": vid, "position": {"x": x, "y": y, "z": len(visual_inventory), "width": w, "height": h, "tabOrder": len(visual_inventory)}, "visual": v}
    write_json(REPORT / f"definition/pages/{page}/visuals/{vid}/visual.json", obj)
    visual_inventory.append({"page": page, "name": name, "visualType": typ, "title": title})
    return obj, REPORT / f"definition/pages/{page}/visuals/{vid}/visual.json"


def textbox(page, name, text, xywh, size=14, color_="#516575"):
    ob, path = visual(page, name, "textbox", xywh, objects={"general": [{"properties": {"paragraphs": [{"textRuns": [{"value": text, "textStyle": {"fontFamily": "Segoe UI", "fontSize": f"{size}px", "color": color_}}], "horizontalTextAlignment": "left"}]}}]})
    ob["visual"]["visualContainerObjects"]["background"] = props(show=False)
    ob["visual"]["visualContainerObjects"]["padding"] = props(top=0, bottom=0, left=0, right=0)
    write_json(path, ob)


def slicer(page, name, t, c, title, x, width, values=None, single=False):
    ob, path = visual(page, name, "slicer", (x, 86, width, 88), {"Values": [col(t, c)]}, objects={
        "data": props(mode="Dropdown"), "header": props(show=True, text=title, textSize=11),
        "items": props(textSize=11), "selection": props(singleSelect=single, selectAllCheckboxEnabled=not single)})
    if values:
        ob["visual"]["objects"]["general"] = [{"properties": {"filter": {"filter": condition(t, c, values)}}}]
    ob["visual"]["syncGroup"] = {"groupName": name, "fieldChanges": True, "filterChanges": True}
    write_json(path, ob)


def cards(page, names):
    obj, path = visual(page, "KPIs", "cardVisual", (24, 188, 1392, 124), {"Data": [ms(n, n.replace("Trọng tâm · ", "")) for n in names]}, objects={
        "value": [{"properties": {"fontSize": literal(27), "labelDisplayUnits": literal(1), "decimalPlaces": literal(2)}, "selector": {"id": "default"}}],
        "label": [{"properties": {"fontSize": literal(11)}, "selector": {"id": "default"}}],
        "outline": [{"properties": {"show": literal(False)}, "selector": {"id": "default"}}],
        "layout": props(paddingUniform=4)})
    for n in names:
        obj["visual"]["objects"]["label"].append({"properties": {"text": literal(n.replace("Trọng tâm · ", ""))}, "selector": {"metadata": "Metrics." + n}})
        if n in {"Năm đang xem", "Số nền kinh tế", "Số quan sát · GDP", "Số quan sát · lao động", "Trọng tâm · Dân số", "Trọng tâm · Dân số 65+"}:
            obj["visual"]["objects"]["value"].append({"properties": {"decimalPlaces": literal(0)}, "selector": {"metadata": "Metrics." + n}})
    write_json(path, obj)


def chart(page, name, typ, xywh, title, roles, **extra):
    objects = {"legend": props(show=True, position="Top", fontSize=12), "categoryAxis": props(show=True, fontSize=12, showAxisTitle=False),
               "valueAxis": props(show=True, fontSize=12, showAxisTitle=False), "labels": props(show=False)}
    if "Series" in roles:
        objects["dataPoint"] = [{"properties": {"fill": color(COLORS[i])}, "selector": {"data": [{"scopeId": {"Comparison": {"ComparisonKind": 0, "Left": field("DimCountry", "Quốc gia"), "Right": {"Literal": {"Value": "'" + VI[iso] + "'"}}}}}]}} for i, iso in enumerate(FOCAL)]
    objects.update(extra)
    ob, path = visual(page, name, typ, xywh, roles, title, objects)
    if "Category" in roles and typ != "scatterChart":
        ob["visual"]["query"]["sortDefinition"] = {"sort": [{"field": roles["Category"][0]["field"], "direction": "Ascending"}], "isDefaultSort": True}
    write_json(path, ob)
    return ob, path


def world_topology():
    """Package the retained Natural Earth boundaries; key is the same repaired ISO3 as figure 04."""
    import shapefile
    stem = "ne_110m_admin_0_countries"
    with zipfile.ZipFile(ROOT / "data/raw/natural_earth_countries.zip") as z:
        reader = shapefile.Reader(shp=io.BytesIO(z.read(stem + ".shp")), shx=io.BytesIO(z.read(stem + ".shx")), dbf=io.BytesIO(z.read(stem + ".dbf")), encoding="utf-8")
        arcs, geometries = [], []
        for sr in reader.iterShapeRecords():
            r = sr.record.as_dict()
            iso = r.get("ISO_A3_EH", r["ADM0_A3"])
            if iso == "-99":
                iso = r["ADM0_A3"]
            if iso == "KOS":
                iso = "XKX"
            if iso == "ATA":
                continue
            geom = sr.shape.__geo_interface__
            polygons = [geom["coordinates"]] if geom["type"] == "Polygon" else geom["coordinates"]
            indices = []
            for polygon in polygons:
                rings = []
                for ring in polygon:
                    rings.append([len(arcs)])
                    arcs.append([[round(x, 5), round(y, 5)] for x, y in ring])
                indices.append(rings)
            geometries.append({"type": "MultiPolygon", "arcs": indices, "id": iso, "properties": {"iso3": iso}})
    topology = {"type": "Topology", "objects": {"countries": {"type": "GeometryCollection", "geometries": geometries}}, "arcs": arcs}
    write_json(REPORT / "StaticResources/RegisteredResources/world_iso3.topojson", topology)


def page(pid, title, subtitle, comparisons=False, threshold=False):
    page_names.append(pid)
    write_json(REPORT / f"definition/pages/{pid}/page.json", {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json",
        "name": pid, "displayName": title, "displayOption": "FitToPage", "height": 960, "width": 1440,
        "objects": {"background": [{"properties": {"color": color("#F3F6F8"), "transparency": literal(0)}}]}})
    textbox(pid, "title", title.upper(), (24, 14, 1392, 42), 27, "#203444")
    textbox(pid, "subtitle", subtitle, (24, 55, 1392, 29), 14)
    slicer(pid, "focus", "FocusCountry", "Quốc gia", "Quốc gia trọng tâm", 24, 300, ["Việt Nam"], True)
    slicer(pid, "year", "SelectedYear", "year", "Năm kết thúc / hiện trạng", 340, 230, [2023], True)
    slicer(pid, "region", "DimCountry", "region", "Vùng (mẫu so sánh)", 586, 360)
    if comparisons:
        slicer(pid, "comparison", "ComparisonCountry", "Quốc gia", "Nhóm đối chiếu", 962, 454, list(VI.values()))
    elif threshold:
        slicer(pid, "focus", "FocusCountry", "Quốc gia", "Quốc gia trọng tâm", 24, 280, ["Việt Nam"], True)
        slicer(pid, "year", "SelectedYear", "year", "Năm hiện trạng", 320, 200, [2023], True)
        slicer(pid, "region", "DimCountry", "region", "Vùng (mẫu so sánh)", 536, 300)
        slicer(pid, "threshold", "ThresholdSelect", "threshold", "Ngưỡng 65+ (%)", 852, 160, [10], True)
        slicer(pid, "comparison", "ComparisonCountry", "Quốc gia", "Nhóm đối chiếu ngưỡng", 1028, 388, list(VI.values()))
    else:
        slicer(pid, "income", "DimCountry", "income_group", "Nhóm thu nhập (mẫu)", 962, 454)
    textbox(pid, "source", "Nguồn: World Bank WDI · Bản lưu 21–22/09/2026 · 1991–2023 · 217 nền kinh tế · Tỷ lệ tính bằng %, thay đổi tính bằng điểm phần trăm.", (24, 918, 1392, 32), 12)


def generate_report():
    shutil.copytree(SEED / "Seed.Report/StaticResources", REPORT / "StaticResources", dirs_exist_ok=True)
    for f in ["definition/version.json", "definition/report.json", "definition.pbir"]:
        p = REPORT / f
        p.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SEED / "Seed.Report" / f, p)
    binding = json.loads((REPORT / "definition.pbir").read_text())
    binding["datasetReference"]["byPath"]["path"] = f"../{NAME}.SemanticModel"
    write_json(REPORT / "definition.pbir", binding)
    report = json.loads((REPORT / "definition/report.json").read_text())
    theme = {"name": "Population Aging", "dataColors": COLORS, "background": "#FFFFFF", "foreground": "#203444", "tableAccent": COLORS[0],
             "textClasses": {"title": {"fontFace": "Segoe UI Semibold", "fontSize": 14}, "label": {"fontFace": "Segoe UI", "fontSize": 11}}}
    write_json(REPORT / "StaticResources/RegisteredResources/PopulationAgingTheme.json", theme)
    report["themeCollection"]["customTheme"] = {"name": "PopulationAgingTheme", "reportVersionAtImport": {"visual": "2.13.0", "report": "3.4.0", "page": "2.3.1"}, "type": "RegisteredResources"}
    report["resourcePackages"].append({"name": "RegisteredResources", "type": "RegisteredResources", "items": [{"name": "PopulationAgingTheme", "path": "PopulationAgingTheme.json", "type": "CustomTheme"}]})
    world_topology()
    report["resourcePackages"][-1]["items"].append({"name": "world_iso3.topojson", "path": "world_iso3.topojson", "type": "ShapeMap"})
    write_json(REPORT / "definition/report.json", report)
    # 01: figures 1–3, with separate axes for population and elderly share.
    p = "overview"
    page(p, "01 · Tổng quan", "Quy mô người cao tuổi, cơ cấu tuổi và sự thay đổi gánh nặng phụ thuộc tại quốc gia trọng tâm.")
    cards(p, ["Quốc gia trọng tâm", "Trọng tâm · Dân số", "Trọng tâm · Dân số 65+", "Trọng tâm · 65+ tuổi (%)"])
    chart(p, "age", "stackedAreaChart", (24, 328, 680, 270), "Cơ cấu dân số theo tuổi (%)", {"Category": [col("DimYear", "year", "Năm")], "Y": [ms("Lịch sử · " + n, n) for n in ["0–14 tuổi (%)", "15–64 tuổi (%)", "65+ tuổi (%)"]]})
    chart(p, "dependency", "lineChart", (720, 328, 696, 270), "Tỷ số phụ thuộc (trên 100 người 15–64 tuổi)", {"Category": [col("DimYear", "year", "Năm")], "Y": [ms("Lịch sử · " + n, n) for n in ["Phụ thuộc trẻ", "Phụ thuộc già", "Tổng phụ thuộc"]]})
    chart(p, "elderly_count", "lineChart", (24, 614, 680, 258), "Số người từ 65 tuổi trở lên (người)", {"Category": [col("DimYear", "year", "Năm")], "Y": [ms("Lịch sử · Dân số 65+", "Dân số 65+")]})
    chart(p, "elderly_share", "lineChart", (720, 614, 696, 258), "Tỷ trọng người từ 65 tuổi trở lên (%)", {"Category": [col("DimYear", "year", "Năm")], "Y": [ms("Lịch sử · 65+ tuổi (%)", "65+ tuổi (%)")]})
    textbox(p, "note", "Quy mô và tỷ trọng được đặt trên hai biểu đồ riêng. Bộ lọc vùng/thu nhập chỉ tác động đến mẫu quốc tế; quốc gia trọng tâm giữ độc lập.", (24, 879, 1392, 32), 13)
    # 02: figures 5–7.
    p = "comparison"
    page(p, "02 · Diễn biến già hóa", "So sánh tỷ trọng 65+, mức sinh và tốc độ tăng tỷ trọng người cao tuổi giữa các quốc gia.", comparisons=True)
    cards(p, ["Trọng tâm · 65+ tuổi (%)", "Trọng tâm · Mức sinh", "Trọng tâm · Chỉ số già hóa", "Trọng tâm · Phụ thuộc già"])
    for name, base, title, xywh in [("compare_aging", "65+ tuổi (%)", "Tỷ trọng 65+ của nhóm đối chiếu (%)", (24, 328, 680, 272)),
                                    ("fertility", "Mức sinh", "Tổng tỷ suất sinh (con/phụ nữ)", (720, 328, 696, 272))]:
        chart(p, name, "lineChart", xywh, title, {"Category": [col("DimYear", "year", "Năm")], "Series": [col("DimCountry", "Quốc gia")], "Y": [ms("So sánh · " + base, base)]})
    ob, path = visual(p, "period_heatmap", "pivotTable", (24, 616, 680, 256), {"Rows": [col("DimCountry", "Quốc gia")], "Columns": [col("PeriodChanges", "period", "Giai đoạn")], "Values": [ms("Tốc độ già hóa (đpt/năm)")]}, "Tốc độ già hóa theo giai đoạn (đpt/năm)", {
        "columnHeaders": props(autoSizeColumnWidth=True, columnAdjustment="growToFit", fontSize=12),
        "rowHeaders": props(fontSize=12), "values": props(fontSize=12), "subTotals": props(rowSubtotals=False, columnSubtotals=False)})
    ob["visual"]["objects"]["values"].append({"properties": {"backColor": {"solid": {"color": {"expr": field("Metrics", "Màu tốc độ", True)}}}}, "selector": {"metadata": "Metrics.Tốc độ già hóa (đpt/năm)", "data": [{"dataViewWildcard": {"matchingOption": 1}}]}})
    write_json(path, ob)
    chart(p, "working_compare", "lineChart", (720, 616, 696, 256), "Dân số trong độ tuổi 15–64 của nhóm đối chiếu (%)", {"Category": [col("DimYear", "year", "Năm")], "Series": [col("DimCountry", "Quốc gia")], "Y": [ms("So sánh · 15–64 tuổi (%)", "15–64 tuổi (%)")]})
    textbox(p, "note", "Tốc độ = chênh lệch tỷ trọng 65+ / số năm giữa hai mốc. Ba giai đoạn là mẫu cố định 1991–2023, không thay đổi theo bộ lọc năm kết thúc.", (24, 879, 1392, 32), 13)
    # 03: figures 8–10; scatter sample counters are recalculated for region/income/year.
    p = "economy"
    page(p, "03 · Già hóa và kinh tế", "Mối liên hệ giữa GDP PPP/người và tỷ trọng 65+; đối chiếu ngưỡng già hóa trong cửa sổ quan sát.", threshold=True)
    cards(p, ["Trọng tâm · GDP PPP/người", "Trọng tâm · 65+ tuổi (%)", "Số quan sát · GDP", "Pearson r · GDP"])
    chart(p, "gdp_scatter", "scatterChart", (24, 328, 840, 330), "GDP PPP/người và tỷ trọng 65+ (trục GDP log)", {"Category": [col("DimCountry", "Quốc gia")], "X": [ms("Hiện trạng · GDP PPP/người", "GDP PPP/người")], "Y": [ms("Hiện trạng · 65+ tuổi (%)", "65+ (%)")], "Tooltips": [ms("Hiện trạng · Dân số", "Dân số"), ms("Năm đang xem", "Năm")]}, categoryAxis=props(show=True, logAxisScale=True, showAxisTitle=True, titleText="GDP PPP/người (USD quốc tế 2021)"), valueAxis=props(show=True, showAxisTitle=True, titleText="65+ (%)"))
    chart(p, "trajectory", "scatterChart", (880, 328, 536, 330), "Quỹ đạo quốc gia trọng tâm (mỗi điểm = một năm)", {"Category": [col("DimYear", "year", "Năm")], "X": [ms("Lịch sử · GDP PPP/người", "GDP PPP/người")], "Y": [ms("Lịch sử · 65+ tuổi (%)", "65+ (%)")], "Tooltips": [ms("Lịch sử · Dân số", "Dân số")]})
    chart(p, "threshold_gdp", "clusteredBarChart", (24, 674, 680, 194), "GDP PPP/người tại năm đầu quan sát vượt ngưỡng", {"Category": [col("DimCountry", "Quốc gia")], "Y": [ms("GDP tại ngưỡng")], "Tooltips": [ms("Năm đầu quan sát tại ngưỡng", "Năm đầu quan sát")]})
    visual(p, "threshold_status", "tableEx", (720, 674, 696, 194), {"Values": [col("DimCountry", "Quốc gia"), ms("Trạng thái ngưỡng"), ms("Năm đầu quan sát tại ngưỡng", "Năm")]}, "Minh chứng trạng thái ngưỡng (1991–2023)", {"columnHeaders": props(autoSizeColumnWidth=True, columnAdjustment="growToFit", fontSize=11), "values": props(fontSize=11)})
    textbox(p, "note", "GDP theo USD quốc tế cố định 2021. Pearson r dùng GDP gốc, không phải log(GDP); tương quan không chứng minh nhân quả. Biểu đồ ngưỡng chỉ có trường hợp quan sát được và có GDP.", (24, 879, 1392, 38), 12)
    # 04: figures 11–12.
    p = "labor"
    page(p, "04 · Cơ cấu tuổi và lao động", "Đối chiếu cơ cấu tuổi với tỷ lệ tham gia lao động và tỷ lệ dân số có việc làm từ 15 tuổi trở lên.")
    cards(p, ["Trọng tâm · 15–64 tuổi (%)", "Trọng tâm · Tham gia lao động (%)", "Trọng tâm · Có việc làm (%)", "Số quan sát · lao động"])
    chart(p, "labor_scatter", "scatterChart", (24, 328, 840, 544), "Tỷ trọng 15–64 và tỷ lệ dân số có việc làm (%)", {"Category": [col("DimCountry", "Quốc gia")], "X": [ms("Hiện trạng · 15–64 tuổi (%)", "15–64 (%)")], "Y": [ms("Hiện trạng · Có việc làm (%)", "Có việc làm (15+) (%)")], "Tooltips": [ms("Hiện trạng · Tham gia lao động (%)", "Tham gia lao động (15+) (%)")]}, categoryAxis=props(show=True, showAxisTitle=True, titleText="Tỷ trọng 15–64 (%)"), valueAxis=props(show=True, showAxisTitle=True, titleText="Dân số có việc làm (15+) (%)"))
    chart(p, "working_history", "lineChart", (880, 328, 536, 254), "Tỷ trọng dân số 15–64 tại quốc gia trọng tâm (%)", {"Category": [col("DimYear", "year", "Năm")], "Y": [ms("Lịch sử · 15–64 tuổi (%)", "15–64 (%)")]})
    chart(p, "labor_history", "lineChart", (880, 598, 536, 274), "Tham gia lao động và có việc làm (15+) (%)", {"Category": [col("DimYear", "year", "Năm")], "Y": [ms("Lịch sử · Tham gia lao động (%)", "Tham gia lao động (15+)"), ms("Lịch sử · Có việc làm (%)", "Có việc làm (15+)")]})
    textbox(p, "note", "Hai chỉ tiêu lao động có mẫu số là dân số 15+, còn cơ cấu tuổi dùng toàn bộ dân số. Không trừ trực tiếp hai loại tỷ lệ; điểm thiếu dữ liệu bị loại khỏi scatter.", (24, 879, 1392, 36), 13)
    # 05: geography and an inspectable native data table.
    p = "world"
    page(p, "05 · Phân bố quốc tế", "Bản đồ tỷ trọng người cao tuổi và bảng đối chiếu dữ liệu của từng nền kinh tế trong năm đang chọn.")
    cards(p, ["Năm đang xem", "Số nền kinh tế", "Trọng tâm · 65+ tuổi (%)", "Trọng tâm · Phụ thuộc già"])
    visual(p, "world_map", "shapeMap", (24, 328, 840, 544), {"Category": [col("DimCountry", "iso3", "ISO3")], "Value": [ms("Hiện trạng · 65+ tuổi (%)", "65+ (%)")], "Tooltips": [ms("Hiện trạng · Dân số 65+", "Dân số 65+"), ms("Hiện trạng · GDP PPP/người", "GDP PPP/người")]}, "Tỷ trọng 65+ (%) · màu đậm biểu thị tỷ trọng cao", {
        "shape": [{"properties": {"map": {"geoJson": {"type": literal("packaged"), "name": literal("world_iso3.topojson"), "content": {"expr": {"ResourcePackageItem": {"PackageName": "RegisteredResources", "PackageType": 1, "ItemName": "world_iso3.topojson"}}}}}, "projectionEnum": literal("equirectangular")}}],
        "dataPoint": [{"properties": {"fillRule": {"linearGradient2": {"min": {"color": literal("#FBE6D7")}, "max": {"color": literal("#9C301D")}}}}}],
        "zoom": props(manualZoom=False)})
    visual(p, "snapshot_table", "tableEx", (880, 328, 536, 544), {"Values": [col("DimCountry", "Quốc gia"), ms("Hiện trạng · 65+ tuổi (%)", "65+ (%)"), ms("Hiện trạng · GDP PPP/người", "GDP PPP/người"), ms("Hiện trạng · Có việc làm (%)", "Có việc làm (15+) (%)")]}, "Dữ liệu hiện trạng · chọn điểm/bảng để lọc chéo", {"columnHeaders": props(autoSizeColumnWidth=True, columnAdjustment="growToFit", fontSize=11), "values": props(fontSize=11)})
    textbox(p, "note", "Ranh giới: Natural Earth 1:110m, ghép bằng ISO3 như Hình 3.4. Có 170/217 nền kinh tế khớp hình học; 47 trường hợp còn lại vẫn có trong bảng. Màu xám = thiếu dữ liệu hoặc không khớp.", (24, 879, 1392, 38), 12)
    # 06: data definitions and usage are in the Power BI file itself.
    p = "guide"
    page(p, "06 · Hướng dẫn và nguồn", "Cách dùng, định nghĩa chỉ số và phạm vi diễn giải của báo cáo Power BI.")
    textbox(p, "guide_content", "CÁCH SỬ DỤNG\n1. Chọn quốc gia trọng tâm và năm kết thúc. Thẻ số liệu dùng năm này; chuỗi thời gian vẫn hiển thị từ 1991.\n2. Vùng và nhóm thu nhập lọc mẫu quốc tế. Quốc gia trọng tâm được giữ độc lập để đối chiếu.\n3. Trang 02 có bộ chọn nhóm quốc gia; mặc định Việt Nam, Thái Lan, Indonesia, Nhật Bản, Hàn Quốc.\n4. Chọn một điểm hoặc một dòng bảng để lọc chéo; nhấp lại điểm hoặc vùng trống để bỏ lựa chọn.\n5. Dùng dấu ... trên biểu đồ để xem bảng dữ liệu hoặc xuất dữ liệu tóm tắt.\n\nDỮ LIỆU VÀ CHỈ SỐ\n• Bảng chuẩn: 7.161 quan sát quốc gia–năm, 217 nền kinh tế, 1991–2023; không gồm các vùng tổng hợp WDI.\n• Nguồn: World Bank World Development Indicators. Bản dữ liệu lưu ngày 21–22/09/2026.\n• Dân số 65+ = dân số × tỷ trọng 65+ / 100.\n• Phụ thuộc già = 100 × tỷ trọng 65+ / tỷ trọng 15–64; tổng phụ thuộc = phụ thuộc trẻ + phụ thuộc già.\n• Tỷ lệ cơ cấu tuổi tổng hợp có trọng số dân số. Mức sinh, GDP/người và chỉ tiêu lao động chỉ hiển thị ở cấp một quốc gia–một năm.\n• GDP PPP theo USD quốc tế cố định 2021. Dữ liệu thiếu giữ là trống, không thay bằng 0.\n\nGIỚI HẠN DIỄN GIẢI\n• Tương quan và quỹ đạo thời gian là bằng chứng mô tả, không xác lập quan hệ nhân quả.\n• Ngưỡng 8%, 10%, 12% là mốc phân tích của đồ án; không coi là phân loại chính thức chung cho mọi nghiên cứu.\n• Năm đầu quan sát vượt ngưỡng nằm trong 1991–2023; trường hợp đã vượt năm 1991 không có năm vượt chính xác.\n• Nhóm thu nhập/vùng là ảnh chụp metadata của bản nguồn, không phải phân loại lịch sử từng năm.\n\nNguồn và định nghĩa: https://data.worldbank.org/ · https://databank.worldbank.org/source/world-development-indicators", (24, 196, 1392, 690), 16, "#203444")
    write_json(REPORT / "definition/pages/pages.json", {"$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.1.0/schema.json", "pageOrder": page_names, "activePageName": "overview"})
    write_json(DEST / f"{NAME}.pbip", {"$schema": "https://developer.microsoft.com/json-schemas/fabric/pbip/pbipProperties/1.0.0/schema.json", "version": "1.0", "artifacts": [{"report": {"path": f"{NAME}.Report"}}], "settings": {"enableAutoRecovery": True}})
    unique_visuals = {(v["page"], v["name"]): v for v in visual_inventory}
    visual_inventory[:] = list(unique_visuals.values())
    write_json(DEST / "visual_inventory.json", visual_inventory)


if __name__ == "__main__":
    DEST.mkdir(parents=True, exist_ok=True)
    generate_model()
    generate_report()
    print(f"Native PBIP: {DEST / (NAME + '.pbip')}")
    print(f"{len(tables)} tables, {len(measures)} DAX measures, {len(page_names)} pages, {len(visual_inventory)} visuals")
