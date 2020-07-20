import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries

"""Loading Data from s3 buckets
to Redshift  
"""
def load_staging_tables(cur, conn):
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()
        
"""Perform query of insert_table_queries to INSERT  
records form staging tables to the dimension and fact tables
"""

def insert_tables(cur, conn):
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    # Get the reguired parameters for Redshift cluster from configuration files 
    config = configparser.ConfigParser()
    config.read('dwh.cfg')
    
    #connect to postgres instance
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    # Execute load_staging_tables function 
    load_staging_tables(cur, conn)
   
    #Execute insert_table function 
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()