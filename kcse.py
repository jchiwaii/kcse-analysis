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
    /* General Padding */
    .main {
        padding: 0rem 1rem;
    }

    /* Styling for Plotly Charts */
    .stPlotlyChart {
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        padding: 1rem;
    }

    /* Section Divider */
    .section-divider {
        margin: 2rem 0;
    }

    /* Metric Styling */
    div[data-testid="stMetricValue"] {
        font-size: 24px;
    }

    div[data-testid="stMetricDelta"] {
        font-size: 16px;
    }

    /* Emotion Cache Margin */
    .st-emotion-cache-1wivap2 {
        margin-bottom: 2rem;
    }

    /* Header Styling */
    .custom-header {
        font-size: 1.8rem;
        font-weight: bold;
        margin: 2rem 0;
        padding: 1rem 0;
        border-bottom: 2px solid #f0f2f6;
    }

        /* Light Mode Styles */
    .highlight-card {
        background-color: #f9fafb; /* Soft neutral background */
        border-radius: 10px; /* Subtle rounding */
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid #0078d7; /* Slightly softer blue for accents */
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08); /* Light shadow */
    }

    .highlight-number {
        font-size: 2rem;
        font-weight: bold;
        color: #2c3e50; /* Dark gray for readability */
        margin-bottom: 0.5rem;
    }

    .highlight-text {
        color: #4a5568; /* Medium gray for text contrast */
        font-size: 1rem;
    }

    .metric-card {
        background-color: #ffffff; /* Neutral white */
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08); /* Light shadow */
    }

    /* Dark Mode Styles */
    @media (prefers-color-scheme: dark) {
        .highlight-card {
            background-color: #1e1e2e; /* Soft dark background */
            border-left: 5px solid #1d4ed8; /* Richer blue for dark mode */
            box-shadow: 0 2px 4px rgba(255, 255, 255, 0.05); /* Softer shadow */
        }

        .highlight-number {
            color: #e2e8f0; /* Light gray for better contrast */
        }

        .highlight-text {
            color: #a0aec0; /* Softer gray for text */
        }

        .metric-card {
            background-color: #2d2d3a; /* Neutral dark */
            box-shadow: 0 2px 4px rgba(255, 255, 255, 0.05); /* Subtle shadow */
        }
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

# Calculate total students by gender
total_male = df_grades['Male'].sum()
total_female = df_grades['Female'].sum()

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
    st.metric("Overall Mean Grade", f"{overall_mean}/12")
with col2:
    passing_percentage = (passing_grades['Total'].sum() / df_grades['Total'].sum() * 100)
    st.metric("University Qualifying Grades (C+ & Above)", 
              f"{passing_percentage:.1f}%")
with col3:
    male_passing = (passing_grades['Male'].sum() / df_grades['Male'].sum() * 100)
    st.metric("Male Qualifying Rate", 
              f"{male_passing:.1f}%")
with col4:
    female_passing = (passing_grades['Female'].sum() / df_grades['Female'].sum() * 100)
    st.metric("Female Qualifying Rate", 
              f"{female_passing:.1f}%")

st.markdown("---")

st.markdown('<p class="custom-header">Notable Statistics</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="highlight-card">
        <h3>Grade Distribution Peaks</h3>
        <ul>
            <li>Female students peaked at grade <strong>D</strong> with 79,832 candidates</li>
            <li>Male students peaked at grade <strong>D-</strong> with 79,306 candidates</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="highlight-card">
        <h3>Gender Ratios at Extremes</h3>
        <ul>
            <li>Male to Female ratio for grade A is <strong>2.04</strong> (male dominance)</li>
            <li>Male to Female ratio for grade E is <strong>1.40</strong> (similar pattern)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="highlight-number">2X</div>
        <div class="highlight-text">Male Top Performers (A & A-) compared to Female</div>
        <div class="highlight-text" style="margin-top: 0.5rem;">
            Males: 6,040 vs Females: 3,396
        </div>
    </div>
    """, unsafe_allow_html=True)

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
              f"{male_top_grades:,}")

with col2:
    male_middle_grades = df_grades[df_grades['Grade'].isin(['B+', 'B', 'B-', 'C+'])]['Male'].sum()
    st.metric("Male Middle Performers (B+ to C+)", 
              f"{male_middle_grades:,}")

with col3:
    male_low_grades = df_grades[df_grades['Grade'].isin(['D+', 'D', 'D-', 'E'])]['Male'].sum()
    st.metric("Male Low Performers (D+ & Below)", 
              f"{male_low_grades:,}")

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
                            color_discrete_sequence=['#9b59b6', '#fda7df'])
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
              f"{female_top_grades:,}")

with col2:
    female_middle_grades = df_grades[df_grades['Grade'].isin(['B+', 'B', 'B-', 'C+'])]['Female'].sum()
    st.metric("Female Middle Performers (B+ to C+)", 
              f"{female_middle_grades:,}")

with col3:
    female_low_grades = df_grades[df_grades['Grade'].isin(['D+', 'D', 'D-', 'E'])]['Female'].sum()
    st.metric("Female Low Performers (D+ & Below)", 
              f"{female_low_grades:,}")

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
    marker_color='#9b59b6'
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

# Comprehensive Summary Metrics
st.markdown("---")
st.markdown('<p class="custom-header">Comprehensive Summary Metrics</p>', unsafe_allow_html=True)

# Performance Distribution Metrics
col1, col2, col3 = st.columns(3)

with col1:
    # Top Grades Analysis
    total_top_grades = df_grades[df_grades['Grade'].isin(['A', 'A-'])]['Total'].sum()
    st.metric("Total A & A- Grades", 
              f"{total_top_grades:,}",
              f"{(total_top_grades/df_grades['Total'].sum()*100):.2f}% of total")
    
    # Gender ratio in top grades
    top_gender_ratio = df_grades[df_grades['Grade'].isin(['A', 'A-'])]['Male'].sum() / \
                      df_grades[df_grades['Grade'].isin(['A', 'A-'])]['Female'].sum()
    st.metric("Male to Female Ratio in A Grades", 
              f"{top_gender_ratio:.2f}")

with col2:
    # Middle Grades Analysis
    middle_grades = df_grades[df_grades['Grade'].isin(['B+', 'B', 'B-'])]['Total'].sum()
    st.metric("Total B+, B, B- Grades", 
              f"{middle_grades:,}",
              f"{(middle_grades/df_grades['Total'].sum()*100):.2f}% of total")
    
    # Gender distribution in middle grades
    middle_gender_ratio = df_grades[df_grades['Grade'].isin(['B+', 'B', 'B-'])]['Male'].sum() / \
                         df_grades[df_grades['Grade'].isin(['B+', 'B', 'B-'])]['Female'].sum()
    st.metric("Male to Female Ratio in B Grades", 
              f"{middle_gender_ratio:.2f}")

with col3:
    # C Grades Analysis
    c_grades = df_grades[df_grades['Grade'].isin(['C+', 'C', 'C-'])]['Total'].sum()
    st.metric("Total C+, C, C- Grades", 
              f"{c_grades:,}",
              f"{(c_grades/df_grades['Total'].sum()*100):.2f}% of total")
    
    # Gender distribution in C grades
    c_gender_ratio = df_grades[df_grades['Grade'].isin(['C+', 'C', 'C-'])]['Male'].sum() / \
                    df_grades[df_grades['Grade'].isin(['C+', 'C', 'C-'])]['Female'].sum()
    st.metric("Male to Female Ratio in C Grades", 
              f"{c_gender_ratio:.2f}")

# Calculate D grades and E grades totals for the detailed analysis
total_d_grades = df_grades[df_grades['Grade'].isin(['D+', 'D', 'D-'])]['Total'].sum()
e_grades = df_grades[df_grades['Grade'] == 'E']['Total'].sum()

# Performance ratio analysis
st.markdown("---")
st.markdown('<p class="custom-header">Performance Ratio Analysis</p>', unsafe_allow_html=True)

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

# Download functionality (rest of the code remains the same)
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
        'Total Top Grades (A, A-)',
        'Total Middle Grades (B+, B, B-)',
        'Total C Grades (C+, C, C-)',
        'Total D Grades (D+, D, D-)',
        'Total E Grades',
        'Male to Female Ratio Overall',
        'Male to Female Ratio in Top Grades',
        'University Qualification Rate',
        'Male Qualification Rate',
        'Female Qualification Rate',
        'Gender Gap in Mean Grade',
        'Total Male Students',
        'Total Female Students'
    ],
    'Value': [
        df_grades['Total'].sum(),
        passing_grades['Total'].sum(),
        passing_grades['Male'].sum(),
        passing_grades['Female'].sum(),
        overall_mean,
        male_mean,
        female_mean,
        total_top_grades,
        middle_grades,
        c_grades,
        total_d_grades,
        e_grades,
        total_male/total_female,
        top_gender_ratio,
        passing_percentage,
        male_passing,
        female_passing,
        male_mean - female_mean,
        total_male,
        total_female
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