# FILE: config.py

# --- 1. CẤU HÌNH QUỐC TỊCH ---
NATIONALITY_MAP = {
    "印尼": "id", "印度尼西亞": "id", "Indonesia": "id",
    "越南": "vi", "Vietnam": "vi",
    "泰國": "th", "Thailand": "th",
    "台灣": "zh", "Taiwan": "zh"
}

# --- 2. TỪ ĐIỂN GIAO DIỆN (UI) ---
UI_LABELS = {
    "welcome": {"zh": "歡迎", "vi": "Xin chào", "th": "ยินดีต้อนรับ", "id": "Selamat Datang"},
    "student_info": {"zh": "學生資訊", "vi": "Thông tin sinh viên", "th": "ข้อมูลนักศึกษา", "id": "Informasi Mahasiswa"},
    "select_doc_label": {"zh": "請選擇要簽署的文件", "vi": "Vui lòng chọn loại văn bản cần ký", "th": "โปรดเลือกเอกสารที่จะลงนาม", "id": "Pilih dokumen untuk ditandatangani"},
    "select_prompt": {"zh": "請選擇文件...", "vi": "Vui lòng chọn văn bản...", "th": "โปรดเลือกเอกสาร...", "id": "Silakan pilih dokumen..."},
    "select_label": {"zh": "選擇簽署文件", "vi": "Chọn loại giấy tờ", "th": "เลือกเอกสาร", "id": "Pilih dokumen"},
    "content_title": {"zh": "切結書內容", "vi": "Nội dung cam kết", "th": "เนื้อหาหนังสือสัญญา", "id": "Isi Surat Pernyataan"},
    "checklist_title": {"zh": "確認條款", "vi": "Xác nhận điều khoản", "th": "ยืนยันข้อกำหนด", "id": "Konfirmasi Ketentuan"},
    "checklist_guide": {
        "zh": "請勾選以下所有項目以確認", 
        "vi": "Vui lòng đánh dấu vào tất cả các ô dưới đây để xác nhận", 
        "th": "กรุณาทำเครื่องหมายที่ช่องด้านล่างทั้งหมดเพื่อยืนยัน", 
        "id": "Silakan centang semua kotak di bawah ini untuk konfirmasi"
    },
    "sign_title": {"zh": "學生簽名", "vi": "Chữ ký sinh viên", "th": "ลายเซ็นนักศึกษา", "id": "Tanda Tangan Mahasiswa"},
    "sign_guide": {
        "zh": "請在下方框內簽名", 
        "vi": "Vui lòng ký tên vào khung bên dưới", 
        "th": "กรุณาลงนามในช่องด้านล่าง", 
        "id": "Silakan tanda tangan di kotak di bawah ini"
    },
    "mobile_hint": {
        "zh": "💡 若使用手機，建議將螢幕「橫向旋轉」以方便簽名。",
        "vi": "💡 Nếu dùng điện thoại, vui lòng xoay ngang màn hình để ký dễ hơn.",
        "th": "💡 หากใช้โทรศัพท์มือถือ โปรดหมุนหน้าจอแนวนอนเพื่อให้ลงนามได้ง่ายขึ้น",
        "id": "💡 Jika menggunakan ponsel, harap putar layar secara horizontal agar lebih mudah menandatangani."
    },
    "btn_clear": {"zh": "清除重簽", "vi": "Xóa & Ký lại", "th": "ล้างและเซ็นใหม่", "id": "Hapus & Tanda Tangan Ulang"},
    "btn_submit": {"zh": "確認並提交", "vi": "Xác nhận & Gửi đi", "th": "ยืนยันและส่ง", "id": "Konfirmasi & Kirim"},
    "error_checklist": {"zh": "您尚未勾選所有條款！", "vi": "Bạn chưa đồng ý tất cả điều khoản!", "th": "คุณยังไม่ได้เลือกข้อกำหนดทั้งหมด!", "id": "Anda belum menyetujui semua ketentuan!"},
    "error_sign": {"zh": "您尚未簽名！", "vi": "Bạn chưa ký tên!", "th": "คุณยังไม่ได้ลงนาม!", "id": "Anda belum tanda tangan!"},
    "success_msg": {
        "zh": "提交成功！文件已寄至您的信箱。", 
        "vi": "Nộp thành công! Văn bản đã được gửi đến email của bạn.", 
        "th": "ส่งสำเร็จ! เอกสารถูกส่งไปยังอีเมลของคุณแล้ว", 
        "id": "Berhasil dikirim! Dokumen telah dikirim ke email Anda."
    },
    "download_btn": {"zh": "下載 PDF", "vi": "Tải về PDF", "th": "ดาวน์โหลด PDF", "id": "Unduh PDF"},
    "email_note": {
        "zh": "請查收附件中的 PDF 文件。",
        "vi": "Vui lòng kiểm tra file PDF đính kèm.",
        "th": "กรุณาตรวจสอบไฟล์ PDF ที่แนบมา",
        "id": "Silakan periksa file PDF yang dilampirkan."
    }
}

