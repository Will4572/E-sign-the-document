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

# ============================================================
# 1. CẤU HÌNH TRANG (FIX MOBILE)
# ============================================================
st.set_page_config(
    page_title="Digital Signature System",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# 2. JAVASCRIPT FIX DROPDOWN
# ============================================================
js_hack = """
<script>
function fixSelectBox() {
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
setInterval(fixSelectBox, 50);
</script>
"""
components.html(js_hack, height=0, width=0)

# ============================================================
# 3. CSS GIAO DIỆN + FIX MOBILE TRIỆT ĐỂ
# ============================================================
custom_style = """
<style>

/* ===== ẨN TOÀN BỘ AVATAR / LOGO / MENU ===== */
header[data-testid="stHeader"],
div[data-testid="stToolbar"],
div[data-testid="stDecoration"],
div[data-testid="stStatusWidget"],
div[data-testid="collapsedControl"],
button[kind="header"],
footer,
a[href*="streamlit.io"] {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
}

/* ===== FULL MÀN HÌNH ===== */
html, body, [data-testid="stAppViewContainer"] {
    width: 100vw !important;
    overflow-x: hidden !important;
}

/* ===== KHUNG CHÍNH ===== */
div.block-container {
    max-width: 100% !important;
    width: 100% !important;
    padding: 1rem !important;
    border: 5px double #8B0000;
    border-radius: 15px;
    background-color: #ffffff;
    box-shadow: 0 20px 50px rgba(61, 12, 2, 0.3);
}

/* ===== NỀN ===== */
.stApp {
    background-color: #fcf6e3;
    background-image: url("https://www.transparenttextures.com/patterns/rice-paper-3.png");
}

/* ===== CHỮ ===== */
h1, h2, h3, h4 {
    font-family: 'Times New Roman', serif !important;
    color: #8B0000 !important;
}
p, span, label, div {
    font-family: 'Times New Roman', serif;
    font-size: 1.1rem;
}

/* ===== INPUT ===== */
.stTextInput input {
    text-align: center;
    font-size: 28px;
    font-weight: 900;
    color: #b22222;
    border: 3px solid #D4AF37;
    background-color: #fffdf0;
    height: 60px;
}

/* ===== BUTTON ===== */
.stButton>button {
    width: 100%;
    height: 4em;
    font-size: 22px;
    font-weight: bold;
    background: linear-gradient(180deg, #b22222, #800000);
    color: #FFD700;
    border: 2px solid #D4AF37;
}

/* ===== CANVAS ===== */
div[data-testid="stCanvas"] canvas {
    max-width: 100% !important;
    height: auto !important;
}

/* ===== MOBILE ===== */
@media (max-width: 768px) {
    h1 { font-size: 1.8rem !important; }
    h4 { font-size: 1rem !important; }
    .stButton>button { font-size: 18px !important; }
    .stTextInput input { font-size: 22px !important; }
}

</style>
"""
st.markdown(custom_style, unsafe_allow_html=True)

# ============================================================
# 4. GLOBAL ERROR
# ============================================================
def global_exception_handler(exctype, value, traceback):
    st.markdown(f"<div style='color:red;font-weight:bold'>⚠️ {value}</div>", unsafe_allow_html=True)

sys.excepthook = global_exception_handler

# ============================================================
# 5. MAIN
# ============================================================
def main():

    EXCEL_FILE = "學生名單表格.xlsx"

    @st.cache_data
    def load_data():
        if not os.path.exists(EXCEL_FILE):
            return None
        df = pd.read_excel(EXCEL_FILE, dtype={'學號': str})
        df.columns = df.columns.str.replace(' ', '')
        return df

    df = load_data()
    if df is None:
        st.error("⚠️ Không tìm thấy file Excel")
        return

    st.markdown("""
    <h1 style="text-align:center">📜 德育護理健康學院</h1>
    <h4 style="text-align:center">線上簽署系統 | DIGITAL SIGNATURE SYSTEM</h4>
    """, unsafe_allow_html=True)

    student_id = st.text_input("🔐 請輸入學號", placeholder="Student ID")

    if not student_id:
        st.stop()

    row = df[df['學號'] == student_id.strip()]
    if row.empty:
        st.error("❌ Student ID Not Found")
        return

    st_data = row.iloc[0]

    st.success(f"👋 歡迎 {st_data['中文姓名']}")

    st.subheader("✍️ 簽名")
    st.info("👉 Dùng tay ký trực tiếp trên màn hình")

    canvas_result = st_canvas(
        stroke_width=3,
        stroke_color="#000000",
        background_color="#ffffff",
        height=250,
        width=600,
        drawing_mode="freedraw",
        key="sig"
    )

    if st.button("🚀 XÁC NHẬN & GỬI"):
        if canvas_result.json_data is None:
            st.error("⚠️ Chưa ký tên")
            return

        st.success("✅ Hoàn tất")

if __name__ == "__main__":
    main()
