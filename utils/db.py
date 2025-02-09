from flask_login import current_user
import os, psycopg2
import uuid

from utils.entities import Candidate, Constituency, County, Election, Voter

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
    
    def insert_sms_code(self, voter_id, code):
        id = str(uuid.uuid4())
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"INSERT INTO {self.schema}.sms_codes (id, voter_id, code) VALUES (%s, %s, %s)"
                cursor.execute(query, (id, voter_id, code))
                self.conn.commit()
                return True
        except Exception as e:
            print(e)
            return False
    
    def get_sms_code(self, voter_id):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"SELECT code FROM {self.schema}.sms_codes WHERE voter_id = %s AND status = 0 ORDER BY created_at DESC LIMIT 1"
                cursor.execute(query, (voter_id,))
                data = cursor.fetchone()
                if data:
                    return data[0]
                else:
                    return None
        except Exception as e:
            print(e)
            return None
    
    def update_sms_code_status(self, voter_id):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"UPDATE {self.schema}.sms_codes SET status = 1 WHERE voter_id = %s"
                cursor.execute(query, (voter_id,))
                self.conn.commit()
                return True
        except Exception as e:
            print(e)
            return False
    
    def get_active_election(self):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"SELECT id, name FROM {self.schema}.elections ORDER BY code ASC LIMIT 1"
                cursor.execute(query, (current_user.id,))
                data = cursor.fetchone()
                if data:
                    return Election(data[0], data[1])
                else:
                    return None
        except Exception as e:
            print(e)
            return None   
      
    def get_candidates(self, election_id):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"""
                SELECT c.id, c.icon, running_mate_icon, unit, unit_id,
                CONCAT(v.first_name, ' ', v.last_name, ' ', v.other_name) AS name, 
                CONCAT(v2.first_name, ' ', v2.last_name, ' ', v2.other_name) AS running_mate_name,
                p.name AS party_name, p.icon AS party_icon
                FROM {self.schema}.candidates c
                JOIN {self.schema}.voters v ON v.id = c.voter_id
                JOIN {self.schema}.voters v2 ON v2.id = c.running_mate_voter_id
                JOIN {self.schema}.parties p ON p.id = c.party_id
                WHERE c.election_id = %s
                """
                cursor.execute(query, (election_id,))
                data = cursor.fetchall()
                candidates = []
                for datum in data:
                    candidates.append(Candidate(datum[0], datum[1], datum[2], datum[3], datum[4], datum[5], datum[6], datum[7], datum[8]))
                
                return candidates
        except Exception as e:
            print(e)
            return None