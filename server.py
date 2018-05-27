from collections import namedtuple
from flask import Flask, request, render_template, session, url_for, jsonify
import os
from uuid import uuid4
from compliments import generate_compliment
import database

context = '/compliments'
app = Flask(__name__, static_url_path=context)
app.secret_key = os.urandom(64)

#db = database.connect()
Recipient = namedtuple('Recipient',('name','number'))

#def get_recipients():
#    cursor = db.cursor()
#    cursor.execute('SELECT id, name FROM users ORDER BY name;')
#    recipients = tuple(cursor)
#    cursor.close()
#    db.commit()
#    return recipients

@app.route(context+'/')
def index():
    #return render_template('index.html', recipients=get_recipients())
    return render_template('index.html', compliment=generate_compliment('Chad'))

@app.route(context+'/generate')
def compliment():
    recipient = request.args.get('recipient',None)
    if recipient != None:
        comp = generate_compliment(recipient)
        user_from = session.get('user', 'guest')
        return jsonify(
            recipient=recipient,
            content=comp,
            sender=user_from
        )

