import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import calendar
from plotly.colors import hex_to_rgb, find_intermediate_color
import base64
from pathlib import Path

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
    df = load_and_standardize_csv(fname)
    current_dfs.append(df)
df_2024 = pd.concat(current_dfs, ignore_index=True)

# Load and concatenate 1990 data
historical_year = 1990
historical_dfs = []
for month in months:
    fname = f"{month}_{historical_year}_temperature_data.csv"
    df = load_and_standardize_csv(fname)
    historical_dfs.append(df)
df_1990 = pd.concat(historical_dfs, ignore_index=True)

# Create a shifted copy of df_1990 for line plots
df_1990_line = df_1990.copy()
df_1990_line['Date'] = df_1990_line['Date'].apply(lambda x: x.replace(year=2024))

# Create a subplot figure
fig = go.Figure()

# Color and style definitions
def rgba(hex_color, alpha):
    rgb = hex_to_rgb(hex_color)
    return f'rgba({rgb[0]},{rgb[1]},{rgb[2]},{alpha})'

current_colors = {
    'Max': '#4A90E2',
    'Min': '#66BB6A',
    'Avg': '#AB47BC',
}
historical_colors = {
    'Max': '#73A3B3',
    'Min': '#A8BFA8',
    'Avg': '#C3A6C7',
}

# --- Enhanced Line Plot Traces (visible by default) ---
# We'll keep track of trace indices for toggling
trace_indices = {
    'line': {'Max': [], 'Avg': [], 'Min': []},
    'box': {'Max': [], 'Avg': [], 'Min': []}
}

# Add current year (2024) traces
for i, (temp_type, col, group) in enumerate([
    ('Max', 'Max Temp', 'Maximum Temperature'),
    ('Avg', 'Avg Temp', 'Average Temperature'),
    ('Min', 'Min Temp', 'Minimum Temperature')
]):
    idx = len(fig.data)
    trace_indices['line'][temp_type].append(idx)
    fig.add_trace(go.Scatter(
        x=df_2024['Date'],
        y=df_2024[col],
        name=f"2024 {temp_type}",
        mode='lines+markers',
        marker=dict(size=2),
        line=dict(color=current_colors[temp_type], width=1),
        legendgroup=group,
        legendgrouptitle_text=group,  # Only first trace in group will show group title
        hovertemplate='%{x|%b %d, %Y}<br>'+temp_type+': %{y}°F<extra></extra>',
        showlegend=True,
        visible=True
    ))

# Add historical year (1990) traces
for i, (temp_type, col, group) in enumerate([
    ('Max', 'Max Temp', 'Maximum Temperature'),
    ('Avg', 'Avg Temp', 'Average Temperature'),
    ('Min', 'Min Temp', 'Minimum Temperature')
]):
    idx = len(fig.data)
    trace_indices['line'][temp_type].append(idx)
    fig.add_trace(go.Scatter(
        x=df_1990_line['Date'],
        y=df_1990_line[col],
        name=f"1990 {temp_type}",
        mode='lines+markers',
        marker=dict(size=1.5),
        line=dict(color=historical_colors[temp_type], width=1, dash='dot'),
        legendgroup=group,
        customdata=df_1990['Date'].dt.strftime('%b %d, %Y'),
        hovertemplate='%{customdata}<br>'+temp_type+': %{y}°F<extra></extra>',
        showlegend=True,
        visible=True
    ))

# --- Monthly Box Plot Traces (hidden by default, new design) ---
import calendar

def interpolate_color(val, vmin, vmax, color1, color2):
    # val in [vmin, vmax] mapped between color1 and color2
    frac = (val - vmin) / (vmax - vmin) if vmax > vmin else 0.5
    return find_intermediate_color(color1, color2, frac, colortype='rgb')

monthly_box_indices_2024 = []
monthly_max_indices_2024 = []
monthly_min_indices_2024 = []
monthly_avg_indices_2024 = []
monthly_box_indices_1990 = []
monthly_max_indices_1990 = []
monthly_min_indices_1990 = []
monthly_avg_indices_1990 = []
box_months = list(range(1, 13))

