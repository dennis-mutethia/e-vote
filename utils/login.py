from flask import render_template, request
import uuid

class Login():
    def __init__(self, db): 
        self.db = db        
     
    def login(self):      
        try:
            pass 
        except Exception as e:
            return render_template('login.html', error=e)
    
    def register(self):      
        try:
            pass
        except Exception as e:
            return render_template('login.html', error=e) 
               
    def __call__(self):
        key = uuid.uuid4()
        #print(key)
        if request.method == 'POST':
            if request.form['action'] == 'register':
                return self.register()
            elif request.form['action'] == 'login':
                return self.login()

        # counties = self.db.get_counties()
        # constituencies = self.db.get_constituencies()
        # print(counties)
        # print(constituencies)
        return render_template('login.html', error=None)
