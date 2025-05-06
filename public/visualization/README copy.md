# Phoenix Temperature Visualization

This project visualizes Phoenix's temperature data (Max, Min, Avg) for 2024 and 1990 using an interactive Dash web app.

## Features
- Interactive line, box, and bar plots for temperature comparison
- Modern color schemes and readable layouts
- Tabs for switching between plot types
- Hover tooltips, grouped legends, and responsive design

## Setup
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Add your data:**
   - Place CSV files named like `january_2024_temperature_data.csv`, `february_1990_temperature_data.csv`, etc. in this directory.
   - Each CSV should have columns: `Date, Max Temp, Min Temp, Avg Temp` (or `Max Temperature`, etc. — both are supported).

## Run Locally
```bash
python temperature_visualization.py
```
Then open [http://127.0.0.1:8051/](http://127.0.0.1:8051/) in your browser.

## Deploy Online
To deploy online (e.g., Heroku, PythonAnywhere), ask for deployment instructions.

## Credits
- Visualization by Maeve Byrne
- Built with Dash, Plotly, and Python
    - Hover information with date and temperature
    - Clickable legend and grouped toggling
    - Toggle between line plot, monthly box plot, and highlight differences

## Sharing/Portability

- All file paths are **relative**; you can move or share the entire folder without breaking the script.
- To share, simply zip the folder and send it (or upload to a repository).
- Recipients need only install dependencies and run `python temperature_visualization.py`.

## License

MIT License (or specify your own)
