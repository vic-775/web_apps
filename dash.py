import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
from datetime import datetime

st.set_page_config(layout='wide')

# Reading the data
df = pd.read_csv(r"C:\Users\PC\Desktop\Python Projects\Pro 3\HRDataset_v14.csv")

#dashboard title
html_title = """
<style>
.head_title {
    font-weight: bold;
    text-align: center;
}
.block-container {
    padding-top: 30px;
}
</style>
<h1 class="head_title">HR Analytics Dashboard</h1>
"""

st.markdown(html_title, unsafe_allow_html=True)

# Sidebar Selection for Filter Type
st.sidebar.header("Choose Filter Type:")
filter_type = st.sidebar.radio("Select which filter to apply:", ("Job Filters", "Demographic Filters"))

# ----------------- Job Filters -----------------
if filter_type == "Job Filters":
    st.sidebar.header("Job Filters")
    # creating filter for department 
    dept_filter = st.sidebar.multiselect("Choose Department: ", \
                                        df["Department"].unique())
    if not dept_filter:
        df2 = df.copy()
    else:
        df2 = df[df["Department"].isin(dept_filter)]
        
    # creating filter for employment status
    emp_filter = st.sidebar.multiselect("Choose Employment Status: ", \
        df["EmploymentStatus"].unique())
    if not emp_filter:
        df3 = df2.copy()
    else:
        df3 = df2[df2["EmploymentStatus"].isin(emp_filter)]
        
    # creating fiter for performnace score
    score_filter = st.sidebar.multiselect("Chose Performance Score: ",\
        df["PerformanceScore"].unique())

    # Filtering the data Frame
    if not dept_filter and not emp_filter and not score_filter:
        df_final = df
    elif dept_filter and emp_filter and score_filter:
        df_final = df3[(df3["Department"].isin(dept_filter)) &
                    (df3["EmploymentStatus"].isin(emp_filter)) &
                    (df3["PerformanceScore"].isin(score_filter))]
    elif dept_filter and emp_filter:
        df_final = df3[(df3["Department"].isin(dept_filter)) & (df3["EmploymentStatus"].isin(emp_filter))]
    elif dept_filter and score_filter:
        df_final = df3[(df3["Department"].isin(dept_filter)) & (df3["PerformanceScore"].isin(score_filter))]
    elif emp_filter and score_filter:
        df_final = df3[(df3["EmploymentStatus"].isin(emp_filter)) & (df3["PerformanceScore"].isin(score_filter))]
    elif dept_filter:
        df_final = df3[df3["Department"].isin(dept_filter)]
    elif emp_filter:
        df_final = df3[df3["EmploymentStatus"].isin(emp_filter)]  # ✅ Fixed spelling
    elif score_filter:
        df_final = df3[df3["PerformanceScore"].isin(score_filter)]
    else:
        df_final = df3

# ----------------- Demographic Filters -----------------
elif filter_type == "Demographic Filters":
    st.sidebar.header("Demographic Filters")

    # creating filter for Gender
    gender_filter = st.sidebar.multiselect("Choose Gender: ", \
                                        df["Sex"].unique())
    if not gender_filter:
        df4 = df.copy()
    else:
        df4 = df[df["Sex"].isin(gender_filter)]

    # creating filter for Marital status
    marital_filter = st.sidebar.multiselect("Choose Marital Status: ", \
                                        df["MaritalDesc"].unique())
    if not marital_filter:
        df5 = df4.copy()
    else:
        df5 = df[df["MaritalDesc"].isin(marital_filter)]
        
    # creating filter for citizenship
    citizenship_filter = st.sidebar.multiselect("Choose Citizenship: ", \
                                        df["CitizenDesc"].unique())
        
    # Filtering based on demographic features
    if not gender_filter and not marital_filter and not citizenship_filter:
        df_demo = df
    elif gender_filter and marital_filter and citizenship_filter:
        df_demo = df5[(df["Sex"].isin(gender_filter)) & 
                    (df5["MaritalDesc"].isin(marital_filter)) & 
                    (df5["CitizenDesc"].isin(citizenship_filter))]
    elif gender_filter and marital_filter:
        df_demo = df5[(df["Sex"].isin(gender_filter)) &
                    (df["MaritalDesc"].isin(marital_filter))]
    elif gender_filter and citizenship_filter:
        df_demo = df5[(df["Sex"].isin(gender_filter)) &
                    (df["CitizenDesc"].isin(citizenship_filter))]
    elif citizenship_filter and marital_filter:
        df_demo = df5[(df5["CitizenDesc"].isin(citizenship_filter)) &
                    (df5["MaritalDesc"].isin(marital_filter))]
    elif citizenship_filter:
        df_demo = df5[df5["CitizenDesc"].isin(citizenship_filter)]
    elif gender_filter:
        df_demo = df5[df5["Sex"].isin(gender_filter)]
    elif marital_filter:
        df_demo = df5[df5["MaritalDesc"].isin(marital_filter)]
    else:
        df_demo = df
        
    df_final = df_demo