min_temp = min(df_2024['Min Temp'].min(), df_1990['Min Temp'].min())
max_temp = max(df_2024['Max Temp'].max(), df_1990['Max Temp'].max())

for month in box_months:
    month_name = calendar.month_abbr[month]
    # 2024 data
    month_df_2024 = df_2024[(df_2024['Date'].dt.month == month) & (df_2024['Date'].dt.year == 2024)]
    if not month_df_2024.empty:
        combined_temps_2024 = pd.concat([
            month_df_2024['Max Temp'],
            month_df_2024['Min Temp'],
            month_df_2024['Avg Temp']
        ])
        month_max = combined_temps_2024.max()
        month_min = combined_temps_2024.min()
        month_avg = combined_temps_2024.mean()
        fig.add_trace(go.Box(
            y=combined_temps_2024,
            x=[month_name]*len(combined_temps_2024),
            name=month_name,
            legendgroup=month_name,
            showlegend=True,
            marker_color='#4A90E2',
            line_color='#4A90E2',
            boxmean=False,
            boxpoints=False,
            hoveron='boxes',
            visible=False,
            opacity=0.85,
            customdata=[[month_max, month_min, month_avg]] * len(combined_temps_2024),
            hoverinfo='skip',
            hovertemplate=(
                '<b>%{x}</b><br>' +
                'Max: %{customdata[0]:.1f}°F<br>' +
                'Min: %{customdata[1]:.1f}°F<br>' +
                'Avg: %{customdata[2]:.1f}°F<br>' +
                '<extra></extra>'
            )
        ))
        monthly_box_indices_2024.append(len(fig.data) - 1)
        fig.add_trace(go.Scatter(
            x=[month_name],
            y=[month_avg],
            mode='lines',
            line=dict(color=current_colors['Avg'], width=4),
            name=None,
            legendgroup=month_name,
            showlegend=False,
            visible=False,
            hovertemplate='<b>%{x}</b><br>Avg: %{y:.1f}°F<br><extra></extra>'
        ))
        monthly_avg_indices_2024.append(len(fig.data) - 1)
        fig.add_trace(go.Scatter(
            x=[month_name],
            y=[month_df_2024['Max Temp'].mean()],
            mode='lines',
            line=dict(color=current_colors['Max'], width=4),
            name=None,
            legendgroup=month_name,
            showlegend=False,
            visible=False,
            hovertemplate='<b>%{x}</b><br>Max: %{y:.1f}°F<br><extra></extra>'
        ))
        monthly_max_indices_2024.append(len(fig.data) - 1)
        fig.add_trace(go.Scatter(
            x=[month_name],
            y=[month_df_2024['Min Temp'].mean()],
            mode='lines',
            line=dict(color=current_colors['Min'], width=4),
            name=None,
            legendgroup=month_name,
            showlegend=False,
            visible=False,
            hovertemplate='<b>%{x}</b><br>Min: %{y:.1f}°F<br><extra></extra>'
        ))
        monthly_min_indices_2024.append(len(fig.data) - 1)
    # 1990 data
    month_df_1990 = df_1990[(df_1990['Date'].dt.month == month) & (df_1990['Date'].dt.year == 1990)]
    if not month_df_1990.empty:
        combined_temps_1990 = pd.concat([
            month_df_1990['Max Temp'],
            month_df_1990['Min Temp'],
            month_df_1990['Avg Temp']
        ])
        month_max_90 = combined_temps_1990.max()
        month_min_90 = combined_temps_1990.min()
        month_avg_90 = combined_temps_1990.mean()
        fig.add_trace(go.Box(
            y=combined_temps_1990,
            x=[month_name]*len(combined_temps_1990),
            name=None,
            legendgroup=month_name,
            showlegend=False,
            marker_color='#888888',
            line_color='#888888',
            boxmean=False,
            boxpoints=False,
            hoveron='boxes',
            visible=False,
            opacity=0.7,
            customdata=[[month_max_90, month_min_90, month_avg_90]] * len(combined_temps_1990),
            hoverinfo='skip',
            hovertemplate=(
                '<b>%{x}</b><br>' +
                'Max: %{customdata[0]:.1f}°F<br>' +
                'Min: %{customdata[1]:.1f}°F<br>' +
                'Avg: %{customdata[2]:.1f}°F<br>' +
                '<extra></extra>'
            )
        ))
        monthly_box_indices_1990.append(len(fig.data) - 1)
        fig.add_trace(go.Scatter(
            x=[month_name],
            y=[month_avg_90],
            mode='lines',
            line=dict(color='white', width=4),
            name=None,
            legendgroup=month_name,
            showlegend=False,
            visible=False,
            hovertemplate='<b>%{x}</b><br>Avg: %{y:.1f}°F<br><extra></extra>'
        ))
        monthly_avg_indices_1990.append(len(fig.data) - 1)
        fig.add_trace(go.Scatter(
            x=[month_name],
            y=[month_df_1990['Max Temp'].mean()],
            mode='lines',
            line=dict(color='#AAAAAA', width=4),
            name=None,
            legendgroup=month_name,
            showlegend=False,
            visible=False,
            hovertemplate='<b>%{x}</b><br>Max: %{y:.1f}°F<br><extra></extra>'
        ))
        monthly_max_indices_1990.append(len(fig.data) - 1)
        fig.add_trace(go.Scatter(
            x=[month_name],
            y=[month_df_1990['Min Temp'].mean()],
            mode='lines',
            line=dict(color='#CCCCCC', width=4),
            name=None,
            legendgroup=month_name,
            showlegend=False,
            visible=False,
            hovertemplate='<b>%{x}</b><br>Min: %{y:.1f}°F<br><extra></extra>'
        ))
        monthly_min_indices_1990.append(len(fig.data) - 1)

