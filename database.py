import sqlite3
from datetime import datetime, timedelta
TEN_CSDL = "gym.db"


def connect():
    conn = sqlite3.connect(TEN_CSDL)
    conn.execute(" PRAGMA foreign_keys = ON")
    return conn


def khoi_tao_csdl():
    conn = connect()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS GOI_TAP(
        Ma_Goi INTEGER PRIMARY KEY AUTOINCREMENT,
        Ten_Goi TEXT UNIQUE NOT NULL,
        Thoi_Han_Thang INTEGER NOT NULL,
        Gia REAL NOT NULL)""")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS HOI_VIEN(
            Ma_HV INTEGER PRIMARY KEY AUTOINCREMENT,
            Ho_Ten text NOT NULL,
            CCCD text UNIQUE NOT NULL,
            SDT text,
            Ngay_Sinh text,
            Dia_Chi text
        )""")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS DANG_KY(
            Ma_DK INTEGER PRIMARY KEY AUTOINCREMENT,
            Ma_HV INTEGER NOT NULL,
            Ma_Goi INTEGER NOT NULL,
            Ngay_Bat_Dau text NOT NULL,
            Ngay_Het_Han text NOT NULL,
            Trang_Thai   TEXT NOT NULL DEFAULT 'Chưa thanh toán',
            FOREIGN KEY (Ma_HV) REFERENCES HOI_VIEN(Ma_HV),
            FOREIGN  KEY (Ma_Goi) REFERENCES GOI_TAP(Ma_Goi)
    )""")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS NHAN_VIEN(
            Ma_NV integer PRIMARY KEY AUTOINCREMENT,
            Ho_Ten text NOT NULL,
            Chuc_Vu text
            )""")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS TAI_KHOAN(
            Ten_DN text PRIMARY KEY,
            Mat_Khau text NOT NULL,
            Ma_NV integer NOT NULL,
            FOREIGN KEY (Ma_NV) REFERENCES NHAN_VIEN(Ma_NV)
            )""")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS DICH_VU(
            Ma_DV INTEGER PRIMARY KEY AUTOINCREMENT,
            Ten_DV text UNIQUE NOT NULL,
            Don_Gia REAL NOT NULL
        )""")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS SU_DUNG_DICH_VU
        (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Ma_DK INTEGER NOT NULL,   
            Ma_DV INTEGER NOT NULL,
            So_Luong INTEGER NOT NULL DEFAULT 1,
            Da_Tinh_Tien INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY( Ma_DK) REFERENCES DANG_KY (Ma_DK),
            FOREIGN KEY( Ma_DV ) REFERENCES DICH_VU (Ma_DV)
            )""")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS DIEM_DANH
        (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Ma_DK INTEGER NOT NULL,
            Thoi_Gian TEXT NOT NULL,
            FOREIGN KEY (Ma_DK) REFERENCES DANG_KY (Ma_DK)
            )""")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS HOA_DON(
            Ma_HD INTEGER PRIMARY KEY AUTOINCREMENT,
            Ma_DK INTEGER NOT NULL,
            Ngay_Lap TEXT NOT NULL,
            Tien_Goi REAL NOT NULL,
            Tien_Dich_Vu REAL NOT NULL,
            Tong_Tien REAL NOT NULL,
            FOREIGN KEY (Ma_DK) REFERENCES DANG_KY(Ma_DK)
        )""")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS NHAT_KY(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Thoi_Gian TEXT NOT NULL,
            Nguoi_Dung TEXT NOT NULL,
            Hanh_Dong TEXT NOT NULL,
            Noi_Dung TEXT
        )""")
    conn.commit()
    conn.close()


# ========== GÓI TẬP ==========

def them_goi(ten, thang, gia):
    conn = connect()
    conn.execute(" INSERT INTO GOI_TAP (Ten_Goi, Thoi_Han_Thang, Gia) VALUES (?, ?, ?)", (ten, thang, gia))
    conn.commit()
    conn.close()


def sua_goi(Ma_Goi, Ten_Goi_Moi, Gia_Moi):
    conn = connect()
    conn.execute(" UPDATE GOI_TAP SET Ten_Goi = ?, Gia = ? WHERE Ma_Goi = ?", (Ten_Goi_Moi, Gia_Moi, Ma_Goi))
    conn.commit()
    conn.close()


