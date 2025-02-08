from flask import redirect, render_template, request, url_for
import random

from flask_login import login_user

class LoginVerify():
    def __init__(self, db): 
        self.db = db   
        self.code = random.randint(1000, 9999)
        self.send_code()
    
    def send_code(self):
        print(self.code)  
    
    def login(self):      
        try:
            code = request.form['code']
            if int(code) != self.code:
                voter = self.db.get_voter(id=1)
                login_user(voter)
                return redirect(url_for('dashboard')) 
            else:
                self.send_code()
                return render_template('login-verify.html', error='Invalid code. Please try again.')
        except Exception as e:
            print(e)
            return render_template('login-verify.html', error=e)
    
    def change_phone(self):      
        try:
            pass
        except Exception as e:
            return render_template('login.html', error=e)        
               
    def __call__(self):
        if request.method == 'POST':
            if request.form['action'] == 'verify':
                return self.login()
            elif request.form['action'] == 'change_phone':
                return self.change_phone()

        # counties = self.db.get_counties()
        # constituencies = self.db.get_constituencies()
        # print(counties)
        # print(constituencies)
        return render_template('login-verify.html', error=None)
