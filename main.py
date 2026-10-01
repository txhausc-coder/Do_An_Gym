
import tkinter as tk
from tkinter import ttk, messagebox
import database as db
db.khoi_tao_csdl()
# ========== CỬA SỔ ĐĂNG NHẬP ==========
def xu_ly_dang_nhap():
    ten_dn = o_ten_dn.get()
    mat_khau = o_mat_khau.get()
    ket_qua = db.dang_nhap(ten_dn, mat_khau)
    if ket_qua is None:
        messagebox.showerror("Lỗi", "Sai tên đăng nhập hoặc mật khẩu!")
        return
    db.dat_nguoi_dung(ket_qua[0])
    Cua_So_Dang_Nhap.destroy()
    mo_cua_so_chinh()

MAU_NEN = "#2C3E50"      # xanh navy đậm
MAU_CHU = "#ECF0F1"      # trắng ngà
MAU_NUT = "#27AE60"      # xanh lá

Cua_So_Dang_Nhap = tk.Tk()
Cua_So_Dang_Nhap.title("Đăng nhập hệ thống")
Cua_So_Dang_Nhap.geometry("380x320")
Cua_So_Dang_Nhap.configure(bg=MAU_NEN)
Cua_So_Dang_Nhap.resizable(False, False)

# Canh giữa màn hình
rong, cao = 380, 320
x = (Cua_So_Dang_Nhap.winfo_screenwidth() - rong) // 2
y = (Cua_So_Dang_Nhap.winfo_screenheight() - cao) // 2
Cua_So_Dang_Nhap.geometry(f"{rong}x{cao}+{x}+{y}")

tk.Label(Cua_So_Dang_Nhap, text="🏋", font=("Arial", 36), bg=MAU_NEN, fg=MAU_CHU).pack(pady=(25, 0))
tk.Label(Cua_So_Dang_Nhap, text="QUẢN LÝ PHÒNG GYM", font=("Arial", 15, "bold"), bg=MAU_NEN, fg=MAU_CHU).pack(pady=(0, 20))

tk.Label(Cua_So_Dang_Nhap, text="Tên đăng nhập", font=("Arial", 10), bg=MAU_NEN, fg=MAU_CHU).pack()
o_ten_dn = tk.Entry(Cua_So_Dang_Nhap, font=("Arial", 11), justify="center", width=25)
o_ten_dn.pack(pady=(3, 12), ipady=4)

tk.Label(Cua_So_Dang_Nhap, text="Mật khẩu", font=("Arial", 10), bg=MAU_NEN, fg=MAU_CHU).pack()
o_mat_khau = tk.Entry(Cua_So_Dang_Nhap, font=("Arial", 11), justify="center", width=25, show="*")
o_mat_khau.pack(pady=(3, 20), ipady=4)

nut_dang_nhap = tk.Button(
    Cua_So_Dang_Nhap, text="ĐĂNG NHẬP", font=("Arial", 11, "bold"),
    bg=MAU_NUT, fg="white", activebackground="#1E8449",
    relief="flat", width=20, pady=8, command=xu_ly_dang_nhap
)
nut_dang_nhap.pack()