def xoa_goi(Ma_Goi):
    conn = connect()
    try:
        conn.execute("DELETE FROM GOI_TAP WHERE Ma_Goi = ?", (Ma_Goi,))
        conn.commit()
        return True, "Đã xóa gói tập."
    except sqlite3.IntegrityError:
        return False, "Gói tập đã có người đăng ký, không thể xóa!"
    finally:
        conn.close()


def ds_goi():
    conn = connect()
    rows = conn.execute(" SELECT * FROM GOI_TAP").fetchall()
    conn.close()
    return rows


def thong_ke_theo_goi():
    conn = connect()
    rows = conn.execute("""
        SELECT GT.Ten_Goi, COUNT(*)
        FROM DANG_KY DK
        JOIN GOI_TAP GT ON DK.Ma_Goi = GT.Ma_Goi
        Group by GT.Ten_Goi""").fetchall()
    conn.close()
    return rows


# ========== HỘI VIÊN ==========

def them_hv(Ho_Ten, CCCD, SDT, Dia_Chi):
    conn = connect()
    try:
        conn.execute(" INSERT INTO HOI_VIEN(Ho_Ten, CCCD, SDT, Dia_Chi) VALUES (?, ?, ?, ?)", (Ho_Ten, CCCD, SDT, Dia_Chi))
        conn.commit()
        ghi_nhat_ky("Thêm hội viên", Ho_Ten)
        return True, "Thêm hội viên thành công."
    except sqlite3.IntegrityError:
        return False, "Số CCCD đã tồn tại"
    finally:
        conn.close()


def sua_hv(Ma_HV, Ho_Ten, SDT, Ngay_Sinh, Dia_Chi):
    conn = connect()
    try:
        conn.execute(
            "UPDATE HOI_VIEN SET Ho_Ten = ?, SDT = ?, Ngay_Sinh = ?, Dia_Chi = ? WHERE Ma_HV = ?",
            (Ho_Ten, SDT, Ngay_Sinh, Dia_Chi, Ma_HV)
        )
        conn.commit()
        ghi_nhat_ky("Sửa hội viên", Ho_Ten)
        return True, "Cập nhật hội viên thành công."
    except sqlite3.IntegrityError:
        return False, "Có lỗi khi cập nhật!"
    finally:
        conn.close()


def tim_hv(Tu_Khoa):
    conn = connect()
    rows = conn.execute("SELECT * FROM HOI_VIEN where Ho_Ten like ?", ("%" + Tu_Khoa + "%",)).fetchall()
    conn.close()
    return rows


def xoa_hv(Ma_HV):
    conn = connect()
    try:
        conn.execute("DELETE FROM HOI_VIEN WHERE Ma_HV = ?", (Ma_HV,))
        conn.commit()
        return True, "Đã xóa hội viên."
    except sqlite3.IntegrityError:
        return False, "Hội viên đã có phiếu đăng ký, không thể xóa!"
    finally:
        conn.close()


def dem_so_hv():
    conn = connect()
    So_Luong = conn.execute("SELECT COUNT(*) FROM HOI_VIEN").fetchone()[0]
    conn.close()
    return So_Luong


def ds_hv():
    conn = connect()
    rows = conn.execute(" SELECT * FROM HOI_VIEN ").fetchall()
    conn.close()
    return rows


# ========== ĐĂNG KÝ GÓI TẬP ==========

def dang_ky_goi(Ma_HV, Ma_Goi, Ngay_Bat_Dau):
    conn = connect()
    try:
        d1 = datetime.strptime(Ngay_Bat_Dau, "%Y-%m-%d")
    except ValueError:
        conn.close()
        return False, "Ngày không đúng định dạng YYYY-MM-DD!"

    ket_qua = conn.execute("SELECT Thoi_Han_Thang FROM GOI_TAP WHERE Ma_Goi = ?", (Ma_Goi,)).fetchone()
    if ket_qua is None:
        conn.close()
        return False, "Không tìm thấy gói tập!"
    Thang = ket_qua[0]

    D2 = d1 + timedelta(days=30 * Thang)
    Ngay_Het_Han = D2.strftime("%Y-%m-%d")

    try:
        conn.execute(
            "INSERT INTO DANG_KY (Ma_HV, Ma_Goi, Ngay_Bat_Dau, Ngay_Het_Han) VALUES (?, ?, ?, ?)",
            (Ma_HV, Ma_Goi, Ngay_Bat_Dau, Ngay_Het_Han)
        )
        conn.commit()
        ghi_nhat_ky("Đăng ký gói tập", f"HV {Ma_HV} - gói {Ma_Goi}, hạn {Ngay_Het_Han}")
        return True, f"Đăng ký thành công. Hạn tập đến {Ngay_Het_Han}."
    except sqlite3.IntegrityError:
        return False, "Mã hội viên hoặc mã gói không hợp lệ!"
    finally:
        conn.close()


