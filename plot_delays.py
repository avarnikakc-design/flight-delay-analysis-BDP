from pyspark.sql import SparkSession
import matplotlib.pyplot as plt
import seaborn as sns

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("FlightDelay_Plotting") \
    .getOrCreate()

flights_df = spark.read.option("header", "true").option("inferSchema", "true") \
    .csv("hdfs://localhost:9000/bigdata/flight_project/input/flights.csv")
flights_df.createOrReplaceTempView("flights")

# Set overall plot style
sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(3, 1, figsize=(10, 15))

# --- 1. Top 5 Airlines Delay Comparison ---
airline_df = spark.sql("""
    SELECT 
        AIRLINE, 
        ROUND(AVG(DEPARTURE_DELAY), 2) as avg_dep_delay,
        ROUND(AVG(ARRIVAL_DELAY), 2) as avg_arr_delay
    FROM flights
    GROUP BY AIRLINE
    ORDER BY avg_dep_delay DESC
    LIMIT 5
""").toPandas()

airline_melted = airline_df.melt(id_vars="AIRLINE", value_vars=["avg_dep_delay", "avg_arr_delay"], 
                                  var_name="Delay_Type", value_name="Minutes")
sns.barplot(data=airline_melted, x="AIRLINE", y="Minutes", hue="Delay_Type", ax=axes[0], palette="Set2")
axes[0].set_title("Top 5 Airlines: Average Departure vs Arrival Delays")
axes[0].set_xlabel("Airline Code")
axes[0].set_ylabel("Average Delay (Minutes)")

# --- 2. Monthly Delay Trend ---
monthly_df = spark.sql("""
    SELECT
        MONTH,
        ROUND(AVG(DEPARTURE_DELAY), 2) as avg_dep_delay,
        ROUND(AVG(ARRIVAL_DELAY), 2) as avg_arr_delay
    FROM flights
    GROUP BY MONTH
    ORDER BY MONTH ASC
""").toPandas()

axes[1].plot(monthly_df["MONTH"], monthly_df["avg_dep_delay"], marker='o', label="Departure Delay", color="coral", linewidth=2)
axes[1].plot(monthly_df["MONTH"], monthly_df["avg_arr_delay"], marker='s', label="Arrival Delay", color="royalblue", linewidth=2)
axes[1].set_title("Average Flight Delays by Month")
axes[1].set_xlabel("Month")
axes[1].set_ylabel("Average Delay (Minutes)")
axes[1].set_xticks(monthly_df["MONTH"])
axes[1].legend()

# --- 3. Root Causes Comparison ---
causes_df = spark.sql("""
    SELECT
        ROUND(AVG(AIR_SYSTEM_DELAY), 2) as Air_System,
        ROUND(AVG(SECURITY_DELAY), 2) as Security,
        ROUND(AVG(AIRLINE_DELAY), 2) as Airline,
        ROUND(AVG(LATE_AIRCRAFT_DELAY), 2) as Late_Aircraft,
        ROUND(AVG(WEATHER_DELAY), 2) as Weather
    FROM flights
""").toPandas()

causes_melted = causes_df.melt(var_name="Cause", value_name="Avg_Delay")
sns.barplot(data=causes_melted, x="Cause", y="Avg_Delay", ax=axes[2], palette="viridis")
axes[2].set_title("Major Root Causes of Flight Delays")
axes[2].set_xlabel("Delay Cause")
axes[2].set_ylabel("Average Delay (Minutes)")
axes[2].tick_params(axis='x', rotation=15)

plt.tight_layout()
plt.savefig("flight_delay_analysis.png", dpi=300)
print("\n[SUCCESS] Graphs plotted and saved successfully as 'flight_delay_analysis.png'!")

spark.stop()
