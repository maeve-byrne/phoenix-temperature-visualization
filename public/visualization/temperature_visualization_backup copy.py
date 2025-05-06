import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime

# Helper function to load and standardize a month's data
def load_and_standardize_csv(filename):
    df = pd.read_csv(filename)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.rename(columns={
        'Max Temperature': 'Max Temp',
        'Min Temperature': 'Min Temp',
        'Avg Temperature': 'Avg Temp'
    })
    return df

# List of months for file naming
months = [
    'january', 'february', 'march', 'april', 'may', 'june',
    'july', 'august', 'september', 'october', 'november', 'december'
]

# Load and concatenate 2024 data
current_year = 2024
current_dfs = []
for month in months:
    fname = f"{month}_{current_year}_temperature_data.csv"
    current_dfs.append(load_and_standardize_csv(fname))
df_2024 = pd.concat(current_dfs, ignore_index=True)

# Load and concatenate 1990 data
historical_year = 1990
historical_dfs = []
for month in months:
    fname = f"{month}_{historical_year}_temperature_data.csv"
    historical_dfs.append(load_and_standardize_csv(fname))
df_1990 = pd.concat(historical_dfs, ignore_index=True)

# Adjust historical dates to 2024 for comparison
# (keeps month and day, changes year)
df_1990['Date'] = df_1990['Date'].apply(lambda x: x.replace(year=2024))

# Create subplot figure
fig = make_subplots(
    rows=1, cols=1,
)

# Define colors for temperature traces
# (You can further expand this for min/avg, or use memory color schemes)
temp_colors = {
    'Max': {
        'current': '#4A90E2',  # Light blue
        'historical': '#73A3B3'  # Grey-blue
    },
    'Min': {
        'current': '#66BB6A',  # Light green
        'historical': '#A8BFA8'  # Grey-green
    },
    'Avg': {
        'current': '#AB47BC',  # Light purple
        'historical': '#C3A6C7'  # Grey-purple
    }
}

# Add current data
current_data = [
    ('2024', df_2024)
]

for year_label, df in current_data:
    # Maximum temperature
    fig.add_trace(
        go.Scatter(
            x=df['Date'],
            y=df['Max Temp'],
            name=f'{year_label} Maximum',
            line=dict(color=temp_colors['Max']['current'], width=2.5),
            mode='lines+markers',
            marker=dict(size=8),
            legendgroup='max',
            legendgrouptitle_text="Maximum Temperature",
            hovertemplate='%{x|%B %d}<br>Maximum: %{y}°F<extra></extra>'
        )
    )
    
    # Average temperature
    fig.add_trace(
        go.Scatter(
            x=df['Date'],
            y=df['Avg Temp'],
            name=f'{year_label} Average',
            line=dict(color=temp_colors['Avg']['current'], width=2.5),
            mode='lines+markers',
            marker=dict(size=8),
            legendgroup='avg',
            legendgrouptitle_text="Average Temperature",
            hovertemplate='%{x|%B %d}<br>Average: %{y}°F<extra></extra>'
        )
    )
    
    # Minimum temperature
    fig.add_trace(
        go.Scatter(
            x=df['Date'],
            y=df['Min Temp'],
            name=f'{year_label} Minimum',
            line=dict(color=temp_colors['Min']['current'], width=2.5),
            mode='lines+markers',
            marker=dict(size=8),
            legendgroup='min',
            legendgrouptitle_text="Minimum Temperature",
            hovertemplate='%{x|%B %d}<br>Minimum: %{y}°F<extra></extra>'
        )
    )

# Add historical data
historical_data = [
    ('1990', df_1990)
]

for year_label, df in historical_data:
    # Maximum temperature
    fig.add_trace(
        go.Scatter(
            x=df['Date'],
            y=df['Max Temp'],
            name=f'{year_label} Maximum',
            line=dict(
                color=temp_colors['Max']['historical'],
                width=2,
                dash='dot'
            ),
            mode='lines+markers',
            marker=dict(size=6),
            legendgroup='max',
            showlegend=True,
            hovertemplate='%{x|%B %d}<br>Maximum: %{y}°F<extra></extra>'
        )
    )
    
    # Average temperature
    fig.add_trace(
        go.Scatter(
            x=df['Date'],
            y=df['Avg Temp'],
            name=f'{year_label} Average',
            line=dict(
                color=temp_colors['Avg']['historical'],
                width=2,
                dash='dot'
            ),
            mode='lines+markers',
            marker=dict(size=6),
            legendgroup='avg',
            showlegend=True,
            hovertemplate='%{x|%B %d}<br>Average: %{y}°F<extra></extra>'
        )
    )
    
    # Minimum temperature
    fig.add_trace(
        go.Scatter(
            x=df['Date'],
            y=df['Min Temp'],
            name=f'{year_label} Minimum',
            line=dict(
                color=temp_colors['Min']['historical'],
                width=2,
                dash='dot'
            ),
            mode='lines+markers',
            marker=dict(size=6),
            legendgroup='min',
            showlegend=True,
            hovertemplate='%{x|%B %d}<br>Minimum: %{y}°F<extra></extra>'
        )
    )

