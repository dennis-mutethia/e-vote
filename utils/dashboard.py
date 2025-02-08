import uuid
from flask import render_template, request

class Dashboard():
    def __init__(self, db):  
        self.db = db        
    
    def vote(self):
        try:
            election_id = request.form['election_id']
            candidate_id = request.form['candidate_id']
            print(election_id, candidate_id)
            return render_template('dashboard.html', election_id=2, success='Presidential Vote Casted Successful.', error=None)
        except Exception as e:
            return render_template('dashboard.html', election_id=1, success=None, error=e)
                  
    def __call__(self):
        key = uuid.uuid4()
        #print(key)
        if request.method == 'POST':
            if request.form['action'] == 'vote':
                return self.vote()

        return render_template('dashboard.html', election_id=1, success=None, error=None)
