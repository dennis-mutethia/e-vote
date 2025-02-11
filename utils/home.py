import uuid
from flask import render_template, request

class Home():
    def __init__(self, db):  
        self.db = db        
    
    def vote(self):
        try:
            election_id = request.form['election_id']
            candidate_id = request.form['candidate_id']
            if self.db.cast_vote(election_id, candidate_id):
                success='Presidential Vote Saved Successful.'
                error=None
            else:
                success=None
                error='An error occurred while casting your vote.'
            return success, error
        except Exception as e:
            return None, e
                  
    def __call__(self):
        id = uuid.uuid5(uuid.NAMESPACE_DNS, ('50298d17-4289-563b-a37c-29019ffbe682'))
        #print(id)
        success = None
        error = None
        if request.method == 'POST':
            if request.form['action'] == 'vote':
                success, error = self.vote()

        election = self.db.get_active_election()
        candidates = self.db.get_candidates(election)
        my_votes = self.db.get_my_votes()
        return render_template('home.html', election=election, candidates=candidates, my_votes=my_votes, success=success, error=error)