def dem_so_dang_ky():
    conn = connect()
    So_Luong = conn.execute(" SELECT count(*) FROM DANG_KY").fetchone()[0]
    conn.close()
    return So_Luong


def ds_dang_ky():
    conn = connect()
    rows = conn.execute(""" SELECT DK.Ma_DK, HV.Ho_Ten, GT.Ten_Goi, DK.Ngay_Bat_Dau, DK.Ngay_Het_Han, DK.Trang_Thai FROM DANG_KY DK
                            JOIN HOI_VIEN HV on DK.Ma_HV = HV.Ma_HV
                            JOIN GOI_TAP GT on DK.Ma_Goi = GT.Ma_Goi
        """).fetchall()
    conn.close()
    return rows


# ========== NHÂN VIÊN & TÀI KHOẢN ==========

def dang_nhap(Ten_DN, Mat_Khau):
    conn = connect()
    ket_qua = conn.execute(" SELECT nv.Ho_Ten FROM TAI_KHOAN tk JOIN NHAN_VIEN nv ON tk.Ma_NV = nv.Ma_NV WHERE tk.Ten_DN =? AND tk.Mat_Khau =?",
                           (Ten_DN, Mat_Khau)).fetchone()
    conn.close()
    return ket_qua


def them_nv(Ho_Ten, Chuc_Vu):
    conn = connect()
    try:
        conn.execute(" INSERT INTO NHAN_VIEN (Ho_Ten, Chuc_Vu) VALUES (?, ?)", (Ho_Ten, Chuc_Vu))
        conn.commit()
        ghi_nhat_ky("Thêm Nhân viên", Ho_Ten)
        return True, "Thêm Nhân viên thành công."
    except sqlite3.IntegrityError:
        return False, "Số CCCD đã tồn tại!"
    finally:
        conn.close()


def xoa_nv(Ma_NV):
    conn = connect()
    try:
        conn.execute("DELETE FROM NHAN_VIEN WHERE Ma_NV = ?", (Ma_NV,))
        conn.commit()
        return True, "Đã xóa nhân viên."
    except sqlite3.IntegrityError:
        return False, "Nhân viên có tài khoản hoặc đã lập phiếu, không thể xóa!"
    finally:
        conn.close()


def ds_nv():
    conn = connect()
    rows = conn.execute(" SELECT * FROM NHAN_VIEN ORDER BY Ma_NV").fetchall()
    conn.close()
    return rows


def them_tai_Khoan(Ten_DN, Mat_Khau, Ma_NV):
    conn = connect()
    try:
        conn.execute("INSERT INTO TAI_KHOAN(Ten_DN, Mat_Khau, Ma_NV) VALUES (?, ?, ?)", (Ten_DN, Mat_Khau, Ma_NV))
        conn.commit()
        return True, "Tạo tài khoản thành công."
    except sqlite3.IntegrityError:
        return False, "Tên đăng nhập đã tồn tại!"
    finally:
        conn.close()


# ========== DỊCH VỤ ==========

def them_dv(Ten_DV, Don_Gia):
    conn = connect()
    try:
        conn.execute("INSERT INTO DICH_VU (Ten_DV, Don_Gia) VALUES (?, ?)", (Ten_DV, Don_Gia))
        conn.commit()
        ghi_nhat_ky("Thêm dịch vụ", Ten_DV)
        return True, "Thêm dịch vụ thành công."
    except sqlite3.IntegrityError:
        return False, "Tên dịch vụ đã tồn tại!"
    finally:
        conn.close()


def xoa_dv(Ma_DV):
    conn = connect()
    try:
        conn.execute("DELETE FROM DICH_VU WHERE Ma_DV = ?", (Ma_DV,))
        conn.commit()
        return True, "Đã xóa dịch vụ."
    except sqlite3.IntegrityError:
        return False, "Dịch vụ đã được sử dụng, không thể xóa!"
    finally:
        conn.close()


def ds_dv():
    conn = connect()
    rows = conn.execute("SELECT * FROM DICH_VU ORDER BY Ma_DV").fetchall()
    conn.close()
    return rows


