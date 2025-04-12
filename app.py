import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mticker

#loading the data
df = pd.read_csv(r"C:\Users\PC\Desktop\sales web app\sales_data.csv")
st.set_page_config(layout='wide')
st.markdown('<style>div.block-container{padding-top:0.5rem:}</style>', unsafe_allow_html=True)
df[['Sales_Amount', 'Quantity_Sold', 'Unit_Cost', 'Unit_Price', 'Discount']] = \
df[['Sales_Amount', 'Quantity_Sold', 'Unit_Cost', 'Unit_Price', 'Discount']].astype(float)
df["Sale_Date"] = pd.to_datetime(df['Sale_Date'])
html_title = """
  <style>
  .title-test {
   font-weight: bold;
   padding:5px;
   border-radius: 6px;
   text-align: center;
  }
  .block-container {
        padding-top: 20px;
    }
  </style>
  <h1 class="title-test">Sales Web Dashboard</h1>
"""
st.markdown(html_title, unsafe_allow_html=True)
#sum computations
total_sales = df["Sales_Amount"].sum()
total_quantity = df["Quantity_Sold"].sum()
total_orders = df.shape[0]
cost_average = df['Unit_Cost'].mean()
price_average = df["Unit_Price"].mean()

product_sales = df.groupby('Product_Category')['Sales_Amount'].sum()
region_sales = df.groupby('Region')['Sales_Amount'].sum()
payment_sales = df.groupby('Payment_Method')['Sales_Amount'].sum()

#creating 5 cards for showing the summations
col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])

#displaying numbers on the cards
with col1:
    st.metric("Total Sales", f"${total_sales:,.0f}")
with col2:
    st.metric("Quantity_Sold", f"{total_quantity:,.0f}")
with col3:
    st.metric("Total Oders", f"{total_orders:,.0f}")
with col4:
    st.metric("Average Cost", f"{cost_average:,.0f}")
with col5:
    st.metric("Average Price", f"{price_average:,.0f}")

#creating sub header
eda_title = """
<style>
.eda {
    text-align: center;
    margin-top: -20px;
    margin-bottom: -20px;
    padding-top: 0px;
    padding-bottom: 0px;
}
</style>
<h2 class="eda">Exploratory Data Analysis</h2>
"""

#st.markdown("<hr style='margin-bottom: -1px; border: 1px solid black; margin-bottom: -10px;'>", unsafe_allow_html=True)
st.markdown(eda_title, unsafe_allow_html=True)
st.markdown("<hr style='margin-top: -15px; border: 1px solid black; margin-bottom: -10px;'>", unsafe_allow_html=True)

#creating 3columns for 3 charts
col_chart1, col_chart2, col_chart3 = st.columns([2,2,2])

#first bar chart
with col_chart1:
    fig, ax = plt.subplots(figsize = (8,5))
    ax.bar(product_sales.index, product_sales.values)
    ax.yaxis.set_major_formatter(mticker.StrMethodFormatter('{x:,.0f}'))
    for i, v in enumerate (product_sales.values):
        ax.text(i, float(product_sales.values[i]), f"{product_sales.values[i]:,.0f}", 
        ha='center', va='bottom', fontsize=12)
    ax.set_xticklabels(product_sales.index, rotation=45, ha='right',fontsize=12)
    ax.set_xlabel("Product Category",fontsize=10)
    ax.set_ylabel("Revenue",fontsize=12)
    ax.set_title("Total Revenue by Product Category")
    st.pyplot(fig)

#2nd bar chart
with col_chart2:
    fig2, ax = plt.subplots(figsize = (8,5))
    ax.bar(region_sales.index, region_sales.values)
    ax.yaxis.set_major_formatter(mticker.StrMethodFormatter('{x:,.0f}'))
    for i, v in enumerate(region_sales.values):
        ax.text(i, v, f"{v:,.0f}", ha='center', va='bottom', fontsize=12)
    ax.set_xticklabels(region_sales.index, rotation=45, ha='right')
    ax.set_xlabel("Region",fontsize=12)
    ax.set_ylabel("Revenue",fontsize=12)
    ax.set_title("Total Revenue by Region")
    st.pyplot(fig2)

#3rd bar Chart
with col_chart3:
    fig3, ax = plt.subplots(figsize = (8,5))
    ax.bar(payment_sales.index, payment_sales.values)
    ax.yaxis.set_major_formatter(mticker.StrMethodFormatter('{x:,.0f}'))
    for i, v in enumerate(payment_sales.values):
        ax.text(i, v, f"{v:,.0f}", ha='center', va='bottom', fontsize=12)
    ax.set_xticklabels(payment_sales.index, rotation=45)
    ax.set_ylabel("Revenue", fontsize=12)
    ax.set_xlabel("Payment Method", fontsize=12)
    ax.set_title("Revenue by Payment Method")
    st.pyplot(fig3)

