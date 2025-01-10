import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import numpy as np
import base64

# Set page config
st.set_page_config(layout="wide", page_title="KCSE 2024 Analysis Dashboard")

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    .stPlotlyChart {
        background-color: white;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stats-card {
        padding: 1rem;
        background-color: white;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Create grade distribution data
grades_data = {
    'Grade': ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'E'],
    'Total': [1693, 7743, 19150, 43120, 75347, 99338, 111717, 118781, 128885, 153334, 151487, 48333],
    'Male': [1137, 4903, 11042, 23339, 39950, 48940, 53769, 56175, 60088, 73501, 79306, 28221],
    'Female': [556, 2840, 8108, 19781, 35397, 50398, 57948, 62606, 68797, 79832, 72181, 20112]
}

df_grades = pd.DataFrame(grades_data)

# Registration data
registration_data = {
    'Gender': ['Male', 'Female'],
    'Count': [481649, 483523]
}

df_registration = pd.DataFrame(registration_data)

# Title
st.title("KCSE 2024 Examination Analysis Dashboard")
st.markdown("---")

# Key Statistics Section
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Registered Students", "965,172", "+62,034")
with col2:
    st.metric("University Eligible (C+ & above)", "246,391", "25.5%")
with col3:
    st.metric("Total A Grade", "1,693", "0.18%")
with col4:
    st.metric("Below University Cut-off", "712,537", "74.5%")

st.markdown("---")

# Gender Distribution Section
st.subheader("Gender Distribution Analysis")
col1, col2 = st.columns(2)

with col1:
    # Registration pie chart
    fig_reg = px.pie(df_registration, values='Count', names='Gender',
                     title='Gender Distribution in Registration',
                     color_discrete_sequence=['#3498db', '#e74c3c'])
    st.plotly_chart(fig_reg, use_container_width=True)

with col2:
    # A grade distribution
    a_grade_data = pd.DataFrame({
        'Gender': ['Male', 'Female'],
        'Count': [1137, 556]
    })
    fig_a = px.pie(a_grade_data, values='Count', names='Gender',
                   title='A Grade Distribution by Gender',
                   color_discrete_sequence=['#3498db', '#e74c3c'])
    st.plotly_chart(fig_a, use_container_width=True)

# Grade Distribution Section
st.subheader("Grade Distribution Analysis")

# Overall grade distribution
fig_grades = px.bar(df_grades, x='Grade', y='Total',
                    title='Overall Grade Distribution',
                    color_discrete_sequence=['#2ecc71'])
fig_grades.update_layout(bargap=0.2)
st.plotly_chart(fig_grades, use_container_width=True)

# Gender comparison in grades
fig_gender = go.Figure()
fig_gender.add_trace(go.Bar(name='Male', x=df_grades['Grade'], y=df_grades['Male'],
                           marker_color='#3498db'))
fig_gender.add_trace(go.Bar(name='Female', x=df_grades['Grade'], y=df_grades['Female'],
                           marker_color='#e74c3c'))
fig_gender.update_layout(barmode='group', title='Grade Distribution by Gender')
st.plotly_chart(fig_gender, use_container_width=True)

# Performance Trends
st.subheader("Performance Analysis")

# Calculate percentages for better comparison
df_grades['Male_Percentage'] = df_grades['Male'] / df_grades['Male'].sum() * 100
df_grades['Female_Percentage'] = df_grades['Female'] / df_grades['Female'].sum() * 100

fig_perf = go.Figure()
fig_perf.add_trace(go.Scatter(x=df_grades['Grade'], y=df_grades['Male_Percentage'],
                             name='Male %', line=dict(color='#3498db')))
fig_perf.add_trace(go.Scatter(x=df_grades['Grade'], y=df_grades['Female_Percentage'],
                             name='Female %', line=dict(color='#e74c3c')))
fig_perf.update_layout(title='Gender Performance Trends (Percentage)',
                      yaxis_title='Percentage')
st.plotly_chart(fig_perf, use_container_width=True)

# University Eligibility Analysis
st.subheader("University Eligibility Analysis")

eligible = df_grades[df_grades['Grade'].isin(['A', 'A-', 'B+', 'B', 'B-', 'C+'])]
not_eligible = df_grades[~df_grades['Grade'].isin(['A', 'A-', 'B+', 'B', 'B-', 'C+'])]

eligibility_data = pd.DataFrame({
    'Category': ['Eligible', 'Not Eligible'],
    'Count': [eligible['Total'].sum(), not_eligible['Total'].sum()]
})

fig_elig = px.pie(eligibility_data, values='Count', names='Category',
                  title='University Eligibility Distribution',
                  color_discrete_sequence=['#27ae60', '#c0392b'])
st.plotly_chart(fig_elig, use_container_width=True)

# Key Conclusions Section
st.markdown("---")
st.subheader("Key Conclusions")
st.markdown("""
1. **Gender Distribution Milestone**
   - First time in history where female registration (483,523) exceeded male registration (481,649)
   - Represents a significant step towards gender parity in education

2. **Performance Patterns**
   - Males dominated in higher grades (A to B+)
   - Females showed stronger performance in middle grades (C+ to D)
   - Gender gap most pronounced in A grades (Male: 1,137, Female: 556)

3. **University Eligibility**
   - Only 25.5% of students qualified for university admission
   - Total of 246,391 students achieved C+ and above
   - Significant number (712,537) fell below university admission threshold

4. **Grade Distribution**
   - Highest concentration of students in D grade range
   - Bell curve skewed towards lower grades
   - Notable gender performance gaps in extreme grades (A and E)

5. **Overall Trends**
   - Total registration increased by 62,034 from 2023
   - Performance distribution shows need for targeted interventions
   - Gender parity achieved in registration but not in top performance
""")

# Add download button for detailed report
st.markdown("---")
st.subheader("Download Detailed Report")
st.download_button(
    label="Download KCSE 2024 Analysis Report",
    data=df_grades.to_csv().encode('utf-8'),
    file_name='kcse_2024_analysis.csv',
    mime='text/csv'
)