def them_su_dung_dv(Ma_DK, Ma_DV, So_Luong):
    conn = connect()
    Hom_Nay = datetime.now().strftime("%Y-%m-%d")
    da_diem_danh = conn.execute(
        "SELECT COUNT(*) FROM DIEM_DANH WHERE Ma_DK = ? AND substr(Thoi_Gian, 1, 10) = ?",
        (Ma_DK, Hom_Nay)).fetchone()[0]
    if da_diem_danh == 0:
        conn.close()
        return False, "Hội viên chưa điểm danh hôm nay, không thể mua dịch vụ!"
    conn.execute("INSERT INTO SU_DUNG_DICH_VU (Ma_DK, Ma_DV, So_Luong) VALUES (?, ?, ?)", (Ma_DK, Ma_DV, So_Luong))
    conn.commit()
    conn.close()
    ghi_nhat_ky("Thêm dịch vụ vào phiếu", f"Phiếu {Ma_DK} - dịch vụ {Ma_DV} x{So_Luong}")
    return True, "Đã thêm dịch vụ vào phiếu."


def tinh_tien_dv(Ma_DK):
    conn = connect()
    tong = conn.execute("""
        SELECT SUM(sd.So_Luong * dv.Don_Gia)
        FROM SU_DUNG_DICH_VU sd
        JOIN DICH_VU dv ON sd.Ma_DV = dv.Ma_DV
        WHERE sd.Ma_DK = ?
    """, (Ma_DK,)).fetchone()[0]
    conn.close()
    return tong if tong else 0


# ========== ĐIỂM DANH ==========