#title for facet grid
facet_title = """
<style>
.eda {
    text-align: center;
    margin-top: -20px;
    margin-bottom: -20px;
    padding-top: 0px;
    padding-bottom: 0px;
}
</style>
<h2 class="eda">Sales by Region, Agent per Region and Total Revenue</h2>
"""

#st.markdown("<hr style='margin-bottom: -1px; border: 1px solid black; margin-bottom: -10px;'>", unsafe_allow_html=True)
st.markdown(facet_title, unsafe_allow_html=True)
st.markdown("<hr style='margin-top: -15px; border: 1px solid black; margin-bottom: -10px;'>", unsafe_allow_html=True)

#facet grid chart    
facet_col = st.columns([1])
with facet_col[0]:
    fig4 = sns.FacetGrid(df, col="Region", sharex=False)
    fig4.map_dataframe(sns.barplot,x="Region_and_Sales_Rep", y="Sales_Amount", errorbar=None)
    fig4.set_xticklabels(rotation=45,ha='right',fontsize=7, fontweight='normal')
    fig4.set_xlabels(fontsize=7,fontweight='normal')
    fig4.set_ylabels(fontsize=7,fontweight='normal')
    fig4.set_titles(fontsize=7,fontweight='normal')
    st.pyplot(fig4.figure)

#trend analysis title
trend_title = """
<style>
.eda {
    text-align: center;
    margin-top: -20px;
    margin-bottom: -20px;
    padding-top: 0px;
    padding-bottom: 0px;
}
</style>
<h2 class="eda">Sales Over time (Trend)</h2>
"""

#st.markdown("<hr style='margin-bottom: -1px; border: 1px solid black; margin-bottom: -10px;'>", unsafe_allow_html=True)
st.markdown(trend_title, unsafe_allow_html=True)
st.markdown("<hr style='margin-top: -15px; border: 1px solid black; margin-bottom: -10px;'>", unsafe_allow_html=True)

#first trend analysis chart  
trend_col1, trend_col2 = st.columns([0.5,0.5])
with trend_col1:
    df["Month"] = df["Sale_Date"].dt.month_name()       
    df["Month_num"] = df["Sale_Date"].dt.month
    df_month = df.groupby(["Month", "Month_num"])["Sales_Amount"].sum().reset_index()
    df_month_sorted = df_month.sort_values("Month_num")  
    
    fig5, ax = plt.subplots(figsize=(8,5))
    ax.barh(df_month_sorted["Month"], df_month_sorted["Sales_Amount"])
    for i, v in enumerate(df_month_sorted["Sales_Amount"]):
        ax.text(v*0.80, i, f"{v:,.0f}", fontweight='bold', va='center', color='black', fontsize=10)
    ax.set_yticklabels(df_month_sorted['Month'], rotation=0)
    ax.set_xlabel("Months per Year")
    ax.set_ylabel("Revenue")
    ax.set_title("Trend by Month")
    st.pyplot(fig5)

#Second trend analysis chart   
with trend_col2: 
    df["Month_Year"] = df["Sale_Date"].dt.strftime("%b-%Y")
    df["Year"] = df["Sale_Date"].dt.year
    df["Month"] = df["Sale_Date"].dt.month
    
    df_month_year = df.groupby(["Year", "Month", "Month_Year"], as_index=False)["Sales_Amount"].sum()
    df_month_year = df_month_year.sort_values(["Year", "Month"])
    fig6, ax = plt.subplots(figsize=(8, 5))
    ax.fill_between(df_month_year["Month_Year"], df_month_year["Sales_Amount"], color="blue", alpha=0.5)
    ax.plot(df_month_year["Month_Year"], df_month_year["Sales_Amount"], marker="o", linestyle="-", color="blue")
    
    ax.set_xticks(range(len(df_month_year["Month_Year"])))  
    ax.set_xticklabels(df_month_year["Month_Year"], rotation=45, ha="right", fontsize=10)
    ax.set_xlabel("Month-Year")
    ax.set_ylabel("Revenue")
    ax.set_title("Sales Trend Over Time")
    st.pyplot(fig6) 

#adding new subheader
data_title = """
<style>
.data {
    text-align: left;
    margin-top: -20px;
    margin-bottom: -20px;
    padding-top: 0px;
    padding-bottom: 0px;
}
</style>
<h2 class="data">All Data</h2>
"""
#st.markdown("<hr style='margin-bottom: -1px; border: 1px solid black; margin-bottom: -10px;'>", unsafe_allow_html=True)
st.markdown(data_title, unsafe_allow_html=True)
st.markdown("<hr style='margin-top: -15px; border: 1px solid black; margin-bottom: -10px;'>", unsafe_allow_html=True)

#adding the data
data_col = st.columns(1)
with data_col[0]:
    st.dataframe(df)
