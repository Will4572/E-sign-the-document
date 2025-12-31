import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import time
import datetime
import config

# --- CẤU HÌNH ---
EXCEL_FILE = "學生名單表格.xlsx"
MY_EMAIL = "will181@gms.dyhu.edu.tw"
# Nhớ điền mật khẩu ứng dụng của bạn vào đây khi chạy trên máy tính
MY_PASS = "rymt qfhl zisg kxjq" 
SENDER_NAME = "德育護理健康學院"
# Link web app (Đã bỏ dấu / ở cuối để link đẹp hơn)
BASE_URL = "https://e-sign-the-document.streamlit.app" 

# --- NỘI DUNG EMAIL CHUNG (KHÔNG CẦN CHỈNH SỬA NHIỀU) ---
DOC_TITLE_ZH = "線上文件簽署通知" # Tiêu đề: Thông báo ký tài liệu trực tuyến

# Từ điển nội dung (Viết chung chung, áp dụng cho mọi loại giấy tờ)
EMAIL_TEXTS = {
    "vi": { 
        "subject": "Thông báo: Vui lòng ký tên xác nhận hồ sơ", 
        "doc_title": "THÔNG BÁO VỀ VIỆC KÝ TÊN HỒ SƠ TRỰC TUYẾN", 
        "greeting": "Chào bạn", 
        "id_label": "Mã sinh viên:", 
        "intro": "Nhà trường có hồ sơ cần bạn ký xác nhận. Vui lòng nhấn vào liên kết bên dưới để truy cập hệ thống:", 
        "btn_label": "Truy cập hệ thống ký tên", 
        "fallback": "Nếu nút trên không hoạt động, hãy copy link này:", 
        "footer": "Link này dành riêng cho bạn" 
    },
    "th": { 
        "subject": "แจ้งเตือน: กรุณาลงนามในเอกสารออนไลน์", 
        "doc_title": "ประกาศเกี่ยวกับการลงนามเอกสารออนไลน์", 
        "greeting": "เรียน", 
        "id_label": "รหัสนักศึกษา:", 
        "intro": "ทางวิทยาลัยมีเอกสารที่ต้องการให้คุณลงนาม กรุณาคลิกลิงก์ด้านล่างเพื่อเข้าสู่ระบบ:", 
        "btn_label": "เข้าสู่ระบบเพื่อลงนาม", 
        "fallback": "หากปุ่มใช้งานไม่ได้ โปรดคัดลอกลิงก์ด้านล่าง:", 
        "footer": "ลิงก์นี้สำหรับคุณเท่านั้น" 
    },
    "id": { 
        "subject": "Pemberitahuan: Silakan Tanda Tangani Dokumen", 
        "doc_title": "PEMBERITAHUAN TANDA TANGAN DOKUMEN ONLINE", 
        "greeting": "Halo", 
        "id_label": "NIM:", 
        "intro": "Ada dokumen yang perlu Anda tanda tangani. Silakan klik tautan di bawah ini:", 
        "btn_label": "Masuk ke Sistem Tanda Tangan", 
        "fallback": "Jika tombol tidak berfungsi, salin tautan ini:", 
        "footer": "Tautan ini khusus untuk Anda" 
    },
    "zh": { 
        "subject": "通知：請簽署線上文件", 
        "doc_title": "線上文件簽署通知", 
        "greeting": "你好", 
        "id_label": "您的學號:", 
        "intro": "學校有文件需要您簽署，請點擊下方連結進入系統：", 
        "btn_label": "進入簽署系統", 
        "fallback": "若按鈕無法使用，請複製下方連結：", 
        "footer": "此連結僅供您使用" 
    }
}

def send_invitation(to_email, name_en, student_id, lang_code='zh'):
    msg = MIMEMultipart()
    msg['From'] = formataddr((SENDER_NAME, MY_EMAIL))
    msg['To'] = to_email
    
    text = EMAIL_TEXTS.get(lang_code, EMAIL_TEXTS['zh'])
    
    # Thêm giờ để tránh bị Gmail gộp thư
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    msg['Subject'] = f"[{current_time}] {text['subject']}"
    
    clean_id = str(student_id).strip()
    # Tạo link: https://...app/?id=12345
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
        
        <p>{text['intro']}</p>
        
        <p style="text-align: center;">
            <a href="{personal_link}" style="background-color: #003366; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 16px;">
               👉 {text['btn_label']}
            </a>
        </p>
        
        <p style="font-size: 12px; color: #777; margin-top: 30px;">
            {text['fallback']}<br>
            <a href="{personal_link}">{personal_link}</a>
        </p>
        <p style="font-size: 12px; color: #999;">{text['footer']}</p>
    </div>
    """
    msg.attach(MIMEText(body, 'html', 'utf-8'))
    
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(MY_EMAIL, MY_PASS)
        server.send_message(msg)
        server.quit()
        print(f"✅ Đã gửi: {name_en} ({lang_code})")
        return True
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False

if __name__ == "__main__":
    try:
        df = pd.read_excel(EXCEL_FILE, dtype={'學號': str})
        df.columns = df.columns.str.replace(' ', '')
        print(f"--- BẮT ĐẦU GỬI EMAIL THÔNG BÁO ({len(df)} sinh viên) ---")
        
        count = 0
        for index, row in df.iterrows():
            email = row.get('Gmail')
            name = row.get('英文姓名') if pd.notna(row.get('英文姓名')) else row.get('中文姓名')
            sid = row.get('學號')
            nat = row.get('國籍', '台灣')
            lang = config.NATIONALITY_MAP.get(nat, 'zh')
            
            if pd.notna(email):
                send_invitation(email, name, sid, lang)
                count += 1
                
                # --- LOGIC CHỐNG SPAM & NGHỈ ---
                # Cứ gửi 1 email thì nghỉ 3 giây (an toàn cho Gmail cá nhân)
                time.sleep(3)
                
                # Cứ gửi 50 email thì nghỉ 5 phút (để tránh bị Google chặn)
                if count % 50 == 0:
                    print("⏳ Đang nghỉ 5 phút để bảo vệ tài khoản...")
                    time.sleep(300)
                    
    except Exception as e:
        print(f"Lỗi chính: {e}")