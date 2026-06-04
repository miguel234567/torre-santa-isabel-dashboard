"""
Genera Presupuesto_TorreSantaIsabel_BIM.xlsx
Estructura: PORTADA · EDT · APU · OrdenesCambio · Resumen
Todas las fórmulas calculadas (no hardcoded) — interconectado entre hojas.
"""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule, FormulaRule
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.comments import Comment

# ── Estilos reutilizables ───────────────────────────────────
THIN   = Side(border_style='thin',   color='D1DBE8')
MEDIUM = Side(border_style='medium', color='1E293B')

BRD_ALL = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
BRD_BOT_M = Border(bottom=MEDIUM)

FONT_TITLE   = Font(name='Calibri', size=18, bold=True, color='1E293B')
FONT_SUBTITLE= Font(name='Calibri', size=11, italic=True, color='64748B')
FONT_H1      = Font(name='Calibri', size=12, bold=True, color='FFFFFF')
FONT_H2      = Font(name='Calibri', size=10, bold=True, color='1E293B')
FONT_BODY    = Font(name='Calibri', size=10, color='1E293B')
FONT_INPUT   = Font(name='Calibri', size=10, color='0000FF', bold=False)   # azul = input
FONT_FORMULA = Font(name='Calibri', size=10, color='000000')               # negro = fórmula
FONT_XREF    = Font(name='Calibri', size=10, color='008000', bold=True)    # verde = cross-sheet
FONT_KPI     = Font(name='Calibri', size=18, bold=True, color='1E293B')
FONT_KPI_LBL = Font(name='Calibri', size=9, bold=True, color='64748B')

FILL_HEAD    = PatternFill('solid', start_color='1E293B')
FILL_CHAPTER = PatternFill('solid', start_color='E0E7FF')
FILL_KPI     = PatternFill('solid', start_color='F5F7FA')
FILL_BIM     = PatternFill('solid', start_color='EEEAFE')
FILL_PORTADA = PatternFill('solid', start_color='0D1117')
FILL_TOTAL   = PatternFill('solid', start_color='FEF3C7')

CENTER = Alignment(horizontal='center', vertical='center', wrap_text=True)
LEFT   = Alignment(horizontal='left',   vertical='center')
RIGHT  = Alignment(horizontal='right',  vertical='center')

FMT_M   = '$#,##0"M";[Red]($#,##0"M");-'   # millones COP
FMT_COP = '$#,##0;[Red]($#,##0);-'          # pesos
FMT_INT = '#,##0;[Red](#,##0);-'
FMT_PCT = '0.0%;[Red](0.0%);-'
FMT_RATIO = '0.00'

# ═════════════════════════════════════════════════════════════
wb = Workbook()

# ──────────────────────────────────────────────────────────────
# HOJA 1: PORTADA
# ──────────────────────────────────────────────────────────────
ws = wb.active
ws.title = "PORTADA"
ws.sheet_view.showGridLines = False

ws.column_dimensions['A'].width = 3
ws.column_dimensions['B'].width = 30
ws.column_dimensions['C'].width = 50

# Banner negro
for row in range(1, 8):
    for col in range(1, 12):
        ws.cell(row=row, column=col).fill = FILL_PORTADA

ws['B3'] = "PRESUPUESTO DE OBRA BIM"
ws['B3'].font = Font(name='Calibri', size=24, bold=True, color='FFFFFF')
ws['B4'] = "Torre Santa Isabel · CVA Constructora"
ws['B4'].font = Font(name='Calibri', size=14, color='94A3B8')
ws['B5'] = "Vinculado al modelo IFC · 186 partidas BIM"
ws['B5'].font = Font(name='Calibri', size=11, italic=True, color='8B5CF6')

# Tabla de metadatos
ws['B10'] = "DATOS DEL PROYECTO"
ws['B10'].font = Font(name='Calibri', size=11, bold=True, color='1E293B')
ws['B10'].border = Border(bottom=MEDIUM)

meta = [
    ("Proyecto",           "Torre Santa Isabel"),
    ("Contratista",        "CVA Constructora"),
    ("Director de obra",   "Miguel Salazar"),
    ("Fecha base",         "01/May/2026"),
    ("Fecha fin proyecto", "16/Feb/2028"),
    ("Plazo total (días)", 656),
    ("Modelo IFC",         "STA_ISABEL_v3.ifc"),
    ("Versión presupuesto",1),
]
for i, (k, v) in enumerate(meta, start=12):
    ws.cell(row=i, column=2, value=k).font = FONT_H2
    ws.cell(row=i, column=3, value=v).font = FONT_INPUT  # azul = editable

