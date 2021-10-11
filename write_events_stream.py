#!/usr/bin/env python
"""Extract events from kafka and write them to hdfs
"""
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, from_json
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, LongType
'''Setting spark config to a timezone'''
# spark.conf.set("spark.sql.sessioin.timeZone", "UTC")
import pyspark.sql.functions as F
from datetime import datetime
from datetime import date


def purchase_events_schema():
    """
    @function: This function provides the table schema for purchase events
    @param: None 
    @return: Returns the table schema for purchase events
    """  
    return StructType(
    [
        StructField('Accept', StringType(), True),
        StructField('Host', StringType(), True),
        StructField('User-Agent', StringType(), True),
        StructField('amount_purchased', LongType(), True),
        StructField('description', StringType(), True),
        StructField('event_type', StringType(), True),
        StructField('item_type', StringType(), True),
        StructField('price', LongType(), True),
        StructField('userid', StringType(), True)
    ]
)

def character_events_schema():
    """
    @function: This function provides the table schema for  character events
    @param: None 
    @return: Returns the table schema for character events 
    """  
    return StructType(
    [
        StructField('Accept', StringType(), True),
        StructField('Host', StringType(), True),
        StructField('User-Agent', StringType(), True),
        StructField('description', StringType(), True),
        StructField('event_type', StringType(), True),
        StructField('userid', StringType(), True)
    ]
)

def character_stats_schema():
    """
    @function: This function provides the table schema for character stats
    @param: None 
    @return: Returns the table schema for character stats
    """  
    return StructType(
    [
        StructField('Accept', StringType(), True),
        StructField('Host', StringType(), True),
        StructField('User-Agent', StringType(), True),
        StructField('attack', LongType(), True),
        StructField('defense', LongType(), True),
        StructField('description', StringType(), True),
        StructField('event_type', StringType(), True),
        StructField('health', LongType(), True),
        StructField('level', LongType(), True),
        StructField('userid', StringType(), True)
    ]
)

def guild_events_schema():
    """
    @function: This function provides the table schema for  guild events
    @param: None 
    @return: Returns the table schema for guild events 
    """  
    return StructType(
    [
        StructField('Accept', StringType(), True),
        StructField('Host', StringType(), True),
        StructField('User-Agent', StringType(), True),
        StructField('description', StringType(), True),
        StructField('event_type', StringType(), True),
        StructField('guild_name', StringType(), True),
        StructField('userid', StringType(), True)
    ]
)

@udf('boolean')
def is_purchase(event_as_json):
    """
    @function: This function uses a json to filter out records by purchase event type
    @param: Takes in extracted json data as a string
    @return: Returns a boolean value
    """    
    event = json.loads(event_as_json)
    if 'purchase' in event['event_type']:
        return True
    return False


@udf('boolean')
def is_character_event(event_as_json):
    """
    @function: This function uses a json to filter out records by character event type
    @param: Takes in extracted json data as a string
    @return: Returns a boolean value
    """    
    event = json.loads(event_as_json)
    if event['event_type'] == 'find_treasure' or event['event_type'] == 'enemy_attack' or event['event_type'] == 'defeat_enemy':
        return True
    return False

@udf('boolean')
def is_character_stat(event_as_json):
    """
    @function: This function uses a json to filter out records by character stat event type
    @param: Takes in extracted json data as a string
    @return: Returns a boolean value
    """    
    event = json.loads(event_as_json)
    if event['event_type'] == 'level_up' or event['event_type'] == 'take_potion':
        return True
    return False

@udf('boolean')
def is_join_guild(event_as_json):
    """
    @function: This function uses a json to filter out records by guild event type
    @param: Takes in extracted json data as a string
    @return: Returns a boolean value
    """   
    event = json.loads(event_as_json)
    if event['event_type'] == 'join_guild':
        return True
    return False

