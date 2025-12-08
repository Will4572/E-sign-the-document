# FILE: pdf_gen.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
import config
from datetime import datetime
import os

FONT_UNIVERSAL = 'UniversalFont'
FONT_THAI = 'ThaiFont'
PATH_UNIVERSAL = 'UniversalFont.ttf'
PATH_THAI = 'ThaiFont.ttf'

try:
    if os.path.exists(PATH_UNIVERSAL):
        pdfmetrics.registerFont(TTFont(FONT_UNIVERSAL, PATH_UNIVERSAL))
        pdfmetrics.registerFont(TTFont(FONT_UNIVERSAL + '-Bold', PATH_UNIVERSAL)) 
        pdfmetrics.registerFont(TTFont(FONT_UNIVERSAL + '-Italic', PATH_UNIVERSAL))
    else:
        FONT_UNIVERSAL = 'Helvetica'
except:
    FONT_UNIVERSAL = 'Helvetica'

try:
    if os.path.exists(PATH_THAI):
        pdfmetrics.registerFont(TTFont(FONT_THAI, PATH_THAI))
    else:
        FONT_THAI = FONT_UNIVERSAL 
except:
    FONT_THAI = FONT_UNIVERSAL

def add_footer(canvas, doc):
    canvas.saveState()
    font_name = FONT_UNIVERSAL if FONT_UNIVERSAL in canvas.getAvailableFonts() else 'Helvetica'
    canvas.setFont(font_name, 9)
    page_num = f"Page {doc.page}"
    canvas.drawRightString(20*cm, 1*cm, page_num)
    canvas.restoreState()

