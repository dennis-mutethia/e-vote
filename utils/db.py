import os, psycopg2

from utils.entities import Constituency, County, Voter

class Db():
    def __init__(self):
        # Access the environment variables
        self.conn_params = {
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT'),
            'database': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD')
        }
        self.schema = os.getenv('DB_SCHEMA')
        
        self.conn = None
        self.ensure_connection()
    
    def ensure_connection(self):
        try:
            # Check if the connection is open
            if self.conn is None or self.conn.closed:
                self.conn = psycopg2.connect(**self.conn_params)
            else:
                # Test the connection
                with self.conn.cursor() as cursor:
                    cursor.execute("SELECT 1")
        except Exception as e:
            # Reconnect if the connection is invalid
            self.conn = psycopg2.connect(**self.conn_params)        
      
    def get_counties(self):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                #query = f"DROP TABLE {self.schema}.counties"
                query = f"SELECT id, name FROM {self.schema}.counties"
                cursor.execute(query)
                data = cursor.fetchall()
                counties = []
                for datum in data:
                    counties.append(County(datum[0], datum[1]))
                
                return counties
        except Exception as e:
            print(e)
            return None      
      
    def get_constituencies(self, county_id=None):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"SELECT id, name FROM {self.schema}.constituencies"
                if county_id is not None:
                    query = f"{query} WHERE county_id = %s"
                cursor.execute(query, (county_id,))
                data = cursor.fetchall()
                constituencies = []
                for datum in data:
                    constituencies.append(Constituency(datum[0], county_id, datum[1]))
                
                return constituencies
        except Exception as e:
            print(e)
            return None
    
    def get_voter(self, id=None, fingerprint_hash=None):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"SELECT id, id_number, first_name, last_name, other_name, phone, polling_station_id FROM {self.schema}.voters"
                if id is not None:
                    query = f"{query} WHERE id = %s"
                    cursor.execute(query, (id,))
                else:
                    query = f"{query} WHERE fingerprint_hash = %s"
                    cursor.execute(query, (fingerprint_hash,))
                data = cursor.fetchone()
                if data:
                    return Voter(data[0], data[1], data[2], data[3], data[4], data[5], data[6])
                else:
                    return None
        except Exception as e:
            print(e)
            return None
    
    def get_voter_by_fingerprint_hash(self, fingerprint_hash):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"SELECT id, id_number, first_name, last_name, other_name, phone, polling_station_id FROM {self.schema}.voters WHERE fingerprint_hash = %s"
                cursor.execute(query, (fingerprint_hash,))
                data = cursor.fetchone()
                if data:
                    return Voter(data[0], data[1], data[2], data[3], data[4], data[5], data[6])
                else:
                    return None
        except Exception as e:
            print(e)
            return None