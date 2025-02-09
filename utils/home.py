import uuid
from flask import render_template, request

class Home():
    def __init__(self, db):  
        self.db = db        
    
    def vote(self):
        try:
            election_id = request.form['election_id']
            candidate_id = request.form['candidate_id']
            print(election_id, candidate_id)
            election = self.db.get_active_election()
            return render_template('home.html', election=election, success='Presidential Vote Casted Successful.', error=None)
        except Exception as e:
            return render_template('home.html', election=election, success=None, error=e)
                  
    def __call__(self):
        id = uuid.uuid5(uuid.NAMESPACE_DNS, ('50298d17-4289-563b-a37c-29019ffbe682'))
        print(id)
        if request.method == 'POST':
            if request.form['action'] == 'vote':
                return self.vote()

        election = self.db.get_active_election()
        candidates = self.db.get_candidates(election.id)
        return render_template('home.html', election=election, candidates=candidates, success=None, error=None)
