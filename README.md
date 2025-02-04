# Social Media Analytics Dashboard

An interactive data visualization dashboard for analyzing social media metrics over time. This application provides comprehensive analytics and visualizations for your social media data.

## Features

- Interactive time series visualizations
- Normalized metrics comparison
- Engagement analysis
- Statistical summaries
- Data download capability
- Responsive design

## Prerequisites

- Python 3.11 or higher
- pip (Python package installer)

## Installation

1. Clone this repository or download the files to your local machine.

2. Open a terminal/command prompt and navigate to the project directory.

3. Install the required packages:
```bash
pip install streamlit pandas plotly numpy
```

## Running the Application

1. Place your data file in the `attached_assets` folder (or update the path in `main.py`).

2. Run the Streamlit application:
```bash
streamlit run main.py
```

3. Open your web browser and navigate to:
- Local: http://localhost:8501
- Network: http://0.0.0.0:8501

## Usage

1. **Date Range Selection**: Use the date pickers at the top to select your desired date range.

2. **Metric Selection**: Choose which metrics you want to visualize using the multi-select dropdown.

3. **Interactive Visualizations**: 
   - Hover over data points for detailed information
   - Click legend items to show/hide specific metrics
   - Use the zoom and pan tools to explore specific time periods

4. **Download Data**: Use the "Download CSV" button to export processed data for further analysis.

## Customizing the Data Source

To use your own data:
1. Ensure your CSV file has the following columns:
   - Date
   - Impressions
   - Clicks
   - Reactions
   - Comments
   - Reposts
   - Engagement rate

2. Update the data file path in `main.py`:
```python
df = pd.read_csv("path_to_your_data.csv")
```

## Troubleshooting

If you encounter any issues:
1. Ensure all required packages are installed
2. Check if the data file exists in the correct location
3. Verify your Python version (3.11+ recommended)
4. Make sure no other application is using port 8501

## Support

For any questions or issues, please open an issue in the repository.
