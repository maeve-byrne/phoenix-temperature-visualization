import pandas as pd
import plotly.graph_objects as go

# Read the recent CSV files
df_dec_24 = pd.read_csv('december_2024_temperature_data.csv')

# Rename columns to match the data format
df_dec_24 = df_dec_24.rename(columns={
    'Max Temperature': 'Max Temp',
    'Min Temperature': 'Min Temp',
    'Avg Temperature': 'Avg Temp'
})

# Read the historical CSV files
df_jan_91 = pd.read_csv('january_1991_temperature_data.csv')
df_dec_90 = pd.read_csv('december_1990_temperature_data.csv')

# Convert all dates to datetime
df_dec_24['Date'] = pd.to_datetime(df_dec_24['Date'])
df_jan_91['Date'] = pd.to_datetime(df_jan_91['Date'])
df_dec_90['Date'] = pd.to_datetime(df_dec_90['Date'])

# Create a copy of December data for January (shifting dates)
df_jan_25 = df_dec_24.copy()
df_jan_25['Date'] = df_jan_25['Date'] + pd.DateOffset(months=1)

# Rename columns to match the data format
df_jan_25 = df_jan_25.rename(columns={
    'Max Temperature': 'Max Temp',
    'Min Temperature': 'Min Temp',
    'Avg Temperature': 'Avg Temp'
})

# Adjust historical dates to overlay with current dates
df_dec_90['Adjusted_Date'] = pd.to_datetime('2024-12-' + df_dec_90['Date'].dt.strftime('%d'))
df_jan_91['Adjusted_Date'] = pd.to_datetime('2025-01-' + df_jan_91['Date'].dt.strftime('%d'))

# Rename columns to match the data format
df_jan_91 = df_jan_91.rename(columns={
    'Max Temperature': 'Max Temp',
    'Min Temperature': 'Min Temp',
    'Avg Temperature': 'Avg Temp'
})
df_dec_90 = df_dec_90.rename(columns={
    'Max Temperature': 'Max Temp',
    'Min Temperature': 'Min Temp',
    'Avg Temperature': 'Avg Temp'
})

# Create an interactive plot
fig = go.Figure()

# Color definitions
colors = {
    'max': {
        'recent': '#9C27B0',  # Bright purple
        'historical': '#6A1B9A'  # Dark purple
    },
    'min': {
        'recent': '#4CAF50',  # Bright green
        'historical': '#1B5E20'  # Dark green
    },
    'avg': {
        'recent': '#2196F3',  # Bright blue
        'historical': '#0D47A1'  # Dark blue
    }
}

# December 2024 data (solid lines)
fig.add_trace(
    go.Scatter(x=df_dec_24['Date'], y=df_dec_24['Max Temp'],
               name='Maximum (2024-25)',
               line=dict(color=colors['max']['recent']), mode='lines+markers',
               legendgroup='max', showlegend=True)
)
fig.add_trace(
    go.Scatter(x=df_dec_24['Date'], y=df_dec_24['Min Temp'],
               name='Minimum (2024-25)',
               line=dict(color=colors['min']['recent']), mode='lines+markers',
               legendgroup='min', showlegend=True)
)
fig.add_trace(
    go.Scatter(x=df_dec_24['Date'], y=df_dec_24['Avg Temp'],
               name='Average (2024-25)',
               line=dict(color=colors['avg']['recent']), mode='lines+markers',
               legendgroup='avg', showlegend=True)
)

# January 2025 data (solid lines)
fig.add_trace(
    go.Scatter(x=df_jan_25['Date'], y=df_jan_25['Max Temp'],
               name='Maximum (2024-25)',
               line=dict(color=colors['max']['recent']), mode='lines+markers',
               legendgroup='max', showlegend=False)
)
fig.add_trace(
    go.Scatter(x=df_jan_25['Date'], y=df_jan_25['Min Temp'],
               name='Minimum (2024-25)',
               line=dict(color=colors['min']['recent']), mode='lines+markers',
               legendgroup='min', showlegend=False)
)
fig.add_trace(
    go.Scatter(x=df_jan_25['Date'], y=df_jan_25['Avg Temp'],
               name='Average (2024-25)',
               line=dict(color=colors['avg']['recent']), mode='lines+markers',
               legendgroup='avg', showlegend=False)
)

