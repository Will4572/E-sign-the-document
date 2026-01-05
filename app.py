import streamlit as st
import pandas as pd
import config
from pdf_gen import create_pdf
from email_sender import send_email_with_pdf
from streamlit_drawable_canvas import st_canvas
from PIL import Image as PILImage
import os
import time
import sys
import streamlit.components.v1 as components

# 1. Cấu hình trang
st.set_page_config(page_title="Digital Signature System", page_icon="📜", layout="centered")

# --- JAVASCRIPT: "SÁT THỦ" DIỆT LOGO & AVATAR (MẠNH NHẤT) ---
js_hack = """
<script>
function killElements() {
    // 1. GIẾT HEADER & AVATAR
    const header = window.parent.document.querySelector('header');
    if (header) { header.remove(); } // Lệnh remove() xóa vĩnh viễn khỏi trang web

    // 2. GIẾT FOOTER & LOGO ĐỎ
    const footer = window.parent.document.querySelector('footer');
    if (footer) { footer.remove(); }
    
    const badges = window.parent.document.querySelectorAll('[class*="viewerBadge"]');
    badges.forEach(el => el.remove()); // Xóa sạch nút đỏ

    // 3. GIẾT TOOLBAR (Dấu 3 chấm)
    const toolbar = window.parent.document.querySelector('.stAppToolbar');
    if (toolbar) { toolbar.remove(); }
    
    // 4. FIX MÀU DROPDOWN (Giữ nguyên)
    const targets = window.parent.document.querySelectorAll('div[data-baseweb="select"]');
    targets.forEach(function(target) {
        const box = target.querySelector('div');
        if (box) {
            box.style.backgroundColor = "#fffdf0"; 
            box.style.borderColor = "#D4AF37"; 
            box.style.borderWidth = "2px";
        }
        const textItems = target.querySelectorAll('div, span');
        textItems.forEach(function(el) {
            el.style.setProperty('color', '#3d0c02', 'important'); 
            el.style.fontWeight = "bold";
        });
        const svgs = target.querySelectorAll('svg');
        svgs.forEach(function(svg) {
            svg.style.setProperty('fill', '#b22222', 'important');
        });
    });
    
    // Fix Menu xổ xuống
    const popovers = window.parent.document.querySelectorAll('div[data-baseweb="popover"]');
    popovers.forEach(function(pop) {
        pop.style.setProperty('background-color', '#fffdf0', 'important');
        pop.style.setProperty('border', '2px solid #D4AF37', 'important');
        const options = pop.querySelectorAll('li, div');
        options.forEach(function(opt) {
            opt.style.setProperty('color', '#3d0c02', 'important');
            opt.style.setProperty('background-color', '#fffdf0', 'important');
            opt.style.fontWeight = "bold";
        });
    });
}
// Chạy liên tục mỗi 50ms để đảm bảo logo không bao giờ kịp hiện ra
setInterval(killElements, 50);
</script>
"""
components.html(js_hack, height=0, width=0)

