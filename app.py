# FILE: app.py
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
st.set_page_config(page_title="Digital Signature System", page_icon="🎓", layout="centered")

# --- JAVASCRIPT HACK (QUAN TRỌNG NHẤT) ---
# Đoạn mã này sẽ can thiệp trực tiếp vào DOM để xóa bỏ dấu ...
# --- JAVASCRIPT HACK (FIX GIAO DIỆN SÁNG/TỐI) ---
# Đoạn mã này ép buộc hộp chọn luôn có Nền Trắng - Chữ Đen để dễ đọc
js_hack = """
<script>
function fixSelectBox() {
    // 1. CHỈNH SỬA CHỮ (Luôn là màu đen đậm)
    const elements = window.parent.document.querySelectorAll('div[data-baseweb="select"] span');
    elements.forEach(function(el) {
        el.style.whiteSpace = "normal"; 
        el.style.overflow = "visible";  
        el.style.textOverflow = "clip"; 
        el.style.height = "auto";
        el.style.display = "block";
        el.style.lineHeight = "1.5";
        el.style.fontWeight = "bold";
        el.style.fontSize = "16px";
        el.style.color = "#333333"; // Màu xám đen (dễ đọc hơn đen tuyền)
    });
    
    // 2. CHỈNH SỬA HỘP BAO NGOÀI (Luôn là nền trắng, viền xanh)
    const boxes = window.parent.document.querySelectorAll('div[data-baseweb="select"] > div');
    boxes.forEach(function(box) {
        box.style.height = "auto";
        box.style.minHeight = "60px";
        box.style.alignItems = "center";
        box.style.backgroundColor = "#ffffff"; // Nền luôn trắng
        box.style.border = "2px solid #003366"; // Viền xanh đậm của trường
        box.style.borderRadius = "8px"; // Bo tròn góc
    });
    
    // 3. XỬ LÝ MÀU ICON MŨI TÊN (Chuyển sang đen)
    const svgs = window.parent.document.querySelectorAll('div[data-baseweb="select"] svg');
    svgs.forEach(function(svg) {
        svg.style.color = "#003366"; 
    });
}
// Chạy liên tục để đảm bảo luôn fix được khi reload
setInterval(fixSelectBox, 500);
</script>
"""
components.html(js_hack, height=0, width=0)

# --- CSS TÙY CHỈNH ---
custom_style = """
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
    .stTextInput>div>div>input { text-align: center; font-size: 20px; font-weight: bold; border: 2px solid #003366; border-radius: 10px; }
    
    .stButton>button {width: 100%; border-radius: 8px; height: 3.5em; font-weight: bold; font-size: 18px; margin-top: 20px; background-color: #003366; color: white;}
    .stButton>button:hover {background-color: #002244; color: #fff;}

    /* Căn giữa dòng nhắc nhập ID */
    .id-prompt {
        text-align: center; font-weight: bold; font-size: 1.2rem; 
        color: #004085; background-color: #cce5ff; 
        padding: 15px; border-radius: 10px; border: 2px solid #b8daff; margin-bottom: 20px;
    }

    /* Welcome Box */
    .welcome-box {
        text-align: center; padding: 15px; border-radius: 10px; 
        background-color: #d4edda; border: 2px solid #c3e6cb;
        color: #155724; margin-bottom: 20px; font-size: 1.1rem;
        font-weight: bold;
    }

    /* Popup Thành công */
    .success-overlay {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.7); z-index: 99998;
    }
    
    .success-container {
        position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
        z-index: 99999; padding: 20px; border-radius: 15px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.8); text-align: center;
        width: 320px; background-color: #ffffff !important; border: 5px solid #28a745;
        animation: popUp 0.4s ease-out;
    }
    
    .success-text { font-size: 1.2rem; font-weight: 900; color: #28a745 !important; margin: 10px 0; }
    .timer-text { font-size: 1rem; color: #333 !important; margin-top: 5px; font-weight: bold; }

    @keyframes popUp { 
        0% { transform: translate(-50%, -50%) scale(0.5); opacity: 0; } 
        100% { transform: translate(-50%, -50%) scale(1); opacity: 1; } 
    }
    
    .notify-error { 
        position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
        z-index: 99999; padding: 25px; border-radius: 15px;
        background-color: #f8d7da; color: #721c24; border: 3px solid #f5c6cb; 
        text-align: center; font-size: 1.2rem; font-weight: bold;
    }
    </style>
"""
st.markdown(custom_style, unsafe_allow_html=True)

def global_exception_handler(exctype, value, traceback):
    st.markdown(f"""<div class="notify-error">⚠️ Server Error: {value}</div>""", unsafe_allow_html=True)
