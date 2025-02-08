from flask import render_template, request

class Dashboard():
    def __init__(self, db):  
        self.db = db        
               
    def __call__(self):
        if request.method == 'POST':
            pass

        return render_template('dashboard.html', error=None)
