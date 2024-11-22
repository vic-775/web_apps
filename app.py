import streamlit as st
import plotly.express as px
import pandas as pd

df = pd.read_excel("sales.xlsx",engine="openpyxl")
st.set_page_config(page_title="Super Store Sales", page_icon=":bar_chart:",layout="wide")
st.title(" :bar_chart: Sample SuperStore EDA")
#st.markdown('<style>div.block-container{padding-top:1rem:}</style>',unsafe_allow_html=True)

#creating platform for uploading a file
fl = st.file_uploader("Upload a file",type=(["csv","txt","xlsx","xls"]))

col1,col2 = st.columns((2))
df["Order Date"]=pd.to_datetime(df["Order Date"]) #converting to datetime

startdate=pd.to_datetime(df["Order Date"]).min()
enddate=pd.to_datetime(df["Order Date"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date",startdate))
with col2:
    date2 = pd.to_datetime(st.date_input("End Date",enddate))

df = df[(df["Order Date"]>= date1) & (df["Order Date"]<=date2)].copy()

#creating filter for region
st.sidebar.header("Chose Your Filter ")
region=st.sidebar.multiselect("Pick Region",df["Region"].unique())
if not region:
    df2 = df.copy()
else:
    df2=df[df["Region"].isin(region)]

#creating filter for state
state=st.sidebar.multiselect("Pick State",df2["State"].unique())
if not state:
    df3=df2.copy()
else:
    df3=df2[df2["State"].isin(state)]

#creating filter for city
city=st.sidebar.multiselect("Pick City", df3["City"].unique())
if not region and not state and not city:
    filtered_df = df
elif not state and not city:
    filtered_df=df[df["Region"].isin(region)]
elif not region and not city:
    filtered_df = df[df["State"].isin(state)]
elif state and city:
    filtered_df=df3[df["State"].isin(state) & (df3["City"].isin(city))]
elif region and city:
    filtered_df = df3[df["Region"].isin(region) & df3["City"].isin(city)]
elif region and state:
    filtered_df = df3[df["Region"].isin(region) & df3["State"].isin(state)]
elif city:
    filtered_df = df3[df3["City"].isin(city)]
else:
    filtered_df=df3[df3["Region"].isin(region) & df3["State"].isin(state) & df3["City"].isin(city)]

#Graph for category vs sales
with col1:
  with st.expander("Region View Data")
     st.subheader("Total Sales by Category")
     category_df = filtered_df.groupby(by=["Category"],as_index=False)["Sales"].sum()
     fig1 = px.bar(category_df,x="Category",y="Sales",template="gridon",height=480)
     st.plotly_chart(fig1,use_container_width=True)
#Graph showing sales by Region
with col2:
     st.subheader("Total Sales by Region")
     region_df = filtered_df.groupby(by=["Region"],as_index=False)["Sales"].sum()
     fig2 = px.pie(filtered_df,values="Sales", names="Region", hole=0.5)
     fig2.update_traces(text=filtered_df["Region"],textposition="outside")
     st.plotly_chart(fig2,use_container_width=True)

results4=

