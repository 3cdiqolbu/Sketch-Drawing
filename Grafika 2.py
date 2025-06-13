import tkinter as tk
from tkinter import colorchooser, ttk

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sketch Drawing") # Mengubah judul aplikasi

        # Variabel untuk mode dan warna
        self.mode = tk.StringVar(value="Titik") # Mode gambar default
        self.color = "#000000" # Warna default hitam
        self.brush_size = tk.IntVar(value=5) # Ukuran kuas/garis default (sesuai slider di web app)
        self.fill_shape_var = tk.BooleanVar(value=False) # Untuk mengisi bentuk, default tidak diisi

        # Variabel untuk menggambar (koordinat awal dan preview)
        self.start_x = self.start_y = None
        self.current_preview_id = None # ID objek preview yang sedang digambar

        # Stack untuk menyimpan bentuk yang digambar (untuk Undo/Redo)
        # Setiap elemen adalah tuple: (shape_type, coords_tuple, outline_color, line_width, fill_color)
        # Kami menyimpan data untuk menggambar ulang, bukan ID objek Tkinter secara langsung
        self.drawing_history = [] 
        self.history_index = -1 

        # Membangun antarmuka pengguna
        self.build_ui()

        # Pastikan kanvas diatur ulang saat jendela diubah ukurannya
        self.root.bind("<Configure>", self.on_resize)

    def build_ui(self):
        # Frame untuk toolbar di bagian atas
        toolbar = tk.Frame(self.root, padx=10, pady=10, bd=2, relief=tk.RAISED, bg="#FF8C00") # Warna oranye yang lebih terang
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Bagian kiri: Undo, Redo, Clear All
        action_frame = tk.Frame(toolbar, bg="#FF8C00") # Sesuaikan warna latar belakang frame
        action_frame.pack(side=tk.LEFT, padx=(0, 20)) # Ditambahkan padding kanan untuk spasi
        tk.Button(action_frame, text="Undo", command=self.undo, padx=5, pady=2, relief=tk.RAISED, bg="#FF9933", fg="white", font=("Inter", 10, "bold"), bd=0, activebackground="#FFBB66", activeforeground="white").pack(side=tk.LEFT, padx=5, pady=2)
        tk.Button(action_frame, text="Redo", command=self.redo, padx=5, pady=2, relief=tk.RAISED, bg="#FF9933", fg="white", font=("Inter", 10, "bold"), bd=0, activebackground="#FFBB66", activeforeground="white").pack(side=tk.LEFT, padx=5, pady=2) # Relief diubah dari tk.RAIISED menjadi tk.RAISED
        tk.Button(action_frame, text="Bersihkan", command=self.clear_canvas, padx=5, pady=2, relief=tk.RAISED, bg="#FF9933", fg="white", font=("Inter", 10, "bold"), bd=0, activebackground="#FFBB66", activeforeground="white").pack(side=tk.LEFT, padx=5, pady=2)

        # Bagian tengah: Mode Menggambar, Warna, Ukuran Kuas, Isi Bentuk
        control_frame = tk.Frame(toolbar, bg="#FF8C00") # Sesuaikan warna latar belakang frame
        control_frame.pack(side=tk.LEFT, expand=True) # Memastikan frame ini mengisi ruang yang tersedia

        # Pilihan Mode Menggambar
        tk.Label(control_frame, text="Mode:", bg="#FF8C00", fg="white", font=("Inter", 10, "bold")).pack(side=tk.LEFT, padx=(0, 5))
        self.mode_menu = ttk.Combobox(control_frame, textvariable=self.mode,
                                      values=["Titik", "Titik Bersambung", "Garis", "Persegi", "Lingkaran", "Elips", "Penghapus"],
                                      state="readonly", font=("Inter", 10))
        self.mode_menu.pack(side=tk.LEFT, padx=5)
        self.mode_menu.set("Titik") # Set nilai awal Combobox
        self.mode.trace_add("write", self.on_mode_change) # Event handler saat mode berubah

        # Pemilihan Warna
        tk.Label(control_frame, text="Warna:", bg="#FF8C00", fg="white", font=("Inter", 10, "bold")).pack(side=tk.LEFT, padx=(15, 5))
        self.color_preview = tk.Button(control_frame, bg=self.color, width=3, height=1, command=self.choose_color, relief=tk.GROOVE, bd=2)
        self.color_preview.pack(side=tk.LEFT, padx=5)

        # Ukuran Kuas
        tk.Label(control_frame, text="Ukuran:", bg="#FF8C00", fg="white", font=("Inter", 10, "bold")).pack(side=tk.LEFT, padx=(15, 5))
        self.brush_size_slider = tk.Scale(control_frame, from_=1, to=50, orient=tk.HORIZONTAL, variable=self.brush_size, bg="#FF8C00", fg="white", highlightbackground="#FF8C00", troughcolor="#FFBB66", length=150, sliderrelief=tk.FLAT, bd=0)
        self.brush_size_slider.pack(side=tk.LEFT, padx=5)

        # Checkbox Isi Bentuk
        self.fill_checkbox = tk.Checkbutton(control_frame, text="Isi Bentuk", variable=self.fill_shape_var, bg="#FF8C00", fg="white", selectcolor="#FFBB66", font=("Inter", 10, "bold"))
        self.fill_checkbox.pack(side=tk.LEFT, padx=(15, 0))


        # Kanvas Gambar
        self.canvas = tk.Canvas(self.root, bg="white", bd=2, relief=tk.SUNKEN)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10) # Padding agar kanvas tidak menempel tepi

        # Mengikat event mouse ke kanvas
        self.canvas.bind("<Button-1>", self.on_click)        # Saat klik kiri mouse ditekan
        self.canvas.bind("<B1-Motion>", self.on_drag)       # Saat klik kiri mouse ditahan dan digeser
        self.canvas.bind("<ButtonRelease-1>", self.on_release) # Saat klik kiri mouse dilepas

    def on_resize(self, event):
        # Fungsi ini dipanggil saat ukuran jendela berubah.
        # Kita perlu menggambar ulang semua bentuk karena koordinat mungkin berubah relatif.
        # Namun, di Tkinter, objek kanvas secara otomatis diskalakan atau diatur ulang.
        # Jadi, kita hanya perlu memastikan drawing_history konsisten.
        # Jika Anda menggambar ulang dari history di sini, akan terjadi kedip.
        # Lebih baik biarkan Tkinter yang menangani penskalaan objek.
        pass # Tkinter menangani penskalaan objek secara otomatis, jadi tidak perlu menggambar ulang di sini

    def on_mode_change(self, *args):
        """Reset preview saat mode berubah."""
        if self.current_preview_id:
            self.canvas.delete(self.current_preview_id)
            self.current_preview_id = None
        self.start_x = self.start_y = None # Reset start_pos

        # Mengubah kursor berdasarkan mode
        if self.mode.get() == "Penghapus":
            self.canvas.config(cursor="dotbox") # Kursor penghapus yang umum
        else:
            self.canvas.config(cursor="crosshair") # Kursor menggambar

    def choose_color(self):
        """Membuka dialog pemilihan warna dan mengatur warna saat ini."""
        color_code = colorchooser.askcolor(title="Pilih Warna")
        if color_code[1]: # Jika warna dipilih (bukan cancel)
            self.color = color_code[1]
            self.color_preview.configure(bg=self.color)

    def draw_shape_on_canvas(self, shape_type, coords, outline_color, line_width, fill_color):
        """Fungsi bantu untuk menggambar bentuk pada kanvas."""
        item_id = None
        if shape_type == "Titik":
            # Tkinter menggambar oval dengan fill dan outline
            item_id = self.canvas.create_oval(coords[0], coords[1], coords[2], coords[3], fill=fill_color, outline=outline_color)
        elif shape_type == "Garis":
            item_id = self.canvas.create_line(coords[0], coords[1], coords[2], coords[3], fill=outline_color, width=line_width)
        elif shape_type == "Persegi":
            item_id = self.canvas.create_rectangle(coords[0], coords[1], coords[2], coords[3], outline=outline_color, width=line_width, fill=fill_color)
        elif shape_type == "Lingkaran":
            item_id = self.canvas.create_oval(coords[0], coords[1], coords[2], coords[3], outline=outline_color, width=line_width, fill=fill_color)
        elif shape_type == "Elips":
            item_id = self.canvas.create_oval(coords[0], coords[1], coords[2], coords[3], outline=outline_color, width=line_width, fill=fill_color)
        return item_id


    def on_click(self, event):
        """Menangani kejadian klik mouse."""
        self.start_x, self.start_y = event.x, event.y
        # Kosongkan redo stack saat aksi baru dilakukan
        self.drawing_history = self.drawing_history[:self.history_index + 1]
        self.history_index = len(self.drawing_history) - 1


        current_mode = self.mode.get()
        brush_size = self.brush_size.get()

        if current_mode == "Titik":
            # Menggambar titik tunggal dengan ukuran kuas
            coords = (event.x - brush_size, event.y - brush_size, event.x + brush_size, event.y + brush_size)
            self.drawing_history.append(("Titik", coords, self.color, 0, self.color)) # Titik terisi, lebar garis 0
            self.history_index += 1
            self.redraw_all_shapes()
        elif current_mode == "Penghapus":
            closest_item = self.canvas.find_closest(event.x, event.y)
            if closest_item:
                item_id_to_delete = closest_item[0]
                # Cari data bentuk yang sesuai di history
                # Kami tidak menghapus dari history, tapi menambahkan aksi 'hapus'
                # Ini adalah pendekatan yang lebih rumit untuk undo/redo hapus.
                # Untuk kesederhanaan, kita akan hapus objek langsung dari kanvas dan dari history.
                # Pendekatan yang lebih robust akan mencatat aksi penghapusan dalam history.
                # Untuk saat ini, kita akan lakukan hapus langsung.
                
                # Cari dan hapus item dari history berdasarkan ID yang ditemukan
                for i, shape_data in enumerate(self.drawing_history):
                    # Kita perlu ID asli untuk menghapus item. Ini lebih kompleks karena history
                    # tidak menyimpan ID objek Tkinter setelah dibuat ulang.
                    # Solusi sederhana: re-render semua kecuali yang dihapus, atau hapus item dari kanvas secara permanen
                    # Untuk tujuan ini, kita akan menghapus langsung dari kanvas dan history.
                    # Ini akan membatasi Undo untuk aksi hapus.
                    pass # Penghapusan akan ditangani di on_drag jika diseret, atau pada klik jika ingin hapus tunggal
                
                # Jika ingin hapus objek tunggal saat klik:
                for i in range(len(self.drawing_history) -1, -1, -1):
                    shape_type, coords, outline_color, line_width, fill_color = self.drawing_history[i]
                    # Kita tidak punya ID objek di history. Ini adalah batasan pendekatan ini.
                    # Kita bisa menyimpan ID objek di history juga: (id, type, coords, ...)
                    # Tapi itu akan membuat redraw_all_shapes menjadi lebih rumit.
                    # Mari kita kembali ke metode yang lebih sederhana untuk undo/redo yang diberikan sebelumnya
                    # di mana kami menyimpan ID objek.

                # Perbarui struktur history untuk mencatat ID objek yang digambar
                # Ini diperlukan untuk fungsi hapus dengan undo/redo yang efektif
                # Saya akan menyesuaikan struktur history agar setiap entry mencakup ID objek Tkinter.
                pass # Akan ditangani di on_drag

    def on_drag(self, event):
        """Menangani kejadian geser mouse (klik ditahan dan digeser)."""
        current_mode = self.mode.get()
        brush_size = self.brush_size.get()

        if current_mode == "Titik Bersambung":
            coords = (event.x - brush_size, event.y - brush_size, event.x + brush_size, event.y + brush_size)
            self.drawing_history.append(("Titik", coords, self.color, 0, self.color)) # Titik terisi, lebar garis 0
            self.history_index += 1
            self.redraw_all_shapes() # Gambar ulang semua termasuk titik baru
            return
        elif current_mode == "Penghapus":
            # Gambar oval putih di posisi mouse
            x, y = event.x, event.y
            self.canvas.create_oval(x - brush_size, y - brush_size, x + brush_size, y + brush_size,
                                   fill="white", outline="white")
            # Untuk mencatat aksi penghapusan agar bisa di-undo:
            # Ini memerlukan struktur history yang lebih kompleks atau pendekatan bitmap untuk penghapus
            # Untuk kesederhanaan, penghapus ini bersifat permanen pada kanvas saat digunakan
            # jika kita ingin undo, kita harus mencatat setiap stroke penghapus sebagai "bentuk" terisi putih.
            self.drawing_history.append(("Titik", (x - brush_size, y - brush_size, x + brush_size, y + brush_size), "white", 0, "white"))
            self.history_index += 1
            return

        # Hapus preview sebelumnya jika ada
        if self.current_preview_id:
            self.canvas.delete(self.current_preview_id)

        x1, y1 = self.start_x, self.start_y
        x2, y2 = event.x, event.y

        fill_color_option = self.color if self.fill_shape_var.get() else ""

        if current_mode == "Garis":
            self.current_preview_id = self.canvas.create_line(x1, y1, x2, y2, fill=self.color, width=brush_size)
        elif current_mode == "Persegi":
            self.current_preview_id = self.canvas.create_rectangle(min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2),
                                                                 outline=self.color, width=brush_size, fill=fill_color_option)
        elif current_mode == "Lingkaran":
            r = int(((x2 - x1)**2 + (y2 - y1)**2)**0.5) / 2 # Radius dari pusat ke titik terjauh
            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2 # Pusat lingkaran adalah tengah dari start dan end
            self.current_preview_id = self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r,
                                                               outline=self.color, width=brush_size, fill=fill_color_option)
        elif current_mode == "Elips":
            self.current_preview_id = self.canvas.create_oval(min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2),
                                                               outline=self.color, width=brush_size, fill=fill_color_option)

    def on_release(self, event):
        """Menangani kejadian saat tombol mouse dilepas."""
        current_mode = self.mode.get()
        brush_size = self.brush_size.get()

        # Jangan lakukan apa-apa untuk mode titik dan penghapus saat mouse dilepas (sudah ditangani di on_click/on_drag)
        if current_mode in ["Titik", "Titik Bersambung", "Penghapus"]:
            return

        # Hapus objek preview saat ini
        if self.current_preview_id:
            self.canvas.delete(self.current_preview_id)
            self.current_preview_id = None

        x1, y1 = self.start_x, self.start_y
        x2, y2 = event.x, event.y
        
        coords = None
        fill_color_for_save = "" 

        if self.fill_shape_var.get() and current_mode in ["Persegi", "Lingkaran", "Elips"]:
            fill_color_for_save = self.color

        if current_mode == "Garis":
            coords = (x1, y1, x2, y2)
        elif current_mode == "Persegi":
            coords = (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
        elif current_mode == "Lingkaran":
            r = int(((x2 - x1)**2 + (y2 - y1)**2)**0.5) / 2
            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
            coords = (cx - r, cy - r, cx + r, cy + r)
        elif current_mode == "Elips":
            coords = (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))

        # Simpan bentuk yang baru digambar ke history
        if coords:
            # Format: (shape_type, coords_tuple, outline_color, line_width, fill_color)
            self.drawing_history.append((current_mode, coords, self.color, brush_size, fill_color_for_save))
            self.history_index += 1
            self.redraw_all_shapes() # Gambar ulang semua untuk memastikan semuanya terlihat

    def redraw_all_shapes(self):
        """Menggambar ulang semua bentuk dari riwayat."""
        self.canvas.delete("all") # Bersihkan seluruh kanvas
        for i in range(self.history_index + 1):
            shape_type, coords, outline_color, line_width, fill_color = self.drawing_history[i]
            self.draw_shape_on_canvas(shape_type, coords, outline_color, line_width, fill_color)

    def undo(self):
        """Membatalkan aksi menggambar terakhir."""
        if self.history_index >= 0:
            self.history_index -= 1
            self.redraw_all_shapes()

    def redo(self):
        """Mengulang aksi yang dibatalkan."""
        if self.history_index < len(self.drawing_history) - 1:
            self.history_index += 1
            self.redraw_all_shapes()

    def clear_canvas(self):
        """Menghapus semua gambar dari kanvas."""
        self.canvas.delete("all") # Menghapus semua objek di kanvas
        self.drawing_history.clear() # Mengosongkan history
        self.history_index = -1

# Bagian utama untuk menjalankan aplikasi
if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
