import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set konfigurasi halaman
st.set_page_config(
    page_title='Bike Sharing Dashboard',
    page_icon='🚲',
)

# Fungsi untuk membaca data
@st.cache_data
def get_bike_data():
    """
    Membaca data bike sharing dari file CSV.
    Menggunakan caching untuk menghindari pembacaan berulang.
    """
    bike_df = pd.read_csv(r'C:\Users\ASUS\Documents\KULIAH\MBKM\BANGKIT 2024\Submission2\Dashboard\filtered_bike_data.csv')
    return bike_df

# Membaca data
bike_df = get_bike_data()

# Judul dan deskripsi
'''
# 🚲 Bike Sharing Dashboard

Melihat data peminjaman sepeda berdasarkan berbagai faktor seperti musim, 
cuaca, dan jenis hari (kerja/libur). Data mencakup informasi peminjaman 
harian dengan berbagai variabel yang mempengaruhi jumlah peminjaman.
'''

# Tambahkan spasi
''

# Filter sidebar
st.sidebar.title("Filter Data")

# Filter musim
seasons = bike_df['season'].unique()
selected_seasons = st.sidebar.multiselect(
    'Pilih Musim',
    seasons,
    default=seasons
)

# Filter cuaca
weather_conditions = bike_df['weathersit'].unique()
selected_weather = st.sidebar.multiselect(
    'Pilih Kondisi Cuaca',
    weather_conditions,
    default=weather_conditions
)

# Filter hari kerja
workingday_options = bike_df['workingday'].unique()
selected_workingday = st.sidebar.multiselect(
    'Pilih Jenis Hari',
    workingday_options,
    default=workingday_options
)

# Filter data berdasarkan pilihan
filtered_df = bike_df[
    (bike_df['season'].isin(selected_seasons)) &
    (bike_df['weathersit'].isin(selected_weather)) &
    (bike_df['workingday'].isin(selected_workingday))
]

# Tampilkan visualisasi

st.header('Peminjaman Sepeda berdasarkan Waktu', divider='gray')
''

# 1. Time series plot
daily_rentals = filtered_df.groupby('dteday')['cnt'].mean().reset_index()
st.line_chart(
    daily_rentals,
    x='dteday',
    y='cnt'
)

# Tambahkan insight untuk time series
st.write("""
### Insight Tren Waktu:
- Terdapat pola musiman yang jelas dalam peminjaman sepeda sepanjang tahun
- Jumlah peminjaman mencapai puncaknya selama bulan-bulan liburan
- Terlihat tren kenaikan secara keseluruhan, yang mungkin mengindikasikan pertumbuhan popularitas layanan
""")

''

st.header('Analisis berdasarkan Faktor', divider='gray')
''

# Buat layout kolom
col1, col2 = st.columns(2)

with col1:
    # 2. Bar plot musim
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.barplot(y='season', x='cnt', data=filtered_df, orient='h', ax=ax1)
    ax1.set_title('Rata-rata Peminjaman per Musim')
    ax1.set_ylabel('Musim')
    ax1.set_xlabel('Jumlah Peminjaman')
    st.pyplot(fig1)
    
    # Insight untuk musim
    st.write("""
    ### Insight Musim:
    Ada kecenderungan peningkatan dari Musim 2 ke Musim 3, yang mungkin mencerminkan pengaruh cuaca yang lebih baik di musim-musim tersebut untuk bersepeda. Penurunan di Musim 1 bisa menunjukkan bahwa musim tersebut berada di kondisi yang kurang mendukung.
    """)

with col2:
    # 3. Bar plot cuaca
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.barplot(y='weathersit', x='cnt', data=filtered_df, orient='h', ax=ax2)
    ax2.set_title('Rata-rata Peminjaman per Kondisi Cuaca')
    ax2.set_ylabel('Kondisi Cuaca')
    ax2.set_xlabel('Jumlah Peminjaman')
    st.pyplot(fig2)
    
    # Insight untuk cuaca
    st.write("""
    ### Insight Cuaca:
    - Kondisi cuaca memiliki korelasi langsung dengan jumlah peminjaman sepeda
    - Terdapat hubungan yang kuat antara kondisi cuaca dan jumlah peminjaman sepeda, di mana cuaca yang lebih baik (kondisi 1 dan 2) mendorong lebih banyak peminjaman.
    - Peminjaman menurun drastis pada kondisi cuaca yang lebih buruk (kondisi 3 dan 4), menunjukkan bahwa faktor cuaca memainkan peran penting dalam keputusan masyarakat untuk bersepeda.
    - Pemahaman tentang dampak cuaca dapat membantu dalam perencanaan inventaris dan maintenance
    """)

''

st.header('Hasil Analisis', divider='gray')
''

# Tampilkan metrik
cols = st.columns(4)

# Metrik 1: Total peminjaman
total_rentals = filtered_df['cnt'].sum()
cols[0].metric(
    label="Total Peminjaman",
    value=f"{total_rentals:,.0f}"
)

# Metrik 2: Rata-rata peminjaman per hari
avg_daily_rentals = filtered_df['cnt'].mean()
cols[1].metric(
    label="Rata-rata Harian",
    value=f"{avg_daily_rentals:.0f}"
)

# Metrik 3: Peminjaman tertinggi
max_rentals = filtered_df['cnt'].max()
cols[2].metric(
    label="Peminjaman Tertinggi",
    value=f"{max_rentals:,.0f}"
)

