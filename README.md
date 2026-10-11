# Hadoop HDFS & Spark Flight Delay Pipeline

End-to-end Big Data workflow processing 5.8M+ flight records (592MB) using Apache Hadoop HDFS and PySpark 3.5.3 in WSL2. This repository features modular analytics scripts, execution logging, automated Matplotlib visualizations, and an interactive web dashboard.

## 📊 Live Web Dashboard
Explore the live, interactive Big Data Flight Delay Analysis dashboard hosted via GitHub Pages:
👉 **[View Live Dashboard](https://avarnikakc-design.github.io/flight-delay-analysis-BDP/)**

## Tech Stack
- **Big Data Engine:** Apache Hadoop HDFS, Apache Spark 3.5.3
- **Frontend & Visualization:** HTML5, Tailwind CSS, Chart.js, GitHub Pages
- **Environment:** WSL2 (Ubuntu on Windows)
- **Languages & Libraries:** Python, PySpark, Pandas, Matplotlib

## Dataset
This pipeline processes large-scale flight performance data. You can access and download the underlying dataset here:
- **Dataset Source:** [Kaggle US Flight Delays and Performance Data](https://www.kaggle.com/datasets/usdot/flight-delays)

## Project Structure
```text
flight-delay-analysis-BDP/
│
├── index.html                     # Interactive Tailwind CSS and Chart.js web dashboard
├── analyze_terminal.py            # Core PySpark script for terminal metric extractions
├── generate_plots.py              # Initial plotting pipeline for performance graphs
├── generate_all_plots.py          # Comprehensive multi-variable plotting script
├── generate_root_causes_plot.py   # Specialized script isolating delay factors (weather, carrier, etc.)
│
├── terminal_output.txt            # Execution logs captured from terminal runs
│
├── monthly_delay.png              # Average departure delay by month (bar chart)
├── monthly_trend_line.png         # Temporal progression of delays (trend line)
├── airline_delays_bar.png         # Comparative delay breakdown across major carriers
├── root_causes_bar.png            # Root-cause distribution of delay factors
│
└── README.md                      # Project documentation and execution guide

Visualization Assets
The repository tracks generated visual artifacts for immediate reporting:
      monthly_delay.png: Monthly average departure delay bar chart.
      monthly_trend_line.png: Temporal progression of delays across months.
      airline_delays_bar.png: Comparative delay breakdown across major carriers.
      root_causes_bar.png: Root-cause distribution of delay factors.