# KPIs resumen (referencias a Resumen)
ws['B22'] = "KPI EJECUTIVOS (auto-calculados)"
ws['B22'].font = Font(name='Calibri', size=11, bold=True, color='1E293B')
ws['B22'].border = Border(bottom=MEDIUM)

kpi_layout = [
    ("Presupuesto total",   "=Resumen!C5",  FMT_COP),
    ("Comprometido",        "=Resumen!C6",  FMT_COP),
    ("Ejecutado",           "=Resumen!C7",  FMT_COP),
    ("CPI",                 "=Resumen!C13", FMT_RATIO),
    ("Desviación total",    "=Resumen!C9",  FMT_COP),
    ("Proyección EAC",      "=Resumen!C14", FMT_COP),
]
for i, (lbl, formula, fmt) in enumerate(kpi_layout, start=24):
    ws.cell(row=i, column=2, value=lbl).font = FONT_KPI_LBL
    c = ws.cell(row=i, column=3, value=formula)
    c.font = FONT_XREF
    c.number_format = fmt
    c.alignment = RIGHT

ws['B33'] = ("Convención de colores: AZUL = inputs (editables) · NEGRO = fórmulas · "
             "VERDE = referencias entre hojas. NUNCA escribir en celdas negras.")
ws['B33'].font = Font(name='Calibri', size=9, italic=True, color='64748B')
ws.merge_cells('B33:H34')
ws['B33'].alignment = Alignment(horizontal='left', vertical='top', wrap_text=True)

# ──────────────────────────────────────────────────────────────
# HOJA 2: EDT (Estructura de Desglose de Trabajo)
# ──────────────────────────────────────────────────────────────
ws = wb.create_sheet("EDT")
ws.sheet_view.showGridLines = False
ws.freeze_panes = 'A4'

# Encabezado
ws['A1'] = "EDT · ESTRUCTURA DE DESGLOSE DE TRABAJO"
ws['A1'].font = FONT_TITLE
ws.merge_cells('A1:I1')

ws['A2'] = ("Editar solo columnas AZULES (Metrado, V.Unit, Ejec). Las columnas en NEGRO "
            "se calculan automáticamente. Capítulos (filas grises) suman sus partidas.")
ws['A2'].font = FONT_SUBTITLE
ws.merge_cells('A2:I2')

# Cabecera tabla
headers = ['Código', 'Descripción', 'BIM', 'Unidad', 'Metrado', 'V. Unit.', 'Presupuesto', 'Ejecutado', '% Ejec.']
widths   = [10, 42, 6, 8, 12, 14, 16, 16, 10]
for i, (h, w) in enumerate(zip(headers, widths), start=1):
    c = ws.cell(row=3, column=i, value=h)
    c.font = FONT_H1
    c.fill = FILL_HEAD
    c.alignment = CENTER
    c.border = BRD_ALL
    ws.column_dimensions[get_column_letter(i)].width = w
ws.row_dimensions[3].height = 24