# Update layout
fig.update_layout(
    title={
        'text': '<b>Temperature Comparison: 1990 vs 2024</b>',
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(size=24)
    },
    xaxis_title='<b>Date</b>',
    yaxis_title='<b>Temperature (°F)</b>',
    showlegend=True,
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=1.05,
        bgcolor='rgba(255, 255, 255, 0.9)',
        bordercolor='rgba(0, 0, 0, 0.3)',
        borderwidth=1,
        font=dict(size=12),
        tracegroupgap=30,
        itemsizing='constant'
    ),
    hoverlabel=dict(
        bgcolor="white",
        font_size=14,
        font_family="Arial"
    ),
    xaxis=dict(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(200, 200, 200, 0.3)',
        tickformat='%b %d',
        title='<b>Date</b>'
    ),
    yaxis=dict(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(200, 200, 200, 0.3)',
        tickfont=dict(size=12),
        ticksuffix='°F',
        title='<b>Temperature (°F)</b>'
    ),
    margin=dict(r=200, t=100),
    plot_bgcolor='white',
    hovermode='x unified',
    updatemenus=[
        dict(
            type="buttons",
            direction="left",
            buttons=list([
                dict(
                    args=[{"visible": [True, True, True, True, True, True]}],
                    label="All",
                    method="update"
                ),
                dict(
                    args=[{"visible": [True, False, False, True, False, False]}],
                    label="Maximum",
                    method="update"
                ),
                dict(
                    args=[{"visible": [False, True, False, False, True, False]}],
                    label="Average",
                    method="update"
                ),
                dict(
                    args=[{"visible": [False, False, True, False, False, True]}],
                    label="Minimum",
                    method="update"
                )
            ]),
            pad={"r": 10, "t": 70},
            showactive=True,
            x=0.11,
            xanchor="right",
            y=1.15,
            yanchor="top"
        )
    ]
)

# Alternate month shading for clarity
min_temp = min(
    df_2024['Min Temp'].min(),
    df_1990['Min Temp'].min()
)
max_temp = max(
    df_2024['Max Temp'].max(),
    df_1990['Max Temp'].max()
)
for month in range(1, 13):
    if month % 2 == 0:  # Shade only even months
        fig.add_shape(
            type="rect",
            x0=pd.Timestamp(f"2024-{month:02d}-01"),
            x1=pd.Timestamp(f"2024-{month % 12 + 1:02d}-01"),  # Next month
            y0=min_temp - 2,
            y1=max_temp + 2,
            fillcolor="rgba(200,200,200,0.15)",
            layer="below",
            line_width=0,
        )

# Update axes
fig.update_xaxes(
    gridwidth=1,
    gridcolor='rgba(0, 0, 0, 0.1)',
    tickformat='%b',  # Only show month abbreviation
    tickfont=dict(size=8),  # Even smaller font
    tickangle=45,  # Slightly less steep for readability
    tickmode='array',
    tickvals=[pd.Timestamp(f'2024-{month:02d}-01') for month in range(1, 13)],
    range=[pd.Timestamp('2023-12-15'), pd.Timestamp('2025-01-15')],
)
fig.update_yaxes(
    gridwidth=1,
    gridcolor='rgba(0, 0, 0, 0.1)'
)

# Clean up hover labels and make plot less crowded
fig.update_traces(
    hoverlabel=dict(bgcolor="white", font_size=11, font_family="Arial"),
    marker=dict(size=3, opacity=0.5),  # Much smaller and more transparent markers
    line=dict(width=1),                # Only width here
    opacity=0.9                        # Less transparent (closer to fully opaque)
)

# Show the figure
fig.show()