# --- Highlight Differences Bar Chart (all data, with bar text labels) ---
highlight_months = [2, 6, 7, 8, 9, 10, 12]
highlight_month_names = [calendar.month_abbr[m] for m in highlight_months]
bar_categories = ['Max', 'Avg', 'Min']

# Prepare data structure: {stat: [per month values]}
vals_2024 = {stat: [] for stat in bar_categories}
vals_1990 = {stat: [] for stat in bar_categories}
text_2024 = {stat: [] for stat in bar_categories}
text_1990 = {stat: [] for stat in bar_categories}

for m in highlight_months:
    month_name = calendar.month_abbr[m]
    month_df_2024 = df_2024[(df_2024['Date'].dt.month == m) & (df_2024['Date'].dt.year == 2024)]
    month_df_1990 = df_1990[(df_1990['Date'].dt.month == m) & (df_1990['Date'].dt.year == 1990)]
    for stat, col in zip(bar_categories, ['Max Temp', 'Avg Temp', 'Min Temp']):
        # 2024
        if not month_df_2024.empty:
            val_2024 = month_df_2024[col].max() if stat == 'Max' else (month_df_2024[col].min() if stat == 'Min' else month_df_2024[col].mean())
            text_2024[stat].append(f"2024 {stat}: {val_2024:.1f}°F")
        else:
            val_2024 = np.nan
            text_2024[stat].append("")
        vals_2024[stat].append(val_2024)
        # 1990
        if not month_df_1990.empty:
            val_1990 = month_df_1990[col].max() if stat == 'Max' else (month_df_1990[col].min() if stat == 'Min' else month_df_1990[col].mean())
            text_1990[stat].append(f"1990 {stat}: {val_1990:.1f}°F")
        else:
            val_1990 = np.nan
            text_1990[stat].append("")
        vals_1990[stat].append(val_1990)

# Remove old highlight bar indices
highlight_bar_indices = []