# --- 3. FOOTER TÁC GIẢ ---
AUTHOR_FOOTER = """
<div style="text-align: center; font-size: 10px; color: #aaa; margin-top: 20px; border-top: 1px dashed #eee; padding-top: 5px;">
    System developed by: Trần Văn Khánh
</div>
"""

# --- 4. EMAIL TEMPLATES ---
EMAIL_TEMPLATES = {
    "zh": { "subject": "簽署完成通知 - 德育護理健康學院", "body": "親愛的 {student_name}：系統已收到您的簽名。" },
    "vi": { "subject": "Xác nhận: Bạn đã ký cam kết thành công", "body": "Chào {student_name}, Hệ thống đã nhận được chữ ký của bạn." },
    "th": { "subject": "ยืนยันการลงนามเอกสาร", "body": "เรียน {student_name}, ทางสถาบันได้รับเอกสารแล้ว" },
    "id": { "subject": "Konfirmasi Penandatanganan", "body": "Halo {student_name}, Sistem telah menerima tanda tangan Anda." }
}

# --- 5. DỮ LIỆU CÁC VĂN BẢN (ĐÃ XÓA TIẾNG ANH Ở MENU) ---
COMMON_FIELDS = {
    "name_cn": {"zh": "學生中文姓名", "vi": "Tên tiếng Hoa", "id": "Nama Mandarin", "th": "ชื่อจีน"},
    "name_en": {"zh": "學生英文姓名", "vi": "Tên tiếng Anh", "id": "Nama Inggris",  "th": "ชื่ออังกฤษ"},
    "std_id":  {"zh": "學生學號",     "vi": "Mã sinh viên",  "id": "NIM",           "th": "รหัสนักศึกษา"},
    "dept":    {"zh": "就讀學系",     "vi": "Khoa",          "id": "Jurusan",       "th": "คณะ"}
}