def create_pdf(filename, student_data, checked_clauses, signature_img, lang, doc_data):
    # GIẢM LỀ TRANG TỐI ĐA ĐỂ TIẾT KIỆM GIẤY (1.2cm)
    doc = SimpleDocTemplate(filename, pagesize=A4, 
                            rightMargin=1.5*cm, leftMargin=1.5*cm, 
                            topMargin=1.2*cm, bottomMargin=1.2*cm)
    story = []
    styles = getSampleStyleSheet()
    
    style_school = ParagraphStyle('School', parent=styles['Normal'], fontName=FONT_UNIVERSAL, fontSize=16, leading=20, alignment=TA_CENTER, spaceAfter=5)
    style_h1 = ParagraphStyle('H1', parent=styles['Normal'], fontName=FONT_UNIVERSAL, fontSize=14, leading=18, alignment=TA_CENTER, spaceAfter=5)
    font_h2 = FONT_THAI if lang == 'th' else FONT_UNIVERSAL
    style_h2 = ParagraphStyle('H2', parent=styles['Normal'], fontName=font_h2, fontSize=11, leading=14, alignment=TA_CENTER, textColor=colors.dimgray, spaceAfter=10)
    
    align_mode = TA_LEFT 
    style_body = ParagraphStyle('Body', parent=styles['Normal'], fontName=FONT_UNIVERSAL, fontSize=11, leading=14, alignment=align_mode)
    style_cell_label = ParagraphStyle('CellL', parent=styles['Normal'], fontName=FONT_UNIVERSAL, fontSize=11, leading=13, alignment=TA_LEFT)
    style_cell_val = ParagraphStyle('CellV', parent=styles['Normal'], fontName=FONT_UNIVERSAL, fontSize=11, leading=13, alignment=TA_LEFT)
    style_check_mark = ParagraphStyle('Check', parent=styles['Normal'], fontName=FONT_UNIVERSAL, fontSize=14, leading=14, alignment=TA_CENTER)

    # 1. HEADER
    story.append(Paragraph(f"<b>德育護理健康學院</b>", style_school))
    story.append(Paragraph(f"<b>{doc_data['header_title']['zh']}</b>", style_h1))
    if lang != 'zh':
        story.append(Paragraph(doc_data['header_title'][lang], style_h2))
    story.append(Spacer(1, 0.4*cm))

    # 2. INFO TABLE
    f = config.COMMON_FIELDS
    def label_cell(key):
        zh_txt = f"<b>{f[key]['zh']}</b>"
        local_txt = f"{f[key][lang]}"
        if lang == 'th': local_txt = f'<font face="{FONT_THAI}">{local_txt}</font>'
        txt = zh_txt
        if lang != 'zh': txt += f"<br/>{local_txt}"
        return Paragraph(txt, style_cell_label)

    s_name_cn = student_data.get('中文姓名', '')
    s_name_en = student_data.get('英文姓名', '')
    s_id = str(student_data.get('學號', ''))
    s_dept = student_data.get('就讀學系', '')

    data_info = [
        [label_cell('name_cn'), Paragraph(s_name_cn, style_cell_val), label_cell('std_id'), Paragraph(s_id, style_cell_val)],
        [label_cell('name_en'), Paragraph(s_name_en, style_cell_val), label_cell('dept'),   Paragraph(s_dept, style_cell_val)],
    ]

    tbl_info = Table(data_info, colWidths=[3*cm, 5.5*cm, 3*cm, 5.5*cm])
    tbl_info.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,0), (0,-1), colors.whitesmoke),
        ('BACKGROUND', (2,0), (2,-1), colors.whitesmoke),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(tbl_info)
    story.append(Spacer(1, 0.5*cm))

    # 3. INTRO
    story.append(Paragraph(doc_data['body_intro']['zh'], style_body))
    if lang != 'zh':
        story.append(Spacer(1, 0.2*cm))
        intro_text = doc_data['body_intro'][lang]
        if lang == 'th': intro_text = f'<font face="{FONT_THAI}">{intro_text}</font>'
        story.append(Paragraph(f"<i>{intro_text}</i>", style_body))
    story.append(Spacer(1, 0.5*cm))

    # 4. CHECKLIST
    for clause in doc_data['checkboxes']:
        is_checked = checked_clauses.get(clause['id'], False)
        mark = "☑" if is_checked else "☐" 
        
        zh_text = clause['zh']
        
        if lang == 'zh':
            full_text = f"<b>{zh_text}</b>"
        else:
            local_text = clause[lang]
            if lang == 'th': local_text = f'<font face="{FONT_THAI}">{local_text}</font>'
            full_text = f"<b>{zh_text}</b><br/><i>{local_text}</i>"
        
        row_data = [[
            Paragraph(mark, style_check_mark), 
            Paragraph(full_text, style_body)
        ]]
        
        tbl_check = Table(row_data, colWidths=[1.2*cm, 15.8*cm])
        tbl_check.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(tbl_check)
        story.append(Spacer(1, 0.3*cm)) 

    # 5. FOOTER (CĂN CHỈNH SÁT NỘI DUNG)
    # Chỉ cách 0.5cm -> Đảm bảo nằm cùng trang 1 nếu còn chỗ
    story.append(Spacer(1, 0.5*cm)) 
    
    if signature_img and os.path.exists(signature_img):
        img_sig = Image(signature_img, width=4.5*cm, height=2.25*cm) 
    else:
        img_sig = Paragraph("", style_body)

    date_str = datetime.now().strftime("%Y / %m / %d")
    sign_label_zh = config.UI_LABELS['sign_title']['zh']
    sign_label_local = config.UI_LABELS['sign_title'][lang]
    if lang == 'th': sign_label_local = f'<font face="{FONT_THAI}">{sign_label_local}</font>'
    
    footer_content = [
        [
            Paragraph("此致<br/><b>德育護理健康學院</b>", style_body),
            [
                Paragraph(f"<b>{sign_label_zh}</b> / {sign_label_local}:", style_body),
                Spacer(1, 0.2*cm), 
                img_sig,
                Spacer(1, 0.2*cm),
                Paragraph(f"Date: {date_str}", style_body)
            ]
        ]
    ]

    tbl_footer = Table(footer_content, colWidths=[8.5*cm, 8.5*cm])
    tbl_footer.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (0,0), 'LEFT'),
        ('ALIGN', (1,0), (1,0), 'LEFT'),
    ]))
    story.append(tbl_footer)

    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
    return filename