Cua_So_Dang_Nhap.bind("<Return>", lambda e: xu_ly_dang_nhap())
o_ten_dn.focus()
# ========== CỬA SỔ CHÍNH ==========
def mo_cua_so_chinh():
    global Cua_So
    Cua_So = tk.Tk()
    Cua_So.title("Quản Lý Phòng Gym")
    Cua_So.configure(bg="#F4F6F7")
    Cua_So.state("zoomed")

    rong, cao = 1024, 800
    x = (Cua_So.winfo_screenwidth() - rong) // 2
    y = (Cua_So.winfo_screenheight() - cao) // 2
    Cua_So.geometry(f"{rong}x{cao}+{x}+{y}")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TNotebook.Tab", font=("Arial", 10, "bold"), padding=[14, 8])
    style.configure("Treeview", font=("Arial", 10), rowheight=26)
    style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#2C3E50", foreground="white")

    notebook = ttk.Notebook(Cua_So)
    notebook.pack(expand=True, fill="both")

    # =======Tab Hội Viên ======

    tab_hv = ttk.Frame(notebook)
    notebook.add(tab_hv, text = " Hội Viên")

    dong_ten_hv = tk.Frame(tab_hv)
    dong_ten_hv.pack( pady=3)
    tk.Label(dong_ten_hv, text="Họ tên:", width=15, anchor="w").pack(side="left")
    o_ten_hv = tk.Entry(dong_ten_hv, width=25)
    o_ten_hv.pack(side="left")

    dong_cccd_hv = tk.Frame(tab_hv)
    dong_cccd_hv.pack( pady=3)
    tk.Label(dong_cccd_hv, text="CCCD:", width=15, anchor="w").pack(side="left")
    o_cccd_hv = tk.Entry(dong_cccd_hv, width=25)
    o_cccd_hv.pack(side="left")

    dong_sdt_hv = tk.Frame(tab_hv)
    dong_sdt_hv.pack(pady=3)
    tk.Label(dong_sdt_hv, text="SĐT:", width=15, anchor="w").pack(side="left")
    o_sdt_hv = tk.Entry(dong_sdt_hv, width=25)
    o_sdt_hv.pack(side="left")

    dong_ns_hv = tk.Frame(tab_hv)
    dong_ns_hv.pack(pady=3)
    tk.Label(dong_ns_hv, text="Ngày sinh (YYYY-MM-DD):", width=15, anchor="w").pack(side="left")
    o_ngaysinh_hv = tk.Entry(dong_ns_hv, width=25)
    o_ngaysinh_hv.pack(side="left")

    dong_diachi_hv = tk.Frame(tab_hv)
    dong_diachi_hv.pack(pady=3)
    tk.Label(dong_diachi_hv, text="Nơi ở:", width=15, anchor="w").pack(side="left")
    o_diachi_hv = tk.Entry(dong_diachi_hv, width=25)
    o_diachi_hv.pack(side="left")

    bang_hv = ttk.Treeview(tab_hv, columns = ("Ma", "TEN", "CCCD", "SDT"), show= "headings")
    bang_hv.heading("Ma", text = "Ma_HV")
    bang_hv.heading("TEN", text = "Họ Tên")
    bang_hv.heading("CCCD", text= "CCCD" )
    bang_hv.heading("SDT", text = "SDT" )
    bang_hv.pack(fill = "both", expand = True)

    def lam_moi_bang_hv():
        for dong in bang_hv.get_children():
            bang_hv.delete(dong)
        for hv in db.ds_hv():
            bang_hv.insert("", "end", values=hv)

    def khi_bam_them_hv():
        ok, thong_bao = db.them_hv(o_ten_hv.get(), o_cccd_hv.get(), o_sdt_hv.get(), o_diachi_hv.get())
        messagebox.showinfo("Thông báo", thong_bao) if ok else messagebox.showerror("Lỗi", thong_bao)
        lam_moi_bang_hv()
    nut_them_hv = tk.Button(tab_hv, text=" Thêm hội viên", command= khi_bam_them_hv)
    nut_them_hv.pack()

    def khi_bam_xoa_hv():
        s = bang_hv.selection()
        if not s:
            messagebox.showwarning("Chưa chọn", "Chọn hội viên cần xóa trong bảng!")
            return
        ma_hv = bang_hv.item(s[0], "values")[0]
        ok, thong_bao = db.xoa_hv(ma_hv)
        messagebox.showinfo("Thông báo", thong_bao) if ok else messagebox.showerror("Lỗi", thong_bao)
        lam_moi_bang_hv()
    tk.Button(tab_hv, text="Xóa hội viên", command=khi_bam_xoa_hv, bg="#E74C3C", fg="white", relief="flat").pack(pady=3)
    lam_moi_bang_hv()

    def khi_chon_dong_hv(event):
        s = bang_hv.selection()
        if not s:
            return
        gia_tri = bang_hv.item(s[0], "values")
        o_ten_hv.delete(0, tk.END);
        o_ten_hv.insert(0, gia_tri[1])
        o_cccd_hv.delete(0, tk.END);
        o_cccd_hv.insert(0, gia_tri[2])
        o_sdt_hv.delete(0, tk.END);
        o_sdt_hv.insert(0, gia_tri[3])
        o_ngaysinh_hv.delete(0, tk.END);
        o_ngaysinh_hv.insert(0, gia_tri[4] or "")
        o_diachi_hv.delete(0, tk.END);
        o_diachi_hv.insert(0, gia_tri[5] or "")
    bang_hv.bind("<<TreeviewSelect>>", khi_chon_dong_hv)

    def khi_bam_sua_hv():
        s = bang_hv.selection()
        if not s:
            messagebox.showwarning("Chưa chọn", "Chọn hội viên cần sửa trong bảng!")
            return
        ma_hv = bang_hv.item(s[0], "values")[0]
        ok, thong_bao = db.sua_hv(ma_hv, o_ten_hv.get(), o_sdt_hv.get(), o_ngaysinh_hv.get(), o_diachi_hv.get())
        messagebox.showinfo("Thông báo", thong_bao) if ok else messagebox.showerror("Lỗi", thong_bao)
        lam_moi_bang_hv()

    tk.Button(tab_hv, text="Sửa hội viên", command=khi_bam_sua_hv, bg="#F39C12", fg="white", relief="flat").pack(pady=3)

