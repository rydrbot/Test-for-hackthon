import streamlit as st
import requests
import pandas as pd

API = "https://test-for-hackthon.onrender.com"

st.title("✈️ Travel Management System")

# ================================
# 📤 Upload Excel
# ================================
st.header("Upload Agents Excel")

file = st.file_uploader("Upload Excel File", key="file_upload")

if file:
    response = requests.post(API + "/upload", files={"file": file})
    st.success("File uploaded successfully!")

# ================================
# 🔍 Search Agents
# ================================
st.header("Search Agents")

search = st.text_input("Enter agent name", key="search_input")

if st.button("Search", key="search_btn"):
    res = requests.get(f"{API}/agents?search={search}")
    st.write(res.json())

# ================================
# 📦 Add Product
# ================================
st.header("Add Product")

col1, col2 = st.columns(2)

with col1:
    prod_name = st.text_input("Product Name", key="prod_name")

with col2:
    prod_season = st.selectbox("Season", ["low", "high"], key="prod_season")

prod_price = st.number_input("Price", min_value=0, key="prod_price")

if st.button("Add Product", key="add_product_btn"):
    requests.post(API + "/products", json={
        "name": prod_name,
        "season": prod_season,
        "price": prod_price
    })
    st.success("Product added successfully!")

# ================================
# ⚡ Commission Calculator
# ================================
st.header("Commission Calculator")

col3, col4 = st.columns(2)

with col3:
    comm_days = st.number_input("Days to Sell", min_value=1, max_value=30, key="comm_days")

with col4:
    comm_price = st.number_input("Product Price", min_value=0, key="comm_price")

comm_season = st.selectbox("Season", ["low", "high"], key="comm_season")

if st.button("Calculate Commission", key="calc_btn"):
    res = requests.post(API + "/commission", json={
        "days": comm_days,
        "price": comm_price,
        "season": comm_season
    })
    st.success(f"Commission: {res.json()['commission']}%")

# ================================
# 📊 Dashboard (Chart)
# ================================
st.header("Sales Dashboard")

# Sample data (you can replace later with real data)
data = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr"],
    "Sales": [10, 25, 15, 40]
})

st.line_chart(data.set_index("Month"))
