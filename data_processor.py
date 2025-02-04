import pandas as pd
import numpy as np
from datetime import datetime

class DataProcessor:
    def __init__(self, data):
        self.raw_data = data
        self.processed_data = None
        
    def process_data(self):
        # Convert data to DataFrame if it's not already
        df = self.raw_data if isinstance(self.raw_data, pd.DataFrame) else pd.read_csv(self.raw_data)
        
        # Convert dates to consistent format
        df['Date'] = pd.to_datetime(df['Date'], format='mixed')
        
        # Sort by date
        df = df.sort_values('Date')
        
        # Calculate rolling averages
        metrics = ['Impressions', 'Clicks', 'Reactions', 'Comments', 'Reposts']
        for metric in metrics:
            df[f'{metric}_7day_avg'] = df[metric].rolling(window=7, min_periods=1).mean()
            
        # Calculate normalized values (0-1 scale)
        for metric in metrics:
            df[f'{metric}_normalized'] = (df[metric] - df[metric].min()) / (df[metric].max() - df[metric].min())
            
        # Additional derived metrics
        df['Click_through_rate'] = df['Clicks'] / df['Impressions']
        df['Total_engagement'] = df['Reactions'] + df['Comments'] + df['Reposts']
        
        self.processed_data = df
        return df
    
    def get_summary_stats(self):
        """Calculate summary statistics for each metric"""
        metrics = ['Impressions', 'Clicks', 'Reactions', 'Comments', 'Reposts', 'Engagement rate']
        summary = {}
        
        for metric in metrics:
            summary[metric] = {
                'mean': self.processed_data[metric].mean(),
                'median': self.processed_data[metric].median(),
                'std': self.processed_data[metric].std(),
                'max': self.processed_data[metric].max(),
                'min': self.processed_data[metric].min()
            }
            
        return summary
