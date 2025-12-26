import imaplib
import email
import os
from email.header import decode_header
import re

# ============================================================
# CẤU HÌNH
# ============================================================
EMAIL_USER = "will181@gms.dyhu.edu.tw"
EMAIL_PASS = "rymt qfhl zisg kxjq" 
IMAP_SERVER = "imap.gmail.com"

ROOT_FOLDER = "KET_QUA_THU_HOACH"

# Cấu hình phân loại (Tên thư mục tiếng Trung)
FOLDER_MAP = {
    "admission":   "1_就讀承諾書",      
    "work_study":  "2_工讀須知切結書",     
    "regulations": "3_法規宣導確認書"     
}
# ============================================================

def clean_filename(filename):
    """Làm sạch tên file (Giữ lại cả chữ tiếng Trung)"""
    # isalpha() trong Python 3 nhận diện được cả chữ Hoa/Hàn/Nhật
    return "".join([c for c in filename if c.isalpha() or c.isdigit() or c in (' ', '.', '_', '-')]).rstrip()

def get_decoded_header(header_text):
    if not header_text: return ""
    decoded_list = decode_header(header_text)
    header_str = ""
    for content, encoding in decoded_list:
        if isinstance(content, bytes):
            try:
                header_str += content.decode(encoding if encoding else "utf-8")
            except:
                header_str += content.decode("utf-8", errors="ignore")
        else:
            header_str += str(content)
    return header_str

def main():
    print("="*50)
    print(f"🚀 BẮT ĐẦU TOOL (FILTERING MODE)")
    print("="*50)

    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")
    except Exception as e:
        print(f"❌ Lỗi đăng nhập: {e}")
        return

    if not os.path.exists(ROOT_FOLDER):
        os.makedirs(ROOT_FOLDER)

    print("🔍 Đang quét hộp thư...")
    status, messages = mail.search(None, '(SUBJECT "[")')
    
    if status != "OK":
        print("⚠️ Không tìm thấy email nào.")
        return

    email_ids = messages[0].split()
    total_emails = len(email_ids)
    print(f"📬 Tìm thấy {total_emails} email tiềm năng. Đang lọc file...\n")

    count_success = 0
    count_ignored = 0

    # Duyệt từ email mới nhất
    for i, e_id in enumerate(reversed(email_ids)):
        try:
            res, msg_data = mail.fetch(e_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    if msg.get_content_maintype() == 'multipart':
                        for part in msg.walk():
                            if part.get_content_maintype() == 'multipart' or part.get('Content-Disposition') is None:
                                continue

                            file_name = part.get_filename()
                            if file_name:
                                file_name = get_decoded_header(file_name)
                                
                                # 1. CHỈ TẢI PDF
                                if file_name.lower().endswith(".pdf"):
                                    
                                    # 2. KIỂM TRA TỪ KHÓA
                                    target_subfolder = None
                                    
                                    for key, folder_name in FOLDER_MAP.items():
                                        if key in file_name:
                                            target_subfolder = folder_name
                                            break
                                    
                                    # 3. NẾU KHÔNG KHỚP -> BỎ QUA
                                    if target_subfolder is None:
                                        count_ignored += 1
                                        continue 

                                    # 4. LƯU FILE
                                    save_dir = os.path.join(ROOT_FOLDER, target_subfolder)
                                    if not os.path.exists(save_dir):
                                        os.makedirs(save_dir)
                                    
                                    safe_name = clean_filename(file_name)
                                    file_path = os.path.join(save_dir, safe_name)

                                    if not os.path.exists(file_path):
                                        with open(file_path, "wb") as f:
                                            f.write(part.get_payload(decode=True))
                                        print(f"✅ [Tải về] {target_subfolder} / {safe_name}")
                                        count_success += 1
                                    else:
                                        pass

        except Exception as e:
            print(f"❌ Lỗi: {e}")
            continue
            
    mail.close()
    mail.logout()
    print("\n" + "="*50)
    print(f"🎉 HOÀN TẤT!")
    print(f"📥 Tải thành công: {count_success} file.")
    print(f"🗑️  Đã lọc bỏ: {count_ignored} file rác.")
    print(f"📂 Thư mục: {os.path.abspath(ROOT_FOLDER)}")
    print("="*50)

if __name__ == "__main__":
    main()