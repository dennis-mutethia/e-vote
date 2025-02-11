from flask import redirect, render_template, request, url_for
import uuid

class Login():
    def __init__(self, db): 
        self.db = db   
        self.error = None     
     
    def login(self):      
        try:
            id_number = request.form['VoterIdNumber']  
            voter = self.db.get_voter(id_number=id_number)
            if voter:
                return redirect(url_for('login_verify', uid=voter.id))
            else:
                self.error = 'Id Number does not Exist'
        except Exception as e:
            self.error = e
    
    def register(self):      
        try:
            pass
        except Exception as e:
            return render_template('login.html', error=e) 
               
    def __call__(self):
        if request.method == 'POST':
            if request.form['action'] == 'register':
                return self.register()
            elif request.form['action'] == 'login':
                return self.login()
            
        return render_template('login.html', error=self.error)
