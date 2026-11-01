# Terminal Tetris

Permainan Tetris berbasis terminal yang dibuat dengan Python dan library `curses`.
Pemain dapat menggerakkan dan memutar balok, mengumpulkan skor, mengubah mode warna,
serta menyimpan skor tertinggi secara lokal.

## Persyaratan

- Python 3.8 atau lebih baru
- Terminal dengan ukuran minimal 38 kolom dan 27 baris
- Dukungan Unicode dan warna terminal

## Instalasi

### Windows

Buka terminal, masuk ke folder project, lalu jalankan:

```
python -m pip install windows-curses
```
```
python start_game.py
```

### Linux dan macOS
```
python3 tetris.py
```
Jika perintah `python` tidak tersedia, gunakan `python3`.

## Cara Bermain

Balok akan jatuh secara otomatis. Susun balok agar membentuk satu baris penuh untuk menghapusnya.
Setiap baris yang berhasil dihapus memberikan 100 poin.
Skor tertinggi disimpan otomatis dalam file `high_score.txt`.

| Tombol | Fungsi |
| --- | --- |
| Panah kiri | Pindah ke kiri |
| Panah kanan | Pindah ke kanan |
| Panah atas | Memutar balok |
| Panah bawah | Menurunkan balok lebih cepat |
| Spasi | Menjatuhkan balok langsung ke bawah |
| C | Mengaktifkan dan menonaktifkan warna |
| ESC | Membuka menu pause |
| Q | Keluar dari permainan |

## Menjalankan Pengujian

```
python -m unittest discover -s tests -v
```

## Struktur Project

terminal-tetris/
├── tetris.py       # Entry point aplikasi
├── game.py         # Loop utama permainan
├── game_logic.py   # Aturan dan perhitungan permainan
├── ui.py           # Tampilan dan interaksi curses
├── config.py       # Konfigurasi papan dan bentuk blok
├── high_score.txt  # Penyimpanan skor tertinggi
└── tests/
    └── test_game_logic.py
