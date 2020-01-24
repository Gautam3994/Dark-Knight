from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\Gautam\\database\\chinook.db'
db = SQLAlchemy(app)

Base = automap_base()
Base.prepare(db.engine, reflect=True)
Tracks = Base.classes.tracks
InvoiceItems = Base.classes.invoice_items


@app.route('/')
def index():
    track_count = db.session.query(Tracks).join(InvoiceItems).filter(InvoiceItems.InvoiceId == 10).count()
    print(track_count)
    return ''


if __name__ == '__main__':
    app.run(debug=True)
