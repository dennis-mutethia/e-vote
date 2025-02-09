from flask import redirect, render_template, request, url_for
import random

from flask_login import login_user

class LoginVerify():
    def __init__(self, db, uid): 
        self.db = db   
        self.voter_id = uid
        self.send_sms_code()
    
    def send_sms_code(self):
        code = self.db.get_sms_code(self.voter_id)
        if code is None:            
            code = random.randint(1000, 9999)
            self.db.insert_sms_code(self.voter_id, code)
            
        #send SMS
        print(f'SMS Code: {code}')
        
    def login(self):      
        try:
            code = request.form['code']
            expected_code = self.db.get_sms_code(self.voter_id)
            if code == expected_code:
                voter = self.db.get_voter(self.voter_id)
                login_user(voter)
                self.db.update_sms_code_status(self.voter_id)
                return redirect(url_for('home', uid=self.voter_id)) 
            else:
                self.send_sms_code()
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
