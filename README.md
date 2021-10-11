# Project 3: Understanding User Behavior

- You're a data scientist at a game development company  

- Your latest mobile game has two events you're interested in tracking: `buy a
  sword` & `join guild`

- Each has metadata characterstic of such events (i.e., sword type, guild name,
  etc)


## Tasks

- Instrument your API server to log events to Kafka

- Assemble a data pipeline to catch these events: use Spark streaming to filter
  select event types from Kafka, land them into HDFS/parquet to make them
  available for analysis using Presto. 

- Use Apache Bench to generate test data for your pipeline.

- Produce an analytics report where you provide a description of your pipeline
  and some basic analysis of the events. Explaining the pipeline is key for this project!

- Submit your work as a git PR as usual. AFTER you have received feedback you have to merge 
  the branch yourself and answer to the feedback in a comment. Your grade will not be 
  complete unless this is done!

Use a notebook to present your queries and findings. Remember that this
notebook should be appropriate for presentation to someone else in your
business who needs to act on your recommendations. 

It's understood that events in this pipeline are _generated_ events which make
them hard to connect to _actual_ business decisions.  However, we'd like
students to demonstrate an ability to plumb this pipeline end-to-end, which
includes initially generating test data as well as submitting a notebook-based
report of at least simple event analytics. That said the analytics will only be a small
part of the notebook. The whole report is the presentation and explanation of your pipeline 
plus the analysis!

  
# Contents

- <b>docker-compose.yml</b> file ([here](docker-compose.yml)): This has all the containers required to run the data pipeline including Kafka, Zookeeper, Spark, HDFS, Cloudera, Flask, and Presto (data query engine).  You may need to update these ports if they are already being utilized.
- <b> Project_3_Final_Elizabeth_Khan_08_06_2021.ipynb</b> ([here](Project_3_Final_Elizabeth_Khan_08_06_2021.ipynb)): This is a Jupyter Notebook file that contains a comprehensive explanation of the project, command line code annotations, and Python Spark code. This includes everything from spinning up docker containers to Spark transformations, loading into tables in HDFS, creating a catalog in Hive, and querying via Presto. Finally, it generates reporting tables to provide examples of potential business use cases.
- <b> Game API (game_api.py)</b> file ([here](game_api.py)): This is an executable python file that contains script to run a Flask application. The Flask API has been enhanced to accept parameters for purchases events and guild name for the guild events.
- <b> Synthetic Data Generator (data_generator.sh)</b> file ([here](data_generator.sh)): This is a shell script that randomly generates mobile app events via Apache Bench. In this shell script, you can specify the number of users, endpoints (in this case 9 since we have 9 events), and events you want generated. See comments in shell script for additional details.
- <b> Spark Streaming Filtering and Transformation of Events (write_events_stream.py) </b>([here](write_events_stream.py)): This is an executable python file that contains a script to Stream events from Kafka queue and load events to HDFS in real-time. This includes filtering events based on event type, parsing out a JSON file from Kafka using a provided schema, and selecting the relevant columns to land on HDFS. 
- <b>Data Flow Conceptual Architecture Image</b> ([here](Conceptual_Flow_Diagram_Project_3.PNG)): This contains the conceptual flow diagram of the end to end data streaming pipeline.

# Setup

This setup is using the latest docker image provided from the <b>midsw205</b> docker repository which was provided to our class. A w205 directory was created within the virtual machine environment in the GCP instance. To connect Jupyter Notebook to the Spark container, Spark has an expose section in the docker-compose.yml file. Moreover, this Jupyter Notebook kernel was started from the command line in the virtual machine and was the ip address was updated to match the virtual machine.

Below is an outline of how my w205 directory is setup for this project.
```
w205/
├──     project-3-elizkhan/
│   ├── docker-compose.yml
│   ├── game_api.py
│   ├── write_events_stream.py
│   ├── Project_3_Final_Elizabeth_Khan_08_06_2021.ipynb
│   └── data_generator.sh