DOCUMENTS = {
    # === DOC 1 ===
    "admission": {
        "menu_names": {
            "zh": "1. 就讀承諾書",
            "vi": "1. Cam kết chịu trách nhiệm (Nhập học)",
            "th": "1. หนังสือสัญญาการเข้าศึกษา",
            "id": "1. Surat Pernyataan Studi"
        },
        "header_title": {
            "zh": "就讀國際專修部與產學專班切結書",
            "vi": "BẢN CAM KẾT CHỊU TRÁCH NHIỆM VỀ VIỆC NHẬP HỌC",
            "th": "หนังสือสัญญาการเข้าศึกษาในหลักสูตรเตรียมความพร้อมนานาชาติและโครงการเรียนควบคู่การทำงาน",
            "id": "SURAT PERNYATAAN MENGIKUTI PROGRAM PERSIAPAN INTERNASIONAL"
        },
        "body_intro": {
            "zh": "本人為德育護理健康學院之外國學生。經詳閱並充分理解學校公告之《國際專修部學生修業辦法》及《國際學生輔導辦法》，本人承諾於就學期間嚴格遵守相關規定。若有違反，本人願負全部責任，並接受學校依規定之處置（包括勒令休學、退學、取消獎助學金、通報移民署及教育部等），絕無異議：",
            "vi": "Tôi là sinh viên nước ngoài của Đại Học Y Tế và Sức Khỏe Đức Dục. Sau khi đã đọc kỹ và hoàn toàn hiểu rõ các thông báo của nhà trường về “Quy định học tập của hệ dự bị Quốc tế” và “Quy định hỗ trợ sinh viên quốc tế”, tôi cam kết trong thời gian học tập sẽ nghiêm túc tuân thủ các quy định liên quan. Nếu có vi phạm, tôi xin chịu hoàn toàn trách nhiệm và chấp nhận mọi hình thức xử lý theo quy định của nhà trường (bao gồm buộc tạm ngừng học, buộc thôi học, hủy bỏ học bổng, thông báo cho Cục Di trú, Bộ Lao Động và Bộ Giáo dục, v.v.), tuyệt đối không có ý kiến phản đối:",
            "id": "Saya adalah mahasiswa asing dari Universitas Kedokteran dan Kesehatan De Yu. Setelah membaca dengan seksama dan sepenuhnya memahami pengumuman universitas mengenai“Peraturan Studi Program Persiapan Internasional” dan“Peraturan Dukungan Mahasiswa Internasional”,saya berjanji selama masa studi akan mematuhi semua ketentuan yang berlaku secara ketat. Jika terjadi pelanggaran, saya bersedia menanggung seluruh tanggung jawab dan menerima tindakan sesuai peraturan universitas (termasuk diberhentikan sementara, dikeluarkan, pembatalan beasiswa, serta dilaporkan kepada Imigrasi, Kementerian Tenaga Kerja, dan Kementerian Pendidikan), tanpa keberatan apa pun:",
            "th": "ข้าพเจ้าเป็นนักศึกษาต่างชาติของมหาวิทยาลัยการแพทย์และสุขภาพเต๋อหยู่หลังจากได้อ่านและเข้าใจประกาศของมหาวิทยาลัยเกี่ยวกับ“ข้อบังคับการศึกษาในหลักสูตรเตรียมความพร้อมนานาชาติ”และ“ข้อบังคับการสนับสนุนนักศึกษาต่างชาติ”อย่างละเอียดแล้ว ข้าพเจ้าขอสัญญาว่าในระหว่างการศึกษาจะปฏิบัติตามข้อบังคับที่เกี่ยวข้องอย่างเคร่งครัดหากมีการฝ่าฝืนข้าพเจ้ายินดีรับผิดชอบทั้งหมดและยอมรับการดำเนินการตามข้อบังคับของมหาวิทยาลัย(รวมถึงการพักการเรียนการให้ออกจากมหาวิทยาลัยการยกเลิกทุนการศึกษาการแจ้งต่อสำนักงานตรวจคนเข้าเมืองกระทรวงแรงงานและกระทรวงศึกษาธิการเป็นต้น)โดยไม่มีข้อโต้แย้งใด ๆ:"
        },
        "checkboxes": [
            { "id": "c1", "zh": "1.修業年限與成績：本人了解華語先修期間以一年為限。每學期學業成績須達60分以上，任一學期未達60分者由學校逕予退學。先修期間課程不得抵免大學應修讀學分。", "vi": "1. Thời hạn học tập và Thành tích: Tôi hiểu rằng khóa dự bị tiếng Hoa giới hạn trong 1 năm. Điểm học tập mỗi kỳ phải đạt từ 60 trở lên, nếu bất kỳ kỳ nào dưới 60 điểm sẽ bị nhà trường buộc thôi học. Tín chỉ trong thời gian dự bị không được dùng để miễn giảm tín chỉ đại học.", "id": "1. Durasi Studi dan Nilai: Saya mengerti bahwa masa pra-studi bahasa Mandarin dibatasi maksimal 1 tahun. Nilai akademik setiap semester harus mencapai 60 poin atau lebih. Jika ada semester dengan nilai di bawah 60, sekolah akan langsung memberhentikan (DO). Kredit mata kuliah selama masa pra-studi tidak dapat ditransfer ke program sarjana.", "th": "1. ระยะเวลาการศึกษาและผลการเรียน: ข้าพเจ้าเข้าใจว่าหลักสูตรเตรียมความพร้อมภาษาจีนมีระยะเวลาจำกัด 1 ปี ผลการเรียนในแต่ละภาคการศึกษาต้องได้ 60 คะแนนขึ้นไป หากภาคการศึกษาใดได้ต่ำกว่า 60 คะแนน จะถูกทางโรงเรียนให้ออก หน่วยกิตในช่วงเตรียมความพร้อมไม่สามารถเทียบโอนหน่วยกิตระดับมหาวิทยาลัยได้" },
            { "id": "c2", "zh": "2.出缺席與獎懲：若曠課時數達該學期授課總時數三分之一者，應予勒令休學。若無故曠課達30節，學校將取消本人次學期獎助學金資格。本人承諾考試絕不作弊，違者除該科以零分計算外，並依校規處分。", "vi": "2. Điểm danh và Khen thưởng/Kỷ luật: Nếu tổng số giờ vắng mặt đạt 1/3 tổng số giờ học của kỳ đó, sẽ bị buộc đình chỉ học. Nếu vắng không phép đạt 30 tiết, nhà trường sẽ hủy tư cách nhận học bổng của kỳ tiếp theo. Tôi cam kết tuyệt đối không gian lận khi thi, nếu vi phạm sẽ bị 0 điểm môn đó và chịu kỷ luật theo quy định.", "id": "2. Kehadiran dan Sanksi: Jika jumlah jam bolos mencapai sepertiga dari total jam pengajaran semester tersebut, maka akan diskors. Jika bolos tanpa alasan mencapai 30 jam pelajaran, sekolah akan membatalkan kualifikasi beasiswa semester berikutnya. Saya berjanji tidak akan menyontek dalam ujian; jika melanggar, nilai mata kuliah tersebut nol dan akan dihukum sesuai peraturan sekolah.", "th": "2. การเข้าเรียนและบทลงโทษ: หากชั่วโมงการขาดเรียนถึง 1 ใน 3 ของชั่วโมงเรียนทั้งหมดในภาคการศึกษานั้น จะถูกสั่งพักการเรียน หากขาดเรียนโดยไม่มีเหตุผลครบ 30 คาบ ทางโรงเรียนจะยกเลิกสิทธิ์ทุนการศึกษาในภาคการศึกษาถัดไป ข้าพเจ้าขอสัญญาว่าจะไม่ทุจริตในการสอบ หากฝ่าฝืนวิชานั้นจะถูกปรับเป็น 0 คะแนนและถูกลงโทษตามระเบียบโรงเรียน" },
            { "id": "c3", "zh": "3.華語文能力測驗標準：於華語先修期間或期滿後，本人華語能力應達TOCFL A2標準；未達標準者由學校逕予退學。修讀四技學士班第二學年課程前，本人華語能力應達TOCFL B1（含）以上標準。對於產學專班：學生在入大學二年級之前必須取得華語 A2級證書；並且承諾在大學二年級時必須取得 B1級以上證書。", "vi": "3. Tiêu chuẩn Năng lực Hoa ngữ: Trong hoặc sau khi kết thúc khóa dự bị, năng lực Hoa ngữ của tôi phải đạt chuẩn TOCFL A2; nếu không đạt sẽ bị buộc thôi học. Trước khi học chương trình năm 2 Đại học, năng lực Hoa ngữ phải đạt chuẩn TOCFL B1 trở lên. Đối với lớp chuyên ban (hệ vừa học vừa làm): Phải có chứng chỉ A2 trước khi vào năm 2; và cam kết phải lấy được chứng chỉ B1 trở lên trong thời gian học năm 2.", "id": "3. Standar Tes Kemampuan Bahasa Mandarin: Selama atau setelah masa pra-studi Mandarin, kemampuan Mandarin saya harus mencapai standar TOCFL A2; jika tidak, akan diberhentikan oleh sekolah. Sebelum mengambil mata kuliah tahun kedua program Sarjana 4 tahun, kemampuan Mandarin saya harus mencapai standar TOCFL B1 (atau lebih). Untuk Kelas Industri-Akademisi: Siswa wajib memperoleh sertifikat A2 sebelum masuk tahun kedua universitas; dan berjanji untuk memperoleh sertifikat B1 atau lebih tinggi selama tahun kedua universitas.", "th": "3. เกณฑ์การทดสอบวัดระดับความรู้ภาษาจีน (TOCFL): ระหว่างหรือหลังจบหลักสูตรเตรียมความพร้อม ความรู้ภาษาจีนของข้าพเจ้าต้องถึงเกณฑ์ TOCFL A2 หากไม่ถึงเกณฑ์จะถูกทางโรงเรียนให้ออก ก่อนเข้าเรียนชั้นปีที่ 2 ของระดับปริญญาตรี ความรู้ภาษาจีนต้องถึงเกณฑ์ TOCFL B1 ขึ้นไป สำหรับหลักสูตรความร่วมมืออุตสาหกรรมและวิชาการ: นักศึกษาต้องได้รับใบรับรองระดับ A2 ก่อนขึ้นปี 2 และสัญญาว่าจะต้องสอบให้ได้ใบรับรองระดับ B1 ขึ้นไปภายในปี 2" },
            { "id": "c4", "zh": "4.升讀四技課程：華語先修課程且通過華測A2者應就讀所屬學系四技課程。若不遵守，學校將逕予退學並通報移民署及相關單位。華語先修期間不得辦理轉系。", "vi": "4. Học lên hệ Đại học 4 năm: Người hoàn thành khóa dự bị và đạt TOCFL A2 phải theo học đúng hệ Đại học của khoa đã đăng ký. Nếu không tuân thủ, nhà trường sẽ buộc thôi học và thông báo cho Cục Di dân cùng các đơn vị liên quan. Không được phép chuyển khoa trong thời gian học dự bị tiếng Hoa.", "id": "4. Melanjutkan ke Program Sarjana 4 Tahun: Mereka yang menyelesaikan kursus pra-studi Mandarin dan lulus TOCFL A2 wajib masuk ke program sarjana departemen terkait. Jika tidak patuh, sekolah akan memberhentikan siswa dan melapor ke Imigrasi serta unit terkait. Dilarang pindah jurusan selama masa pra-studi Mandarin.", "th": "4. การศึกษาต่อระดับปริญญาตรี 4 ปี: ผู้ที่เรียนหลักสูตรเตรียมความพร้อมและสอบผ่าน TOCFL A2 ต้องเข้าศึกษาต่อในสาขาวิชาที่กำหนด หากไม่ปฏิบัติตาม โรงเรียนจะให้ออกและแจ้งสำนักงานตรวจคนเข้าเมืองและหน่วยงานที่เกี่ยวข้อง ห้ามทำเรื่องย้ายสาขาวิชาระหว่างเรียนหลักสูตรเตรียมความพร้อม" },
            { "id": "c5", "zh": "5.工作許可規範：本人承諾遵守每星期工作時數為上限二十小時之規定（寒暑假除外）。若本人違反上述任何條款，本人願負完全責任並接受學校之處分（包括退學、取消獎助學金、遣返），絕無異議。", "vi": "5. Quy định về Giấy phép làm việc: Tôi cam kết tuân thủ quy định thời gian làm việc tối đa 20 giờ mỗi tuần (trừ kỳ nghỉ đông và nghỉ hè). Nếu tôi vi phạm bất kỳ điều khoản nào nêu trên, tôi xin chịu hoàn toàn trách nhiệm và chấp nhận các hình thức xử lý của nhà trường (bao gồm buộc thôi học, hủy học bổng, trục xuất về nước) mà không có bất kỳ khiếu nại nào.", "id": "5. Peraturan Izin Kerja: Saya berjanji untuk mematuhi peraturan batas jam kerja maksimal 20 jam per minggu (kecuali liburan musim dingin dan panas). Jika saya melanggar ketentuan di atas, saya bersedia bertanggung jawab penuh dan menerima sanksi dari sekolah (termasuk dikeluarkan, pembatalan beasiswa, deportasi) tanpa keberatan.", "th": "5. กฎระเบียบใบอนุญาตทำงาน: ข้าพเจ้าขอสัญญาว่าจะปฏิบัติตามกฎระเบียบจำกัดชั่วโมงการทำงานไม่เกิน 20 ชั่วโมงต่อสัปดาห์ (ยกเว้นช่วงปิดเทอมฤดูหนาวและฤดูร้อน) หากข้าพเจ้าฝ่าฝืนข้อกำหนดข้างต้น ข้าพเจ้ายินดีรับผิดชอบทั้งหมดและยอมรับบทลงโทษของทางโรงเรียน (รวมถึงการไล่ออก การยกเลิกทุนการศึกษา การส่งกลับประเทศ) โดยไม่มีข้อโต้แย้งใดๆ" },
            { "id": "c6", "zh": "6.我知道本文件經簽署後，不可任意更動。", "vi": "6. Tôi biết rằng văn bản này sau khi đã ký tên thì không được tùy ý thay đổi.", "id": "6. Saya tahu bahwa dokumen ini tidak dapat diubah secara sepihak setelah ditandatangani.", "th": "6. ข้าพเจ้าทราบว่าเอกสารนี้เมื่อลงนามแล้ว ห้ามทำการแก้ไขเปลี่ยนแปลงใดๆ" }
        ]
    },

    # === DOC 2 ===
    "work_study": {
        "menu_names": {
            "zh": "2. 工讀須知切結書",
            "vi": "2. Cam kết quy định làm thêm",
            "th": "2. ข้อควรทราบเกี่ยวกับการทำงานพาร์ทไทม์",
            "id": "2. Surat Pernyataan Kerja Paruh Waktu"
        },
        "header_title": {
            "zh": "國際專修部華語先修班與國際學生工讀須知切結書",
            "vi": "BẢN CAM KẾT VỀ QUY ĐỊNH LÀM THÊM DÀNH CHO SINH VIÊN QUỐC TẾ HỆ DỰ BỊ",
            "th": "หนังสือสัญญาข้อควรทราบเกี่ยวกับการทำงานพาร์ทไทม์สำหรับนักศึกษาหลักสูตรเตรียมความพร้อมและนักศึกษาต่างชาติ",
            "id": "SURAT PERNYATAAN MENGENAI PERATURAN KERJA PARUH WAKTU UNTUK MAHASISWA INTERNASIONAL"
        },
        "body_intro": {
            "zh": "因為我工讀的單位沒有正式的工讀合約，我在此聲明我已經了解，並且會遵守台灣就業服務法對於國際學生工讀的相關規定，說明如下：",
            "vi": "Vì đơn vị tôi làm việc không có hợp đồng chính thức, tôi xin tuyên bố đã hiểu và sẽ tuân thủ các quy định của Luật Dịch vụ Việc làm Đài Loan về việc làm thêm của sinh viên quốc tế, cụ thể như sau:",
            "id": "Karena unit tempat saya bekerja paruh waktu tidak memiliki kontrak resmi, saya menyatakan bahwa saya telah memahami dan akan mematuhi peraturan Layanan Ketenagakerjaan Taiwan terkait kerja paruh waktu bagi mahasiswa internasional, sebagai berikut:",
            "th": "เนื่องจากหน่วยงานที่ข้าพเจ้าทำงานพาร์ทไทม์ไม่มีสัญญาจ้างงานอย่างเป็นทางการ ข้าพเจ้าขอประกาศว่าข้าพเจ้าเข้าใจและจะปฏิบัติตามกฎระเบียบของกฎหมายบริการการจ้างงานไต้หวันเกี่ยวกับการทำงานพาร์ทไทม์ของนักศึกษาต่างชาติ ดังนี้:"
        },
        "checkboxes": [
            { "id": "w1", "zh": "1. 我知道我必須依照規定申請並取得工作證之後，才可以開始課餘工讀。", "vi": "1. Tôi biết rằng tôi phải nộp đơn và được cấp GIẤY PHÉP LÀM VIỆC theo quy định trước khi bắt đầu làm thêm.", "id": "1. Saya tahu bahwa saya harus mengajukan dan mendapatkan ijin kerja sesuai peraturan sebelum memulai kerja paruh waktu.", "th": "1. ข้าพเจ้าทราบว่าต้องยื่นขอและได้รับใบอนุญาตทำงานตามระเบียบก่อน จึงจะเริ่มทำงานพาร์ทไทม์นอกเวลาเรียนได้" },
            { "id": "w2", "zh": "2. 我知道台灣的基本薪資是196元，我確定我的工讀薪資高於196元。", "vi": "2. Tôi biết mức lương cơ bản ở Đài Loan là 196 Đài tệ, và tôi xác nhận lương làm thêm của tôi cao hơn 196 Đài tệ.", "id": "2. Saya tahu upah minimum di Taiwan adalah 196 NTD, dan saya pastikan upah kerja paruh waktu saya lebih tinggi dari 196 NTD.", "th": "2. ข้าพเจ้าทราบว่าค่าจ้างขั้นต่ำของไต้หวันคือ 196 ดอลลาร์ไต้หวัน และข้าพเจ้ายืนยันว่าค่าจ้างพาร์ทไทม์ของข้าพเจ้าสูงกว่า 196 ดอลลาร์ไต้หวัน" },
            { "id": "w3", "zh": "3. 我知道在學期上課期間，每個星期可以工讀的時數上限是20個小時。", "vi": "3. Tôi biết rằng trong thời gian học kỳ, thời gian làm thêm tối đa là 20 GIỜ mỗi tuần.", "id": "3. Saya tahu bahwa selama semester perkuliahan, batas waktu kerja paruh waktu adalah 20 JAM per minggu.", "th": "3. ข้าพเจ้าทราบว่าในระหว่างภาคการศึกษา ชั่วโมงทำงานพาร์ทไทม์สูงสุดคือ 20 ชั่วโมงต่อสัปดาห์" },
            { "id": "w4", "zh": "4. 我知道在學期期間如果超時工讀，經過查報屬實，我會被政府罰款台幣3萬元以上，15萬元以下。我的雇主會被罰款台幣15萬元以上，75萬元以下。我也會失去領取校內獎助學金的資格，而且已經領取的獎助學金必須全部繳回。", "vi": "4. Tôi biết nếu làm quá giờ quy định, tôi sẽ bị phạt từ 30.000 đến 150.000 Đài tệ. Chủ thuê sẽ bị phạt từ 150.000 đến 750.000 Đài tệ. Tôi cũng sẽ mất tư cách nhận học bổng và phải hoàn trả học bổng đã nhận.", "id": "4. Saya tahu jika bekerja melebihi batas waktu, saya akan didenda 30.000-150.000 NTD. Majikan akan didenda 150.000-750.000 NTD. Saya juga akan kehilangan beasiswa dan wajib mengembalikan beasiswa yang telah diterima.", "th": "4. ข้าพเจ้าทราบว่าหากทำงานเกินเวลา จะถูกปรับ 30,000-150,000 TWD นายจ้างถูกปรับ 150,000-750,000 TWD ข้าพเจ้าจะหมดสิทธิ์รับทุนการศึกษาและต้องคืนทุนที่ได้รับไปแล้วทั้งหมด" },
            { "id": "w5", "zh": "我已經充分理解以上工讀相關規定。我在尋找工讀機會時，我會維護自身權益，並且遵守相關法令規範。", "vi": "Tôi đã hiểu rõ các quy định trên. Khi tìm việc, tôi sẽ bảo vệ quyền lợi của mình và tuân thủ pháp luật.", "id": "Saya memahami sepenuhnya peraturan di atas. Saya akan menjaga hak saya dan mematuhi hukum saat mencari kerja.", "th": "ข้าพเจ้าเข้าใจกฎระเบียบข้างต้นอย่างครบถ้วน ข้าพเจ้าจะรักษาผลประโยชน์ของตนและปฏิบัติตามกฎหมายเมื่อหางานทำ" }
        ]
    }
}