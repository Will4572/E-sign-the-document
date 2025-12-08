# FILE: send_bulk_emails.py
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import time
import datetime # Thư viện lấy giờ hiện tại
import config   

# --- CẤU HÌNH ---
EXCEL_FILE = "學生名單表格.xlsx"
MY_EMAIL = "will181@gms.dyhu.edu.tw"
MY_PASS = "" 
SENDER_NAME = "德育護理健康學院"
BASE_URL = "https://e-sign-the-document-a3225vjbjqzbnzicnuskbh.streamlit.app/" 

# --- NỘI DUNG TIẾNG TRUNG MỚI (BẠN ĐÃ SỬA) ---
DOC_TITLE_ZH = "就讀國際專修部與產學專班切結書"

# --- TỪ ĐIỂN EMAIL ---
EMAIL_TEXTS = {
    "vi": { "subject": "Vui lòng ký cam kết học tập", "doc_title": "BẢN CAM KẾT XIN HỌC ĐẠI HỌC (ĐẠT CHUẨN A2)", "greeting": "Chào bạn", "id_label": "Mã sinh viên:", "intro": "Nhấn link dưới để ký:", "btn_label": "Ký ngay", "fallback": "Copy link:", "footer": "Link riêng tư" },
    "th": { "subject": "กรุณาลงนามในหนังสือสัญญา", "doc_title": "หนังสือสัญญาสำหรับนักศึกษา (ผ่านระดับ A2)", "greeting": "เรียน", "id_label": "รหัสนักศึกษา:", "intro": "คลิกลิงก์เพื่อลงนาม:", "btn_label": "ลงนาม", "fallback": "คัดลอกลิงก์:", "footer": "ห้ามแชร์" },
    "id": { "subject": "Silakan Tanda Tangani Surat", "doc_title": "SURAT PERNYATAAN MAHASISWA (LULUS A2)", "greeting": "Halo", "id_label": "NIM:", "intro": "Klik tautan:", "btn_label": "Tanda Tangan", "fallback": "Salin tautan:", "footer": "Jangan bagikan" },
    "zh": { "subject": "請簽署就讀切結書", "doc_title": "申請就讀大學切結書", "greeting": "你好", "id_label": "您的學號:", "intro": "請點擊連結簽署：", "btn_label": "點擊簽署", "fallback": "複製連結：", "footer": "請勿分享" }
}

def send_invitation(to_email, name_en, student_id, lang_code='zh'):
    msg = MIMEMultipart()
    msg['From'] = formataddr((SENDER_NAME, MY_EMAIL))
    msg['To'] = to_email
    
    text = EMAIL_TEXTS.get(lang_code, EMAIL_TEXTS['zh'])
    
    # [QUAN TRỌNG] THÊM GIỜ VÀO TIÊU ĐỀ ĐỂ KHÔNG BỊ GỘP EMAIL CŨ
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    msg['Subject'] = f"[{current_time}] {text['subject']}"
    
    clean_id = str(student_id).strip()
    personal_link = f"{BASE_URL}/?id={clean_id}"
    
    body = f"""
    <div style="font-family: Arial, sans-serif; border: 1px solid #ddd; padding: 20px; max-width: 600px; margin: auto;">
        <h2 style="color: #003366; text-align: center;">德育護理健康學院</h2>
        <div style="text-align: center; border-bottom: 2px solid #eee; padding-bottom: 15px;">
            <h3 style="color: #003366; margin: 5px;">{DOC_TITLE_ZH}</h3>
            <p style="color: #555; font-weight: bold;">{text['doc_title']}</p>
        </div>
        <p>Dear <b>{name_en}</b> / {text['greeting']} <b>{name_en}</b>,</p>
        <div style="background-color: #eef7ff; padding: 15px; text-align: center; margin: 20px 0;">
            ID: <b style="font-size: 20px; color: #003366;">{clean_id}</b>
        </div>
        <p style="text-align: center;">
            <a href="{personal_link}" style="background-color: #003366; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
               ✍️ {text['btn_label']}
            </a>
        </p>
        <p style="font-size: 12px; color: #777;">{personal_link}</p>
    </div>
    """
    msg.attach(MIMEText(body, 'html', 'utf-8'))
    
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(MY_EMAIL, MY_PASS)
        server.send_message(msg)
        server.quit()
        print(f"✅ Đã gửi: {name_en} - {current_time}")
        return True
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False

if __name__ == "__main__":
    try:
        df = pd.read_excel(EXCEL_FILE, dtype={'學號': str})
        df.columns = df.columns.str.replace(' ', '')
        print(f"Bắt đầu gửi {len(df)} email...")
        for index, row in df.iterrows():
            email = row.get('Gmail')
            name = row.get('英文姓名') if pd.notna(row.get('英文姓名')) else row.get('中文姓名')
            sid = row.get('學號')
            nat = row.get('國籍', '台灣')
            lang = config.NATIONALITY_MAP.get(nat, 'zh')
            
            if pd.notna(email):
                send_invitation(email, name, sid, lang)
                time.sleep(2)
    except Exception as e:

        print(f"Lỗi: {e}")
