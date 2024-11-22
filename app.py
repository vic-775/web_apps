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
    
cl1,cl2 = st.columns(2)
with cl1:
    with st.expander("Category_view_data"):
       st.write(category_df.style.background_gradient(cmap="Blues"))
       csv=category_df.to_csv(index=False).encode("utf-8")
       st.download_button("Download data", data = csv, file_name="Category.csv", mime="text/csv")

with cl2:
    with st.expander("Region_view_data"):
       st.write(region_df.style.background_gradient(cmap="Blues"))
       csv=category_df.to_csv(index=False).encode("utf-8")
       st.download_button("Download data", data = csv, file_name="region.csv", mime="text/csv")

#Line graph showing sales over time
filtered_df["month_year"]=filtered_df["Order Date"].dt.to_period("M") #keeps only month and year
Line = pd.DataFrame(filtered_df.groupby(filtered_df["month_year"].dt.strftime("%Y : %b"))["Sales"].sum()).reset_index()
st.subheader("TimeSeries: Sales over time")
fig3 = px.line(Line,x="month_year",y="Sales",labels={"Sales": "Amount"}, height=500, width=1000, template="gridon")
st.plotly_chart(fig3,use_container_width=True)

with st.expander("View Sales overtime"):
    st.write(Line.T.style.background_gradient(cmap="Blues"))
    csv = Line.to_csv(index=False).encode("utf-8")
    st.download_button("Download", data=csv,file_name="Timeseries.csv",mime="text/csv")
#treemap based on region category and sub-category
st.subheader("View of Sales using a Treemap")
fig4 = px.treemap(filtered_df, path=["Region","Category","Sub-Category"], values="Sales",
                  hover_data=["Sales"], color="Sub-Category")
fig4.update_layout(width=800,height=650)
st.plotly_chart(fig4,use_container_width=True)
#2 pie charts showing segment wise sales  and category wise sales
chart1,chart2=st.columns(2)
with chart1:
    st.subheader("Segment wise Sales")
    fig = px.pie(filtered_df,values="Sales",names="Segment",template="plotly_dark")
    fig.update_traces(text=filtered_df["Segment"],textposition="inside")
    st.plotly_chart(fig,use_container_width=True)

with chart2:
    st.subheader("Category wise Sales")
    fig = px.pie(filtered_df,values="Sales",names="Category",template="plotly_dark")
    fig.update_traces(text=filtered_df["Category"],textposition="inside")
    st.plotly_chart(fig,use_container_width=True)

#pivittable showing sales by month
st.subheader("Month wise Sub-Category Sales")
filtered_df["Month"] = filtered_df["Order Date"].dt.month_name()
sub_category_year=pd.pivot_table(data=filtered_df,values="Sales",index=["Sub-Category"],columns="Month")
st.write(sub_category_year.style.background_gradient(cmap="Blues"))

#creating a scatter plot
data1 = px.scatter(filtered_df,x="Sales",y="Profit",size="Quantity")
data1['layout'].update(title="Relationship between Sales and Profit using a sactter plot.",
                        titlefont=dict(size=20),xaxis=dict(title="Sales",titlefont=dict(size=19)),
                        yaxis=dict(title="Profit",titlefont=dict(size=19)))
st.plotly_chart(data1,use_container_width=True)