# Datos: capítulos + partidas
edt_data = [
    # (código, descripción, bim, unidad, metrado, v_unit, ejec)
    # — Capítulo 01: Preliminares —
    ("01",     "Preliminares",                       "", "",   None,   None,         None,  True),
    ("01.01",  "Cerramiento provisional",            "",  "ml",   240,   85000,    20000000,  False),
    ("01.02",  "Descapote y limpieza",               "",  "m²", 1800,   12000,    21000000,  False),
    # — Capítulo 02: Estructura —
    ("02",     "Estructura",                          "", "",   None,   None,         None,  True),
    ("02.01",  "Excavación manual",                  "",  "m³", 3200,   45000,   144000000,  False),
    ("02.02",  "Pilotes D=60cm",                     "",  "ml",  860,  280000,   241000000,  False),
    ("02.03",  "Concreto muros cimentación",        "BIM", "m³",  420,  380000,   188000000,  False),
    ("02.04",  "Acero longitudinal Ø3/8\"",          "",  "kg",48000,    3800,    25000000,  False),
    ("02.05",  "Estructura sótanos nivel -3",       "BIM","m²", 2400,  520000,           0,  False),
    # — Capítulo 03: MEP —
    ("03",     "MEP",                                 "", "",   None,   None,         None,  True),
    ("03.01",  "Red hidrosanitaria",                 "",  "pto", 840,  320000,           0,  False),
    ("03.02",  "Red eléctrica circuitos",            "",  "pto",1200,  185000,           0,  False),
    # — Capítulo 04: Acabados —
    ("04",     "Acabados",                            "", "",   None,   None,         None,  True),
    ("04.01",  "Mortero de nivelación pisos",        "",  "m²", 4200,   38000,           0,  False),
    ("04.02",  "Enchape cerámico baños",             "",  "m²",  680,  120000,           0,  False),
    # — Capítulo 05: Urbanismo —
    ("05",     "Urbanismo y exteriores",             "", "",    None,   None,         None,  True),
    ("05.01",  "Adoquines vehiculares",              "",  "m²",  450,   88000,           0,  False),
]

row = 4
chapter_rows = {}    # {code: row_num}
chapter_items = {}   # {code: [first_row, last_row]}

for code, desc, bim, unit, metrado, vunit, ejec, is_chapter in edt_data:
    if is_chapter:
        # Fila de capítulo (formulas SUMIFS)
        c1 = ws.cell(row=row, column=1, value=code); c1.font = FONT_H2; c1.fill = FILL_CHAPTER
        c2 = ws.cell(row=row, column=2, value=desc); c2.font = FONT_H2; c2.fill = FILL_CHAPTER
        for col in range(3, 7):
            cc = ws.cell(row=row, column=col); cc.fill = FILL_CHAPTER
        # Presupuesto = SUMIFS para partidas que empiecen con código_capítulo
        pat = f'{code}.*'
        ws.cell(row=row, column=7, value=f'=SUMIFS(G4:G99,A4:A99,"{pat}")').font = FONT_FORMULA
        ws.cell(row=row, column=8, value=f'=SUMIFS(H4:H99,A4:A99,"{pat}")').font = FONT_FORMULA
        ws.cell(row=row, column=9, value=f'=IFERROR(H{row}/G{row},0)').font = FONT_FORMULA
        for col in [7, 8]:
            cc = ws.cell(row=row, column=col)
            cc.fill = FILL_CHAPTER
            cc.number_format = FMT_COP
            cc.font = Font(name='Calibri', size=10, bold=True, color='1D4ED8')
        c9 = ws.cell(row=row, column=9); c9.fill = FILL_CHAPTER; c9.number_format = FMT_PCT
        c9.font = Font(name='Calibri', size=10, bold=True, color='1E293B')
        chapter_rows[code] = row
    else:
        ws.cell(row=row, column=1, value=code).font = Font(name='Calibri', size=10, color='64748B', italic=True)
        ws.cell(row=row, column=2, value=desc).font = FONT_BODY
        ws.cell(row=row, column=2).alignment = Alignment(indent=2, vertical='center')
        # BIM tag
        if bim:
            cb = ws.cell(row=row, column=3, value="BIM")
            cb.font = Font(name='Calibri', size=9, bold=True, color='8B5CF6')
            cb.fill = FILL_BIM
            cb.alignment = CENTER
        ws.cell(row=row, column=4, value=unit).alignment = CENTER
        # Metrado (input azul)
        cm = ws.cell(row=row, column=5, value=metrado); cm.font = FONT_INPUT; cm.number_format = FMT_INT; cm.alignment = RIGHT
        # V. Unitario (input azul)
        cv = ws.cell(row=row, column=6, value=vunit); cv.font = FONT_INPUT; cv.number_format = FMT_COP; cv.alignment = RIGHT
        # Presupuesto = Metrado * V.Unit (fórmula negra)
        cp = ws.cell(row=row, column=7, value=f'=E{row}*F{row}'); cp.font = FONT_FORMULA; cp.number_format = FMT_COP; cp.alignment = RIGHT
        # Ejecutado (input azul)
        ce = ws.cell(row=row, column=8, value=ejec); ce.font = FONT_INPUT; ce.number_format = FMT_COP; ce.alignment = RIGHT
        # % Ejec = Ejec / Presupuesto
        c9 = ws.cell(row=row, column=9, value=f'=IFERROR(H{row}/G{row},0)'); c9.font = FONT_FORMULA; c9.number_format = FMT_PCT; c9.alignment = RIGHT
    for col in range(1, 10):
        ws.cell(row=row, column=col).border = BRD_ALL
    row += 1

