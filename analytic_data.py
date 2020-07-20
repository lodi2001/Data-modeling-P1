import configparser
import psycopg2
from sql_queries import select_count_rows_queries


def count_rows(cur, conn):
    
    #count number or rows 
    
    for query in select_count_rows_queries:
        print(' ' + query)
        cur.execute(query)
        rows = cur.fetchone()

        for row in rows:
            print("   ", row)


def main():
    
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    count_rows(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()