# Metrik 4: Persentase hari kerja
workingday_percent = (filtered_df['workingday'] == 1).mean() * 100
cols[3].metric(
    label="Persentase Hari Kerja",
    value=f"{workingday_percent:.1f}%"
)

# Insight untuk metrik
st.write("""
### Insight Metrik Utama:
- Total peminjaman yang tinggi menunjukkan layanan yang baik dari bike sharing
- Rata-rata harian memberikan gambaran tentang kapasitas yang dibutuhkan untuk operasi normal
- Peminjaman tertinggi bisa menjadi acuan untuk perencanaan kapasitas maksimum
- Persentase hari kerja vs akhir pekan membantu memahami pola penggunaan mingguan
""")

# Tambahkan heatmap di bagian bawah
st.header('Interaksi Musim dan Cuaca', divider='gray')
''

# 4. Heatmap
season_weather_pivot = pd.pivot_table(
    filtered_df, 
    values='cnt', 
    index='season', 
    columns='weathersit', 
    aggfunc='mean'
)
fig4, ax4 = plt.subplots(figsize=(10, 6))
sns.heatmap(season_weather_pivot, annot=True, fmt='.0f', cmap='YlOrRd', ax=ax4)
ax4.set_title('Heatmap Rata-rata Peminjaman: Musim vs Cuaca')
st.pyplot(fig4)

# Insight untuk heatmap
st.write("""
### Insight Interaksi Musim dan Cuaca:
- Terdapat pola yang jelas dalam interaksi antara musim dan kondisi cuaca
- Cuaca memiliki dampak signifikan terhadap jumlah peminjaman di semua musim. Cuaca yang baik (cuaca 1 dan 2) selalu terkait dengan angka peminjaman yang lebih tinggi, terutama pada musim 3.
- Musim 3 adalah musim dengan performa tertinggi secara keseluruhan, terlepas dari cuacanya, yang mengindikasikan kondisi yang paling mendukung untuk aktivitas bersepeda.
""")


st.header('Analisis Pola Harian', divider='gray')
''

# Layout kolom untuk plot baru
col3, col4 = st.columns(2)

with col3:
    # 1. Line plot untuk pola peminjaman per jam
    hourly_avg = filtered_df.groupby(['hr', 'workingday'])['cnt'].mean().reset_index()
    fig5, ax5 = plt.subplots(figsize=(10, 6))
    sns.lineplot(x='hr', y='cnt', hue='workingday', data=hourly_avg, ax=ax5)
    ax5.set_title('Pola Peminjaman Sepeda per Jam: Hari Kerja vs Libur')
    ax5.set_xlabel('Jam')
    ax5.set_ylabel('Rata-rata Peminjaman')
    st.pyplot(fig5)
    
    # Insight untuk pola harian
    st.write("""
    ### Insight Pola Harian:
    - Pada hari kerja, peminjaman sepeda sangat terpusat pada jam sibuk (rush hour), mencerminkan pemakaian sepeda sebagai moda transportasi untuk bekerja.
    - Pada hari libur, pola peminjaman lebih merata sepanjang hari, mengindikasikan bahwa orang lebih cenderung meminjam sepeda untuk rekreasi, dan waktu peminjaman tidak terikat dengan jam kerja atau rutinitas tetap.
    """)

with col4:
    # 2. Bar plot untuk perbandingan hari libur
    fig6, ax6 = plt.subplots(figsize=(10, 6))
    sns.barplot(x='holiday', y='cnt', data=filtered_df, ax=ax6)
    ax6.set_title('Perbandingan Peminjaman: Hari Libur vs Hari Biasa')
    ax6.set_xlabel('Hari Libur')
    ax6.set_ylabel('Rata-rata Peminjaman')
    st.pyplot(fig6)
    
    # Insight untuk perbandingan hari libur
    st.write("""
    ### Insight Hari Libur vs Hari Biasa:
    - Terdapat perbedaan signifikan dalam jumlah peminjaman antara hari libur dan hari biasa
    - Permintaan lebih tinggi pada hari libur, menunjukkan penggunaan lebih banyak untuk rekreasi
    """)

# Menambahkan ringkasan keseluruhan di akhir dashboard
st.header('Ringkasan Keseluruhan', divider='gray')
st.write("""
### Kesimpulan Utama:
1. **Pola Musiman**: Terdapat variasi yang jelas dalam penggunaan sepeda berdasarkan musim, 
   dengan puncak di musim panas dan gugur.

2. **Pengaruh Cuaca**: Kondisi cuaca memiliki dampak signifikan terhadap jumlah peminjaman, 
   dengan cuaca cerah menghasilkan peminjaman tertinggi.

3. **Pola Harian**: 
   - Hari kerja menunjukkan pola commuting yang jelas dengan dua puncak peminjaman
   - Akhir pekan memiliki pola yang lebih merata dengan fokus pada aktivitas siang hari

4. **Implikasi Operasional**:
   - Perlu strategi berbeda untuk hari kerja vs akhir pekan
   - Antisipasi variasi musiman dalam perencanaan kapasitas
   - Pertimbangkan dampak cuaca dalam prediksi permintaan

### Rekomendasi:
1. Optimalkan distribusi sepeda berdasarkan pola harian dan mingguan
2. Sesuaikan strategi maintenance dengan variasi musiman
3. Kembangkan promosi khusus untuk meningkatkan penggunaan pada periode low-demand
4. Pertimbangkan penambahan fasilitas perlindungan cuaca di lokasi-lokasi strategis
""")