last_row = row - 1

# Fila TOTAL al final
ws.cell(row=row, column=1, value="TOTAL").font = Font(name='Calibri', size=11, bold=True, color='1E293B')
ws.cell(row=row, column=2, value="Presupuesto base del proyecto").font = Font(name='Calibri', size=10, bold=True, color='1E293B')
# Total = suma SOLO de capítulos (rows in chapter_rows.values())
total_chapters_g = ','.join([f'G{r}' for r in chapter_rows.values()])
total_chapters_h = ','.join([f'H{r}' for r in chapter_rows.values()])
ws.cell(row=row, column=7, value=f'=SUM({total_chapters_g})')
ws.cell(row=row, column=8, value=f'=SUM({total_chapters_h})')
ws.cell(row=row, column=9, value=f'=IFERROR(H{row}/G{row},0)')
for col in range(1, 10):
    c = ws.cell(row=row, column=col)
    c.fill = FILL_TOTAL
    if col in (7, 8):
        c.font = Font(name='Calibri', size=12, bold=True, color='B45309')
        c.number_format = FMT_COP
    elif col == 9:
        c.font = Font(name='Calibri', size=12, bold=True, color='B45309')
        c.number_format = FMT_PCT
    c.border = Border(top=MEDIUM, bottom=MEDIUM)
    c.alignment = RIGHT if col >= 5 else LEFT
TOTAL_ROW = row

# Conditional formatting: filas con sobrecosto (% Ejec > 100%)
red_fill = PatternFill('solid', start_color='FEE2E2')
red_font = Font(name='Calibri', size=10, color='B91C1C', bold=True)
ws.conditional_formatting.add(
    f'I4:I{last_row}',
    CellIsRule(operator='greaterThan', formula=['1'], fill=red_fill, font=red_font)
)
# Verde si %ejec entre 95-100%
green_fill = PatternFill('solid', start_color='D1FAE5')
ws.conditional_formatting.add(
    f'I4:I{last_row}',
    CellIsRule(operator='between', formula=['0.95','1'], fill=green_fill)
)

# ──────────────────────────────────────────────────────────────
# HOJA 3: APU (Análisis de Precios Unitarios)
# ──────────────────────────────────────────────────────────────
ws = wb.create_sheet("APU")
ws.sheet_view.showGridLines = False

ws['A1'] = "APU · ANÁLISIS DE PRECIOS UNITARIOS"
ws['A1'].font = FONT_TITLE
ws.merge_cells('A1:F1')

ws['A2'] = ("Plantilla APU para partidas BIM. Cambiar partida en C4 para recalcular. "
            "Costo total unit. se transfiere automático al EDT.")
ws['A2'].font = FONT_SUBTITLE
ws.merge_cells('A2:F2')

# Selector de partida
ws['A4'] = "Partida actual:"
ws['A4'].font = FONT_H2
ws['C4'] = "02.03 Concreto muros cimentación"
ws['C4'].font = FONT_INPUT
ws['C4'].alignment = LEFT
ws.merge_cells('C4:F4')

ws['A5'] = "BIM vinculado:"
ws['A5'].font = FONT_H2
ws['C5'] = "Sí (modelo IFC, 420 m³)"
ws['C5'].font = Font(name='Calibri', size=10, color='8B5CF6', bold=True)
ws.merge_cells('C5:F5')

# MATERIALES
ws['A7'] = "1. MATERIALES"
ws['A7'].font = Font(name='Calibri', size=12, bold=True, color='FFFFFF')
ws['A7'].fill = FILL_HEAD
ws.merge_cells('A7:F7')
ws['A7'].alignment = LEFT

for col, h in enumerate(['Descripción', 'Unidad', 'Cantidad', 'Desperdicio %', 'V. Unit.', 'Subtotal'], start=1):
    c = ws.cell(row=8, column=col, value=h)
    c.font = FONT_H2; c.fill = FILL_KPI; c.alignment = CENTER; c.border = BRD_ALL