# December 1990 data (dotted lines)
fig.add_trace(
    go.Scatter(x=df_dec_90['Adjusted_Date'], y=df_dec_90['Max Temp'],
               name='Maximum (1990-91)',
               line=dict(color=colors['max']['historical'], dash='dot'), mode='lines+markers',
               legendgroup='max', showlegend=True)
)
fig.add_trace(
    go.Scatter(x=df_dec_90['Adjusted_Date'], y=df_dec_90['Min Temp'],
               name='Minimum (1990-91)',
               line=dict(color=colors['min']['historical'], dash='dot'), mode='lines+markers',
               legendgroup='min', showlegend=True)
)
fig.add_trace(
    go.Scatter(x=df_dec_90['Adjusted_Date'], y=df_dec_90['Avg Temp'],
               name='Average (1990-91)',
               line=dict(color=colors['avg']['historical'], dash='dot'), mode='lines+markers',
               legendgroup='avg', showlegend=True)
)

# January 1991 data (dotted lines)
fig.add_trace(
    go.Scatter(x=df_jan_91['Adjusted_Date'], y=df_jan_91['Max Temp'],
               name='Maximum (1990-91)',
               line=dict(color=colors['max']['historical'], dash='dot'), mode='lines+markers',
               legendgroup='max', showlegend=False)
)
fig.add_trace(
    go.Scatter(x=df_jan_91['Adjusted_Date'], y=df_jan_91['Min Temp'],
               name='Minimum (1990-91)',
               line=dict(color=colors['min']['historical'], dash='dot'), mode='lines+markers',
               legendgroup='min', showlegend=False)
)
fig.add_trace(
    go.Scatter(x=df_jan_91['Adjusted_Date'], y=df_jan_91['Avg Temp'],
               name='Average (1990-91)',
               line=dict(color=colors['avg']['historical'], dash='dot'), mode='lines+markers',
               legendgroup='avg', showlegend=False)
)

# Add month selector traces
fig.add_trace(
    go.Scatter(x=[None], y=[None],
               name='December',
               line=dict(color='black'), mode='lines',
               legendgroup='month', showlegend=True)
)
fig.add_trace(
    go.Scatter(x=[None], y=[None],
               name='January',
               line=dict(color='black', dash='dot'), mode='lines',
               legendgroup='month', showlegend=True)
)

# Find max temperatures for annotation placement
max_temp_2024 = max(df_dec_24['Max Temp'].max(), df_jan_25['Max Temp'].max())
max_temp_1990 = max(df_dec_90['Max Temp'].max(), df_jan_91['Max Temp'].max())

# Add year annotations
fig.add_annotation(
    x=df_dec_24['Date'].iloc[0],
    y=max_temp_2024 + 2,
    text='**2024-25**',
    showarrow=False,
    font=dict(size=14, color='black')
)
fig.add_annotation(
    x=df_dec_90['Adjusted_Date'].iloc[0],
    y=max_temp_1990 + 2,
    text='**1990-91**',
    showarrow=False,
    font=dict(size=14, color='black')
)

# Update layout
fig.update_layout(
    title='Temperature Comparison: Winter 1990-91 vs 2024-25',
    xaxis_title='Date',
    yaxis_title='Temperature (°F)',
    hovermode='x unified',
    template='plotly_white',
    legend=dict(
        yanchor="top",
        y=-0.2,  # Move legend below the plot
        xanchor="center",
        x=0.5,
        orientation="h",  # Horizontal legend
        groupclick="toggleitem"
    ),
    margin=dict(b=100),  # Add bottom margin for legend
    plot_bgcolor='white'
)

# Add grid lines
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#E5E5E5')
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#E5E5E5')

# Save the plot to an HTML file
fig.write_html('temperature_data_plotter.html')

# Show the plot
fig.show()
