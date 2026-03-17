import streamlit as st, requests, pandas as pd

API="http://localhost:5000"

st.title("Travel Management Pro")

st.header("Upload Excel")
file=st.file_uploader("Upload file")
if file:
    requests.post(API+"/upload", files={"file":file})
    st.success("Uploaded")

st.header("Search Agents")
q=st.text_input("Search")
if st.button("Go"):
    st.write(requests.get(API+f"/agents?search={q}").json())

st.header("Add Product")
name=st.text_input("Product Name")
season=st.selectbox("Season",["low","high"])
price=st.number_input("Price",0)
if st.button("Add Product"):
    requests.post(API+"/products",json={"name":name,"season":season,"price":price})
    st.success("Added")

st.header("Commission Calculator")
d=st.number_input("Days",1,30)
p=st.number_input("Price",0)
s=st.selectbox("Season2",["low","high"])
if st.button("Calc"):
    st.write(requests.post(API+"/commission",json={"days":d,"price":p,"season":s}).json())

st.header("Demo Chart")
data=pd.DataFrame({"Sales":[10,20,30,40]})
st.bar_chart(data)
