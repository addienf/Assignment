import streamlit as st # type: ignore
import pandas as pd # type: ignore
import plotly.express as px # type: ignore

# --- Konfigurasi halaman utama ---
st.set_page_config(page_title='Dashboard Penjualan & RFM', layout='wide')

# --- Fungsi Load Data ---
@st.cache_data
def load_data():
    df_sales = pd.read_csv('Dataset/data_clean.csv')
    rfm = pd.read_csv('Dataset/RFM.csv')
    return df_sales, rfm
df_sales, rfm = load_data()

# --- Sidebar Navigasi ---
st.sidebar.title("Navigasi")
if "halaman" not in st.session_state:
    st.session_state.halaman = "Overview Dashboard"

if st.sidebar.button("📊 Overview Dashboard"):
    st.session_state.halaman = "Overview Dashboard"

if st.sidebar.button("🧮 Analisis RFM"):
    st.session_state.halaman = "Analisis RFM"

pilihan_halaman = st.session_state.halaman

if pilihan_halaman == "Overview Dashboard":
    st.title("📈 Dashboard Analisis Penjualan")
    st.markdown("Menampilkan ringkasan performa penjualan berdasarkan data transaksi yang tersedia.")

    # --- FILTER UNTUK DASHBOARD ---
    st.sidebar.markdown("### Filter")

    negara_terpilih = st.sidebar.selectbox(
        "Pilih Negara",
        options=["Semua Negara"] + sorted(df_sales["Country"].unique())
    )

    filtered_df = df_sales.copy()

    if negara_terpilih != "Semua Negara":
        filtered_df = filtered_df[filtered_df["Country"] == negara_terpilih]

    # --- KPI Ringkasan ---
    total_sales = filtered_df["TotalPrice"].sum()
    total_orders = filtered_df["Invoice"].nunique()
    total_customers = filtered_df["Customer ID"].nunique()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Penjualan", f"${total_sales:,.0f}")
    col2.metric("Jumlah Transaksi", f"{total_orders:,}")
    col3.metric("Jumlah Pelanggan", f"{total_customers:,}")

    # --- Visualisasi 1: Penjualan per Negara ---
    country_sales = (
        filtered_df.groupby("Country")["TotalPrice"].sum()
        .reset_index()
        .sort_values(by="TotalPrice", ascending=False)
        .head(10)
    )
    fig_country = px.bar(
        country_sales,
        x="Country",
        y="TotalPrice",
        color="Country",
        title="🌍 Top 10 Negara dengan Total Penjualan Tertinggi"
    )
    fig_country.update_layout(
        xaxis_title="Negara",
        yaxis_title="Total Penjualan"
    )

    # --- Visualisasi 2: Produk Terlaris ---
    top_products = (
        filtered_df.groupby("Description")["Quantity"].sum()
        .reset_index()
        .sort_values(by="Quantity", ascending=False)
        .head(10)
    )
    fig_top_products = px.bar(
        top_products,
        x="Description",
        y="Quantity",
        color="Quantity",
        title="🛍️ Top 10 Produk Terlaris"
    )

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_country, use_container_width=True)
    with col2:
        st.plotly_chart(fig_top_products, use_container_width=True)

    # --- Visualisasi 3: Tren Penjualan per Bulan & Tahun ---
    filtered_df["InvoiceDate"] = pd.to_datetime(filtered_df["InvoiceDate"])
    filtered_df["YearMonth"] = filtered_df["InvoiceDate"].dt.to_period("M").astype(str)

    sales_trend = (
        filtered_df.groupby("YearMonth")["TotalPrice"].sum().reset_index()
    )

    fig_sales_trend = px.line(
        sales_trend,
        x="YearMonth",
        y="TotalPrice",
        title="📆 Tren Penjualan Bulanan",
        markers=True
    )
    fig_sales_trend.update_layout(
        xaxis_title="Periode (Tahun-Bulan)",
        yaxis_title="Total Penjualan",
        xaxis_tickangle=-45
    )

    st.plotly_chart(fig_sales_trend, use_container_width=True)

elif pilihan_halaman == "Analisis RFM":
    st.title("👥 Analisis RFM (Recency, Frequency, Monetary)")
    st.markdown("Analisis ini membantu memahami perilaku pelanggan berdasarkan **Recency**, **Frequency**, dan **Monetary Value**.")

    st.sidebar.markdown("### Filter")

    segment_terpilih = st.sidebar.selectbox(
        "Pilih Segment Pelanggan",
        options=["Semua Segment"] + sorted(rfm["Segment"].unique())
    )

    filtered_rfm = rfm.copy()
    if segment_terpilih != "Semua Segment":
        filtered_rfm = filtered_rfm[filtered_rfm["Segment"] == segment_terpilih]

    # --- KPI RFM ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Rata-rata Recency", f"{filtered_rfm['Recency'].mean():.1f}")
    col2.metric("Rata-rata Frequency", f"{filtered_rfm['Frequency'].mean():.1f}")
    col3.metric("Rata-rata Monetary", f"${filtered_rfm['Monetary'].mean():,.0f}")

    col1, col2 = st.columns(2)

    # === Distribusi R, F, M ===
    with col1:
        st.write("#### Distribusi RFM Metrics")
        c1, c2, c3 = st.columns(3)
        c1.plotly_chart(px.histogram(filtered_rfm, x='Recency', nbins=20, title='Distribusi Recency'), use_container_width=True)
        c2.plotly_chart(px.histogram(filtered_rfm, x='Frequency', nbins=20, title='Distribusi Frequency'), use_container_width=True)
        c3.plotly_chart(px.histogram(filtered_rfm, x='Monetary', nbins=20, title='Distribusi Monetary'), use_container_width=True)

    # === Jumlah Pelanggan per Segment ===
    with col2:
        st.write("#### Jumlah Pelanggan per Segment")
        segment_count = filtered_rfm['Segment'].value_counts().reset_index()
        segment_count.columns = ['Segment', 'count']

        fig_segment = px.bar(
            segment_count,
            x='Segment',
            y='count',
            color='Segment',
            title='Distribusi Pelanggan Berdasarkan Segment'
        )
        fig_segment.update_layout(xaxis_title="Segment", yaxis_title="Jumlah Pelanggan")
        st.plotly_chart(fig_segment, use_container_width=True)

    # --- Visualisasi 5: Rata-rata RFM per Segment ---
    st.subheader("Rata-rata Nilai RFM per Segment")
    rfm_segment_mean = filtered_rfm.groupby('Segment')[['Recency', 'Frequency', 'Monetary']].mean().reset_index()
    fig_avg_segment = px.bar(
        rfm_segment_mean.melt(id_vars='Segment', value_vars=['Recency', 'Frequency', 'Monetary']),
        x='Segment', y='value', color='variable', barmode='group',
        title='Rata-rata Nilai R, F, M per Segment'
    )
    st.plotly_chart(fig_avg_segment, use_container_width=True)