# Add bars: for each stat/year
bar_colors_2024 = {'Max': '#4A90E2', 'Avg': '#AB47BC', 'Min': '#66BB6A'}
bar_colors_1990 = {'Max': '#73A3B3', 'Avg': '#C3A6C7', 'Min': '#A8BFA8'}
for stat in bar_categories:
    # 2024
    idx_2024 = len(fig.data)
    fig.add_trace(go.Bar(
        x=highlight_month_names,
        y=vals_2024[stat],
        name=f'2024 {stat}',
        marker_color=bar_colors_2024[stat],
        opacity=0.9,
        showlegend=True,
        visible=False,
        legendgroup=f'highlight_{stat}',
        hovertemplate='2024 '+stat+'<br>%{x}: %{y:.1f}°F<extra></extra>',
        text=text_2024[stat],
        textposition='auto',
    ))
    highlight_bar_indices.append(idx_2024)
    # 1990
    idx_1990 = len(fig.data)
    fig.add_trace(go.Bar(
        x=highlight_month_names,
        y=vals_1990[stat],
        name=f'1990 {stat}',
        marker_color=bar_colors_1990[stat],
        opacity=0.7,
        showlegend=True,
        visible=False,
        legendgroup=f'highlight_{stat}',
        hovertemplate='1990 '+stat+'<br>%{x}: %{y:.1f}°F<extra></extra>',
        text=text_1990[stat],
        textposition='auto',
    ))
    highlight_bar_indices.append(idx_1990)

# Only bar indices should be visible for highlight differences
all_highlight_indices = highlight_bar_indices

# Remove highlight_annotations from layout (none needed for simple bars)
fig.layout.annotations = [a for a in fig.layout.annotations if not (isinstance(a, dict) and a.get('text', '').startswith('Δ'))]

# --- Add invisible dummy traces for each month to pin all months on the x-axis (with out-of-range y-values)
for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
    fig.add_trace(go.Scatter(
        x=[month],
        y=[-9999],
        mode='markers',
        marker=dict(opacity=0),
        showlegend=False,
        hoverinfo='skip',
        visible=True
    ))

# Map month names to x-axis indices for categorical axis
month_names = [calendar.month_abbr[m] for m in box_months]
month_name_to_idx = {name: idx for idx, name in enumerate(month_names)}

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
)
fig.update_yaxes(
    gridwidth=1,
    gridcolor='rgba(0, 0, 0, 0.1)'
)

# Load header image as base64 so it embeds directly in the HTML
header_image_path = Path("climate vis phoenix header.png")
if header_image_path.exists():
    with open(header_image_path, "rb") as img_file:
        header_image_base64 = base64.b64encode(img_file.read()).decode()
    header_source = f"data:image/png;base64,{header_image_base64}"
else:
    header_source = None  # Fallback – will try path reference

# Define header annotation once so it can be reused in layout updates
header_annotation = dict(
    text="<b>Phoenix Temperature Comparison 1990 vs 2024</b>",
    xref="paper", yref="paper",
    x=0.5, y=1.09,
    showarrow=False,
    font=dict(size=26, family="Arial Black", color="#222"),
    xanchor="center",
    yanchor="top"
)

# Restore trace count variables for updatemenus logic
n_line = sum(len(v) for v in trace_indices['line'].values())
n_box = len(monthly_box_indices_2024) + len(monthly_box_indices_1990)
n_max = len(monthly_max_indices_2024) + len(monthly_max_indices_1990)
n_min = len(monthly_min_indices_2024) + len(monthly_min_indices_1990)
n_avg = len(monthly_avg_indices_2024) + len(monthly_avg_indices_1990)
n_highlight = len(all_highlight_indices)

all_line_indices = [i for v in trace_indices['line'].values() for i in v]
all_box_indices = monthly_box_indices_2024 + monthly_box_indices_1990
all_max_indices = monthly_max_indices_2024 + monthly_max_indices_1990
all_min_indices = monthly_min_indices_2024 + monthly_min_indices_1990
all_avg_indices = monthly_avg_indices_2024 + monthly_avg_indices_1990

