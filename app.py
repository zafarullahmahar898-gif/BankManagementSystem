
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>Bank Management System</title>
    </head>
    <body style="font-family: Arial; text-align: center; margin-top: 100px;">
        <h1>Bank Management System</h1>
        <h3>Web Application</h3>
        <p>Welcome! Aapki website chal rahi hai.</p>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=False)
