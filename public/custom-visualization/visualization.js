// This is a placeholder file for your custom visualization
// Replace this file with your own visualization code

document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM loaded - ready for visualization")

  // Button references
  const lineChartBtn = document.getElementById("line-chart-btn")
  const boxPlotBtn = document.getElementById("box-plot-btn")
  const barGraphBtn = document.getElementById("bar-graph-btn")

  // Chart type state
  let currentChartType = "line"

  // Button event listeners
  lineChartBtn.addEventListener("click", () => {
    setActiveButton(lineChartBtn)
    currentChartType = "line"
    loadVisualization(currentChartType)
  })

  boxPlotBtn.addEventListener("click", () => {
    setActiveButton(boxPlotBtn)
    currentChartType = "box"
    loadVisualization(currentChartType)
  })

  barGraphBtn.addEventListener("click", () => {
    setActiveButton(barGraphBtn)
    currentChartType = "bar"
    loadVisualization(currentChartType)
  })

  function setActiveButton(activeButton) {
    // Remove active class from all buttons
    ;[lineChartBtn, boxPlotBtn, barGraphBtn].forEach((btn) => {
      btn.classList.remove("active")
    })
    // Add active class to the clicked button
    activeButton.classList.add("active")
  }

  function loadVisualization(chartType) {
    document.getElementById("loading-message").style.display = "block"

    // Load your temperature data (this part should be customized for your data format)
    fetch("/temperature_data.csv")
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`)
        }
        return response.text()
      })
      .then((csvText) => {
        console.log("CSV data loaded successfully")
        // Parse your data and create the visualization
        createPlaceholderVisualization(chartType)
        document.getElementById("loading-message").style.display = "none"
      })
      .catch((error) => {
        console.error("Error loading CSV:", error)
        document.getElementById("loading-message").style.display = "none"
        document.getElementById("error-message").textContent = "Error loading temperature data: " + error.message
        document.getElementById("error-message").style.display = "block"
      })
  }

  function createPlaceholderVisualization(chartType) {
    // This is where you'd replace with your custom visualization code

    let traces = []
    let layout = {}

    if (chartType === "line") {
      traces = [
        {
          x: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
          y: [70, 75, 80, 90, 95, 100, 105, 110, 105, 95, 85, 75],
          type: "scatter",
          mode: "lines+markers",
          name: "Temperature",
        },
      ]

      layout = {
        title: "Temperature Visualization (Placeholder)",
        xaxis: { title: "Month" },
        yaxis: { title: "Temperature (°F)" },
      }
    } else if (chartType === "box") {
      traces = [
        {
          y: [70, 75, 80, 90, 95, 100, 105, 110, 105, 95, 85, 75],
          type: "box",
          name: "Temperature",
        },
      ]

      layout = {
        title: "Temperature Distribution (Placeholder)",
        yaxis: { title: "Temperature (°F)" },
      }
    } else if (chartType === "bar") {
      traces = [
        {
          x: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
          y: [70, 75, 80, 90, 95, 100, 105, 110, 105, 95, 85, 75],
          type: "bar",
          name: "Temperature",
        },
      ]

      layout = {
        title: "Monthly Temperatures (Placeholder)",
        xaxis: { title: "Month" },
        yaxis: { title: "Temperature (°F)" },
      }
    }

    if (typeof Plotly !== "undefined") {
      Plotly.newPlot("plotly-container", traces, layout, { responsive: true })
    } else {
      console.error("Plotly is not defined. Make sure it is properly loaded.")
    }
  }

  // Load the default visualization
  loadVisualization(currentChartType)
})
