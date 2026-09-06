# Hadoop HDFS & Spark Flight Delay Pipeline

End-to-end Big Data workflow processing 5.8M+ flight records (592MB) using Apache Hadoop HDFS and PySpark 3.5.3 in WSL2. This repository features modular analytics scripts, execution logging, and automated Matplotlib visualizations highlighting monthly trends, carrier comparisons, and delay root causes.

## Tech Stack
* **Big Data Engine:** Apache Hadoop HDFS, Apache Spark 3.5.3
* **Environment:** WSL2 (Ubuntu on Windows)
* **Languages & Libraries:** Python, PySpark, Pandas, Matplotlib

## Dataset
This pipeline processes large-scale flight performance data. You can access and download the underlying dataset here:
* **Dataset Source:** [Kaggle US Flight Delays and Performance Data](https://www.kaggle.com/datasets/usdot/flight-delays)

## Project Structure
* `analyze_terminal.py`: Core PySpark script for processing terminal-based data extractions and metrics.
* `generate_plots.py`: Basic plotting pipeline for generating initial trend lines and performance graphs.
* `generate_all_plots.py`: Comprehensive plotting suite covering multiple variables simultaneously.
* `generate_root_causes_plot.py`: Specialized script isolating delay factors (weather, carrier, system, security).
* `terminal_output.txt`: Captured logs of pipeline execution runs.

## Visualization Assets
The repository tracks generated visual artifacts for immediate reporting:
* `monthly_delay.png`: Monthly average departure delay bar chart.
* `monthly_trend_line.png`: Temporal progression of delays across months.
* `airline_delays_bar.png`: Comparative delay breakdown across major carriers.
* `root_causes_bar.png`: Root-cause distribution of delay factors.
  flight-delay-analysis-BDP/
│
├── analyze_terminal.py              # Core PySpark script for terminal metric extractions
├── generate_plots.py                # Initial plotting pipeline for performance graphs
├── generate_all_plots.py            # Comprehensive multi-variable plotting script
├── generate_root_causes_plot.py     # Specialized script isolating delay factors (weather, carrier, etc.)
│
├── terminal_output.txt              # Execution logs captured from terminal runs
│
├── monthly_delay.png                # Average departure delay by month (bar chart)
├── monthly_trend_line.png           # Temporal progression of delays (trend line)
├── airline_delays_bar.png           # Comparative delay breakdown across major carriers
├── root_causes_bar.png              # Root-cause distribution of delay factors
│
└── README.md                        # Project documentation and execution guide

## Execution Guide
1. Ensure Hadoop HDFS and Spark are running in your WSL2 environment:
   ```bash
   start-dfs.sh
Upload the flight dataset to HDFS:

Bash
hdfs dfs -mkdir -p /bigdata/flight_project/input
hdfs dfs -put flights.csv /bigdata/flight_project/input/
Run the analysis or plotting scripts using Spark:

Bash
spark-submit analyze_terminal.py
spark-submit generate_all_plots.py
spark-submit generate_root_causes_plot.py
