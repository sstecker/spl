import numpy as np
import plotly.graph_objects as go

# Define ranges
sensitivity = np.arange(84, 99, 1)  # Even values from 84 to 98 dB
target_db = np.arange(84, 125, 1)   # 84 to 124 dB
sensitivity_mesh, target_db_mesh = np.meshgrid(sensitivity, target_db)

# Calculate watts required: Watts = 10^((Target_dB - Sensitivity)/10)
watts = 10 ** ((target_db_mesh - sensitivity_mesh) / 10)

# Define discrete colorscale: green (<100), yellow (101-200), red (>200)
colorscale = [
    [0.0, 'rgb(0, 255, 0)'],      # Green for watts <= 100
    [100/1000, 'rgb(0, 255, 0)'], # Green up to 100 watts
    [100/1000, 'rgb(255, 255, 0)'], # Yellow starts at 101 watts
    [200/1000, 'rgb(255, 255, 0)'], # Yellow up to 200 watts
    [200/1000, 'rgb(255, 0, 0)'],   # Red starts at 201 watts
    [1.0, 'rgb(255, 0, 0)']        # Red for watts > 200
]

# Normalize watts for colorscale (map to [0, 1] based on max watts)
watts_max = np.max(watts)
watts_normalized = watts / watts_max if watts_max > 0 else watts

# Create 3D surface plot
fig = go.Figure(data=[
    go.Surface(
        x=sensitivity,
        y=target_db,
        z=watts,
        surfacecolor=watts,  # Map color to watts
        colorscale=colorscale,
        colorbar=dict(
            title='Watts Required',
            title_side='right',
            tickmode='array',
            tickvals=[0, 100, 200, 500],  # Key wattage thresholds
            ticktext=['0', '100', '200', '>200'],
            ticks='outside'
        ),
        cmin=0,
        cmax=1000  # Set to cover range of watts (max ~1000 for visibility)
    )
])

# Update layout
fig.update_layout(
    title='Watts Required for Target SPL',
    scene=dict(
        xaxis_title='Speaker Sensitivity (dB @ 1W)',
        yaxis_title='Target SPL (dB)',
        zaxis=dict(
            title='Watts Required',
            type='log'  # Log scale for watts
        )
    ),
    width=800,
    height=600,
    margin=dict(l=50, r=50, b=50, t=50)
)

# Save to HTML
fig.write_html('spl_watts_chart.html')