
from flask_login import UserMixin


class County():
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Constituency():
    def __init__(self, id, county_id, name):
        self.id = id
        self.county_id = county_id
        self.name = name

class Ward():
    def __init__(self, id, constituency_id, name):
        self.id = id
        self.constituency_id = constituency_id
        self.name = name

class PollingStation():
    def __init__(self, id, ward_id, name):
        self.id = id
        self.ward_id = ward_id
        self.name = name

class Voter(UserMixin):
    def __init__(self, id, id_number, first_name, last_name, other_name, phone, polling_station_id):
        self.id = id
        self.id_number = id_number
        self.first_name = first_name
        self.last_name = last_name
        self.other_name = other_name
        self.phone = phone
        self.polling_station_id = polling_station_id
        
class Election():
    def __init__(self, id, name):
        self.id = id
        self.name = name