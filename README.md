# Gate Entrance Using Face

Proyek ini bertujuan untuk membuat sistem gerbang masuk yang menggunakan pengenalan wajah (*face recognition*) untuk memberikan akses kepada wajah yang dikenali/telah terdaftar.

Catatan: Proyek dibuat yang merupakan versi pengembangan dari [Mjrovai](https://github.com/Mjrovai/OpenCV-Face-Recognition) project.

## Requirements

- Device yang memiliki modul kamera (Laptop/PC/Raspberry Pi)
- Python 3
- OpenCV
- numpy
- pillow
- pyfiglet
- halo

## Installation

1. Clone repository.
2. Pastikan Python 3 sudah terinstall.
3. Install semua library yang diperlukan menggunakan pip

    `pip3 install -r requirements.txt`

## Usage

1. Daftarkan wajah yang akan dikenali dengan cara menjalankan script `pendaftaran.py` dan mengikuti instruksi yang diberikan.

    `python3 pendaftaran.py`
2. Untuk memulai simulasi sistem gerbang masuk, jalankan script `start.py`.

    `python3 start.py`
3. Jika ingin menghapus semua data wajah yang telah terdaftar, jalankan script `reset_data.py`.

    `python3 reset_data.py`

## Troubleshooting

- Jika terjadi error saat melakukan pendaftaran, lihat pada folder database dan pastikan gambar yang diambil apakah terbalik atau tidak, jika iya tambahkan kode berikut pada baris ke-12 di file `pendaftaran.py` dan file `start.py`.

    ```python
    img = cv2.flip(img, -1) # flip video image vertically
    ```
    setelah itu reset data dan lakukan pendaftaran ulang. 

## Conclusion

Project ini berguna untuk mempermudah dalam mengakses suatu tempat yang membutuhkan autentikasi seperti pada gerbang masuk KAI dll.