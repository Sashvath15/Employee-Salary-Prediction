# Create fixed version with proper syntax
with open('salary_app.py', 'w') as f:
    f.write('''
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Salary Dashboard", layout="wide")
st.title("💰 Employee Salary Prediction Dashboard")

# File uploader
uploaded_file = st.file_uploader("Upload your employee data (CSV)", type=['csv'])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success(f"✅ Loaded {len(df)} employees")
    
    # Show data preview
    st.subheader("📊 Data Preview")
    st.dataframe(df.head())
    
    # Basic stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Employees", len(df))
    with col2:
        st.metric("Avg Salary", f"${df['Salary'].mean():,.0f}")
    with col3:
        st.metric("Avg Experience", f"{df['Experience_Years'].mean():.1f} years")
    
    # Salary vs Experience Chart
    st.subheader("📈 Salary vs Experience")
    fig = px.scatter(df, x='Experience_Years', y='Salary', 
                     color='Gender', title='Salary by Experience')
    st.plotly_chart(fig)
    
    # Salary distribution by gender
    st.subheader("📊 Salary by Gender")
    fig2 = px.box(df, x='Gender', y='Salary', title='Salary Distribution')
    st.plotly_chart(fig2)
    
else:
    st.info("📁 Please upload your CSV file to get started")
    st.markdown("""
    **Expected columns:**
    * Experience_Years - Years of work experience
    * Age - Employee age
    * Gender - Male/Female
    * Salary - Annual salary
    """)
''')

# Verify the file was created correctly
with open('salary_app.py', 'r') as f:
    print("First 10 lines of the file:")
    print("-" * 40)
    lines = f.readlines()[:10]
    for line in lines:
        print(line.rstrip())

# Download the file
from google.colab import files
files.download('salary_app.py')

print("\n✅ File created and downloaded!")
print("📤 Now upload this salary_app.py to your GitHub repository")