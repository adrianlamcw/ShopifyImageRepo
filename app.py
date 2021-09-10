from flask import Flask, flash, render_template, request, redirect, url_for
from passlib.hash import sha256_crypt
import sqlite3
from sqlite3 import Error
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config["UPLOAD_PATH"] = "static/images/"
app.config["MAX_CONTENT_LENGTH"] = 32 * 1024 * 1024
app.config["UPLOAD_EXTENSIONS"] = [".jpg", ".png", ".gif"]

# User session id
CURRENT_USER_ID = 0

### INITIALIZATION ###
# Connect to the sqlite database and sets up a cursor object
def get_cursor_connection():
    try:
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        return (cur, con)
    except Error:
        print(Error)

# Initialize all databases and sets up some sample users and sample images
def initialize():
    (cur, con) = get_cursor_connection()

    # Setup a users table with sample users
    cur.execute("DROP TABLE IF EXISTS users")
    cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")

    # Add sample users
    add_user("bunny", "carrots", cur)
    add_user("cat", "salmon", cur)
    add_user("bird", "seeds", cur)

    # Setup an images table with sample images
    cur.execute("DROP TABLE IF EXISTS images")
    cur.execute("CREATE TABLE images (id INTEGER PRIMARY KEY, user_id INTEGER, image_location TEXT) ")
    cur.execute("""INSERT INTO images (user_id, image_location) VALUES
        (1, 'brownbunny.jpg'),
        (1, 'easter.jpg'),
        (2, 'catlookingup.jpg'),
        (2, 'sleepycat.jpg'),
        (3, 'goose.jpg')
    """)

    # Commit the db changes
    con.commit()
    print("Database has been succesfully initialized with sample data")

### HELPER FUNCTIONS ###
def add_user(username, password, cur):
    hash_password = sha256_crypt.hash(password)
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_password))

### ROUTES ###
@app.route("/logout")
@app.route("/")
def login_page():
    return render_template("index.html")

@app.route("/home")
def home():
    (cur, con) = get_cursor_connection()
    cur.execute("SELECT * FROM images WHERE user_id = ?", (CURRENT_USER_ID,))
    rows = cur.fetchall()

    # Format images for html template
    images = []
    for row in rows:
        images.append({
            "image_id": row[0],
            "user_id": row[1],
            "src": "/static/images/" + row[2],
        })

    # Get username of current user
    cur.execute("SELECT * FROM users WHERE id = ?", (CURRENT_USER_ID,))
    rows = cur.fetchall()
    username = rows[0][1]

    return render_template("home.html", user=username, images=images)

@app.route("/upload", methods=["POST"])
def upload():
    (cur, con) = get_cursor_connection()
    for uploaded_image in request.files.getlist("file"):
        # Check for valid filenames
        filename = secure_filename(uploaded_image.filename)
        if filename != "":
            file_type = os.path.splitext(filename)[1]
            if file_type not in app.config['UPLOAD_EXTENSIONS']:
                print("Accepted image types are .png .jpg .gif")
            else:
                uploaded_image.save(os.path.join(app.config['UPLOAD_PATH'], filename))
                cur.execute("INSERT INTO images (user_id, image_location) VALUES (?, ?)",
                    (CURRENT_USER_ID, filename))

    con.commit()
    return redirect(url_for("home"))

@app.route("/login", methods=["GET", "POST"])
def login():
    (cur, con) = get_cursor_connection()

    if request.method == "POST":
        username = request.form['username']
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cur.fetchall()

        # Will only return one row since username should be unique
        hash = row[0][2]
        password = request.form['password']
    
        # Validate password and set current user session
        if sha256_crypt.verify(password, hash):
            global CURRENT_USER_ID
            CURRENT_USER_ID = row[0][0]
            return redirect(url_for("home"))
        else:
            return render_template("index.html", error="Invalid Credentials")

    return render_template("index.html")

if __name__ == "__main__":
    initialize()
    app.run(debug = True)