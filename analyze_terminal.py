from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("FlightDelay_TerminalAnalysis") \
    .getOrCreate()

flights_df = spark.read.option("header", "true").option("inferSchema", "true") \
    .csv("hdfs://localhost:9000/bigdata/flight_project/input/flights.csv")
flights_df.createOrReplaceTempView("flights")

print("\n=== 1. DELAY PATTERNS ACROSS AIRLINES ===")
spark.sql("""
    SELECT AIRLINE, COUNT(*) as total_flights, ROUND(AVG(DEPARTURE_DELAY), 2) as avg_dep_delay
    FROM flights
    GROUP BY AIRLINE
    ORDER BY avg_dep_delay DESC
    LIMIT 5
""").show(truncate=False)

print("\n=== 2. MAJOR CAUSES OF FLIGHT DELAYS (ROOT CAUSES) ===")
spark.sql("""
    SELECT 
        ROUND(AVG(AIR_SYSTEM_DELAY), 2) as avg_air_system,
        ROUND(AVG(SECURITY_DELAY), 2) as avg_security,
        ROUND(AVG(AIRLINE_DELAY), 2) as avg_airline,
        ROUND(AVG(LATE_AIRCRAFT_DELAY), 2) as avg_late_aircraft,
        ROUND(AVG(WEATHER_DELAY), 2) as avg_weather
    FROM flights
""").show(truncate=False)

print("\n=== 3. AVERAGE DEPARTURE & ARRIVAL DELAYS BY MONTH ===")
spark.sql("""
    SELECT 
        MONTH, 
        COUNT(*) as total_flights, 
        ROUND(AVG(DEPARTURE_DELAY), 2) as avg_dep_delay,
        ROUND(AVG(ARRIVAL_DELAY), 2) as avg_arr_delay
    FROM flights
    GROUP BY MONTH
    ORDER BY MONTH ASC
""").show(truncate=False)

print("\n=== 4. AVERAGE DEPARTURE & ARRIVAL DELAYS BY DAY OF WEEK ===")
spark.sql("""
    SELECT 
        DAY_OF_WEEK, 
        COUNT(*) as total_flights, 
        ROUND(AVG(DEPARTURE_DELAY), 2) as avg_dep_delay,
        ROUND(AVG(ARRIVAL_DELAY), 2) as avg_arr_delay
    FROM flights
    GROUP BY DAY_OF_WEEK
    ORDER BY DAY_OF_WEEK ASC
""").show(truncate=False)

print("\n=== 5. TERMINAL ANALYSIS COMPLETE ===")
spark.stop()
