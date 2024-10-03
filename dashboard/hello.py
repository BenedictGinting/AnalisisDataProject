import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

# Fungsi untuk memuat datacd
def load_data():
    all_data = pd.read_csv("all_data.csv") 
    return all_data

# Fungsi untuk analisis kategori produk
def analyze_product_category(all_data):
    total_sales_per_category = all_data.groupby('product_category_name')['order_id'].count().reset_index()
    total_sales_per_category.columns = ['product_category_name', 'total_sales']

    avg_review_per_category = all_data.groupby('product_category_name')['review_score'].mean().reset_index()
    avg_review_per_category.columns = ['product_category_name', 'avg_review_score']

    combined_data = pd.merge(total_sales_per_category, avg_review_per_category, on='product_category_name')

    return combined_data

# Fungsi untuk analisis pelanggan VIP
def analyze_vip_customers(all_data):
    rfm_df = all_data.groupby('customer_id').agg({
        'order_purchase_timestamp': 'max',
        'order_id': 'count',
        'payment_value': 'sum'
    }).reset_index()
    
    rfm_df.columns = ['customer_id', 'last_purchase', 'frequency', 'monetary_value']
    rfm_df['recency'] = (datetime.now() - pd.to_datetime(rfm_df['last_purchase'])).dt.days
    rfm_df['rfm_score'] = rfm_df[['recency', 'frequency', 'monetary_value']].sum(axis=1)

    # Mengambil 5 pelanggan VIP
    vip_customers = rfm_df.nlargest(5, 'rfm_score')
    
    return vip_customers

# Fungsi untuk analisis penjualan produk
def analyze_top_products(all_data):
    top_products = all_data.groupby('product_id')['order_id'].count().reset_index()
    top_products.columns = ['product_id', 'total_sales']
    top_product = top_products.nlargest(1, 'total_sales')

    return top_product

# Fungsi untuk visualisasi
def plot_data(combined_data):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=combined_data, x='total_sales', y='avg_review_score', hue='product_category_name', s=100)
    plt.title('Hubungan antara Total Penjualan dan Rata-rata Ulasan per Kategori Produk')
    plt.xlabel('Total Penjualan')
    plt.ylabel('Rata-rata Ulasan')
    plt.legend(title='Kategori Produk', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid()
    st.pyplot(plt)

def plot_sales_trend(all_data):
    # Visualisasi Tren Penjualan
    all_data['order_purchase_timestamp'] = pd.to_datetime(all_data['order_purchase_timestamp'])
    sales_trend = all_data.resample('M', on='order_purchase_timestamp').size().reset_index(name='total_sales')
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=sales_trend, x='order_purchase_timestamp', y='total_sales')
    plt.title('Tren Penjualan Bulanan')
    plt.xlabel('Tanggal')
    plt.ylabel('Total Penjualan')
    plt.grid()
    st.pyplot(plt)

def plot_sales_vs_review(all_data):
    # Visualisasi Hubungan antara Total Penjualan dan Review Score
    sales_vs_review = all_data.groupby('product_id').agg({
        'order_id': 'count',
        'review_score': 'mean'
    }).reset_index()
    sales_vs_review.columns = ['product_id', 'total_sales', 'avg_review_score']

    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=sales_vs_review, x='total_sales', y='avg_review_score', s=100)
    plt.title('Hubungan antara Total Penjualan dan Rata-rata Ulasan Produk')
    plt.xlabel('Total Penjualan')
    plt.ylabel('Rata-rata Ulasan')
    plt.grid()
    st.pyplot(plt)

def plot_price_vs_sales(all_data):
    # Visualisasi Hubungan antara Harga Produk dan Total Penjualan
    price_vs_sales = all_data.groupby('product_id').agg({
        'payment_value': 'mean',
        'order_id': 'count'
    }).reset_index()
    price_vs_sales.columns = ['product_id', 'avg_price', 'total_sales']

    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=price_vs_sales, x='avg_price', y='total_sales', s=100)
    plt.title('Hubungan antara Harga Produk dan Total Penjualan')
    plt.xlabel('Harga Rata-rata Produk')
    plt.ylabel('Total Penjualan')
    plt.grid()
    st.pyplot(plt)

# Membuat dashboard dengan Streamlit
def main():
    st.title("Dashboard E-commerce Analysis")
    
    # Memuat data
    all_data = load_data()
    
# Menampilkan logo di sidebar
    st.sidebar.image("logo.png", width=200)  # Ganti dengan nama file logo Anda

# Menambahkan kalender di sidebar
    st.header("Benedict Raditya Pradipta Ginting")
    st.sidebar.subheader("Pilih Tanggal")
    selected_date = st.sidebar.date_input("Tanggal", datetime.now())
    
    # Analisis kategori produk
    st.subheader("Kategori Produk: Penjualan dan Ulasan")
    combined_data = analyze_product_category(all_data)
    st.write(combined_data)
    plot_data(combined_data)
    
    # Analisis pelanggan VIP
    st.subheader("Pelanggan Paling Berharga (VIP)")
    vip_customers = analyze_vip_customers(all_data)
    st.write(vip_customers)

    # Analisis produk terlaris
    st.subheader("Produk Terlaris")
    top_product = analyze_top_products(all_data)
    st.write(top_product)
     # Visualisasi Hubungan antara Total Penjualan dan Review Score
    st.subheader("Hubungan antara Total Penjualan dan Rata-rata Ulasan Produk")
    plot_sales_vs_review(all_data)

    # Visualisasi Hubungan antara Harga Produk dan Total Penjualan
    st.subheader("Hubungan antara Harga Produk dan Total Penjualan")
    plot_price_vs_sales(all_data)

    # Visualisasi Tren Penjualan
    st.subheader("Tren Penjualan Bulanan")
    plot_sales_trend(all_data)

# Menjalankan aplikasi Streamlit
if __name__ == "__main__":
    main()