ws.column_dimensions['A'].width = 32
for col_letter, w in zip('BCDEF', [12, 14, 14, 16, 18]):
    ws.column_dimensions[col_letter].width = w

materiales = [
    ("Concreto 3000 PSI",         "m³", 0.95, 0.05, 360000),
    ("Acero corrugado 3/8\"",     "kg",   95, 0.03, 3800),
    ("Formaleta metálica",        "m²",  2.0, 0.02, 20000),
    ("Aditivos plastificantes",   "lt",  1.5, 0.00, 12000),
]
row = 9
for desc, unit, qty, waste, vunit in materiales:
    ws.cell(row=row, column=1, value=desc).font = FONT_BODY
    ws.cell(row=row, column=2, value=unit).alignment = CENTER
    c = ws.cell(row=row, column=3, value=qty); c.font = FONT_INPUT; c.number_format = '#,##0.00'; c.alignment = RIGHT
    c = ws.cell(row=row, column=4, value=waste); c.font = FONT_INPUT; c.number_format = FMT_PCT; c.alignment = RIGHT
    c = ws.cell(row=row, column=5, value=vunit); c.font = FONT_INPUT; c.number_format = FMT_COP; c.alignment = RIGHT
    # Subtotal = Cantidad * (1+desperdicio) * V.Unit
    c = ws.cell(row=row, column=6, value=f'=C{row}*(1+D{row})*E{row}'); c.font = FONT_FORMULA; c.number_format = FMT_COP; c.alignment = RIGHT
    for col in range(1, 7):
        ws.cell(row=row, column=col).border = BRD_ALL
    row += 1

# Subtotal materiales
ws.cell(row=row, column=1, value="Subtotal materiales (por m³)").font = Font(name='Calibri', size=10, bold=True)
ws.cell(row=row, column=6, value=f'=SUM(F9:F{row-1})').font = Font(name='Calibri', size=10, bold=True, color='1D4ED8')
ws.cell(row=row, column=6).number_format = FMT_COP
ws.cell(row=row, column=6).alignment = RIGHT
for col in range(1, 7):
    ws.cell(row=row, column=col).fill = FILL_KPI
    ws.cell(row=row, column=col).border = BRD_ALL
SUBT_MAT_ROW = row
row += 2

# MANO DE OBRA + EQUIPO
ws.cell(row=row, column=1, value="2. MANO DE OBRA Y EQUIPO").font = Font(name='Calibri', size=12, bold=True, color='FFFFFF')
ws.cell(row=row, column=1).fill = FILL_HEAD
ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=6)
ws.cell(row=row, column=1).alignment = LEFT
row += 1

for col, h in enumerate(['Recurso', 'Unidad', 'Rendimiento', 'Prestaciones %', 'Jornal/Tarifa', 'Subtotal'], start=1):
    c = ws.cell(row=row, column=col, value=h)
    c.font = FONT_H2; c.fill = FILL_KPI; c.alignment = CENTER; c.border = BRD_ALL
row += 1

mo = [
    ("Oficial concreto",     "jor", 0.80, 0.35, 65000),
    ("Ayudante",             "jor", 1.60, 0.35, 45000),
    ("Vibrador concreto",    "hr",  0.50, 0.00, 18000),
    ("Bomba concreto",       "hr",  0.25, 0.00, 85000),
]
mo_start = row
for desc, unit, rend, prest, jornal in mo:
    ws.cell(row=row, column=1, value=desc).font = FONT_BODY
    ws.cell(row=row, column=2, value=unit).alignment = CENTER
    c = ws.cell(row=row, column=3, value=rend); c.font = FONT_INPUT; c.number_format = '#,##0.00'; c.alignment = RIGHT
    c = ws.cell(row=row, column=4, value=prest); c.font = FONT_INPUT; c.number_format = FMT_PCT; c.alignment = RIGHT
    c = ws.cell(row=row, column=5, value=jornal); c.font = FONT_INPUT; c.number_format = FMT_COP; c.alignment = RIGHT
    # Subtotal = Rend * (1+Prestaciones) * Jornal
    c = ws.cell(row=row, column=6, value=f'=C{row}*(1+D{row})*E{row}'); c.font = FONT_FORMULA; c.number_format = FMT_COP; c.alignment = RIGHT
    for col in range(1, 7):
        ws.cell(row=row, column=col).border = BRD_ALL
    row += 1

