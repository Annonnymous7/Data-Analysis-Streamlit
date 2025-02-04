import streamlit as st
import pandas as pd
from data_processor import DataProcessor
from visualizations import DataVisualizer
import plotly.express as px
import os

# Page config
st.set_page_config(
    page_title="Social Media Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title and description
st.title("📊 Social Media Analytics Dashboard")
st.markdown("""
This dashboard provides interactive visualizations of social media metrics over time.
Analyze trends, engagement rates, and compare different metrics.
""")

# Load and process data
@st.cache_data
def load_data(data_path=None):
    """Load data from CSV file"""
    if data_path is None:
        # Default to the sample data file
        data_path = os.path.join('attached_assets', 
            'national-institute-of-biomedical-genomics_content_1738664497849.csv')

    if not os.path.exists(data_path):
        st.error(f"Data file not found: {data_path}")
        st.stop()

    try:
        df = pd.read_csv(data_path)
        processor = DataProcessor(df)
        processed_df = processor.process_data()
        return processed_df, processor
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.stop()

# Allow users to upload their own data file
uploaded_file = st.sidebar.file_uploader("Upload your own data file (CSV)", type=['csv'])
if uploaded_file is not None:
    data, data_processor = load_data(uploaded_file)
else:
    data, data_processor = load_data()

visualizer = DataVisualizer(data)

# Date range selector
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input(
        "Start Date",
        min_value=data['Date'].min().date(),
        max_value=data['Date'].max().date(),
        value=data['Date'].min().date()
    )
with col2:
    end_date = st.date_input(
        "End Date",
        min_value=data['Date'].min().date(),
        max_value=data['Date'].max().date(),
        value=data['Date'].max().date()
    )

# Filter data based on date range
filtered_data = data[(data['Date'].dt.date >= start_date) & 
                    (data['Date'].dt.date <= end_date)]
visualizer.data = filtered_data

# Metric selector
metrics = st.multiselect(
    "Select metrics to display",
    ['Impressions', 'Clicks', 'Reactions', 'Comments', 'Reposts'],
    default=['Impressions', 'Clicks']
)

# Main metrics time series
st.subheader("Metrics Over Time")
if metrics:
    st.plotly_chart(visualizer.create_time_series(metrics), use_container_width=True)

# Normalized comparison
st.subheader("Normalized Metrics Comparison")
st.plotly_chart(visualizer.create_normalized_comparison(), use_container_width=True)

# Engagement analysis
st.subheader("Engagement Analysis")
st.plotly_chart(visualizer.create_engagement_analysis(), use_container_width=True)

# Create a new DataProcessor instance with filtered data and process it
filtered_processor = DataProcessor(filtered_data)
filtered_processor.process_data()
summary_stats = filtered_processor.get_summary_stats()

# Summary statistics
st.subheader("Statistical Summary")
col1, col2, col3 = st.columns(3)

metrics_to_show = ['Impressions', 'Clicks', 'Engagement rate']

for i, metric in enumerate(metrics_to_show):
    with [col1, col2, col3][i]:
        st.metric(
            label=metric,
            value=f"{summary_stats[metric]['mean']:.2f}",
            delta=f"{summary_stats[metric]['std']:.2f} std"
        )

# Download processed data
st.subheader("Download Processed Data")
csv = filtered_data.to_csv(index=False)
st.download_button(
    label="Download CSV",
    data=csv,
    file_name="processed_social_media_metrics.csv",
    mime="text/csv"
)

# Footer
st.markdown("---")
st.markdown("""
<style>
.footer {
    text-align: center;
    padding: 20px;
    color: #666;
}
</style>
<div class="footer">
    Created with Streamlit • Data updated daily
</div>
""", unsafe_allow_html=True)