# Sum Computations
total_employees = df_final.shape[0]
average_salary = df_final["Salary"].mean()
managers_num = df_final['ManagerName'].nunique()

# Calculating Attribution rate
# number of inactive employeess
inactive_employees = df[df["EmploymentStatus"] != "Active"]
inactive_employees = inactive_employees.shape[0]

attribution_rate = round(((inactive_employees/total_employees)*100),2)

col1, col2, col3, col4 = st.columns([1,1,1,1])
# Displaying metrics inside styled boxes
with col1:
    st.markdown(
        f'<div style="padding:15px;text-align:center; color:white;">'
        f'<h4>📊 Total Employees</h4>'
        f'<p style="font-size:24px; font-weight:bold;">{total_employees}</p>'
        f'</div>', unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f'<div style="padding:15px;text-align:center;color:white;">'
        f'<h4>💰 Average Salary</h4>'
        f'<p style="font-size:24px; font-weight:bold;">${average_salary:,.0f}</p>'
        f'</div>', unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f'<div style="padding:15px;text-align:center; color:white;">'
        f'<h4>👥 Total Managers</h4>'
        f'<p style="font-size:24px; font-weight:bold;">{managers_num}</p>'
        f'</div>', unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f'<div style="padding:15px;text-align:center; color:white;">'
        f'<h4>📉 Atribution Rate</h4>'
        f'<p style="font-size:24px; font-weight:bold;">{attribution_rate}%</p>'
        f'</div>', unsafe_allow_html=True
    )

    
emp_sex = df_final.groupby("Sex").size()
emp_citizen = df_final.groupby("CitizenDesc").size()
emp_marital_status = df_final.groupby("MaritalDesc").size()

pie1, pie2, pie3 = st.columns([1,1,1])

with pie1:
    fig1, ax = plt.subplots(figsize=(5,3))
    ax.pie(emp_sex, labels=emp_sex.index,autopct='%1.1f%%', wedgeprops=dict(width=0.3))
    ax.axis('equal')
    ax.set_title("Gender Distribution",)
    st.pyplot(fig1)
with pie2:
    fig2, ax = plt.subplots(figsize = (5,4.4))
    ax.pie(emp_citizen,labels=emp_citizen.index, autopct='%1.1f%%', wedgeprops=dict(width=0.3))
    ax.axis('equal')
    ax.set_title("Total Employees by Citizenship")
    legend = ax.legend(labels=emp_citizen.index, loc='upper right',
                       fontsize=6,frameon=False)
    st.pyplot(fig2)
    
with pie3:
    fig3, ax = plt.subplots(figsize = (5,3))
    ax.pie(emp_marital_status,labels=emp_marital_status.index, autopct='%1.1f%%', wedgeprops=dict(width=0.3))
    ax.axis('equal')
    ax.set_title("Total Employees by Marital Status")
    legend = ax.legend(labels=emp_marital_status.index, loc='upper right',
                       fontsize=6,frameon=False)
    st.pyplot(fig3)
    
bar1, bar2, bar3 = st.columns([1,1,1])

with bar1:
    dept_num = df_final.groupby("Department").size().sort_values()
    fig4, ax = plt.subplots(figsize=(6,5))
    ax.barh(dept_num.index, dept_num.values)
    for index, value in enumerate(dept_num.values):
        ax.text(value, index, str(value), va='center',
                fontsize=10, fontweight='bold')
    ax.set_yticklabels(dept_num.index)
    ax.set_xlabel("Counts")
    ax.set_ylabel("Department")
    ax.set_title("Total Employees by Department")
    st.pyplot(fig4)
    
with bar2:
    race_num = df_final.groupby("RaceDesc").size().sort_values()
    fig5, ax = plt.subplots(figsize=(6,5.7))
    ax.barh(race_num.index, race_num.values)
    for index, value in enumerate(race_num.values):
        ax.text(value, index, str(value), va='center',
                fontsize=10, fontweight='bold')
    ax.set_yticklabels(race_num.index)
    ax.set_xlabel("Counts")
    ax.set_ylabel("Race")
    ax.set_title("Total Employess by Race")
    st.pyplot(fig5)
    
df_final["DOB"] = pd.to_datetime(df_final["DOB"])
df_final["Age"] = (datetime.now() - df_final["DOB"]).dt.days // 365
def age_band(age):
    if age < 30:
        return "Under 30"
    elif 31 <= age <= 40:
        return "31-40"
    elif 41 <= age <= 50:
        return "41-50"
    else:
        return "51+"
# Apply the function to create the 'Age Band' column
df_final["Age Band"] = df_final["Age"].apply(age_band)