# --- Enhanced legend appearance (keep this only, but do NOT increase line width for legend) ---
fig.update_layout(
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=1.05,
        bgcolor='rgba(255, 255, 255, 0.95)',
        bordercolor='rgba(0, 0, 0, 0.3)',
        borderwidth=1,
        font=dict(size=15),
        tracegroupgap=30,
        itemsizing='constant',
        title_font=dict(size=16),
        itemwidth=40,
        itemclick='toggleothers',
        itemdoubleclick='toggle'
    ),
    legend_traceorder='grouped',
)

# --- Layout polish: white background, header, and horizontal tab buttons ---
# Set background to white
fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(t=40)
)

# --- Update updatemenus to horizontal tab-style buttons ---
fig.update_layout(
    updatemenus=[
        dict(
            buttons=[
                dict(
                    label='Line Plot',
                    method='update',
                    args=[
                        {'visible': [i in all_line_indices for i in range(n_line + n_box + n_max + n_min + n_avg + n_highlight + 12)]},
                        {'xaxis': {'type': 'date', 'title': 'Date / Month', 'tickangle': 45, 'automargin': True},
                         'annotations': []}
                    ],
                ),
                dict(
                    label='Monthly Box Plot',
                    method='update',
                    args=[
                        {'visible': [i in (all_box_indices + all_max_indices + all_min_indices + all_avg_indices) for i in range(n_line + n_box + n_max + n_min + n_avg + n_highlight + 12)]},
                        {'xaxis': {'type': 'category', 'title': 'Month', 'categoryorder': 'array', 'automargin': True},
                         'annotations': []},
                    ],
                ),
                dict(
                    label='Highlight Differences',
                    method='update',
                    args=[
                        {'visible': [i in all_highlight_indices for i in range(n_line + n_box + n_max + n_min + n_avg + n_highlight + 12)]},
                        {'xaxis': {'type': 'category', 'title': 'Month', 'automargin': True},
                         'annotations': []},
                    ],
                ),
            ],
            direction='right',  # Horizontal row
            showactive=True,
            x=0.5,
            xanchor='center',
            y=1.06,
            yanchor='top',
            bordercolor="#888",
            bgcolor="#f6f6f6",
            borderwidth=1,
            font=dict(size=16, family="Arial"),
            pad=dict(r=10, t=10, b=10, l=10),
            type='buttons',
        ),
    ]
)

# Set default: show line plot traces only
for i, trace in enumerate(fig.data):
    trace.visible = (i in all_line_indices)

# --- Dash App Layout ---
import dash
from dash import html, dcc

# Make sure the header image is in the 'assets' folder as 'climate-phoenix-header.png'
# If not, move it there for Dash to serve it automatically.

app = dash.Dash(__name__)