def main():
    """
    @function: This is a main function that executes a spark job including extracting string, parsing json using a provided schema, etc.
    @param: none, uses previously defined functions
    @return: none, lands tables via streaming on HDFS
    """  
    spark = SparkSession \
        .builder \
        .appName("ExtractEventsJob") \
        .getOrCreate()

    raw_events = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:29092") \
        .option("subscribe", "events") \
        .load()

    purchases = raw_events \
        .filter(is_purchase(raw_events.value.cast('string'))) \
        .select(raw_events.value.cast('string').alias('raw_event'),
                raw_events.timestamp.cast('string'),
                from_json(raw_events.value.cast('string'),
                          purchase_events_schema()).alias('json')) \
        .select('timestamp', 'json.*') \
        .select( \
                  F.from_utc_timestamp(F.col('timestamp'),'GMT').alias('event_ts') \
                 ,F.col('userid') \
                 ,F.col('Host') \
                 ,F.col('event_type') \
                 ,F.col('item_type') \
                 ,F.col('description') \
                 ,F.col('amount_purchased') \
                 ,F.col('price') \
                ) \
        .distinct()
        
    
    char = raw_events \
        .filter(is_character_event(raw_events.value.cast('string'))) \
        .select(raw_events.value.cast('string').alias('raw_event'),
                raw_events.timestamp.cast('string'),
                from_json(raw_events.value.cast('string'),
                          character_events_schema()).alias('json')) \
        .select('timestamp', 'json.*') \
        .select( \
                  F.from_utc_timestamp(F.col('timestamp'),'GMT').alias('event_ts') \
                 ,F.col('userid') \
                 ,F.col('Host') \
                 ,F.col('description') \
                 ,F.col('event_type') \
                ) \
        .distinct()
      
    
    stats = raw_events \
        .filter(is_character_stat(raw_events.value.cast('string'))) \
        .select(raw_events.value.cast('string').alias('raw_event'),
                raw_events.timestamp.cast('string'),
                from_json(raw_events.value.cast('string'),
                          character_stats_schema()).alias('json')) \
        .select('timestamp', 'json.*') \
        .select( \
                  F.from_utc_timestamp(F.col('timestamp'),'GMT').alias('event_ts') \
                 ,F.col('userid') \
                 ,F.col('Host') \
                 ,F.col('event_type') \
                 ,F.col('description') \
                 ,F.col('level') \
                 ,F.col('attack') \
                 ,F.col('defense') \
                 ,F.col('health') \
                 ) \
        .distinct() 
        
    guild = raw_events \
        .filter(is_join_guild(raw_events.value.cast('string'))) \
        .select(raw_events.value.cast('string').alias('raw_event'),
                raw_events.timestamp.cast('string'),
                from_json(raw_events.value.cast('string'),
                          guild_events_schema()).alias('json')) \
        .select('timestamp', 'json.*') \
        .select( \
                  F.from_utc_timestamp(F.col('timestamp'),'GMT').alias('event_ts') \
                 ,F.col('userid') \
                 ,F.col('Host') \
                 ,F.col('event_type') \
                 ,F.col('description') \
                 ,F.col('guild_name') \
                ) \
        .distinct()
    
        

    sink_purchases = purchases \
        .writeStream \
        .format("parquet") \
        .option("checkpointLocation", "/tmp/checkpoints_for_purchase_events") \
        .option("path", "/tmp/purchase_events") \
        .trigger(processingTime="10 seconds") \
        .start()
    
    sink_char = char \
        .writeStream \
        .format("parquet") \
        .option("checkpointLocation", "/tmp/checkpoints_for_character_events") \
        .option("path", "/tmp/character_events") \
        .trigger(processingTime="10 seconds") \
        .start()
    
    sink_stats = stats \
        .writeStream \
        .format("parquet") \
        .option("checkpointLocation", "/tmp/checkpoints_for_character_stats") \
        .option("path", "/tmp/character_stats") \
        .trigger(processingTime="10 seconds") \
        .start()
    
    sink_guild = guild \
        .writeStream \
        .format("parquet") \
        .option("checkpointLocation", "/tmp/checkpoints_for_guild_events") \
        .option("path", "/tmp/guild_events") \
        .trigger(processingTime="10 seconds") \
        .start()

    sink_purchases.awaitTermination()
    sink_char.awaitTermination()
    sink_stats.awaitTermination()
    sink_guild.awaitTermination()

    
    
if __name__ == "__main__":
        main()
