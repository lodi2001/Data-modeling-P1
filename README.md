## Introduction
A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

The aim of this project is to build  an ETL pipeline that extracts their data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for  analytics team to continue finding insights in what songs their users are listening to. queires are given by analytics team from Sparkify that enable me to  test database and ETL pipeline, and compare the results with the expected one.



## How it works?
#### 1.configure dwh.cfg file 
To run this project  the following information is obtained , and saved in  dwh.cfg in the project root folder.

```
[CLUSTER]
HOST= dwhcluster.cb5xywksqp5g.us-west-2.redshift.amazonaws.com
DB_NAME=dwh
DB_USER=dwhuser
DB_PASSWORD=******
DB_PORT=5439

[IAM_ROLE]
ARN= arn:aws:iam::************:role/dwhRole

[S3]
LOG_DATA='s3://udacity-dend/log_data'
LOG_JSONPATH='s3://udacity-dend/log_json_path.json'
SONG_DATA='s3://udacity-dend/song_data'

[AWS]
KEY= ******
SECRET=*****

[DWH] 
DWH_CLUSTER_TYPE       =multi-node
DWH_NUM_NODES          =4
DWH_NODE_TYPE          =dc2.large
DWH_IAM_ROLE_NAME      =dwhRole
DWH_CLUSTER_IDENTIFIER =dwhCluster
DWH_DB                 =dwh
DWH_DB_USER            =dwhuser
DWH_DB_PASSWORD        =*******
DWH_PORT               =5439

```

#### 2. Creating a new AWS Redshift Cluster

To launch the cluster and to set up the needed infrastructure , script of Iac_create_cluster has to be executed:

`$ python Iac_create_cluster.py`

#### 3. Creating The Tables

Run the create_tables script to set up the database staging and analytical tables

`$ python create_tables.py`

#### 4. Build ETL Pipeline
Finally, run the etl script to extract data from the files in S3, stage it in redshift, and finally store it in the dimensional tables.

`$ python etl.py`

## The Database Design Structure 


#### Staging Tables
* staging_events

```
CREATE TABLE staging_events(
        artist              VARCHAR,
        auth                VARCHAR,
        firstName           VARCHAR,
        gender              VARCHAR,
        itemInSession       INTEGER,
        lastName            VARCHAR,
        length              FLOAT,
        level               VARCHAR,
        location            VARCHAR,
        method              VARCHAR,
        page                VARCHAR,
        registration        FLOAT,
        sessionId           INTEGER,
        song                VARCHAR,
        status              INTEGER,
        ts                  TIMESTAMP,
        userAgent           VARCHAR,
        userId              INTEGER 
    )
```

**Copying the Staging events table way**

``
("""
    copy staging_events from {data_bucket}
    credentials 'aws_iam_role={role_arn}'
    region 'us-west-2' format as JSON {log_json_path}
    timeformat as 'epochmillisecs';
""").format(data_bucket=config['S3']['LOG_DATA'], role_arn=config['IAM_ROLE']['ARN'], log_json_path=config['S3']['LOG_JSONPATH'])
``


* staging_songs

```
 CREATE TABLE staging_songs(
        num_songs           INTEGER,
        artist_id           VARCHAR,
        artist_latitude     FLOAT,
        artist_longitude    FLOAT,
        artist_location     VARCHAR,
        artist_name         VARCHAR,
        song_id             VARCHAR,
        title               VARCHAR,
        duration            FLOAT,
        year                INTEGER
    )
```
**Copying the Staging songs table way**

``
("""
    copy staging_songs from {data_bucket}
    credentials 'aws_iam_role={role_arn}'
    region 'us-west-2' format as JSON 'auto';
""").format(data_bucket=config['S3']['SONG_DATA'], role_arn=config['IAM_ROLE']['ARN'])
``

#### Fact Table
* songplays - records in event data associated with song plays i.e. records with page NextSong - songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

```
 CREATE TABLE songplays(
        songplay_id         INTEGER         IDENTITY(0,1)  SORTKEY,
        start_time          TIMESTAMP,
        user_id             INTEGER ,
        level               VARCHAR,
        song_id             VARCHAR,
        artist_id           VARCHAR ,
        session_id          INTEGER,
        location            VARCHAR,
        user_agent          VARCHAR
    )
```


#### Dimension Tables
* users - users in the app - user_id, first_name, last_name, gender, level

```
    CREATE TABLE users(
        user_id             INTEGER PRIMARY KEY,
        first_name          VARCHAR,
        last_name           VARCHAR,
        gender              VARCHAR,
        level               VARCHAR
    )
```

* songs - songs in music database - song_id, title, artist_id, year, duration

```
    CREATE TABLE songs(
        song_id             VARCHAR PRIMARY KEY,
        title               VARCHAR ,
        artist_id           VARCHAR ,
        year                INTEGER ,
        duration            FLOAT
    )
```
* artists - artists in music database - artist_id, name, location, lattitude, longitude

```
CREATE TABLE artists(
        artist_id           VARCHAR  PRIMARY KEY,
        name                VARCHAR ,
        location            VARCHAR,
        latitude            FLOAT,
        longitude           FLOAT
    )
```
* time - timestamps of records in songplays broken down into specific units - start_time, hour, day, week, month, year, weekday

```
CREATE TABLE time(
        start_time          TIMESTAMP       NOT NULL PRIMARY KEY,
        hour                INTEGER         NOT NULL,
        day                 INTEGER         NOT NULL,
        week                INTEGER         NOT NULL,
        month               INTEGER         NOT NULL,
        year                INTEGER         NOT NULL,
        weekday             VARCHAR(20)     NOT NULL
    )
```
![Tables](https://github.com/lodi2001/Data-modeling-P1/blob/master/schema_star.png?raw=true)


## Results of Queries
I executed the analytics_data.py file which gives me the number of rows in each table  following result: 

| Tables |  Rows  |   |   |   |
|---|---|---|---|---|
|  staging_events	  | 8056  |   |   |   |
|  staging_songs  | 14896  |   |   |   |
|  artists  | 10025  |   |   |   |
|  songplays | 333  |   |   |   |
|  songs  | 14896  |   |   |   |
|  time  | 8023  |   |   |   |
|  users  | 105  |   |   |   |

