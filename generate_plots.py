import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("FlightDelay_Plotting") \
    .getOrCreate()

flights_df = spark.read.option("header", "true").option("inferSchema", "true") \
    .csv("hdfs://localhost:9000/bigdata/flight_project/input/flights.csv")
flights_df.createOrReplaceTempView("flights")

monthly_pd = spark.sql("""
    SELECT MONTH, ROUND(AVG(DEPARTURE_DELAY), 2) as avg_dep_delay
    FROM flights
    GROUP BY MONTH
    ORDER BY MONTH ASC
""").toPandas()

plt.figure(figsize=(10, 5))
plt.plot(monthly_pd['MONTH'], monthly_pd['avg_dep_delay'], marker='o', color='b', linewidth=2)
plt.title('Average Departure Delay by Month')
plt.xlabel('Month')
plt.ylabel('Average Delay (Minutes)')
plt.grid(True, linestyle='--', alpha=0.6)
plt.savefig('monthly_delays.png', dpi=300, bbox_inches='tight')
plt.close()

spark.stop()
print("Successfully generated and saved monthly_delays.png")
