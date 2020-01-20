from flask_blog import app


if __name__ == '__main__':
    app.run(debug=True)
    # must set FLASK_APP=filename i.e run.py to use cmd(flask run)
    # Can use set FLASK_DEBUG=1 if you are using flask run
    # else can use python run.py
