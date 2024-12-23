import streamlit as st
import pandas as pd
import random
import time
import matplotlib.pyplot as plt

# Daftar nama Karyawan
nama_Karyawan = [
    "Rosa", "Annissa", "Ocha", "Issa", "Diana", "Imel", "Michel", "Hadi", "Indah", "Joko",
    "Kurnia", "Lia", "Maya", "Nina", "Oka", "Putra", "Qori", "Rini", "Sinta", "Tari",
    "Umar", "Vina", "Wulan", "Yusuf", "Zahra"
]

# Fungsi iteratif untuk menghitung total penghasilan
@st.cache
def hitung_iteratif(data):
    total_penghasilan = 0
    for index, row in data.iterrows():
        total_penghasilan += row['Gaji_Pokok'] + row['Tunjangan'] + row['Bonus'] - row['Potongan']
    return total_penghasilan

# Fungsi rekursif untuk menghitung total penghasilan
def hitung_rekursif(data, index=0):
    if index == len(data):
        return 0
    row = data.iloc[index]
    return (row['Gaji_Pokok'] + row['Tunjangan'] + row['Bonus'] - row['Potongan']) + hitung_rekursif(data, index + 1)

# Simulasi data karyawan
def generate_data(jumlah):
    data = {
        "Nama": [random.choice(nama_orang_indonesia) for _ in range(jumlah)],
        "Gaji_Pokok": [random.randint(2000000, 10000000) for _ in range(jumlah)],
        "Tunjangan": [random.randint(500000, 3000000) for _ in range(jumlah)],
        "Bonus": [random.randint(0, 2000000) for _ in range(jumlah)],
        "Potongan": [random.randint(0, 1000000) for _ in range(jumlah)],
    }
    return pd.DataFrame(data)

# Streamlit antarmuka utama
st.title("Penghitungan Penghasilan Bulanan Karyawan")

# Jumlah karyawan tetap 400
jumlah_karyawan = 400

# Inisialisasi data karyawan
data_karyawan = generate_data(jumlah_karyawan)

# Hitung total penghasilan iteratif
start_time_iterative = time.time()
total_iterative = hitung_iteratif(data_karyawan)
iterative_time = time.time() - start_time_iterative

# Hitung total penghasilan rekursif
start_time_recursive = time.time()
total_recursive = hitung_rekursif(data_karyawan)
recursive_time = time.time() - start_time_recursive

# Menentukan penghasilan tertinggi
max_penghasilan = data_karyawan.apply(
    lambda row: row['Gaji_Pokok'] + row['Tunjangan'] + row['Bonus'] - row['Potongan'], axis=1
)
max_index = max_penghasilan.idxmax()
max_nama = data_karyawan.iloc[max_index]['Nama']
max_value = max_penghasilan[max_index]

# Tampilkan hasil
st.write("### Hasil Perhitungan")
st.write(f"Total Penghasilan (Iteratif): {total_iterative:,}")
st.write(f"Waktu Eksekusi (Iteratif): {iterative_time:.6f} detik")
st.write(f"Total Penghasilan (Rekursif): {total_recursive:,}")
st.write(f"Waktu Eksekusi (Rekursif): {recursive_time:.6f} detik")

st.write("### Penghasilan Tertinggi")
st.write(f"Nama: {max_nama}, Penghasilan Tertinggi: {max_value:,}")

# Tampilkan tabel data
st.write("### Data Karyawan")
st.dataframe(data_karyawan)

# Membuat grafik perbandingan waktu eksekusi
n_values = range(100, jumlah_karyawan + 1, 100)
iterative_times = []
recursive_times = []

for n in n_values:
    data_sample = generate_data(n)

    start_time_iter = time.time()
    hitung_iteratif(data_sample)
    iterative_times.append(time.time() - start_time_iter)

    start_time_rec = time.time()
    hitung_rekursif(data_sample)
    recursive_times.append(time.time() - start_time_rec)

# Plot grafik
fig, ax = plt.subplots()
ax.plot(n_values, iterative_times, marker='o', label='Iteratif', color='blue')
ax.plot(n_values, recursive_times, marker='o', label='Rekursif', color='red')
ax.set_xlabel("Nilai n")
ax.set_ylabel("Waktu Eksekusi (detik)")
ax.set_title("Perbandingan Waktu Eksekusi Iteratif vs Rekursif")
ax.legend()
st.pyplot(fig)
