# Custom Visualization Instructions

## How to Replace with Your Own Visualization

1. **Backup your files first:** Keep a copy of the existing files in case you need to reference them.

2. **Replace the files:** Replace the following files with your own:
   - `visualization.js`: Your main visualization code
   - `style.css` (optional): Your custom styles
   - `index.html` (optional): If you need to change the HTML structure

3. **Working with temperature_data.csv:** 
   - The `temperature_data.csv` file should be placed in the main `/public` folder
   - If your file uses a different name or path, update the fetch path in your visualization code

4. **Keep the iframe integration:** 
   - The main website uses an iframe to display your visualization
   - Make sure your visualization works well within an iframe

5. **Responsiveness:**
   - Ensure your visualization is responsive and works on different screen sizes

## File Structure

\`\`\`
public/
├── temperature_data.csv
├── custom-visualization/
│   ├── index.html
│   ├── style.css
│   ├── visualization.js
│   └── README.md (this file)
\`\`\`

## Tips for Integration

- Keep the controls (buttons) if you're implementing multiple visualization types
- Update the error handling as needed for your visualization
- If you need additional libraries or dependencies, add them to the `index.html` file