# --- CSS TÙY CHỈNH: CÂN ĐỐI MÁY TÍNH & ĐIỆN THOẠI ---
custom_style = """
    <style>
    /* ========================================================= */
    /* 1. ẨN CÁC THÀNH PHẦN THỪA (HỖ TRỢ CHO JS)                 */
    /* ========================================================= */
    header {visibility: hidden !important; display: none !important;}
    footer {display: none !important;}
    #MainMenu {display: none !important;}
    div[data-testid="stToolbar"] {display: none !important;}
    div[class*="viewerBadge"] {display: none !important;} 

    /* ========================================================= */
    /* 2. CĂN CHỈNH BỐ CỤC (FIX LỖI LỆCH MÁY TÍNH)               */
    /* ========================================================= */
    
    /* Thiết lập lề chuẩn, bỏ qua margin âm để tránh lỗi hiển thị trên PC */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 750px;
    }

    /* Nền Giấy Dó */
    .stApp {
        background-color: #fcf6e3;
        background-image: url("https://www.transparenttextures.com/patterns/rice-paper-3.png");
    }

    /* Khung Viền Hoàng Gia */
    div.block-container {
        border: 5px double #8B0000;
        border-radius: 15px;
        background-color: #ffffff;
        box-shadow: 0 15px 40px rgba(61, 12, 2, 0.4);
        margin-top: 20px;
    }

    /* --- RESPONSIVE: TỰ ĐỘNG ĐIỀU CHỈNH KHI VÀO ĐIỆN THOẠI --- */
    @media (max-width: 640px) {
        .block-container {
            padding: 15px !important; /* Lề nhỏ hơn cho điện thoại */
            margin-top: 0px !important; /* Sát lên trên */
            width: 100% !important;
            border-width: 3px !important; /* Viền thanh thoát hơn */
        }
        
        /* Chữ tiêu đề nhỏ lại xíu cho vừa màn hình */
        h1 { font-size: 2rem !important; }
        
        /* Ẩn trang trí màu sắc */
        div[data-testid="stDecoration"] { display: none !important; }
        
        /* Input to ra cho dễ bấm bằng ngón tay */
        .stTextInput>div>div>input {
            font-size: 22px !important;
            height: 55px !important;
        }
        
        /* Nút bấm to ra */
        .stButton>button {
            height: 4em !important;
            font-size: 20px !important;
        }
    }

    /* ========================================================= */
    /* 3. CHI TIẾT GIAO DIỆN HOÀNG GIA                           */
    /* ========================================================= */

    /* Font chữ */
    h1, h2, h3, h4 {
        font-family: 'Times New Roman', serif !important;
        color: #8B0000 !important;
        text-transform: uppercase;
        text-shadow: 1px 1px 0px #fff;
    }
    p, label, span, div {
        color: #000000; 
        font-family: 'Times New Roman', serif;
        font-size: 1.1rem;
    }

    /* Dropdown Menu */
    div[data-baseweb="popover"], div[data-baseweb="menu"], ul[role="listbox"] {
        background-color: #fffdf0 !important;
        border: 2px solid #D4AF37 !important;
    }
    li[role="option"] {
        color: #3d0c02 !important;
        background-color: #fffdf0 !important;
        font-weight: bold !important;
        border-bottom: 1px dashed #e0d0a0 !important;
    }
    li[role="option"]:hover, li[role="option"][aria-selected="true"] {
        background-color: #8B0000 !important;
        color: #FFD700 !important;
    }

    /* Khung nhập ID */
    .id-prompt-container {
        text-align: center;
        background: linear-gradient(180deg, #8B0000 0%, #5c0000 100%);
        padding: 15px;
        border-radius: 10px 10px 0 0;
        border: 2px solid #D4AF37;
        border-bottom: none;
        margin-bottom: -2px;
        box-shadow: 0 -5px 10px rgba(0,0,0,0.1);
    }
    .id-prompt-text-main {
        color: #FFD700 !important;
        font-size: 1.6rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px #000;
        margin-bottom: 5px;
    }
    .id-prompt-text-sub {
        color: #fff8e1 !important;
        font-size: 1rem;
        opacity: 0.9;
    }

    /* Input ID */
    .stTextInput>div>div>input { 
        text-align: center; font-size: 28px; font-weight: 900; 
        color: #b22222; 
        border: 3px solid #D4AF37;
        border-radius: 0 0 10px 10px; 
        height: 60px;
        background-color: #fffdf0;
    }

    /* Nút Bấm */
    .stButton>button {
        width: 100%; border-radius: 8px; height: 4.5em; 
        font-weight: bold; font-size: 22px; 
        border: 2px solid #D4AF37;
        background: linear-gradient(180deg, #b22222 0%, #800000 100%);
        color: #FFD700;
        box-shadow: 0 5px 0 #4a0000;
    }
    .stButton>button:hover {
        background: #c92a2a; transform: translateY(3px); box-shadow: 0 2px 0 #4a0000; color: #fff;
    }

    /* Canvas Container */
    .signature-container {
        border: 3px double #b22222;
        background-color: #fff; padding: 5px;
        border-radius: 8px;
        display: flex; justify-content: center; align-items: center;
        width: 100%;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.05);
    }
    /* Đảm bảo canvas luôn vừa vặn */
    div[data-testid="stCanvas"] canvas { 
        width: 100% !important; 
        max-width: 100% !important;
    }
    div[data-testid="stCanvas"] {
        width: 100% !important;
    }

    /* Notifications */
    .notify-error {
        position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 99999;
        padding: 30px; background: #fff; border: 4px solid #b22222; border-radius: 15px;
        text-align: center; color: #b22222; font-size: 1.3rem; font-weight: bold;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        width: 90%;
        max-width: 400px;
    }
    .success-container {
        position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 99999;
        padding: 30px; background: #fffdf0; border: 5px double #28a745; border-radius: 15px;
        text-align: center; width: 90%; max-width: 350px; box-shadow: 0 0 50px rgba(255,215,0,0.5);
    }
    .success-text { color: #28a745 !important; font-size: 1.4rem; font-weight: bold; }
    </style>
"""
st.markdown(custom_style, unsafe_allow_html=True)