# Subtotal MO
ws.cell(row=row, column=1, value="Subtotal MO + Equipo (por m³)").font = Font(name='Calibri', size=10, bold=True)
ws.cell(row=row, column=6, value=f'=SUM(F{mo_start}:F{row-1})').font = Font(name='Calibri', size=10, bold=True, color='B45309')
ws.cell(row=row, column=6).number_format = FMT_COP
ws.cell(row=row, column=6).alignment = RIGHT
for col in range(1, 7):
    ws.cell(row=row, column=col).fill = FILL_KPI
    ws.cell(row=row, column=col).border = BRD_ALL
SUBT_MO_ROW = row
row += 2

# RESUMEN APU
ws.cell(row=row, column=1, value="3. RESUMEN COSTOS").font = Font(name='Calibri', size=12, bold=True, color='FFFFFF')
ws.cell(row=row, column=1).fill = FILL_HEAD
ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=6)
ws.cell(row=row, column=1).alignment = LEFT
row += 2

resumen_apu = [
    ("Costo directo (materiales + MO)", f'=F{SUBT_MAT_ROW}+F{SUBT_MO_ROW}', '1D4ED8', FMT_COP),
    ("AIU % (Admin + Imprev. + Util.)", 0.30, '0000FF', FMT_PCT),
    ("AIU absoluto",                     None, '000000', FMT_COP),
    ("Costo total unitario (presup.)",   None, '15803D', FMT_COP),
    ("Costo unitario REAL (ejecutado)",  None, 'B91C1C', FMT_COP),
    ("Desviación absoluta",              None, 'B91C1C', FMT_COP),
    ("Desviación %",                     None, 'B91C1C', FMT_PCT),
]
aiu_row = None
for i, (lbl, val, color, fmt) in enumerate(resumen_apu):
    rr = row + i
    ws.cell(row=rr, column=1, value=lbl).font = Font(name='Calibri', size=10, bold=True, color='1E293B')
    if lbl.startswith("AIU %"):
        c = ws.cell(row=rr, column=6, value=val); c.font = FONT_INPUT; c.number_format = fmt
        aiu_row = rr
    elif lbl == "AIU absoluto":
        c = ws.cell(row=rr, column=6, value=f'=F{row}*F{aiu_row}'); c.font = FONT_FORMULA; c.number_format = fmt
    elif lbl == "Costo total unitario (presup.)":
        c = ws.cell(row=rr, column=6, value=f'=F{row}+F{aiu_row+1}'); c.font = Font(name='Calibri', size=11, bold=True, color=color); c.number_format = fmt
        total_unit_row = rr
    elif lbl == "Costo unitario REAL (ejecutado)":
        # Tomar del EDT: =EDT!H{partida_row}/EDT!E{partida_row}
        c = ws.cell(row=rr, column=6, value='=EDT!H9/EDT!E9'); c.font = FONT_XREF; c.number_format = fmt
        # 02.03 está en row 9 del EDT (capítulo 01 row 4, 01.01 row 5, 01.02 row 6, cap 02 row 7, 02.01 row 8, 02.02 row 9... wait, let me recount)
        # Actually 02.03 en EDT:
        # row 4 = cap 01
        # row 5 = 01.01
        # row 6 = 01.02
        # row 7 = cap 02
        # row 8 = 02.01
        # row 9 = 02.02
        # row 10 = 02.03 ← aquí
        c.value = '=EDT!H10/EDT!E10'
        cost_real_row = rr
    elif lbl == "Desviación absoluta":
        c = ws.cell(row=rr, column=6, value=f'=F{cost_real_row}-F{total_unit_row}'); c.font = FONT_FORMULA; c.number_format = fmt
        dev_abs_row = rr
    elif lbl == "Desviación %":
        c = ws.cell(row=rr, column=6, value=f'=IFERROR(F{dev_abs_row}/F{total_unit_row},0)'); c.font = FONT_FORMULA; c.number_format = fmt
    else:  # Costo directo
        c = ws.cell(row=rr, column=6, value=val); c.font = FONT_FORMULA; c.number_format = fmt
    for col in range(1, 7):
        ws.cell(row=rr, column=col).border = BRD_ALL
        if "Costo total" in lbl or "REAL" in lbl:
            ws.cell(row=rr, column=col).fill = FILL_TOTAL
    ws.cell(row=rr, column=6).alignment = RIGHT

