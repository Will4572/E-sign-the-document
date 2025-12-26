# FILE: send_bulk_emails.py
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import time
import datetime 
import config   

# --- CẤU HÌNH CHUNG ---
EXCEL_FILE = "學生名單表格.xlsx"
MY_EMAIL = "will181@gms.dyhu.edu.tw"
MY_PASS = "rymt qfhl zisg kxjq" 
SENDER_NAME = "德育護理健康學院"
BASE_URL = "https://e-sign-the-document-a3225vjbjqzbnzicnuskbh.streamlit.app" 

# ==============================================================================
# 👇 [CÔNG TẮC] BẠN MUỐN GỬI VĂN BẢN NÀO? SỬA SỐ Ở ĐÂY (1 HOẶC 2) 👇
# ==============================================================================
CHON_VAN_BAN = 1  
# Số 1 = Cam kết Nhập học (Cũ)
# Số 2 = Cam kết Làm thêm (Mới)
# ==============================================================================

# --- CẤU HÌNH NỘI DUNG DỰA TRÊN SỐ BẠN CHỌN ---
if CHON_VAN_BAN == 1:
    # --- VĂN BẢN 1: NHẬP HỌC ---
    DOC_TITLE_ZH = "就讀國際專修部與產學專班切結書"
    EMAIL_TEXTS = {
        "vi": { "subject": "Vui lòng ký cam kết học tập", "doc_title": "BẢN CAM KẾT THEO HỌC HỆ DỰ BỊ QUỐC TẾ & VỪA HỌC VỪA LÀM", "greeting": "Chào bạn", "id_label": "Mã sinh viên:", "intro": "Vui lòng nhấn vào liên kết bên dưới để ký cam kết:", "btn_label": "Nhấn để ký ngay", "fallback": "(Nếu nút trên không hoạt động, hãy copy link này):", "footer": "(Link này dành riêng cho bạn, vui lòng không chia sẻ)" },
        "th": { "subject": "กรุณาลงนามในหนังสือสัญญา", "doc_title": "หนังสือสัญญาการเข้าศึกษาในหลักสูตรเตรียมความพร้อมนานาชาติ", "greeting": "เรียน", "id_label": "รหัสนักศึกษา:", "intro": "กรุณาคลิกลิงก์ด้านล่างเพื่อลงนามในเอกสาร:", "btn_label": "คลิกเพื่อลงนาม", "fallback": "(หากปุ่มใช้งานไม่ได้ โปรดคัดลอกลิงก์ด้านล่าง):", "footer": "(ลิงก์นี้สำหรับคุณเท่านั้น โปรดอย่าแชร์)" },
        "id": { "subject": "Silakan Tanda Tangani Surat", "doc_title": "SURAT PERNYATAAN MENGIKUTI PROGRAM PERSIAPAN INTERNASIONAL", "greeting": "Halo", "id_label": "NIM:", "intro": "Silakan klik tautan di bawah ini untuk menandatangani:", "btn_label": "Klik untuk Tanda Tangan", "fallback": "(Jika tombol tidak berfungsi, salin tautan ini):", "footer": "(Tautan ini khusus untuk Anda, mohon jangan dibagikan)" },
        "zh": { "subject": "請簽署就讀切結書", "doc_title": "就讀國際專修部與產學專班切結書", "greeting": "你好", "id_label": "您的學號:", "intro": "請點擊以下連結簽署文件：", "btn_label": "點擊簽署", "fallback": "(若按鈕無法使用，請複製下方連結)：", "footer": "(此連結僅供您使用，請勿分享)" }
    }
else:
    # --- VĂN BẢN 2: LÀM THÊM ---
    DOC_TITLE_ZH = "國際專修部華語先修班與國際學生工讀須知切結書"
    EMAIL_TEXTS = {
        "vi": { "subject": "Vui lòng ký cam kết quy định làm thêm", "doc_title": "BẢN CAM KẾT VỀ QUY ĐỊNH LÀM THÊM (WORK-STUDY)", "greeting": "Chào bạn", "id_label": "Mã sinh viên:", "intro": "Vui lòng nhấn vào liên kết bên dưới để ký cam kết:", "btn_label": "Nhấn để ký ngay", "fallback": "(Nếu nút trên không hoạt động, hãy copy link này):", "footer": "(Link này dành riêng cho bạn, vui lòng không chia sẻ)" },
        "th": { "subject": "กรุณาลงนามในข้อตกลงการทำงานพาร์ทไทม์", "doc_title": "หนังสือสัญญาข้อควรทราบเกี่ยวกับการทำงานพาร์ทไทม์", "greeting": "เรียน", "id_label": "รหัสนักศึกษา:", "intro": "กรุณาคลิกลิงก์ด้านล่างเพื่อลงนามในเอกสาร:", "btn_label": "คลิกเพื่อลงนาม", "fallback": "(หากปุ่มใช้งานไม่ได้ โปรดคัดลอกลิงก์ด้านล่าง):", "footer": "(ลิงก์นี้สำหรับคุณเท่านั้น โปรดอย่าแชร์)" },
        "id": { "subject": "Silakan Tanda Tangani Peraturan Kerja", "doc_title": "SURAT PERNYATAAN MENGENAI PERATURAN KERJA PARUH WAKTU", "greeting": "Halo", "id_label": "NIM:", "intro": "Silakan klik tautan di bawah ini untuk menandatangani:", "btn_label": "Klik untuk Tanda Tangan", "fallback": "(Jika tombol tidak berfungsi, salin tautan ini):", "footer": "(Tautan ini khusus untuk Anda, mohon jangan dibagikan)" },
        "zh": { "subject": "請簽署工讀須知切結書", "doc_title": "國際專修部華語先修班與國際學生工讀須知切結書", "greeting": "你好", "id_label": "您的學號:", "intro": "請點擊以下連結簽署文件：", "btn_label": "點擊簽署", "fallback": "(若按鈕無法使用，請複製下方連結)：", "footer": "(此連結僅供您使用，請勿分享)" }
    }

