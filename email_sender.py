# FILE: email_sender.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formataddr
import config
import streamlit as st 
import os

# --- CẤU HÌNH GMAIL ---
MY_EMAIL = "will181@gms.dyhu.edu.tw" 
SENDER_NAME = "德育護理健康學院"

# Lấy mật khẩu từ secrets của Streamlit hoặc dùng trực tiếp (nếu chạy local)
try:
    MY_PASSWORD = st.secrets["EMAIL_PASSWORD"]
except:
    MY_PASSWORD = "rymt qfhl zisg kxjq" 

def send_email_with_pdf(to_email, pdf_path, student_name, student_id, lang_code='zh', is_admin=False):
    """
    Hàm này dùng để gửi email xác nhận KÈM FILE PDF sau khi học sinh ký xong trên Web.
    """
    
    # --- 1. CHẶN GỬI CHO ADMIN (Theo yêu cầu của bạn) ---
    if is_admin:
        return True 

    # --- 2. XỬ LÝ GỬI CHO HỌC SINH ---
    msg = MIMEMultipart()
    msg['From'] = formataddr((SENDER_NAME, MY_EMAIL))
    msg['To'] = to_email
    
    # --- TIÊU ĐỀ SONG NGỮ ---
    # Lấy template từ config.py
    tmpl_zh = config.EMAIL_TEMPLATES['zh']
    tmpl_local = config.EMAIL_TEMPLATES.get(lang_code, config.EMAIL_TEMPLATES['zh'])
    
    subject_final = tmpl_zh['subject']
    if lang_code != 'zh':
        subject_final += f" / {tmpl_local['subject']}"
    msg['Subject'] = subject_final
    
    # --- NỘI DUNG CHÀO HỎI ---
    try: body_zh = tmpl_zh['body'].format(student_name=student_name)
    except: body_zh = tmpl_zh['body'].replace("{student_name}", student_name)
    
    try: body_local = tmpl_local['body'].format(student_name=student_name)
    except: body_local = tmpl_local['body'].replace("{student_name}", student_name)

    # --- LỜI NHẮN FILE ĐÍNH KÈM ---
    note_zh = config.UI_LABELS['email_note']['zh']
    note_local = config.UI_LABELS['email_note'][lang_code]

    # --- GHÉP KHỐI NỘI DUNG ---
    content_block = f'<div style="margin-bottom: 5px; font-weight: bold; color: #000;">{body_zh}</div>'
    if lang_code != 'zh':
        content_block += f'<div style="margin-bottom: 15px; color: #555;">{body_local}</div>'

    note_block = f'<p style="font-size: 14px; color: #333; margin-top: 20px; font-weight: bold;">{note_zh}</p>'
    if lang_code != 'zh':
        note_block += f'<p style="font-size: 14px; color: #555; margin-top: 5px;">{note_local}</p>'

    # --- HTML EMAIL GIAO DIỆN ĐẸP ---
    html_body = f"""
    <div style="font-family: Arial, sans-serif; border: 1px solid #ddd; border-radius: 10px; overflow: hidden; max-width: 600px; margin: auto;">
        <div style="background-color: #003366; color: white; padding: 20px; text-align: center;">
            <h2 style="margin: 0;">德育護理健康學院</h2>
        </div>
        <div style="padding: 25px; background-color: #fff;">
            <div style="text-align: center; margin-bottom: 20px;">
                <h3 style="color: #003366; margin: 0;">簽署完成通知</h3>
                <p style="font-weight: bold; color: #777; margin: 5px 0; font-size: 14px;">CONFIRMATION OF SIGNATURE</p>
            </div>

            {content_block}
            
            <div style="background-color: #f0f7ff; border-left: 5px solid #003366; padding: 15px; margin: 20px 0;">
                <p style="margin: 0; font-size: 13px; color: #666;">您的學號 / Student ID:</p>
                <p style="margin: 5px 0 0 0; font-size: 24px; font-weight: bold; color: #003366; letter-spacing: 1px;">
                    {student_id}
                </p>
            </div>

            {note_block}
        </div>
        <div style="background-color: #f8f9fa; padding: 15px; text-align: center; font-size: 11px; color: #999; border-top: 1px solid #eee;">
             System developed by: Trần Văn Khánh<br>
             (此郵件由系統自動發送 / This is an automated email)
        </div>
    </div>
    """
    msg.attach(MIMEText(html_body, 'html', 'utf-8'))

    # --- 3. ĐÍNH KÈM FILE PDF & GỬI ---
    try:
        if pdf_path and os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                attach = MIMEApplication(f.read(), _subtype="pdf")
                filename_only = os.path.basename(pdf_path)
                attach.add_header('Content-Disposition', 'attachment', filename=filename_only)
                msg.attach(attach)
            
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(MY_EMAIL, MY_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"✅ Gửi thành công tới: {to_email}")
        return True, "Success"
    except Exception as e:
        print(f"❌ Lỗi gửi email: {e}") 
        return False, str(e)