# ====== Gói Tập ========

    tab_goi = ttk.Frame(notebook)
    notebook.add(tab_goi, text=" Gói tập")

    dong_ten_goi = tk.Frame(tab_goi)
    dong_ten_goi.pack(pady=3)
    tk.Label(dong_ten_goi, text="Tên gói:", width=15, anchor="w").pack(side="left")
    o_ten_goi = tk.Entry(dong_ten_goi, width=25)
    o_ten_goi.pack(side="left")

    dong_thang_goi = tk.Frame(tab_goi)
    dong_thang_goi.pack(pady=3)
    tk.Label(dong_thang_goi, text="Thời hạn (tháng):", width=15, anchor="w").pack(side="left")
    o_thang_goi = tk.Entry(dong_thang_goi, width=25)
    o_thang_goi.pack(side="left")

    dong_gia_goi = tk.Frame(tab_goi)
    dong_gia_goi.pack(pady=3)
    tk.Label(dong_gia_goi, text="Giá (VNĐ):", width=15, anchor="w").pack(side="left")
    o_gia_goi = tk.Entry(dong_gia_goi, width=25)
    o_gia_goi.pack(side="left")

    bang_goi = ttk.Treeview(tab_goi, columns = ("Ma", "Ten", "Thang", "Gia"), show= "headings")
    bang_goi.heading("Ma", text = "Mã Gói")
    bang_goi.heading("Ten", text=" Tên Gói")
    bang_goi.heading( "Thang", text=" Thời hạn (tháng)" )
    bang_goi.heading("Gia", text="Giá")
    bang_goi.pack( fill = "both", expand = True)

    def lam_moi_bang_goi():
        for dong in bang_goi.get_children():
            bang_goi.delete(dong)
        for g in db.ds_goi():
            bang_goi.insert("", "end", values=g)

    def khi_bam_them_goi():
        ten = o_ten_goi.get()
        thang = int(o_thang_goi.get())
        gia = float(o_gia_goi.get())
        ok, thong_bao = db.them_goi(ten, thang, gia)
        messagebox.showinfo("Thông báo", thong_bao) if ok else messagebox.showerror("Lỗi", thong_bao)
        lam_moi_bang_goi()

    def khi_bam_xoa_goi():
        s = bang_goi.selection()
        if not s:
            messagebox.showwarning("Chưa chọn", "Chọn gói tập cần xóa trong bảng!")
            return
        ma_goi = bang_goi.item(s[0], "values")[0]
        ok, thong_bao = db.xoa_goi(ma_goi)
        messagebox.showinfo("Thông báo", thong_bao) if ok else messagebox.showerror("Lỗi", thong_bao)
        lam_moi_bang_goi()

    tk.Button(tab_goi, text="Xóa gói tập", command=khi_bam_xoa_goi, bg="#E74C3C", fg="white", relief="flat").pack(
        pady=3)

    nut_them_goi = tk.Button(tab_goi, text=" Thêm gói tập", command= khi_bam_them_goi)
    nut_them_goi.pack()
    lam_moi_bang_goi()

    # ========== TAB NHÂN VIÊN ==========

    tab_nv = ttk.Frame(notebook)
    notebook.add(tab_nv, text="Nhân viên")

    dong_ten_nv = tk.Frame(tab_nv)
    dong_ten_nv.pack(pady=3)
    tk.Label(dong_ten_nv, text="Họ tên:", width=15, anchor="w").pack(side="left")
    o_ten_nv = tk.Entry(dong_ten_nv, width=25)
    o_ten_nv.pack(side="left")

    dong_cv_nv = tk.Frame(tab_nv)
    dong_cv_nv.pack(pady=3)
    bang_nv = ttk.Treeview(tab_nv, columns=("Ma", "Ten", "CV"), show="headings")
    bang_nv.heading("Ma", text="Mã NV")
    bang_nv.heading("Ten", text="Họ tên")
    bang_nv.heading("CV", text="Chức vụ")
    bang_nv.pack(fill="both", expand=True)
    tk.Label(dong_cv_nv, text="Chức vụ:", width=15, anchor="w").pack(side="left")
    o_chuc_vu_nv = tk.Entry(dong_cv_nv, width=25)
    o_chuc_vu_nv.pack(side="left")

    def lam_moi_bang_nv():
        for dong in bang_nv.get_children():
            bang_nv.delete(dong)
        for nv in db.ds_nv():
            bang_nv.insert("", "end", values=nv)

    def nut_bam_them_nv():
        ok, thong_bao = db.them_nv(o_ten_nv.get(), o_chuc_vu_nv.get())
        messagebox.showinfo("Thông báo", thong_bao) if ok else messagebox.showerror("Lỗi", thong_bao)
        lam_moi_bang_nv()

    nut_them_nv = tk.Button(tab_nv, text =" Thêm nhân viên", command= nut_bam_them_nv)
    nut_them_nv.pack()
    lam_moi_bang_nv()

    def khi_bam_xoa_nv():
        s = bang_nv.selection()
        if not s:
            messagebox.showwarning("Chưa chọn", "Chọn nhân viên cần xóa trong bảng!")
            return
        ma_nv = bang_nv.item(s[0], "values")[0]
        ok, thong_bao = db.xoa_nv(ma_nv)
        messagebox.showinfo("Thông báo", thong_bao) if ok else messagebox.showerror("Lỗi", thong_bao)
        lam_moi_bang_nv()

    tk.Button(tab_nv, text="Xóa nhân viên", command=khi_bam_xoa_nv, bg="#E74C3C", fg="white", relief="flat").pack(
        pady=3)

    # ========== TAB DỊCH VỤ ==========

    tab_dv = ttk.Frame(notebook)
    notebook.add(tab_dv, text=" Dịch vụ")

    dong_ten_dv = tk.Frame(tab_dv)
    dong_ten_dv.pack(pady=3)
    tk.Label(dong_ten_dv, text="Tên dịch vụ:", width=15, anchor="w").pack(side="left")
    o_ten_dv = tk.Entry(dong_ten_dv, width=25)
    o_ten_dv.pack(side="left")

    dong_gia_dv = tk.Frame(tab_dv)
    dong_gia_dv.pack(pady=3)
    tk.Label(dong_gia_dv, text="Đơn giá (VNĐ):", width=15, anchor="w").pack(side="left")
    o_gia_dv = tk.Entry(dong_gia_dv, width=25)
    o_gia_dv.pack(side="left")
    bang_dv = ttk.Treeview(tab_dv, columns=("Ma", "Ten", "Gia"), show="headings")
    bang_dv.heading("Ma", text="Mã DV")
    bang_dv.heading("Ten", text="Tên DV")
    bang_dv.heading("Gia", text="Giá DV")
    bang_dv.pack(fill="both", expand=True)

    def lam_moi_bang_dv():
        for dong in bang_dv.get_children():
            bang_dv.delete(dong)
        for dv in db.ds_dv():
            bang_dv.insert("", "end", values=dv)

    def khi_bam_them_dv():
        ten = o_ten_dv.get()
        gia = float(o_gia_dv.get())
        ok, thong_bao = db.them_dv(ten, gia)
        messagebox.showinfo("Thông báo", thong_bao) if ok else messagebox.showerror("Lỗi", thong_bao)
        lam_moi_bang_dv()

    nut_them_dv = tk.Button(tab_dv, text=" Thêm dịch vụ", command= khi_bam_them_dv)
    nut_them_dv.pack()
    lam_moi_bang_dv()

    def khi_bam_xoa_dv():
        s = bang_dv.selection()
        if not s:
            messagebox.showwarning("Chưa chọn", "Chọn dịch vụ cần xóa trong bảng!")
            return
        ma_dv = bang_dv.item(s[0], "values")[0]
        ok, thong_bao = db.xoa_dv(ma_dv)
        messagebox.showinfo("Thông báo", thong_bao) if ok else messagebox.showerror("Lỗi", thong_bao)
        lam_moi_bang_dv()

    tk.Button(tab_dv, text="Xóa dịch vụ", command=khi_bam_xoa_dv, bg="#E74C3C", fg="white", relief="flat").pack(pady=3)

    # ========== TAB ĐĂNG KÝ & THANH TOÁN ==========

    tab_dk = ttk.Frame(notebook)
    notebook.add(tab_dk, text=" Đăng ký & Thanh toán")

    danh_sach_hv_dk = db.ds_hv()
    danh_sach_goi_dk = db.ds_goi()

    dong_hv_dk = tk.Frame(tab_dk)
    dong_hv_dk.pack(pady=3)
    tk.Label(dong_hv_dk, text="Hội viên:", width=15, anchor="w").pack(side="left")
    o_chon_hv_dk = ttk.Combobox(dong_hv_dk, values=[hv[1] for hv in danh_sach_hv_dk], state="readonly", width=22)
    o_chon_hv_dk.pack(side="left")

    dong_goi_dk = tk.Frame(tab_dk)
    dong_goi_dk.pack(pady=3)
    tk.Label(dong_goi_dk, text="Gói tập:", width=15, anchor="w").pack(side="left")
    o_chon_goi_dk = ttk.Combobox(dong_goi_dk, values=[g[1] for g in danh_sach_goi_dk], state="readonly", width=22)
    o_chon_goi_dk.pack(side="left")

    dong_ngay_dk = tk.Frame(tab_dk)
    dong_ngay_dk.pack(pady=3)
    tk.Label(dong_ngay_dk, text="Ngày bắt đầu:", width=15, anchor="w").pack(side="left")
    o_ngay_dk = tk.Entry(dong_ngay_dk, width=25)
    o_ngay_dk.pack(side="left")

    bang_dk = ttk.Treeview(tab_dk, columns = ("Ma", "HV", "Goi", "BD", "HH", "TT"), show="headings")
    bang_dk.heading("Ma", text="Mã DK")
    bang_dk.heading("HV", text=" Hội viên")
    bang_dk.heading("Goi", text= "Gói tập")
    bang_dk.heading("BD", text=" Ngày bắt đầu")
    bang_dk.heading("HH", text="Ngày hết hạn")
    bang_dk.heading("TT", text=" Trạng thái")
    bang_dk.pack(fill="both", expand = True)

    def lam_moi_danh_sach_hv_dk():
        global danh_sach_hv_dk
        danh_sach_hv_dk = db.ds_hv()
        o_chon_hv_dk['values'] = [hv[1] for hv in danh_sach_hv_dk]
    o_chon_hv_dk.configure(postcommand=lam_moi_danh_sach_hv_dk)

    def lam_moi_bang_dk():
        for dong in bang_dk.get_children():
          bang_dk.delete(dong)
        for dk in db.ds_dang_ky():
          bang_dk.insert("", "end", values=dk)

    def khi_bam_dang_ky():
        ten_hv_da_chon = o_chon_hv_dk.get()
        ten_goi_da_chon = o_chon_goi_dk.get()
        if not ten_hv_da_chon or not ten_goi_da_chon:
            messagebox.showwarning("Thiếu dữ liệu", "Chọn hội viên và gói tập!")
            return

        ma_hv = None
        for hv in danh_sach_hv_dk:
            if hv[1] == ten_hv_da_chon:
                ma_hv = hv[0]
                break

        ma_goi = None
        for g in danh_sach_goi_dk:
            if g[1] == ten_goi_da_chon:
                ma_goi = g[0]
                break

        if ma_hv is None or ma_goi is None:
            messagebox.showerror("Lỗi", "Không tìm thấy hội viên hoặc gói đã chọn!")
            return

        ok, thong_bao = db.dang_ky_goi(ma_hv, ma_goi, o_ngay_dk.get())
        messagebox.showinfo("Thông báo", thong_bao) if ok else messagebox.showerror("Lỗi", thong_bao)
        lam_moi_bang_dk()

    tk.Label(tab_dk, text="─── Thêm dịch vụ vào phiếu ───", font=("Arial", 9, "italic")).pack(pady=(10, 3))
    danh_sach_dv_dk = db.ds_dv()
    dong_ma_dk_dv = tk.Frame(tab_dk)
    dong_ma_dk_dv.pack(pady=3)
    tk.Label(dong_ma_dk_dv, text="Mã phiếu:", width=15, anchor="w").pack(side="left")
    o_ma_dk_dv = tk.Entry(dong_ma_dk_dv, width=25)
    o_ma_dk_dv.pack(side="left")

    dong_chon_dv = tk.Frame(tab_dk)
    dong_chon_dv.pack(pady=3)
    tk.Label(dong_chon_dv, text="Dịch vụ:", width=15, anchor="w").pack(side="left")
    o_chon_dv_dk = ttk.Combobox(dong_chon_dv, values=[dv[1] for dv in danh_sach_dv_dk], state="readonly", width=22)
    o_chon_dv_dk.pack(side="left")

    dong_sl_dv = tk.Frame(tab_dk)
    dong_sl_dv.pack(pady=3)
    tk.Label(dong_sl_dv, text="Số lượng:", width=15, anchor="w").pack(side="left")
    o_sl_dv_dk = tk.Entry(dong_sl_dv, width=25)
    o_sl_dv_dk.pack(side="left")

    def khi_bam_them_dv_vao_phieu():
        ma_dk = o_ma_dk_dv.get()
        vi_tri_dv = o_chon_dv_dk.current()
        if vi_tri_dv < 0:
            messagebox.showwarning("Thiếu dữ liệu", "Chọn dịch vụ trước!")
            return
        ma_dv = danh_sach_dv_dk[vi_tri_dv][0]
        so_luong = int(o_sl_dv_dk.get())
        ok, thong_bao = db.them_su_dung_dv(ma_dk, ma_dv, so_luong)
        messagebox.showinfo("Thông báo", thong_bao) if ok else messagebox.showerror("Lỗi", thong_bao)

    tk.Button(tab_dk, text="Thêm dịch vụ vào phiếu", command=khi_bam_them_dv_vao_phieu,
              bg="#3498DB", fg="white", relief="flat").pack(pady=5)

    def khi_bam_thanh_toan():
        s = bang_dk.selection()
        if not s:
            messagebox.showwarning("Chưa chọn", "Chọn phiếu trong bảng!")
            return
        ma_dk = bang_dk.item(s[0], "values")[0]
        ok, thong_bao = db.thanh_toan(ma_dk)
        messagebox.showinfo("Thông báo", thong_bao) if ok else messagebox.showerror("Lỗi", thong_bao)
        lam_moi_bang_dk()

    tk.Button(tab_dk, text=" Đăng ký", command= khi_bam_dang_ky).pack()
    tk.Button(tab_dk, text=" Thanh toán (chọn dòng trong bảng trước)", command=khi_bam_thanh_toan).pack()
    lam_moi_bang_dk()

    # ========== TAB ĐIỂM DANH ==========

    tab_dd = ttk.Frame(notebook)
    notebook.add(tab_dd, text=" Điểm danh")

    tk.Label(tab_dd, text=" Nhập mã phiếu đăng ký: ").pack()
    o_ma_dk_dd = ttk.Entry(tab_dd)
    o_ma_dk_dd.pack()

    bang_dd = ttk.Treeview(tab_dd, columns = ("ID", "DK", "TG"), show="headings")
    bang_dd.heading("ID", text="STT")
    bang_dd.heading("DK", text="Mã DK")
    bang_dd.heading("TG", text="Thời gian")
    bang_dd.pack(fill="both", expand = True)

    def lam_moi_bang_dd():
        for dong in bang_dd.get_children():
            bang_dd.delete(dong)
        for dd in db.ds_diem_danh():
            bang_dd.insert("", "end", values= dd)

    def khi_bam_diem_danh():
        ma_dk = o_ma_dk_dd.get()
        ok, thong_bao = db.diem_danh(ma_dk)
        messagebox.showinfo("Thông báo", thong_bao) if ok else messagebox.showerror("Lỗi", thong_bao)
        lam_moi_bang_dd()

    tk.Button(tab_dd, text=" Điểm danh", command= khi_bam_diem_danh).pack()
    lam_moi_bang_dd()

    # ========== TAB THỐNG KÊ ==========

    tab_tk = ttk.Frame(notebook)
    notebook.add(tab_tk, text=" Hóa đơn & thống kê")

    nhan_tong_quan = tk.Label(tab_tk, text="")
    nhan_tong_quan.pack()

    bang_hd = ttk.Treeview(tab_tk, columns = ("Ma", "DK", "Ngay", "Gia", "DV", "Tong"), show="headings")
    bang_hd.heading("Ma", text="Mã HĐ")
    bang_hd.heading("DK", text=" Mã ĐK")
    bang_hd.heading("Ngay", text="Ngày Lập")
    bang_hd.heading("Gia", text="Tiền Gói")
    bang_hd.heading("DV", text="Tiền DV")
    bang_hd.heading("Tong", text=" Tổng")
    bang_hd.pack(fill="both", expand = True)

    def lam_moi_thong_ke():
        so_hv = len(db.ds_hv())
        nhan_tong_quan.config(text=f" Tổng số hội viên:: {so_hv}")
        for dong in bang_hd.get_children():
            bang_hd.delete(dong)
        for hd in db.ds_hoa_don():
            bang_hd.insert("", "end", values=hd)

    tk.Button(tab_tk, text="Làm mới thống kê", command=lam_moi_thong_ke).pack()
    lam_moi_thong_ke()

    # ========== TAB NHẬT KÝ THAY ĐỔI ==========

    tab_nk = ttk.Frame(notebook)
    notebook.add(tab_nk, text=" Nhật ký thay đổi")

    bang_nk = ttk.Treeview(tab_nk, columns=("ID", "TG", "ND", "HD", "CT"), show="headings")
    bang_nk.heading("ID", text="STT")
    bang_nk.heading("TG", text="Thời gian")
    bang_nk.heading("ND", text="Người dùng")
    bang_nk.heading("HD", text="Hành động")
    bang_nk.heading("CT", text="Chi tiết")
    bang_nk.pack(fill="both", expand = True)

    def lam_moi_bang_nk():
        for dong in bang_nk.get_children():
            bang_nk.delete(dong)
        for nk in db.ds_nhat_ky():
            bang_nk.insert("", "end", values=nk)

    tk.Button(tab_nk, text= "Làm mới", command=lam_moi_bang_nk).pack()
    lam_moi_bang_nk()

    Cua_So.mainloop()
Cua_So_Dang_Nhap.mainloop()