with bar3:
    age_num = df_final.groupby("Age Band").size().sort_values()
    fig5, ax = plt.subplots(figsize=(6.6,4.6))
    ax.barh(age_num.index, age_num.values)
    for index, value in enumerate(age_num.values):
        ax.text(value, index, str(value), va='center',
                fontsize=10, fontweight='bold')
    ax.set_yticklabels(age_num.index)
    ax.set_xlabel("Counts")
    ax.set_ylabel("Race")
    ax.set_title("Total Employees by Age Band")
    st.pyplot(fig5)
    
# trends
# Extract month-year from hiredate
df_final["DateofHire"] = pd.to_datetime(df_final["DateofHire"])
df_final["DateofHire_month"] = df_final["DateofHire"].dt.month
df_final["DateofHire_year"] = df_final["DateofHire"].dt.year
df_final["DateofHire_month_year"] = df_final["DateofHire"].dt.strftime("%b-%Y")
# creating 2 more columns
hire1, hire2 = st.columns([1,1])
with hire1:
    hire_year = df_final.groupby('DateofHire_year') \
        .size().reset_index(name="count") \
        .sort_values(by='DateofHire_year')

    hire_year_filtered = hire_year[hire_year['count'] > 0]

    fig8, ax = plt.subplots(figsize=(8, 4))
    
    ax.fill_between(hire_year_filtered['DateofHire_year'], hire_year_filtered['count'],
                    color='skyblue')
    ax.plot(hire_year_filtered['DateofHire_year'], hire_year_filtered['count'],
                    color='blue', marker='o')
    ax.set_title("Annual Hire Rate Trend")
    ax.set_xlabel("Year")
    ax.set_ylabel("Counts of Hire")
    st.pyplot(fig8)

# bar chart for recruitmentsource
with hire2:
    source = df_final.groupby("RecruitmentSource").size().sort_values()
    fig9, ax = plt.subplots(figsize=(8, 5.1))
    ax.barh(source.index, source.values)
    for index, value in enumerate(source):
        ax.text(value, index, str(value), va='center',
                fontsize=10, fontweight='bold')
    ax.set_xlabel('Count')
    ax.set_ylabel('Recruitment Source')
    ax.set_title("Employees Verses Recruitment Source")

    st.pyplot(fig9)
# --- Atribution Rate  
# Extract month-year from date of termination
df_final["DateofTermination"] = pd.to_datetime(df_final["DateofTermination"])
df_final["Termination_month"] = df_final["DateofTermination"].dt.month
df_final["Termination_year"] = df_final["DateofTermination"].dt.year
df_final["Termination_Month_Year"] = df_final["DateofTermination"].dt.strftime("%b-%Y")

trend1, trend2 = st.columns([1,1])

with trend1:
    atri = df_final.groupby(['Termination_Month_Year', "Termination_month", "Termination_year"])\
        .size().reset_index(name="count")\
        .sort_values(by=["Termination_year", "Termination_month"])
    
    # Filter out rows where 'count' is 1
    atri_filtered = atri[atri['count'] > 0]
    fig6, ax = plt.subplots(figsize=(8, 3))
    ax.fill_between(atri_filtered['Termination_Month_Year'], atri_filtered['count'],
                    color='skyblue')
    ax.plot(atri_filtered['Termination_Month_Year'], atri_filtered['count'],
            marker='o')
    
    # Set x-tick labels for the filtered values
    ax.set_xticks(atri_filtered['Termination_Month_Year'])
    ax.set_xticklabels(atri_filtered['Termination_Month_Year'], rotation=90)
    ax.set_title("Trend of Attribute Rate")
    ax.set_xlabel("Month_Year")
    ax.set_ylabel("Counts")
    st.pyplot(fig6)

# bar chart for reason for termination
with trend2:
    # Filtering out people who are still employed
    df_term = df_final[df_final["TermReason"] != "N/A-StillEmployed"]
    term_reason = df_term.groupby("TermReason").size().sort_values()
    fig7, ax = plt.subplots(figsize=(8, 5.2))
    for index, value in enumerate(term_reason):
        ax.text(value, index, str(value), va='center',
                fontsize=10, fontweight='bold')
    ax.barh(term_reason.index, term_reason.values)
    ax.set_xlabel('Count')
    ax.set_ylabel('Termination Reason')
    ax.set_title("Terminated Employees (Atrributed Rate) by TermReason")

    st.pyplot(fig7)

columns_displayed = ["Employee_Name", "EmpID", "Salary", "Position", 
                      "State", "Sex", "MaritalDesc", "CitizenDesc", 
                      "RaceDesc", "EmploymentStatus","Department", 
                      "ManagerName", "PerformanceScore", "Age"]
      
st.dataframe(df_final[columns_displayed])

