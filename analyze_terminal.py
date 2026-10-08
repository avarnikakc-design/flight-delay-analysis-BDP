from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("FlightDelay_TerminalAnalysis") \
    .getOrCreate()

flights_df = spark.read.option("header", "true").option("inferSchema", "true") \
    .csv("hdfs://localhost:9000/bigdata/flight_project/input/flights.csv")
flights_df.createOrReplaceTempView("flights")

print("\n=== 0. DATASET OVERVIEW ===")

# Total rows and columns
total_rows = flights_df.count()
total_columns = len(flights_df.columns)
print(f"Total Number of Rows (Flights): {total_rows:,}")
print(f"Total Number of Columns: {total_columns}")

# Unique counts for airlines and airports using correct column names
spark.sql("""
    SELECT 
        COUNT(DISTINCT AIRLINE) as unique_airlines,
        COUNT(DISTINCT ORIGIN_AIRPORT) as unique_origin_airports,
        COUNT(DISTINCT DESTINATION_AIRPORT) as unique_dest_airports
    FROM flights
""").show(truncate=False)

# Combined unique airports using correct column names
unique_airports = flights_df.select("ORIGIN_AIRPORT").union(flights_df.select("DESTINATION_AIRPORT")).distinct().count()
print(f"Total Combined Unique Airports: {unique_airports}")
print("-" * 40)

print("\n=== 1. DELAY PATTERNS ACROSS AIRLINES (Departure & Arrival Averages + Min/Max Baseline) ===")
spark.sql("""
    SELECT 
        AIRLINE, 
        COUNT(*) as total_flights, 
        MIN(DEPARTURE_DELAY) as min_dep_delay, 
        ROUND(AVG(DEPARTURE_DELAY), 2) as avg_dep_delay,
        MAX(DEPARTURE_DELAY) as max_dep_delay,
        MIN(ARRIVAL_DELAY) as min_arr_delay,
        ROUND(AVG(ARRIVAL_DELAY), 2) as avg_arr_delay,
        MAX(ARRIVAL_DELAY) as max_arr_delay
    FROM flights
    GROUP BY AIRLINE
    ORDER BY avg_dep_delay DESC
    LIMIT 5
""").show(truncate=False)

print("\n=== 2. AVERAGE DEPARTURE & ARRIVAL DELAYS BY MONTH (With Min/Max Baseline) ===")
spark.sql("""
    SELECT
        MONTH,
        COUNT(*) as total_flights,
        MIN(DEPARTURE_DELAY) as min_dep_delay,
        ROUND(AVG(DEPARTURE_DELAY), 2) as avg_dep_delay,
        MAX(DEPARTURE_DELAY) as max_dep_delay,
        MIN(ARRIVAL_DELAY) as min_arr_delay,
        ROUND(AVG(ARRIVAL_DELAY), 2) as avg_arr_delay,
        MAX(ARRIVAL_DELAY) as max_arr_delay
    FROM flights
    GROUP BY MONTH
    ORDER BY MONTH ASC
""").show(truncate=False)

print("\n=== 3. AVERAGE DEPARTURE & ARRIVAL DELAYS BY DAY OF WEEK (With Min/Max Baseline) ===")
spark.sql("""
    SELECT
        DAY_OF_WEEK,
        COUNT(*) as total_flights,
        MIN(DEPARTURE_DELAY) as min_dep_delay,
        ROUND(AVG(DEPARTURE_DELAY), 2) as avg_dep_delay,
        MAX(DEPARTURE_DELAY) as max_dep_delay,
        MIN(ARRIVAL_DELAY) as min_arr_delay,
        ROUND(AVG(ARRIVAL_DELAY), 2) as avg_arr_delay,
        MAX(ARRIVAL_DELAY) as max_arr_delay
    FROM flights
    GROUP BY DAY_OF_WEEK
    ORDER BY DAY_OF_WEEK ASC
""").show(truncate=False)

print("\n=== 4. MAJOR CAUSES OF FLIGHT DELAYS (ROOT CAUSES) ===")
spark.sql("""
    SELECT
        ROUND(AVG(AIR_SYSTEM_DELAY), 2) as avg_air_system,
        ROUND(AVG(SECURITY_DELAY), 2) as avg_security,
        ROUND(AVG(AIRLINE_DELAY), 2) as avg_airline,
        ROUND(AVG(LATE_AIRCRAFT_DELAY), 2) as avg_late_aircraft,
        ROUND(AVG(WEATHER_DELAY), 2) as avg_weather
    FROM flights
""").show(truncate=False)

print("\n=== 5. TERMINAL ANALYSIS COMPLETE ===")
spark.stop()
