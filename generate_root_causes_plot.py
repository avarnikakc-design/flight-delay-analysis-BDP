import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pyspark.sql import SparkSession
import pyspark.sql.functions as F

spark = SparkSession.builder.appName("RootCausesPlot").getOrCreate()
flights_df = spark.read.option("header", "true").option("inferSchema", "true") \
    .csv("hdfs://localhost:9000/bigdata/flight_project/input/flights.csv")

cols = ['AIR_SYSTEM_DELAY', 'SECURITY_DELAY', 'AIRLINE_DELAY', 'LATE_AIRCRAFT_DELAY', 'WEATHER_DELAY']
for c in cols:
    if c in flights_df.columns:
        flights_df = flights_df.withColumn(c, F.coalesce(F.col(c).cast("double"), F.lit(0.0)))

flights_df.createOrReplaceTempView("flights")

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
print("Successfully generated root_causes_bar.png")
