import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import numpy as np

class DataVisualizer:
    def __init__(self, data):
        self.data = data
        self.color_sequence = px.colors.qualitative.Set3

    def create_time_series(self, metrics):
        """Create enhanced multi-metric time series plot"""
        fig = go.Figure()

        for idx, metric in enumerate(metrics):
            # Main metric line
            fig.add_trace(
                go.Scatter(
                    x=self.data['Date'],
                    y=self.data[metric],
                    name=metric,
                    mode='lines',
                    line=dict(width=2, color=self.color_sequence[idx % len(self.color_sequence)]),
                    hovertemplate=(
                        f"<b>{metric}</b><br>" +
                        "Date: %{x}<br>" +
                        "Value: %{y:,.0f}<br>" +
                        "<extra></extra>"
                    )
                )
            )

            # Add rolling average
            rolling_avg = self.data[metric].rolling(window=7).mean()
            fig.add_trace(
                go.Scatter(
                    x=self.data['Date'],
                    y=rolling_avg,
                    name=f'{metric} (7-day avg)',
                    mode='lines',
                    line=dict(
                        width=1,
                        color=self.color_sequence[idx % len(self.color_sequence)],
                        dash='dash'
                    ),
                    opacity=0.5,
                    showlegend=True,
                    hovertemplate=(
                        f"<b>{metric} 7-day Average</b><br>" +
                        "Date: %{x}<br>" +
                        "Value: %{y:,.0f}<br>" +
                        "<extra></extra>"
                    )
                )
            )

        fig.update_layout(
            title={
                'text': 'Social Media Metrics Over Time',
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(size=24)
            },
            xaxis=dict(
                title="Date",
                showline=True,
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(211, 211, 211, 0.3)'
            ),
            yaxis=dict(
                title="Value",
                showline=True,
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(211, 211, 211, 0.3)'
            ),
            hovermode='x unified',
            showlegend=True,
            template='plotly_white',
            plot_bgcolor='white',
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="sans-serif"
            ),
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=1.05,
                bgcolor='rgba(255, 255, 255, 0.8)'
            )
        )

        return fig

    def create_normalized_comparison(self):
        """Create enhanced normalized metrics comparison"""
        metrics = ['Impressions', 'Clicks', 'Reactions', 'Comments']

        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Normalized Metrics Comparison', 'Metrics Distribution'),
            vertical_spacing=0.22
        )

        # Normalized time series
        for idx, metric in enumerate(metrics):
            normalized_values = (self.data[metric] - self.data[metric].min()) / (self.data[metric].max() - self.data[metric].min())

            fig.add_trace(
                go.Scatter(
                    x=self.data['Date'],
                    y=normalized_values,
                    name=metric,
                    mode='lines',
                    line=dict(width=2, color=self.color_sequence[idx]),
                    hovertemplate=(
                        f"<b>{metric}</b><br>" +
                        "Date: %{x}<br>" +
                        "Value: %{y:.3f}<br>" +
                        "<extra></extra>"
                    )
                ),
                row=1, col=1
            )

            # Add violin plot for distribution
            fig.add_trace(
                go.Violin(
                    y=normalized_values,
                    name=metric,
                    box_visible=True,
                    meanline_visible=True,
                    fillcolor=self.color_sequence[idx],
                    line_color='black',
                    opacity=0.6
                ),
                row=2, col=1
            )

        fig.update_layout(
            height=800,
            showlegend=True,
            template='plotly_white',
            hovermode='x unified',
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="sans-serif"
            ),
            legend=dict(
                yanchor="top",
                y=1.15,
                xanchor="center",
                x=0.5,
                orientation="h"
            )
        )

        fig.update_xaxes(title_text="Date", row=1, col=1)
        fig.update_yaxes(title_text="Normalized Value (0-1)", row=1, col=1)
        fig.update_yaxes(title_text="Distribution", row=2, col=1)

        return fig

    def create_engagement_analysis(self):
        """Create enhanced engagement metrics analysis"""
        # Create figure with secondary y-axis
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Total Engagement Over Time',
                'Engagement Rate Distribution',
                'Engagement Types',
                'Engagement vs. Impressions'
            ),
            specs=[
                [{"type": "xy", "secondary_y": True}, {"type": "xy"}],
                [{"type": "pie"}, {"type": "xy"}]
            ],
            horizontal_spacing=0.15,
            vertical_spacing=0.15
        )

        # Total Engagement Over Time
        fig.add_trace(
            go.Bar(
                x=self.data['Date'],
                y=self.data['Total_engagement'],
                name="Total Engagement",
                marker_color='rgba(158,202,225,0.8)',
                hovertemplate="Date: %{x}<br>Total Engagement: %{y}<br><extra></extra>"
            ),
            row=1, col=1
        )

        # Add trend line
        z = np.polyfit(range(len(self.data['Date'])), self.data['Total_engagement'], 1)
        p = np.poly1d(z)

        fig.add_trace(
            go.Scatter(
                x=self.data['Date'],
                y=p(range(len(self.data['Date']))),
                name="Trend",
                line=dict(color='red', dash='dot'),
                hovertemplate="Trend<br>Date: %{x}<br>Value: %{y:.0f}<br><extra></extra>"
            ),
            row=1, col=1
        )

        # Engagement Rate Distribution
        fig.add_trace(
            go.Histogram(
                x=self.data['Engagement rate'],
                nbinsx=30,
                name="Engagement Rate",
                marker_color='rgba(255,127,14,0.7)',
                hovertemplate="Engagement Rate: %{x}<br>Count: %{y}<br><extra></extra>"
            ),
            row=1, col=2
        )

        # Engagement Composition (Pie Chart)
        engagement_types = ['Reactions', 'Comments', 'Reposts']
        values = [self.data[metric].sum() for metric in engagement_types]

        fig.add_trace(
            go.Pie(
                labels=engagement_types,
                values=values,
                hole=.3,
                name="Engagement Types",
                hovertemplate="Type: %{label}<br>Count: %{value}<br>Percentage: %{percent}<extra></extra>"
            ),
            row=2, col=1
        )

        # Engagement vs. Impressions Scatter
        fig.add_trace(
            go.Scatter(
                x=self.data['Impressions'],
                y=self.data['Total_engagement'],
                mode='markers',
                marker=dict(
                    size=8,
                    color=self.data['Engagement rate'],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Engagement Rate")
                ),
                name='Engagement vs Impressions',
                hovertemplate=(
                    "Impressions: %{x:,}<br>" +
                    "Total Engagement: %{y:,}<br>" +
                    "Engagement Rate: %{marker.color:.2%}<br>" +
                    "<extra></extra>"
                )
            ),
            row=2, col=2
        )

        fig.update_layout(
            height=1000,
            showlegend=True,
            template='plotly_white',
            margin=dict(t=150, b=20, l=80, r=80),  # Adjusted margins
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="sans-serif"
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5,
                bgcolor='rgba(255, 255, 255, 0.8)',
                bordercolor="rgba(0,0,0,0.1)",
                borderwidth=1,
                itemclick="toggleothers",
                itemdoubleclick="toggle"
            )
        )

        # Update axis labels and titles
        fig.update_xaxes(title_text="Date", row=1, col=1)
        fig.update_yaxes(title_text="Total Engagement", row=1, col=1)
        fig.update_xaxes(title_text="Engagement Rate", row=1, col=2)
        fig.update_yaxes(title_text="Count", row=1, col=2)
        fig.update_xaxes(title_text="Impressions", row=2, col=2)
        fig.update_yaxes(title_text="Total Engagement", row=2, col=2)

        return fig