sys.excepthook = global_exception_handler

def main():
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

    st.markdown("<h2 style='text-align: center; color: #003366;'>德育護理健康學院</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #555;'>線上簽署系統 / Digital Signature System</h4>", unsafe_allow_html=True)

    if not student_id:
        st.write("---")
        st.markdown("""
            <div class="id-prompt">
                👋 請輸入學號以開始<br>Enter Student ID to start
            </div>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            student_id_input = st.text_input("", max_chars=15, label_visibility="collapsed", placeholder="Ex: 1151234567")
        if student_id_input: student_id = student_id_input
        else: st.stop() 

    if student_id and df is not None:
        clean_search_id = str(student_id).strip()
        student_row = df[df['學號'] == clean_search_id]
        
        if student_row.empty:
            st.error(f"❌ Sdutent ID Not Found: {clean_search_id}")
        else:
            st_data = student_row.iloc[0]
            nat_col = '國籍' if '國籍' in st_data else '籍國'
            nationality_zh = st_data.get(nat_col, '台灣')
            lang_code = config.NATIONALITY_MAP.get(nationality_zh, 'zh')
            
            def get_ui(key): return f"{config.UI_LABELS[key]['zh']} / {config.UI_LABELS[key][lang_code]}"

            st.divider()
            
            wel_zh = config.UI_LABELS['welcome']['zh']
            wel_local = config.UI_LABELS['welcome'][lang_code]
            if lang_code == 'zh':
                welcome_text = f"👋 {wel_zh} <b>{st_data['中文姓名']}</b>"
            else:
                welcome_text = f"👋 {wel_zh} {wel_local} <b>{st_data['中文姓名']}</b>"
            
            st.markdown(f"""<div class="welcome-box">{welcome_text}</div>""", unsafe_allow_html=True)

            st.info(f"👇 {get_ui('select_doc_label')}")
            
            doc_keys = list(config.DOCUMENTS.keys())
            doc_keys.insert(0, None)

            def format_option(key):
                if key is None:
                    name_zh = config.UI_LABELS['select_prompt']['zh']
                    name_local = config.UI_LABELS['select_prompt'][lang_code]
                    return f"--- 📂 {name_zh}\n{name_local} ---"
                
                name_zh = config.DOCUMENTS[key]['menu_names']['zh']
                name_local = config.DOCUMENTS[key]['menu_names'][lang_code]
                if lang_code == 'zh': return name_zh
                else: 
                    # Dùng ký tự đặc biệt để ép xuống dòng trong mọi trường hợp
                    return f"{name_zh}\n\n{name_local}"

            selected_doc_key = st.selectbox(
                label="Select Document",
                options=doc_keys,
                format_func=format_option,
                label_visibility="collapsed"
            )

            if selected_doc_key is not None:
                current_doc = config.DOCUMENTS[selected_doc_key]

                st.markdown(f"<h4 style='text-align: center; margin-top: 20px; color: #b30000;'>{current_doc['header_title']['zh']}</h4>", unsafe_allow_html=True)
                if lang_code != 'zh':
                     st.markdown(f"<h6 style='text-align: center; color: #555;'>{current_doc['header_title'][lang_code]}</h6>", unsafe_allow_html=True)
                
                with st.container(border=True):
                    st.caption(f"👤 {get_ui('student_info')}")
                    c1, c2 = st.columns(2)
                    c1.markdown(f"**Name:** {st_data['中文姓名']}")
                    c1.markdown(f"**ID:** {st_data['學號']}")
                    c2.markdown(f"**Dept:** {st_data['就讀學系']}")
                    c2.markdown(f"**Nat:** {nationality_zh}")

                st.write("")
                st.subheader(f"📜 {get_ui('content_title')}")
                content_style = "text-align: justify; font-size: 1.05rem; padding: 15px; border: 1px solid #ddd; border-radius: 8px; margin-bottom: 10px;"
                st.markdown(f"<div style='{content_style}'>{current_doc['body_intro']['zh']}</div>", unsafe_allow_html=True)
                if lang_code != 'zh':
                    st.markdown(f"<div style='{content_style} font-style: italic; opacity: 0.9;'>{current_doc['body_intro'][lang_code]}</div>", unsafe_allow_html=True)

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
                st.markdown(f"<p style='color: #d9534f; font-size: 0.9rem; font-style: italic;'>{mobile_hint}</p>", unsafe_allow_html=True)

                canvas_result = st_canvas(stroke_width=2, stroke_color="#000000", background_color="#ffffff", height=220, width=450, drawing_mode="freedraw", key="sig")
                
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
                                pdf_filename = f"{safe_name}_{student_id}_{selected_doc_key}.pdf"
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

