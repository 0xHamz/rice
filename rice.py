import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf

st.title('Data Kota Penghasil Beras di INDONESIA')

st.markdown("""
aplikasi menampilkan data pneghasil beras sesuai dengan kota di Indonesia.
""")

st.sidebar.header('User Input Features')

# Web scraping of S&P 500 data
#
@st.cache_resource
def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print(f"File '{file_path}' tidak ditemukan.")
        return None

file_path = "Rice Production Indonesia 2020-2022.csv"
df = load_data(file_path)

sector = df.groupby('Provinsi')

# Sidebar - Sector selection
sorted_sector_unique = sorted( df['Provinsi'].unique() )
selected_sector = st.sidebar.multiselect('Kota', sorted_sector_unique, sorted_sector_unique)

# Filtering data
df_selected_sector = df[ (df['Provinsi'].isin(selected_sector)) ]

st.dataframe(df_selected_sector)

# Download S&P500 data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="best-selling-manga.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_sector), unsafe_allow_html=True)

# https://pypi.org/project/yfinance/

@st.cache_resource
def create_top_10_manga_plot(df):
    # Mengurutkan data berdasarkan penjualan tertinggi
    sorted_data = df.sort_values(by='Production.(ton)', ascending=False)

    # Mengambil 10 manga terlaris
    top_10_manga = sorted_data.head(10)

    # Membuat grafik bar untuk manga terlaris
    plt.figure(figsize=(12, 6))
    plt.barh(top_10_manga['Provinsi'], top_10_manga['Production.(ton)'])
    plt.xlabel('Penjualan (juta kopi)')
    plt.title('Daftar Gaji')
    plt.gca().invert_yaxis()  # Membalik urutan agar yang terlaris di atas

    return plt

# ...

st.title("Grafik Penghasilan Beras Setiap Kota")
st.header("Klik tombol 'Show Chart' untuk menampilkan grafik")

if st.button("Show Chart"):
    manga_plot = create_top_10_manga_plot(df_selected_sector)  # Update plot dengan data yang baru
    st.pyplot(manga_plot)