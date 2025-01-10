import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots

# Set page config
st.set_page_config(layout="wide", page_title="KCSE 2024 Analysis Dashboard", page_icon="📊")

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    .stPlotlyChart {
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
        padding: 1rem;
    }
    .section-divider {
        margin: 2rem 0;
    }
    div[data-testid="stMetricValue"] {
        font-size: 24px;
    }
    div[data-testid="stMetricDelta"] {
        font-size: 16px;
    }
    .st-emotion-cache-1wivap2 {
        margin-bottom: 2rem;
    }
    .custom-header {
        font-size: 1.8rem;
        font-weight: bold;
        margin: 2rem 0;
        padding: 1rem 0;
        border-bottom: 2px solid #f0f2f6;
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

# Calculate mean grade and other metrics
grade_points = {
    'A': 12, 'A-': 11, 'B+': 10, 'B': 9, 'B-': 8, 'C+': 7,
    'C': 6, 'C-': 5, 'D+': 4, 'D': 3, 'D-': 2, 'E': 1
}

# Calculate weighted averages
def calculate_mean_grade(data, column):
    total_points = sum(data[column] * [grade_points[g] for g in data['Grade']])
    total_students = data[column].sum()
    return round(total_points / total_students, 2)

overall_mean = calculate_mean_grade(df_grades, 'Total')
male_mean = calculate_mean_grade(df_grades, 'Male')
female_mean = calculate_mean_grade(df_grades, 'Female')

# Calculate passing grades (A to C+)
passing_grades = df_grades[df_grades['Grade'].isin(['A', 'A-', 'B+', 'B', 'B-', 'C+'])]
failing_grades = df_grades[~df_grades['Grade'].isin(['A', 'A-', 'B+', 'B', 'B-', 'C+'])]

# Title
st.title("📊 KCSE 2024 Comprehensive Analysis Dashboard")
st.markdown("---")

# Top Summary Section
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Overall Mean Grade", f"{overall_mean}/12", 
              delta=f"Male: {male_mean} | Female: {female_mean}")
with col2:
    passing_percentage = (passing_grades['Total'].sum() / df_grades['Total'].sum() * 100)
    st.metric("University Qualifying Grades (C+ & Above)", 
              f"{passing_percentage:.1f}%",
              f"{passing_grades['Total'].sum():,} students")
with col3:
    male_passing = (passing_grades['Male'].sum() / df_grades['Male'].sum() * 100)
    st.metric("Male Qualifying Rate", 
              f"{male_passing:.1f}%",
              f"{passing_grades['Male'].sum():,} students")
with col4:
    female_passing = (passing_grades['Female'].sum() / df_grades['Female'].sum() * 100)
    st.metric("Female Qualifying Rate", 
              f"{female_passing:.1f}%",
              f"{passing_grades['Female'].sum():,} students")

st.markdown("---")

