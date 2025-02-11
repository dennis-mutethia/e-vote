from flask_login import current_user
import os, psycopg2
import uuid

from utils.entities import Candidate, Constituency, County, Election, MyVote, Voter

class Db():
    def __init__(self):
        # Access the environment variables
        self.conn_params = {
            'host': os.getenv('DB_HOST'),
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
    
    def get_voter(self, id=None, id_number=None, fingerprint_hash=None):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"""SELECT voters.id, id_number, first_name, last_name, other_name, phone, polling_station_id, ward_id, constituency_id, county_id 
                FROM {self.schema}.voters
                JOIN {self.schema}.polling_stations ON polling_station_id = polling_stations.id
                JOIN {self.schema}.wards ON polling_stations.ward_id = wards.id
                JOIN {self.schema}.constituencies ON wards.constituency_id = constituencies.id
                WHERE 1=1
                """                
                params = []
                if id is not None:
                    query = f"{query} AND voters.id = %s"
                    params.append(id)
                elif id_number is not None:
                    query = f"{query} AND id_number = %s"
                    params.append(id_number)
                else:
                    query = f"{query} AND fingerprint_hash = %s"
                    params.append(fingerprint_hash)
                cursor.execute(query, tuple(params))
                data = cursor.fetchone()
                if data:
                    return Voter(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9])
                else:
                    return None
        except Exception as e:
            print(e)
            return None

    def insert_sms_code(self, voter, code):
        id = str(uuid.uuid4())
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"INSERT INTO {self.schema}.sms_codes (id, voter_id, polling_station_id, code) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (id, voter.id, voter.polling_station_id, code))
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
                query = f"""
                SELECT id, code, name 
                FROM {self.schema}.elections 
                WHERE id NOT IN(
                    SELECT election_id FROM {self.schema}.votes WHERE voter_id = %s
                )
                ORDER BY code ASC 
                LIMIT 1
                """
                cursor.execute(query, (current_user.id,))
                data = cursor.fetchone()
                if data:
                    return Election(data[0], data[1], data[2])
                else:
                    return None
        except Exception as e:
            print(e)
            return None   
      
    def get_candidates(self, election):
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
                LEFT JOIN {self.schema}.voters v2 ON v2.id = c.running_mate_voter_id
                JOIN {self.schema}.parties p ON p.id = c.party_id
                JOIN {self.schema}.polling_stations ON v.polling_station_id = polling_stations.id 
                JOIN {self.schema}.wards ON ward_id = wards.id   
                JOIN {self.schema}.constituencies ON constituency_id = constituencies.id
                JOIN {self.schema}.counties ON county_id = counties.id
                WHERE c.election_id = %s
                """                             
                params = [election.id]
                if election.code == '1': #president
                    pass                  
                elif election.code == 2: #mp
                    query = f"{query} AND constituency_id = %s"
                    params.append(current_user.constituency_id)     
                elif election.code in [3, 4, 5]: #woman rep, senator, governor
                    query = f"{query} AND county_id = %s"
                    params.append(current_user.county_id)     
                elif election.code == 6: #mca
                    query = f"{query} AND ward_id = %s"
                    params.append(current_user.ward_id)
                    
                cursor.execute(query, tuple(params))
                
                data = cursor.fetchall()
                candidates = []
                for datum in data:
                    candidates.append(Candidate(datum[0], datum[1], datum[2], datum[3], datum[4], datum[5], datum[6], datum[7], datum[8]))
                
                return candidates
        except Exception as e:
            print(e)
            return None
    
    def cast_vote(self, election_id, candidate_id):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"""INSERT INTO {self.schema}.votes 
                (election_id, candidate_id, voter_id, polling_station_id, ward_id, constituency_id, county_id, created_at) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                """
                cursor.execute(query, (election_id, candidate_id, current_user.id, current_user.polling_station_id, current_user.ward_id, current_user.constituency_id, current_user.county_id))
                self.conn.commit()
                return True
        except Exception as e:
            print(e)
            return False

    def get_my_votes(self):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                query = f"""
                WITH votes AS(
                    SELECT votes.election_id, CONCAT(first_name, ' ', last_name, ' ', other_name) AS candidate_name, icon
                    FROM {self.schema}.votes 
                    LEFT JOIN {self.schema}.candidates ON candidate_id = candidates.id
                    LEFT JOIN {self.schema}.voters ON candidates.voter_id = voters.id
                    WHERE votes.voter_id = %s
                )
                SELECT elections.code, elections.name, candidate_name, icon
                FROM e_vote.elections 
                LEFT JOIN votes ON election_id = elections.id
                ORDER BY elections.code
                """
                cursor.execute(query, (current_user.id,))
                data = cursor.fetchall()
                my_votes = []
                for datum in data:
                    my_votes.append(MyVote(datum[0], datum[1], datum[2], datum[3]))
                
                return my_votes
        except Exception as e:
            print(e)
            return None