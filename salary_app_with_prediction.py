
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

st.set_page_config(page_title="Salary Dashboard", layout="wide")
st.title("💰 Employee Salary Prediction Dashboard")

# File uploader
uploaded_file = st.file_uploader("Upload your employee data (CSV)", type=['csv'])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success(f"✅ Loaded {len(df)} employees")
    
    # ========== DATA PREVIEW SECTION ==========
    with st.expander("📊 View Raw Data"):
        st.dataframe(df.head(10))
    
    # ========== KEY METRICS ==========
    st.subheader("📈 Key Metrics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Employees", len(df))
    with col2:
        st.metric("Avg Salary", f"${df['Salary'].mean():,.0f}")
    with col3:
        st.metric("Avg Experience", f"{df['Experience_Years'].mean():.1f} years")
    
    # ========== VISUALIZATION SECTION ==========
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Salary vs Experience")
        fig = px.scatter(df, x='Experience_Years', y='Salary', 
                         color='Gender', title='Salary by Experience')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Salary by Gender")
        fig2 = px.box(df, x='Gender', y='Salary', title='Salary Distribution')
        st.plotly_chart(fig2, use_container_width=True)
    
    # ========== PREDICTION SECTION ==========
    st.markdown("---")
    st.header("🎯 Predict Salary for New Employee")
    
    # Prepare data for model
    df_encoded = df.copy()
    df_encoded['Gender_Encoded'] = (df_encoded['Gender'] == 'Male').astype(int)
    
    X = df_encoded[['Experience_Years', 'Age', 'Gender_Encoded']]
    y = df_encoded['Salary']
    
    # Train model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Input fields
    col1, col2, col3 = st.columns(3)
    
    with col1:
        exp_input = st.number_input(
            "Years of Experience",
            min_value=0,
            max_value=30,
            value=5,
            step=1
        )
    
    with col2:
        age_input = st.number_input(
            "Age",
            min_value=18,
            max_value=70,
            value=30,
            step=1
        )
    
    with col3:
        gender_input = st.selectbox(
            "Gender",
            df['Gender'].unique()
        )
    
    # Make prediction button
    if st.button("💰 Predict Salary", type="primary"):
        gender_encoded = 1 if gender_input == 'Male' else 0
        prediction = model.predict([[exp_input, age_input, gender_encoded]])[0]
        
        # Show prediction
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.success(f"### 💰 Predicted Salary: **${prediction:,.2f}**")
            
            # Show confidence range
            predictions = []
            for tree in model.estimators_[:10]:
                pred = tree.predict([[exp_input, age_input, gender_encoded]])[0]
                predictions.append(pred)
            
            st.info(f"📊 Prediction Range: ${min(predictions):,.0f} - ${max(predictions):,.0f}")
        
        # Show similar employees
        st.subheader("👥 Similar Employees in Database")
        similar = df[
            (abs(df['Experience_Years'] - exp_input) <= 2) &
            (abs(df['Age'] - age_input) <= 3) &
            (df['Gender'] == gender_input)
        ]
        
        if len(similar) > 0:
            st.dataframe(similar[['Experience_Years', 'Age', 'Gender', 'Salary']], use_container_width=True)
        else:
            st.info("No similar employees found")
    
    # ========== MODEL PERFORMANCE ==========
    with st.expander("📊 Model Performance Metrics"):
        y_pred = model.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("R² Score", f"{r2:.3f}")
        with col2:
            st.metric("Mean Absolute Error", f"${mae:,.0f}")
        
        st.caption("R² measures how well the model explains salary variations. Higher is better.")
    
else:
    st.info("📁 Please upload your CSV file to get started")
    st.markdown("""
    ### 📋 Expected CSV format:
    Your file should have these columns:
    * **Experience_Years** - Years of work experience
    * **Age** - Employee age  
    * **Gender** - Male/Female
    * **Salary** - Annual salary
    
    ### 🔧 How it works:
    1. Upload your employee data
    2. View analytics and charts
    3. Enter new employee details
    4. Click "Predict Salary" to get prediction
    """)