# Overall Performance Analysis
st.markdown('<p class="custom-header">Overall Performance Distribution</p>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    # Overall grade distribution
    fig_overall = px.bar(df_grades, x='Grade', y='Total',
                        title='Grade Distribution (All Students)',
                        color='Total',
                        color_continuous_scale='Viridis')
    fig_overall.update_layout(
        height=500,
        bargap=0.2,
        title_x=0.5,
        showlegend=False
    )
    st.plotly_chart(fig_overall, use_container_width=True)

with col2:
    # Passing vs Non-passing
    pass_fail_data = pd.DataFrame({
        'Category': ['Qualifying Grades (C+ & Above)', 'Below University Cutoff'],
        'Count': [passing_grades['Total'].sum(), failing_grades['Total'].sum()]
    })
    fig_pass_fail = px.pie(pass_fail_data, values='Count', names='Category',
                          title='University Qualification Distribution',
                          color_discrete_sequence=['#2ecc71', '#e74c3c'])
    fig_pass_fail.update_layout(
        height=500,
        title_x=0.5
    )
    st.plotly_chart(fig_pass_fail, use_container_width=True)

st.markdown("---")

# Male Students Analysis
st.markdown('<p class="custom-header">Male Students Performance Analysis</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Male grade distribution
    male_grade_dist = px.bar(df_grades, x='Grade', y='Male',
                            title='Male Students Grade Distribution',
                            color='Male',
                            color_continuous_scale='Blues')
    male_grade_dist.update_layout(
        height=500,
        bargap=0.2,
        title_x=0.5
    )
    st.plotly_chart(male_grade_dist, use_container_width=True)

with col2:
    # Male passing vs failing
    male_pass_fail = pd.DataFrame({
        'Category': ['Qualifying Grades', 'Below Cutoff'],
        'Count': [passing_grades['Male'].sum(), failing_grades['Male'].sum()]
    })
    fig_male_pass = px.pie(male_pass_fail, values='Count', names='Category',
                          title='Male Students: University Qualification',
                          color_discrete_sequence=['#3498db', '#bdc3c7'])
    fig_male_pass.update_layout(
        height=500,
        title_x=0.5
    )
    st.plotly_chart(fig_male_pass, use_container_width=True)

# Male performance metrics
col1, col2, col3 = st.columns(3)

with col1:
    male_top_grades = df_grades[df_grades['Grade'].isin(['A', 'A-'])]['Male'].sum()
    st.metric("Male Top Performers (A & A-)", 
              f"{male_top_grades:,}",
              f"{(male_top_grades/df_grades['Male'].sum()*100):.2f}%")

with col2:
    male_middle_grades = df_grades[df_grades['Grade'].isin(['B+', 'B', 'B-', 'C+'])]['Male'].sum()
    st.metric("Male Middle Performers (B+ to C+)", 
              f"{male_middle_grades:,}",
              f"{(male_middle_grades/df_grades['Male'].sum()*100):.2f}%")

with col3:
    male_low_grades = df_grades[df_grades['Grade'].isin(['D+', 'D', 'D-', 'E'])]['Male'].sum()
    st.metric("Male Low Performers (D+ & Below)", 
              f"{male_low_grades:,}",
              f"{(male_low_grades/df_grades['Male'].sum()*100):.2f}%")

st.markdown("---")

# Female Students Analysis
st.markdown('<p class="custom-header">Female Students Performance Analysis</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Female grade distribution
    female_grade_dist = px.bar(df_grades, x='Grade', y='Female',
                              title='Female Students Grade Distribution',
                              color='Female',
                              color_continuous_scale='RdPu')
    female_grade_dist.update_layout(
        height=500,
        bargap=0.2,
        title_x=0.5
    )
    st.plotly_chart(female_grade_dist, use_container_width=True)

with col2:
    # Female passing vs failing
    female_pass_fail = pd.DataFrame({
        'Category': ['Qualifying Grades', 'Below Cutoff'],
        'Count': [passing_grades['Female'].sum(), failing_grades['Female'].sum()]
    })
    fig_female_pass = px.pie(female_pass_fail, values='Count', names='Category',
                            title='Female Students: University Qualification Distribution',
                            color_discrete_sequence=['#e84393', '#fd79a8'])
    fig_female_pass.update_layout(
        height=500,
        title_x=0.5
    )
    st.plotly_chart(fig_female_pass, use_container_width=True)

# Female performance metrics
col1, col2, col3 = st.columns(3)

with col1:
    female_top_grades = df_grades[df_grades['Grade'].isin(['A', 'A-'])]['Female'].sum()
    st.metric("Female Top Performers (A & A-)", 
              f"{female_top_grades:,}",
              f"{(female_top_grades/df_grades['Female'].sum()*100):.2f}%")

with col2:
    female_middle_grades = df_grades[df_grades['Grade'].isin(['B+', 'B', 'B-', 'C+'])]['Female'].sum()
    st.metric("Female Middle Performers (B+ to C+)", 
              f"{female_middle_grades:,}",
              f"{(female_middle_grades/df_grades['Female'].sum()*100):.2f}%")

with col3:
    female_low_grades = df_grades[df_grades['Grade'].isin(['D+', 'D', 'D-', 'E'])]['Female'].sum()
    st.metric("Female Low Performers (D+ & Below)", 
              f"{female_low_grades:,}",
              f"{(female_low_grades/df_grades['Female'].sum()*100):.2f}%")

st.markdown("---")

# Comparative Analysis
st.markdown('<p class="custom-header">Gender Comparative Analysis</p>', unsafe_allow_html=True)

# Gender comparison by grade
fig_compare = go.Figure()
fig_compare.add_trace(go.Bar(
    name='Male',
    x=df_grades['Grade'],
    y=df_grades['Male'],
    marker_color='#3498db'
))
fig_compare.add_trace(go.Bar(
    name='Female',
    x=df_grades['Grade'],
    y=df_grades['Female'],
    marker_color='#e84393'
))
fig_compare.update_layout(
    barmode='group',
    title='Grade Distribution Comparison by Gender',
    height=600,
    title_x=0.5,
    bargap=0.2,
    bargroupgap=0.1
)
st.plotly_chart(fig_compare, use_container_width=True)

# Performance ratio analysis
col1, col2 = st.columns(2)

with col1:
    # Calculate gender performance ratios for each grade level
    df_grades['M_F_Ratio'] = df_grades['Male'] / df_grades['Female']
    fig_ratio = px.bar(df_grades, x='Grade', y='M_F_Ratio',
                       title='Male to Female Performance Ratio by Grade',
                       color='M_F_Ratio',
                       color_continuous_scale='RdBu')
    fig_ratio.add_hline(y=1, line_dash="dash", line_color="gray")
    fig_ratio.update_layout(
        height=500,
        title_x=0.5,
        yaxis_title="Male/Female Ratio"
    )
    st.plotly_chart(fig_ratio, use_container_width=True)

with col2:
    # Performance distribution
    df_grades['Male_Pct'] = df_grades['Male'] / df_grades['Male'].sum() * 100
    df_grades['Female_Pct'] = df_grades['Female'] / df_grades['Female'].sum() * 100
    
    fig_dist = go.Figure()
    fig_dist.add_trace(go.Scatter(
        x=df_grades['Grade'],
        y=df_grades['Male_Pct'],
        name='Male %',
        line=dict(color='#3498db', width=2)
    ))
    fig_dist.add_trace(go.Scatter(
        x=df_grades['Grade'],
        y=df_grades['Female_Pct'],
        name='Female %',
        line=dict(color='#e84393', width=2)
    ))
    fig_dist.update_layout(
        title='Grade Distribution Percentage by Gender',
        height=500,
        title_x=0.5,
        yaxis_title='Percentage of Students',
        showlegend=True
    )
    st.plotly_chart(fig_dist, use_container_width=True)

# D Grades Analysis
st.markdown('<p class="custom-header">D Grades Analysis</p>', unsafe_allow_html=True)

d_grades = df_grades[df_grades['Grade'].isin(['D+', 'D', 'D-'])]

col1, col2 = st.columns(2)

with col1:
    # D grades distribution by gender
    fig_d_grades = go.Figure()
    fig_d_grades.add_trace(go.Bar(
        name='Male',
        x=d_grades['Grade'],
        y=d_grades['Male'],
        marker_color='#3498db'
    ))
    fig_d_grades.add_trace(go.Bar(
        name='Female',
        x=d_grades['Grade'],
        y=d_grades['Female'],
        marker_color='#e84393'
    ))
    fig_d_grades.update_layout(
        title='D Grades Distribution by Gender',
        height=500,
        title_x=0.5,
        barmode='group',
        bargap=0.2,
        bargroupgap=0.1
    )
    st.plotly_chart(fig_d_grades, use_container_width=True)

with col2:
    # D grades percentage composition
    d_grades_total = {
        'Grade': ['D+', 'D', 'D-'],
        'Percentage': [
            (d_grades[d_grades['Grade'] == 'D+']['Total'].iloc[0] / d_grades['Total'].sum() * 100),
            (d_grades[d_grades['Grade'] == 'D']['Total'].iloc[0] / d_grades['Total'].sum() * 100),
            (d_grades[d_grades['Grade'] == 'D-']['Total'].iloc[0] / d_grades['Total'].sum() * 100)
        ]
    }
    fig_d_composition = px.pie(
        d_grades_total, 
        values='Percentage', 
        names='Grade',
        title='Distribution of D Grades',
        color_discrete_sequence=['#74b9ff', '#0984e3', '#74b9ff']
    )
    fig_d_composition.update_layout(
        height=500,
        title_x=0.5
    )
    st.plotly_chart(fig_d_composition, use_container_width=True)

# D grades metrics
col1, col2, col3 = st.columns(3)

with col1:
    total_d_plus = d_grades[d_grades['Grade'] == 'D+']['Total'].iloc[0]
    st.metric(
        "Total D+ Grades",
        f"{total_d_plus:,}",
        f"{(total_d_plus/df_grades['Total'].sum()*100):.2f}% of total"
    )

with col2:
    total_d = d_grades[d_grades['Grade'] == 'D']['Total'].iloc[0]
    st.metric(
        "Total D Grades",
        f"{total_d:,}",
        f"{(total_d/df_grades['Total'].sum()*100):.2f}% of total"
    )

with col3:
    total_d_minus = d_grades[d_grades['Grade'] == 'D-']['Total'].iloc[0]
    st.metric(
        "Total D- Grades",
        f"{total_d_minus:,}",
        f"{(total_d_minus/df_grades['Total'].sum()*100):.2f}% of total"
    )

# Add a section for gender comparison in D grades
st.markdown("### D Grades Gender Analysis")
d_grades_gender = pd.DataFrame({
    'Grade': ['D+', 'D', 'D-'] * 2,
    'Gender': ['Male'] * 3 + ['Female'] * 3,
    'Percentage': [
        d_grades['Male'].iloc[0] / d_grades['Male'].sum() * 100,
        d_grades['Male'].iloc[1] / d_grades['Male'].sum() * 100,
        d_grades['Male'].iloc[2] / d_grades['Male'].sum() * 100,
        d_grades['Female'].iloc[0] / d_grades['Female'].sum() * 100,
        d_grades['Female'].iloc[1] / d_grades['Female'].sum() * 100,
        d_grades['Female'].iloc[2] / d_grades['Female'].sum() * 100
    ]
})

fig_d_gender = px.bar(
    d_grades_gender,
    x='Grade',
    y='Percentage',
    color='Gender',
    barmode='group',
    title='Gender Distribution within D Grades',
    color_discrete_sequence=['#3498db', '#e84393']
)
fig_d_gender.update_layout(
    height=500,
    title_x=0.5,
    yaxis_title='Percentage within Gender',
    bargap=0.2,
    bargroupgap=0.1
)
st.plotly_chart(fig_d_gender, use_container_width=True)

# Final metrics dashboard for D grades
st.markdown("### D Grades Summary Metrics")
col1, col2 = st.columns(2)

with col1:
    total_d_grades = d_grades['Total'].sum()
    st.metric(
        "Total Students with D Grades",
        f"{total_d_grades:,}",
        f"{(total_d_grades/df_grades['Total'].sum()*100):.2f}% of all students"
    )

with col2:
    d_gender_ratio = d_grades['Male'].sum() / d_grades['Female'].sum()
    st.metric(
        "Male to Female Ratio in D Grades",
        f"{d_gender_ratio:.2f}",
        "Males per Female"
    )

# Add download functionality for the analysis
st.markdown("---")
st.markdown("### Download Analysis Data")

# Create detailed analysis DataFrame
detailed_analysis = pd.DataFrame({
    'Metric': [
        'Total Students',
        'University Qualifying Students',
        'Male Qualifying Students',
        'Female Qualifying Students',
        'Overall Mean Grade',
        'Male Mean Grade',
        'Female Mean Grade',
        'Total D Grade Students',
        'Male D Grade Students',
        'Female D Grade Students'
    ],
    'Value': [
        df_grades['Total'].sum(),
        passing_grades['Total'].sum(),
        passing_grades['Male'].sum(),
        passing_grades['Female'].sum(),
        overall_mean,
        male_mean,
        female_mean,
        d_grades['Total'].sum(),
        d_grades['Male'].sum(),
        d_grades['Female'].sum()
    ]
})

# Convert DataFrame to CSV
csv = detailed_analysis.to_csv(index=False)
st.download_button(
    label="Download Detailed Analysis",
    data=csv,
    file_name="kcse_2024_detailed_analysis.csv",
    mime="text/csv"
)