# Sketch-Drawing
tugas 2 grafika komputer 2025
plikasi menggambar desktop sederhana yang dibangun menggunakan Python dan Tkinter. Aplikasi ini memungkinkan pengguna untuk menggambar berbagai bentuk, memilih warna, mengatur ukuran kuas, dan memiliki fitur undo/redo.

Fitur
Mode Menggambar:

Titik: Menggambar titik tunggal.

Titik Bersambung: Menggambar garis bebas dengan menyeret mouse.

Garis: Menggambar garis lurus dari titik awal ke titik akhir.

Persegi: Menggambar persegi atau persegi panjang.

Lingkaran: Menggambar lingkaran.

Elips: Menggambar elips.

Penghapus: Menghapus bagian gambar dengan menyeret.

Pemilihan Warna: Pilih warna untuk menggambar.

Ukuran Kuas: Atur ketebalan kuas atau garis menggunakan slider.

Isi Bentuk: Opsi untuk mengisi bentuk (persegi, lingkaran, elips) dengan warna yang dipilih.

Undo/Redo: Batalkan atau ulangi aksi menggambar terakhir.

Bersihkan: Hapus semua gambar dari kanvas.

Persyaratan
Python 3.x (Tkinter sudah termasuk dalam instalasi standar Python)

Cara Menjalankan Aplikasi
Pastikan Python terinstal di sistem Anda.

Salin kode aplikasi dari Canvas ini ke dalam sebuah file .py (misalnya, sketchpad.py).

Buka Command Prompt atau Terminal Anda.

Navigasi ke direktori tempat Anda menyimpan file sketchpad.py.

cd <jalur_direktori_anda>


Jalankan aplikasi dengan perintah:

python sketchpad.py


Cara Penggunaan
Pilih Mode: Gunakan dropdown "Mode" di toolbar untuk memilih jenis bentuk yang akan digambar (Titik, Garis, Persegi, dll.).

Pilih Warna: Klik pada tombol kotak warna untuk membuka pemilih warna.

Atur Ukuran Kuas: Geser slider "Ukuran" untuk mengubah ketebalan goresan.

Isi Bentuk: Centang kotak "Isi Bentuk" untuk mengisi bentuk geometris dengan warna saat menggambar.

Menggambar:

Untuk Titik dan Titik Bersambung, klik dan seret mouse di kanvas.

Untuk Garis, Persegi, Lingkaran, Elips, klik di titik awal, seret ke titik akhir yang diinginkan, lalu lepas mouse.

Undo/Redo: Gunakan tombol "Undo" dan "Redo" di toolbar.

Bersihkan Kanvas: Klik tombol "Bersihkan" untuk menghapus semua gambar.

Catatan Penting untuk itch.io
Aplikasi ini adalah aplikasi desktop yang dibuat dengan Tkinter. Untuk mengunggahnya ke itch.io, Anda biasanya perlu:

Mengkompilasinya menjadi executable (misalnya, file .exe untuk Windows) menggunakan alat seperti PyInstaller.

Mengunggah file executable tersebut ke itch.io.

Aplikasi ini tidak dapat dijalankan langsung di peramban web melalui HTML. Jika Anda ingin aplikasi menggambar yang dapat dimainkan langsung di browser, Anda harus membangunnya menggunakan teknologi web (HTML, CSS, dan JavaScript)