def global_exception_handler(exctype, value, traceback):
    st.markdown(f"""<div class="notify-error">⚠️ Server Error: {value}</div>""", unsafe_allow_html=True)
sys.excepthook = global_exception_handler

def main():
    # --- 1. TẠO KHUNG LED ---
    marquee_placeholder = st.empty()

    def show_marquee(lang_code):
        MARQUEE_MSGS = {
            "zh": """📌 請注意： 學生完成簽名後，系統將自動寄送一份確認文件至 學生的電子郵件，同時另一份將保存於 學校系統。由於這是重要文件，所有資訊將依照學校規定進行 嚴格保密。""",
            "vi": """📌 Chú ý: Sau khi ký xong, hệ thống sẽ gửi file xác nhận về email của bạn và lưu một bản sao tại trường. Mọi thông tin sẽ được bảo mật nghiêm ngặt theo quy định.""",
            "th": """📌 หมายเหตุ: หลังจากลงนามเสร็จ ระบบจะส่งไฟล์ยืนยันไปที่อีเมลของคุณและบันทึกสำเนาไว้ที่โรงเรียน ข้อมูลทั้งหมดจะถูกเก็บเป็นความลับอย่างเคร่งครัด""",
            "id": """📌 Perhatian: Setelah tanda tangan, sistem akan mengirim konfirmasi ke email Anda dan menyimpan salinannya di sekolah. Semua informasi dijaga kerahasiaannya dengan ketat."""
        }
        
        text = MARQUEE_MSGS.get(lang_code, MARQUEE_MSGS['zh'])
        
        # --- ÉP MÀU CHỮ VÀNG TƯƠI (#FFFF00) ---
        marquee_placeholder.markdown(f"""
        <style>
        .marquee-container {{
            width: 100%; 
            background: linear-gradient(90deg, #8B0000, #5c0000);
            padding: 12px 0; 
            white-space: nowrap; overflow: hidden;
            box-sizing: border-box; 
            border-top: 3px solid #D4AF37;
            border-bottom: 3px solid #D4AF37;
            margin-bottom: 25px;
            border-radius: 5px;
            box-shadow: 0 5px 10px rgba(0,0,0,0.3);
        }}
        .marquee-content {{
            display: inline-block; padding-left: 100%;
            animation: scroll-left 25s linear infinite;
            font-family: 'Times New Roman', serif;
            letter-spacing: 1px;
        }}
        .marquee-text-span {{
            color: #FFFF00 !important; /* Vàng Chanh */
            font-size: 18px !important; 
            font-weight: 900 !important; 
            text-shadow: 2px 2px 4px #000000 !important; 
        }}
        @keyframes scroll-left {{ 0% {{ transform: translateX(0); }} 100% {{ transform: translateX(-100%); }} }}
        </style>
        <div class="marquee-container">
            <div class="marquee-content">
                <span class="marquee-text-span">{text}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Mặc định tiếng Trung
    show_marquee('zh')

    EXCEL_FILE = "學生名單表格.xlsx" 
    ADMIN_EMAIL = "will181@ems.dyhu.edu.tw"

    @st.cache_data
    def load_data():
        if not os.path.exists(EXCEL_FILE): return None
        df = pd.read_excel(EXCEL_FILE, dtype={'學號': str})
        df.columns = df.columns.str.replace(' ', '') 
        return df

    try:
        df = load_data()
        if df is None: st.error("⚠️ Không tìm thấy file Excel!"); return
    except Exception as e: st.error(f"⚠️ Lỗi đọc Excel: {e}"); return

    query_params = st.query_params
    student_id = query_params.get("id", "")

    # HEADER
    st.markdown("""
        <h1 style='text-align: center; margin-bottom: 5px; font-size: 2.5rem; text-shadow: 2px 2px 0 #fff; color: #8B0000;'>
            📜 德育護理健康學院
        </h1>
        <h4 style='text-align: center; color: #5d4037; font-weight: bold; letter-spacing: 2px; margin-top: 0;'>
            線上簽署系統 | DIGITAL SIGNATURE SYSTEM
        </h4>
    """, unsafe_allow_html=True)

    if not student_id:
        st.write("")
        st.write("")
        st.markdown("""
            <div class="id-prompt-container">
                <div class="id-prompt-text-main">🔐 請輸入學號以開始</div>
                <div class="id-prompt-text-sub">Please enter Student ID to start</div>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 10, 1]) 
        with col2:
            student_id_input = st.text_input("", max_chars=15, label_visibility="collapsed", placeholder="...")
        
        if student_id_input: student_id = student_id_input
        else: st.stop() 

    if student_id and df is not None:
        clean_search_id = str(student_id).strip()
        student_row = df[df['學號'] == clean_search_id]
        
        if student_row.empty:
            st.error(f"❌ Student ID Not Found: {clean_search_id}")
        else:
            st_data = student_row.iloc[0]
            nat_col = '國籍' if '國籍' in st_data else '籍國'
            nationality_zh = st_data.get(nat_col, '台灣')
            lang_code = config.NATIONALITY_MAP.get(nationality_zh, 'zh')
            
            show_marquee(lang_code)

            def get_ui(key): return f"{config.UI_LABELS[key]['zh']} / {config.UI_LABELS[key][lang_code]}"

            st.divider()
            
            wel_zh = config.UI_LABELS['welcome']['zh']
            wel_local = config.UI_LABELS['welcome'][lang_code]
            if lang_code == 'zh':
                welcome_text = f"👋 {wel_zh} <b>{st_data['中文姓名']}</b>"
            else:
                welcome_text = f"👋 {wel_zh} {wel_local} <b>{st_data['中文姓名']}</b>"
            
            st.markdown(f"""
            <div style="text-align: center; padding: 20px; border-radius: 10px; background-color: #fffdf0; border: 3px double #D4AF37; color: #8B0000; font-size: 1.3rem; margin-bottom: 20px;">
                {welcome_text}
            </div>
            """, unsafe_allow_html=True)

            # Dropdown Label nổi bật
            st.markdown(f"<div style='font-weight: bold; color: #8B0000; margin-bottom: 5px; font-size: 1.1rem;'>👇 {get_ui('select_doc_label')}</div>", unsafe_allow_html=True)
            
            doc_keys = list(config.DOCUMENTS.keys())
            doc_keys.insert(0, None)

            def format_option(key):
                if key is None:
                    name_zh = config.UI_LABELS['select_prompt']['zh']
                    name_local = config.UI_LABELS['select_prompt'][lang_code]
                    return f"📂 {name_zh} | {name_local}"
                
                name_zh = config.DOCUMENTS[key]['menu_names']['zh']
                name_local = config.DOCUMENTS[key]['menu_names'][lang_code]
                if lang_code == 'zh': return name_zh
                else: return f"{name_zh} - {name_local}"

            selected_doc_key = st.selectbox(
                label="Select Document",
                options=doc_keys,
                format_func=format_option,
                label_visibility="collapsed"
            )

            if selected_doc_key is not None:
                current_doc = config.DOCUMENTS[selected_doc_key]

                st.markdown(f"""
                <div style="background-color: #fffdf0; border-top: 3px solid #8B0000; border-bottom: 3px solid #8B0000; padding: 20px; margin-top: 20px; text-align: center;">
                    <h3 style="margin:0; color: #b22222; text-shadow: 1px 1px 0 #fff;">{current_doc['header_title']['zh']}</h3>
                    {'<h5 style="margin:8px 0 0 0; color: #555;">' + current_doc['header_title'][lang_code] + '</h5>' if lang_code != 'zh' else ''}
                </div>
                """, unsafe_allow_html=True)
                
                with st.container(border=True):
                    st.caption(f"👤 {get_ui('student_info')}")
                    c1, c2 = st.columns(2)
                    c1.markdown(f"**Name:** {st_data['中文姓名']}")
                    c1.markdown(f"**ID:** {st_data['學號']}")
                    c2.markdown(f"**Dept:** {st_data['就讀學系']}")
                    c2.markdown(f"**Nat:** {nationality_zh}")

                st.write("")
                st.subheader(f"📜 {get_ui('content_title')}")
                content_style = "text-align: justify; font-size: 1.15rem; padding: 25px; border: 1px solid #d4af37; border-radius: 5px; margin-bottom: 10px; background-color: #fff; font-family: 'Times New Roman', serif; line-height: 1.6;"
                st.markdown(f"<div style='{content_style}'>{current_doc['body_intro']['zh']}</div>", unsafe_allow_html=True)
                if lang_code != 'zh':
                    st.markdown(f"<div style='{content_style} font-style: italic; opacity: 0.95; margin-top: -5px;'>{current_doc['body_intro'][lang_code]}</div>", unsafe_allow_html=True)

                st.divider()
                st.subheader(f"✅ {get_ui('checklist_title')}")
                st.info(get_ui('checklist_guide'))
                
                checked_results = {}
                for clause in current_doc['checkboxes']:
                    label_zh = f"**{clause['zh']}**"
                    label_fn = f"\n\n_{clause[lang_code]}_" if lang_code != 'zh' else ""
                    val = st.checkbox(label_zh + label_fn, key=clause['id'])
                    checked_results[clause['id']] = val
                    st.write("") 

                st.divider()
                st.subheader(f"✍️ {get_ui('sign_title')}")
                st.write(get_ui('sign_guide'))
                
                mobile_hint = f"{config.UI_LABELS['mobile_hint']['zh']}<br>{config.UI_LABELS['mobile_hint'][lang_code]}"
                st.markdown(f"<div style='color: #b22222; font-size: 1rem; font-weight: bold; background: #fff5f5; padding: 10px; border: 1px dashed #b22222; text-align: center; margin-bottom: 10px;'>⚠️ {mobile_hint}</div>", unsafe_allow_html=True)

                # --- CANVAS KÝ TÊN (CĂN GIỮA & RESPONSIVE) ---
                st.markdown('<div class="signature-container">', unsafe_allow_html=True)
                canvas_result = st_canvas(
                    stroke_width=3, 
                    stroke_color="#000000", 
                    background_color="#ffffff", 
                    height=250, 
                    width=600, 
                    drawing_mode="freedraw", 
                    key="sig"
                )
                st.markdown('</div>', unsafe_allow_html=True)
                
                # --- NÚT GỬI CĂN GIỮA ---
                b1, b2, b3 = st.columns([1, 2, 1]) 
                with b2:
                    submit_btn = st.button(f"🚀 {get_ui('btn_submit')}", type="primary")

                if submit_btn:
                    missing_checks = [k for k, v in checked_results.items() if not v]
                    
                    if missing_checks:
                        st.markdown(f"""<div class="notify-error">⚠️ {get_ui('error_checklist')}</div>""", unsafe_allow_html=True)
                        time.sleep(2); st.rerun()
                    elif canvas_result.json_data is None or len(canvas_result.json_data["objects"]) == 0:
                        st.markdown(f"""<div class="notify-error">⚠️ {get_ui('error_sign')}</div>""", unsafe_allow_html=True)
                        time.sleep(2); st.rerun()
                    else:
                        with st.spinner('Processing... / 正在處理...'):
                            try:
                                folder_name = "PDF_DA_KY"
                                if not os.path.exists(folder_name): os.makedirs(folder_name)

                                img_data = canvas_result.image_data
                                img = PILImage.fromarray(img_data.astype("uint8"), "RGBA")
                                sig_filename = f"sig_{student_id}.png"
                                img.save(sig_filename)

                                safe_name = str(st_data['中文姓名']).replace(" ", "_")
                                pdf_filename = f"{student_id}_{safe_name}_{selected_doc_key}.pdf"
                                full_pdf_path = os.path.join(folder_name, pdf_filename)
                                
                                create_pdf(full_pdf_path, st_data, checked_results, sig_filename, lang_code, current_doc)

                                if os.path.exists(sig_filename): os.remove(sig_filename)
                                
                                if 'Gmail' in st_data and pd.notna(st_data['Gmail']):
                                    send_email_with_pdf(st_data['Gmail'], full_pdf_path, st_data['中文姓名'], student_id, lang_code, is_admin=False)
                                
                                st.balloons()
                                
                                success_msg = get_ui('success_msg')
                                placeholder = st.empty()
                                gif_url = "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExdXBqeDBzNjRwNmJydHF2dTluam9qd244bW5mcnlnM3RkNzY5cHJ4YSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3UkqVq3F50bVCi9URl/giphy.gif"
                                
                                for i in range(10, -1, -1):
                                    with placeholder.container():
                                        st.markdown(f"""
                                        <div class="success-overlay"></div>
                                        <div class="success-container">
                                            <img src="{gif_url}" width="150" style="border-radius:15px; margin-bottom:10px; display:block; margin-left:auto; margin-right:auto;">
                                            <div class="success-text">{success_msg}</div>
                                            <div class="timer-text">⏳ Closing in {i}s...</div>
                                        </div>
                                        """, unsafe_allow_html=True)
                                        if i == 10: 
                                            with open(full_pdf_path, "rb") as f:
                                                st.download_button(label=f"📥 {get_ui('download_btn')}", data=f, file_name=pdf_filename, mime="application/pdf")
                                    time.sleep(1)
                                st.rerun()
                                
                            except Exception as e:
                                st.error(f"⚠️ Server Error – Contact Admin: {e}")
            else:
                st.write("") 

if __name__ == "__main__":
    main()