def diem_danh(Ma_DK):
    conn = connect()
    ket_qua = conn.execute(
        "SELECT Ngay_Het_Han, Trang_Thai FROM DANG_KY WHERE Ma_DK = ?", (Ma_DK,)).fetchone()
    if ket_qua is None:
        conn.close()
        return False, "Không tìm thấy phiếu đăng ký!"
    Ngay_Het_Han, Trang_Thai = ket_qua
    if Trang_Thai != "Đã thanh toán":
        conn.close()
        return False, "Phiếu chưa thanh toán, vui lòng thanh toán trước khi tập!"
    Hom_Nay = datetime.now().strftime("%Y-%m-%d")
    if Hom_Nay > Ngay_Het_Han:
        conn.close()
        return False, "Phiếu đã hết hạn!"
    Da_Diem_Danh = conn.execute(
        "SELECT COUNT(*) FROM DIEM_DANH WHERE Ma_DK = ? AND substr(Thoi_Gian, 1, 10) = ?", (Ma_DK, Hom_Nay)).fetchone()[0]
    if Da_Diem_Danh > 0:
        conn.close()
        return False, "Đã điểm danh hôm nay rồi!"
    conn.execute(
        "INSERT INTO DIEM_DANH (Ma_DK, Thoi_Gian) VALUES (?, ?)", (Ma_DK, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()
    ghi_nhat_ky("Điểm danh", f"Phiếu {Ma_DK} check-in")
    return True, "Điểm danh thành công."


def ds_diem_danh():
    conn = connect()
    rows = conn.execute(" SELECT * FROM DIEM_DANH ORDER BY ID DESC ").fetchall()
    conn.close()
    return rows


# ========== THANH TOÁN & HÓA ĐƠN ==========
# Nếu phiếu đã hết hạn, thanh toán vẫn được — coi như GIA HẠN: tự động
# tính lại Ngay_Bat_Dau (hôm nay) và Ngay_Het_Han (hôm nay + thời hạn
# gói), tính lại tiền gói. Không thay đổi gì ở dang_ky_goi.

def thanh_toan(Ma_DK):
    conn = connect()
    ket_qua = conn.execute("""
        SELECT gt.Gia, dk.Trang_Thai, dk.Ngay_Het_Han, gt.Thoi_Han_Thang FROM DANG_KY dk
        JOIN GOI_TAP gt on dk.Ma_Goi = gt.Ma_Goi
        WHERE dk.Ma_DK = ?
    """, (Ma_DK,)).fetchone()
    if ket_qua is None:
        conn.close()
        return False, "Không tìm thấy phiếu đăng ký!"

    gia_goi, Trang_Thai, Ngay_Het_Han, Thoi_Han_Thang = ket_qua
    lan_dau = (Trang_Thai != "Đã thanh toán")

    Hom_Nay = datetime.now().strftime("%Y-%m-%d")
    # Ap dung CHUNG 1 dieu kien cho moi truong hop: neu ngay het han hien
    # dang luu (du la lan dau hay da tung thanh toan) da qua so voi hom
    # nay, thi tinh lai ngay bat dau/ket thuc = hom nay + thoi han goi.
    # Nho vay, ke ca phieu dang ky voi ngay qua cu (het han ngay tu luc
    # dang ky, chua tung thanh toan) cung duoc cap nhat dung ngay ngay
    # trong LAN THANH TOAN DAU TIEN, khong can thanh toan 2 lan.
    da_qua_han = Hom_Nay > Ngay_Het_Han

    if da_qua_han:
        D1 = datetime.strptime(Hom_Nay, "%Y-%m-%d")
        D2 = D1 + timedelta(days=30 * Thoi_Han_Thang)
        Ngay_Bat_Dau_Moi = Hom_Nay
        Ngay_Het_Han_Moi = D2.strftime("%Y-%m-%d")
        tien_goi = gia_goi
    else:
        # Con han: lan dau thi tinh tien goi (giu nguyen ngay da dang ky),
        # da thanh toan roi thi khong tinh lai tien goi nua.
        tien_goi = gia_goi if lan_dau else 0

    tien_dich_vu_moi = conn.execute("""
        SELECT COALESCE(SUM(sd.So_Luong * dv.Don_Gia), 0)
        FROM SU_DUNG_DICH_VU sd
        JOIN DICH_VU dv ON sd.Ma_DV = dv.Ma_DV
        WHERE sd.Ma_DK = ? AND sd.Da_Tinh_Tien = 0
    """, (Ma_DK,)).fetchone()[0]

    if tien_goi == 0 and tien_dich_vu_moi == 0:
        conn.close()
        return False, "Không có khoản nào cần thanh toán!"

    tong_tien = tien_goi + tien_dich_vu_moi
    conn.execute(
        "INSERT INTO HOA_DON (Ma_DK, Ngay_Lap, Tien_Goi, Tien_Dich_Vu, Tong_Tien) VALUES (?, ?, ?, ?, ?)",
        (Ma_DK, Hom_Nay, tien_goi, tien_dich_vu_moi, tong_tien)
    )
    conn.execute(
        "UPDATE SU_DUNG_DICH_VU SET Da_Tinh_Tien = 1 WHERE Ma_DK = ? AND Da_Tinh_Tien = 0", (Ma_DK,)
    )
    if da_qua_han:
        conn.execute(
            "UPDATE DANG_KY SET Trang_Thai = ?, Ngay_Bat_Dau = ?, Ngay_Het_Han = ? WHERE Ma_DK = ?",
            ("Đã thanh toán", Ngay_Bat_Dau_Moi, Ngay_Het_Han_Moi, Ma_DK)
        )
    elif lan_dau:
        conn.execute("UPDATE DANG_KY SET Trang_Thai = ? WHERE Ma_DK = ?", ("Đã thanh toán", Ma_DK))
    conn.commit()
    conn.close()
    ghi_nhat_ky("Thanh toán", f"Phiếu {Ma_DK}, số tiền {tong_tien:,.0f} đ")
    return True, f"Thanh toán thành công! Số tiền lần này: {tong_tien:,.0f} đ"


def ds_hoa_don():
    conn = connect()
    rows = conn.execute("SELECT * FROM HOA_DON ORDER BY Ma_HD DESC").fetchall()
    conn.close()
    return rows


# ========== NHẬT KÝ THAY ĐỔI ==========

NGUOI_DUNG_HIEN_TAI = "Hệ thống"


def dat_nguoi_dung(ho_ten):
    global NGUOI_DUNG_HIEN_TAI
    NGUOI_DUNG_HIEN_TAI = ho_ten


def ghi_nhat_ky(Hanh_Dong, Noi_Dung):
    conn = connect()
    conn.execute(
        "INSERT INTO NHAT_KY (Thoi_Gian, Nguoi_Dung, Hanh_Dong, Noi_Dung) VALUES (?, ?, ?, ?)",
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), NGUOI_DUNG_HIEN_TAI, Hanh_Dong, Noi_Dung)
    )
    conn.commit()
    conn.close()


def ds_nhat_ky():
    conn = connect()
    rows = conn.execute("SELECT * FROM NHAT_KY ORDER BY ID DESC").fetchall()
    conn.close()
    return rows
