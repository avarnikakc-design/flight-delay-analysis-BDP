import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("FlightDelay_AllPlots") \
    .getOrCreate()

flights_df = spark.read.option("header", "true").option("inferSchema", "true") \
    .csv("hdfs://localhost:9000/bigdata/flight_project/input/flights.csv")
flights_df.createOrReplaceTempView("flights")

# 1. Monthly Delay Bar & Trend Line
monthly_pd = spark.sql("""
    SELECT MONTH, ROUND(AVG(DEPARTURE_DELAY), 2) as avg_dep_delay
    FROM flights
    GROUP BY MONTH
    ORDER BY MONTH ASC
""").toPandas()

# Monthly Delay Bar Chart
plt.figure(figsize=(10, 5))
plt.bar(monthly_pd['MONTH'], monthly_pd['avg_dep_delay'], color='skyblue', edgecolor='black')
plt.title('Monthly Delay (Bar Chart)')
plt.xlabel('Month')
plt.ylabel('Average Departure Delay (Minutes)')
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.savefig('monthly_delay.png', dpi=300, bbox_inches='tight')
plt.close()

# Monthly Trend Line
plt.figure(figsize=(10, 5))
plt.plot(monthly_pd['MONTH'], monthly_pd['avg_dep_delay'], marker='o', color='crimson', linewidth=2.5)
plt.title('Monthly Trend Line')
plt.xlabel('Month')
plt.ylabel('Average Departure Delay (Minutes)')
plt.grid(True, linestyle='--', alpha=0.6)
plt.savefig('monthly_trend_line.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. Airline Delays Bar Chart
airline_pd = spark.sql("""
    SELECT AIRLINE, ROUND(AVG(DEPARTURE_DELAY), 2) as avg_dep_delay
    FROM flights
    GROUP BY AIRLINE
    ORDER BY avg_dep_delay DESC
    LIMIT 10
""").toPandas()

plt.figure(figsize=(12, 6))
plt.bar(airline_pd['AIRLINE'], airline_pd['avg_dep_delay'], color='orange', edgecolor='black')
plt.title('Airline Delays (Bar Chart)')
plt.xlabel('Airline')
plt.ylabel('Average Departure Delay (Minutes)')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.savefig('airline_delays_bar.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. Root Causes Bar Chart
root_causes_pd = spark.sql("""
    SELECT 
        ROUND(AVG(AIR_SYSTEM_DELAY), 2) as Air_System,
        ROUND(AVG(SECURITY_DELAY), 2) as Security,
        ROUND(AVG(AIRLINE_DELAY), 2) as Airline,
        ROUND(AVG(LATE_AIRCRAFT_DELAY), 2) as Late_Aircraft,
        ROUND(AVG(WEATHER_DELAY), 2) as Weather
    FROM flights
""").toPandas()

causes = ['Air System', 'Security', 'Airline', 'Late Aircraft', 'Weather']
delays = [
    root_causes_pd['Air_System'].values[0],
    root_causes_pd['Security'].values[0],
    root_causes_pd['Airline'].values[0],
    root_causes_pd['Late_Aircraft'].values[0],
    root_causes_pd['Weather'].values[0]
]

plt.figure(figsize=(10, 5))
plt.bar(causes, delays, color='mediumseagreen', edgecolor='black')
plt.title('Root Causes of Flight Delays')
plt.xlabel('Delay Cause')
plt.ylabel('Average Delay (Minutes)')
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.savefig('root_causes_bar.png', dpi=300, bbox_inches='tight')
plt.close()

spark.stop()
print("Successfully generated all requested plot files.")
