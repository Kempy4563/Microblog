from flask import Flask, render_template, request
import datetime
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb+srv://leekempson73:uSrajPcNoq01l03h@microblog.b0f4c.mongodb.net/?retryWrites=true&w=majority&appName=Microblog")
app.db = client.microblog

entries = []


@app.route('/', methods=['GET', 'POST'])  # (methods)
def home():
    print([e for e in app.db.entries.find({})])
    if request.method == 'POST':
        entry_content = request.form.get('content')
        formatted_date = str(datetime.datetime.today().strftime('%Y-%m-%d'))
        entries.append((entry_content, formatted_date))
        print(formatted_date)
        app.db.entries.insert_one({'content': entry_content, 'date': formatted_date})

    entries_with_date = [
        (entry["content"], entry["date"], datetime.datetime.strptime(entry["date"],
                                                        '%Y-%m-%d').strftime("%b %d")
         )
        for entry in app.db.entries.find({})]
    return render_template('home.html', entries=entries_with_date)  # (render)