def send_invitation(to_email, name_en, student_id, lang_code='zh'):
    msg = MIMEMultipart()
    msg['From'] = formataddr((SENDER_NAME, MY_EMAIL))
    msg['To'] = to_email
    
    text = EMAIL_TEXTS.get(lang_code, EMAIL_TEXTS['zh'])
    
    # Thêm thời gian để tránh bị gộp email
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    msg['Subject'] = f"[{current_time}] {text['subject']}"
    
    clean_id = str(student_id).strip()
    personal_link = f"{BASE_URL}/?id={clean_id}"
    
    # --- ĐÂY LÀ GIAO DIỆN HTML ĐẸP MÀ BẠN YÊU CẦU (GIỮ NGUYÊN GỐC) ---
    body = f"""
    <div style="font-family: Arial, sans-serif; border: 1px solid #ddd; border-radius: 10px; overflow: hidden; max-width: 600px; margin: auto;">
        <div style="background-color: #003366; color: white; padding: 20px; text-align: center;">
            <h2 style="margin: 0;">德育護理健康學院</h2>
        </div>

        <div style="padding: 20px; background-color: #fff;">
            
            <div style="border-bottom: 2px solid #eee; padding-bottom: 15px; margin-bottom: 20px; text-align: center;">
                <p style="font-weight: bold; color: #003366; margin: 5px 0;">{DOC_TITLE_ZH}</p>
                <p style="font-weight: bold; color: #555; margin: 5px 0;">{text['doc_title']}</p>
            </div>

            <p style="font-size: 16px;">
                親愛的 <b>{name_en}</b> 同學 您好 / {text['greeting']} <b>{name_en}</b>,
            </p>
            
            <div style="background-color: #eef7ff; border-left: 5px solid #003366; padding: 10px; margin: 15px 0;">
                <p style="margin: 0; font-size: 14px; color: #333;">您的學號 / {text['id_label']}</p>
                <p style="margin: 5px 0 0 0; font-size: 20px; font-weight: bold; color: #003366; letter-spacing: 2px;">
                    {clean_id}
                </p>
            </div>

            <p>請點擊以下連結簽署文件：<br>
            {text['intro']}</p>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="{personal_link}" style="background-color: #003366; color: white; padding: 15px 25px; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 16px; display: inline-block;">
                   ✍️ 點擊簽署 / {text['btn_label']}
                </a>
            </div>
            
            <p style="color: #666; font-size: 14px;">若按鈕無法使用，請複製下方連結：<br>
            {text['fallback']}</p>
            <p style="background-color: #f0f0f0; padding: 10px; word-break: break-all; font-family: monospace;">{personal_link}</p>
            
            <br>
            <p style="color: #555;">(此連結僅供您使用，請勿分享)<br>
            {text['footer']}</p>
        </div>
        
        <div style="text-align: center; font-size: 10px; color: #aaa; margin-bottom: 10px; border-top: 1px dashed #eee; padding-top: 5px;">
             System developed by: Trần Văn Khánh
        </div>
    </div>
    """
    msg.attach(MIMEText(body, 'html', 'utf-8'))
    
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(MY_EMAIL, MY_PASS)
        server.send_message(msg)
        server.quit()
        print(f"✅ Đã gửi cho: {name_en} ({to_email}) [Lang: {lang_code}]")
        return True
    except Exception as e:
        print(f"❌ Lỗi gửi cho {name_en}: {e}")
        return False

# --- CHẠY ---
if __name__ == "__main__":
    try:
        df = pd.read_excel(EXCEL_FILE, dtype={'學號': str})
        df.columns = df.columns.str.replace(' ', '')
        
        print(f"--- ĐANG CHẠY CHẾ ĐỘ GỬI VĂN BẢN SỐ: {CHON_VAN_BAN} ---")
        print(f"Tiêu đề: {DOC_TITLE_ZH}")
        
        for index, row in df.iterrows():
            email = row.get('Gmail')
            name = row.get('英文姓名') if pd.notna(row.get('英文姓名')) else row.get('中文姓名')
            sid = row.get('學號')
            nat = row.get('國籍', '台灣')
            lang = config.NATIONALITY_MAP.get(nat, 'zh')
            
            if pd.notna(email):
                send_invitation(email, name, sid, lang)
                time.sleep(2)
            else:
                print(f"⚠️ Bỏ qua {sid}")
                
        print("\n✅ HOÀN TẤT!")
    except Exception as e:
        print(f"Lỗi: {e}")