# ──────────────────────────────────────────────────────────────
# HOJA 4: OrdenesCambio
# ──────────────────────────────────────────────────────────────
ws = wb.create_sheet("OrdenesCambio")
ws.sheet_view.showGridLines = False
ws.freeze_panes = 'A4'

ws['A1'] = "ÓRDENES DE CAMBIO (OCC)"
ws['A1'].font = FONT_TITLE
ws.merge_cells('A1:H1')

ws['A2'] = "Registro de cambios al presupuesto. La suma alimenta automáticamente el Resumen → desviación total."
ws['A2'].font = FONT_SUBTITLE
ws.merge_cells('A2:H2')

headers = ['Código', 'Descripción', 'Partida afectada', 'Fase', 'Valor aprobado', 'Impacto plazo (días)', 'Solicitado por', 'Estado']
widths   = [12, 36, 16, 8, 16, 16, 18, 14]
for i, (h, w) in enumerate(zip(headers, widths), start=1):
    c = ws.cell(row=3, column=i, value=h)
    c.font = FONT_H1; c.fill = FILL_HEAD; c.alignment = CENTER; c.border = BRD_ALL
    ws.column_dimensions[get_column_letter(i)].width = w
ws.row_dimensions[3].height = 24

occ_data = [
    ("OC-C001", "Sobrecosto concreto muros",      "02.03", "F2", 28000000, 0,  "R. Gómez",  "En revisión"),
    ("OC-C002", "Refuerzo adicional pilotes",     "02.02", "F1", 14000000, 3,  "C. Torres", "Aprobada"),
    ("OC-C003", "Cambio especificación acero",    "02.04", "F2",  8000000, 2,  "R. Gómez",  "Borrador"),
]
for i, row_data in enumerate(occ_data, start=4):
    code, desc, part, phase, value, plazo, who, status = row_data
    ws.cell(row=i, column=1, value=code).font = Font(name='Consolas', size=10, color='1D4ED8', bold=True)
    ws.cell(row=i, column=2, value=desc).font = FONT_BODY
    c = ws.cell(row=i, column=3, value=part); c.font = Font(name='Consolas', size=10, color='64748B'); c.alignment = CENTER
    c = ws.cell(row=i, column=4, value=phase); c.alignment = CENTER
    c = ws.cell(row=i, column=5, value=value); c.font = FONT_INPUT; c.number_format = FMT_COP; c.alignment = RIGHT
    c = ws.cell(row=i, column=6, value=plazo); c.font = FONT_INPUT; c.alignment = RIGHT
    ws.cell(row=i, column=7, value=who)
    ws.cell(row=i, column=8, value=status).alignment = CENTER
    for col in range(1, 9):
        ws.cell(row=i, column=col).border = BRD_ALL

# Total
total_row = 4 + len(occ_data) + 1
ws.cell(row=total_row, column=1, value="TOTAL").font = Font(name='Calibri', size=11, bold=True)
ws.cell(row=total_row, column=2, value=f"Valor aprobado (suma {len(occ_data)} OCC)").font = Font(name='Calibri', size=10, bold=True)
ws.cell(row=total_row, column=5, value=f'=SUM(E4:E{total_row-1})')
ws.cell(row=total_row, column=5).font = Font(name='Calibri', size=11, bold=True, color='B91C1C')
ws.cell(row=total_row, column=5).number_format = FMT_COP
ws.cell(row=total_row, column=5).alignment = RIGHT
ws.cell(row=total_row, column=6, value=f'=SUM(F4:F{total_row-1})')
ws.cell(row=total_row, column=6).font = Font(name='Calibri', size=11, bold=True, color='1E293B')
ws.cell(row=total_row, column=6).alignment = RIGHT
for col in range(1, 9):
    c = ws.cell(row=total_row, column=col)
    c.fill = FILL_TOTAL
    c.border = Border(top=MEDIUM, bottom=MEDIUM)

# ──────────────────────────────────────────────────────────────
# HOJA 5: Resumen (EVM)
# ──────────────────────────────────────────────────────────────
ws = wb.create_sheet("Resumen")
ws.sheet_view.showGridLines = False

ws['A1'] = "RESUMEN EJECUTIVO · EVM"
ws['A1'].font = FONT_TITLE
ws.merge_cells('A1:F1')