app.layout = html.Div([
    # Header image with overlay text (fixed height)
    html.Div([
        html.Img(
            src='/assets/climate-phoenix-header.png',
            style={
                'width': '100%',
                'height': '320px',
                'objectFit': 'cover',
                'filter': 'brightness(0.65)',
                'display': 'block',
                'boxShadow': '0 4px 16px 0 rgba(0,0,0,0.13)'
            },
            alt='Phoenix Climate Header Image'
        ),
        html.Div(
            "Phoenix Temperature Comparison 1990 vs 2024 by Maeve Byrne",
            style={
                'position': 'absolute',
                'top': '50%',
                'left': '50%',
                'transform': 'translate(-50%, -50%)',
                'width': '100%',
                'textAlign': 'center',
                'color': 'white',
                'fontSize': '2.6em',
                'fontWeight': 'bold',
                'textShadow': '2px 2px 8px #000',
                'pointerEvents': 'none',
                'padding': '0 12px',
                'zIndex': 2
            }
        )
    ], style={
        'position': 'relative',
        'height': '320px',
        'overflow': 'hidden',
        'marginBottom': '0px',
        'boxShadow': '0 4px 16px 0 rgba(0,0,0,0.13)'
    }),

    # Intro/Explanation section above the data
    html.Div([
        html.H2("About This Visualization", style={'color': '#1E3D59', 'fontWeight': 'bold', 'marginBottom': '18px'}),
        html.P("This data shows the monthly maximum, minimum, and average temperature of the Phoenix Metropolitan area for the years 2024 and 1990. Can you see how the temperature has changed over the last 25 years?", style={'fontSize': '1.18em', 'margin': 'auto', 'maxWidth': '700px'}),
        html.H4("What do the tabs show?", style={'color': '#2E7D32', 'marginTop': '28px'}),
        html.Ul([
            html.Li([
                html.B("Line Plot: "),
                "Overarching view of the maximum, minimum, and average temperatures for both years."
            ]),
            html.Li([
                html.B("Monthly Box Plot: "),
                "Comparison of averaged daily temperatures for each month."
            ]),
            html.Li([
                html.B("Highlight Differences: "),
                "Key differences in temperature statistics between the two years."
            ]),
        ], style={'textAlign': 'left', 'maxWidth': '700px', 'margin': '24px auto', 'fontSize': '1.08em'})
    ], style={
        'background': '#e7f0fa',  # Soft blue
        'padding': '36px 0 24px 0',
        'textAlign': 'center',
        'borderRadius': '0 0 18px 18px',
        'marginBottom': '28px',
        'boxShadow': '0 2px 8px 0 rgba(30,61,89,0.06)'
    }),

    # Data section fills the viewport after scroll
    html.Div([
        dcc.Graph(
            figure=fig,
            id='temperature-plot',
            style={
                'height': '80vh',  # Responsive height
                'width': '100%',
            },
            config={
                'responsive': True
            }
        )
    ], style={
        'width': '90vw',
        'maxWidth': '1200px',
        'minHeight': '80vh',
        'margin': '0 auto',
        'display': 'flex',
        'alignItems': 'center',
        'justifyContent': 'center',
        'paddingTop': '48px',
        'paddingBottom': '48px'
    }),

    # Resources section below the data
    html.Div([
        html.H2("Further Resources", style={'color': '#2E7D32', 'fontWeight': 'bold', 'marginBottom': '18px'}),
        html.Div([
            html.Iframe(
                src="https://www.youtube.com/embed/ZQ6fSHr5TJg",
                style={'width': '100%', 'height': '360px', 'border': 'none', 'borderRadius': '12px', 'maxWidth': '700px', 'margin': 'auto', 'display': 'block'}
            )
        ], style={'maxWidth': '700px', 'margin': 'auto'}),
        html.H4("Explore More:"),
        html.Ul([
            html.Li(html.A("National Weather Service: Phoenix", href="https://www.weather.gov/psr/", target="_blank")),
            html.Li(html.A("Climate Data Online", href="https://www.ncdc.noaa.gov/cdo-web/", target="_blank")),
            html.Li(html.A("City of Phoenix Sustainability Department", href="https://www.phoenix.gov/administration/departments/sustainability.html", target="_blank"))
        ], style={'listStyleType': 'none', 'padding': 0, 'fontSize': '1.08em', 'margin': '24px auto', 'maxWidth': '700px'}),
    ], style={
        'background': '#e8f5e9',  # Soft green
        'padding': '36px 0 36px 0',
        'textAlign': 'center',
        'borderRadius': '18px 18px 0 0',
        'marginTop': '32px',
        'boxShadow': '0 -2px 8px 0 rgba(46,125,50,0.09)'
    })
])

if __name__ == '__main__':
    # --- Export complete interactive visualization ---
    import plotly.io as pio
    import webbrowser
    
    # Configure HTML export
    config = {
        'scrollZoom': True,
        'displayModeBar': True,
        'responsive': True
    }
    
    # Export to HTML with all data included
    pio.write_html(
        fig, 
        "final-temperature-visualization.html",
        config=config,
        auto_open=True,
        include_plotlyjs='cdn',  # Smaller file size
        full_html=True,
        include_mathjax='cdn'
    )
    print("Complete visualization saved to final-temperature-visualization.html")
    port = int(os.environ.get("PORT", 8051))
    app.run(debug=True, host="0.0.0.0", port=port)
