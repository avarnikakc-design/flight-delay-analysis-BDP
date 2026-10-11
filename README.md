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

Execution Guide
Step 1: Launch WSL and Start Hadoop HDFS
Open your WSL/Ubuntu terminal ( window key +R) and start your Hadoop Distributed File System services:
Bash
   start-dfs.sh
Step 2: Verify Active Services
Bash
   jps
Step 3: Navigate to Your Project Directory
Bash
   cd /mnt/c/Users/user/flight_project_repo
Step 4: Run the PySpark Analytics Pipeline
Bash
   spark-submit analyze_terminal.py
# 1. Run the plotting scripts
   spark-submit generate_all_plots.py
   spark-submit generate_root_causes_plot.py
# 2. Open all generated plot images directly in Windows
    explorer.exe monthly_delay.png
    explorer.exe monthly_trend_line.png
    explorer.exe airline_delays_bar.png
    explorer.exe root_causes_bar.png

5.open the interactive dashboard in your Windows web browser:
Bash
   explorer.exe index.html

Suggested Flow for Your Final Review Presentation:
1.The Infrastructure & Logs: Start by running start-dfs.sh and spark-submit analyze_terminal.py to prove the Big Data pipeline runs live on Hadoop HDFS and PySpark.
2.The Visualizations: Run your plotting scripts and pop open the charts using explorer.exe monthly_trend_line.png (and the others) to show statistical breakdowns.
3.The Climax (The Dashboard): Open your live GitHub Pages link or run explorer.exe index.html to show off the fully interactive UI, complete with filters, KPI metric cards, and the interactive Spark CLI terminal drawer!



      