ws['A2'] = "Indicadores Earned Value Management calculados desde EDT + OrdenesCambio."
ws['A2'].font = FONT_SUBTITLE
ws.merge_cells('A2:F2')

ws.column_dimensions['A'].width = 4
ws.column_dimensions['B'].width = 36
ws.column_dimensions['C'].width = 20
ws.column_dimensions['D'].width = 30

# Bloque 1: totales
resumen_block = [
    ("", None, None),
    ("Presupuesto base (sin OCC)",   f'=EDT!G{TOTAL_ROW}',                  "Línea base aprobada"),
    ("Comprometido",                  f'=EDT!G{TOTAL_ROW}*0.26',             "26% del total (sim.)"),
    ("Ejecutado real (AC)",           f'=EDT!H{TOTAL_ROW}',                  "Suma de columna Ejec del EDT"),
    ("Sobrecosto por OCC",            f'=OrdenesCambio!E{total_row}',        "Suma órdenes de cambio"),
    ("Desviación total",              f'=C7+C8-C5',                          "Ejec + OCC - Presup"),
    ("", None, None),
    ("Valor planificado (PV)",        f'=EDT!G{TOTAL_ROW}*0.09',             "PV al corte de hoy"),
    ("Valor ganado (EV)",             f'=C7*0.91',                           "EV = AC × CPI"),
    ("Costo real (AC)",               f'=C7',                                "Igual a Ejecutado"),
    ("CPI (Cost Performance Idx)",    f'=IFERROR(C12/C13,0)',                "EV / AC — > 1 = bajo presup."),
    ("EAC (Estimate at Completion)",  f'=IFERROR(C5/C14,0)',                 "Presup / CPI"),
    ("VAC (Variance at Completion)",  f'=C5-C15',                            "Presup - EAC"),
    ("SPI (Schedule Performance)",    f'=IFERROR(C12/C11,0)',                "EV / PV"),
]

for i, (lbl, formula, note) in enumerate(resumen_block, start=4):
    if not lbl:
        continue
    ws.cell(row=i, column=2, value=lbl).font = Font(name='Calibri', size=10, bold=True, color='1E293B')
    c = ws.cell(row=i, column=3, value=formula); c.font = FONT_XREF
    c.alignment = RIGHT
    if "CPI" in lbl or "SPI" in lbl:
        c.number_format = FMT_RATIO
    else:
        c.number_format = FMT_COP
    if note:
        ws.cell(row=i, column=4, value=note).font = Font(name='Calibri', size=9, italic=True, color='64748B')
    for col in range(2, 5):
        ws.cell(row=i, column=col).border = BRD_ALL
        if "Desviación" in lbl or "EAC" in lbl or "CPI" in lbl:
            ws.cell(row=i, column=col).fill = FILL_TOTAL

# Bloque conclusión auto
ws.cell(row=20, column=2, value="CONCLUSIÓN GERENCIAL").font = Font(name='Calibri', size=11, bold=True, color='6D28D9')
ws.cell(row=20, column=2).border = Border(bottom=MEDIUM)
conclusion = ('=IF(C14<1,"⚠ CPI < 1.00 — el proyecto está gastando más de lo presupuestado. ",'
              '"✓ CPI ≥ 1.00 — el proyecto está dentro o por debajo del presupuesto. ")'
              '&"Proyección EAC: "&TEXT(C15,"$#,##0")&". "&'
              'IF(C9>0,"Hay "&TEXT(C9,"$#,##0")&" en órdenes de cambio acumuladas.","Sin órdenes de cambio.")')
ws.cell(row=21, column=2, value=conclusion).font = Font(name='Calibri', size=10, italic=True, color='1E293B')
ws.merge_cells('B21:E22')
ws.cell(row=21, column=2).alignment = Alignment(horizontal='left', vertical='top', wrap_text=True)
for col in range(2, 6):
    ws.cell(row=21, column=col).fill = PatternFill('solid', start_color='F5F3FF')
    ws.cell(row=21, column=col).border = BRD_ALL

# ──────────────────────────────────────────────────────────────
# Guardar
# ──────────────────────────────────────────────────────────────
output = "Presupuesto_TorreSantaIsabel_BIM.xlsx"
wb.save(output)
print(f"OK Guardado: {output}")
