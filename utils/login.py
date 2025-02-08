from flask import render_template, request

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
    
    def change_phone(self):      
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
            elif request.form['action'] == 'change_phone':
                return self.change_phone()

        return render_template('login.html', error=None)
