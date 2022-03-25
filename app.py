from flask import Flask
from flask import request, escape, redirect
import string
import random
import urllib
import mysql.connector

app = Flask(__name__)

@app.route("/")
def index():
        original_url = str(escape(request.args.get("URL", "")))
        if original_url:
            original_url = original_url.replace("&amp;", "&")
            original_url = original_url.replace("&lt;", "<")
            original_url = original_url.replace("&gt;", ">")
            shortened_url = shorten(original_url)
        else:
            shortened_url = ""
        return( """
                    <!doctype html>
                    <html>
                        <Title>2Short</Title>
                        <head>
                            <style>
                                * {
                                    box-sizing: border-box;
                                }
                                body {
                                    font-family: Arial;
                                    width: 100%;
                                    border-radius: 5px;
                                    background-color: #45a049;
                                    padding: 20px;
                                    text-align: center;
                                    color: #c9cdd1;
                                }
                                .header {
                                    padding: 30px;
                                    text-align: center;
                                }
                                input[type=text], select {
                                    width: 75%;
                                    padding: 12px 20px;
                                    margin: 8px 0;
                                    display: inline-block;
                                    border: 1px solid #ccc;
                                    border-radius: 25px;
                                    box-sizing: border-box;
                                    box-shadow:0 10px 16px 0 rgba(0,0,0,0.2),0 6px 20px 0 rgba(0,0,0,0.19);
                                }
                                input[type=submit] {
                                    width: 10%;
                                    background-color: #26802a;
                                    color: white;
                                    padding: 14px 20px;
                                    margin: 8px 0;
                                    border: none;
                                    border-radius: 25px;
                                    cursor: pointer;
                                    box-shadow:0 10px 16px 0 rgba(0,0,0,0.2),0 6px 20px 0 rgba(0,0,0,0.19);
                                }
                                input[type=submit]:hover {
                                    background-color: #45a049;
                                }
                                button {
                                    width: 10%;
                                    background-color: #26802a;
                                    color: white;
                                    padding: 14px 20px;
                                    margin: 8px 0;
                                    border: none;
                                    border-radius: 25px;
                                    cursor: pointer;
                                    box-shadow:0 10px 16px 0 rgba(0,0,0,0.2),0 6px 20px 0 rgba(0,0,0,0.19);
                                }
                                button:hover {
                                    background-color: #45a049;
                                }
                            </style>
                        </head>
                        <body>
                            <div class=header>
                                <h1>URL Shortener</h1>
                            </div>
                            <div>
                                <form action="" method="get">
                                    <input type="text" name="URL">
                                    <p></p>
                                    <input type="submit" value="Shorten">
                                </form>
                            </div>
                            <script>
                                function CopyToClipboard(containerid) {
                                    if (document.selection) {
                                        var range = document.body.createTextRange();
                                        range.moveToElementText(document.getElementById(containerid));
                                        range.select().createTextRange();
                                        document.execCommand("copy");
                                    } else if (window.getSelection) {
                                        var range = document.createRange();
                                        range.selectNode(document.getElementById(containerid));
                                        window.getSelection().addRange(range);
                                        document.execCommand("copy");
                                    }
                                }
                            </script>
                        </body>
                    </html>
                """
                + shortened_url
        )

@app.route("/<string:original_url>")
def retrieve(original_url):
    shortened_url = original_url
    shortened_url = shortened_url.split("/")
    shuffled_string = shortened_url[-1]

    sql_connection = mysql.connector.connect(host="localhost", user="database_user", passwd="database_user_password", database="linkshortener")
    sql_cursor = sql_connection.cursor()
    sql_cursor.execute("SELECT * FROM shortslinks WHERE shorts = '"+shuffled_string+"';")
    query_results = sql_cursor.fetchall()
    try:
        return(redirect(query_results[0][1]))
    except:
        return("The link you requested does not exist!")

def shorten(original_url):
    original_url = original_url

    sql_connection = mysql.connector.connect(host="localhost", user="database_user", passwd="database_user_password", database="linkshortener")
    sql_cursor = sql_connection.cursor()

    sql_cursor.execute("SELECT * FROM shortslinks WHERE shorts = '"+original_url+"';")
    initial_query_results = sql_cursor.fetchall()
    
    if len(initial_query_results) != 0:
        retrieve(original_url)

    original_url = urllib.parse.unquote_plus(original_url)
    original_url = original_url.replace(" ", "+")

    def random_string():
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits

        random_lowercase = "".join((random.choice(string.ascii_lowercase) for x in range(2)))
        random_uppercase = "".join((random.choice(string.ascii_uppercase) for x in range(2)))
        random_digits = "".join((random.choice(string.digits) for x in range(2)))

        joined_string = random_lowercase + random_uppercase + random_digits
        list_joined_string = list(joined_string)
        random.shuffle(list_joined_string)
        shuffled_string = "".join(list_joined_string)


        sql_cursor.execute("SELECT * FROM shortslinks WHERE shorts = '"+shuffled_string+"';")
        query_results = sql_cursor.fetchall()

        if len(query_results) != 0:
            random_string()
        else:
            return shuffled_string

    shuffled_string = random_string()

    sql_cursor.execute("INSERT INTO shortslinks (shorts, links) VALUES ('"+shuffled_string+"', '"+original_url+"');")

    sql_connection.commit()
    sql_connection.close()

    shortened_url = "https://example.com/" + shuffled_string
    return("""
            <div calss=sl>
                <h3>Shortened URL</h3>
                <p id="surl">{surl}</p>
                <button onclick="CopyToClipboard('surl')">Copy 2Short URL</button>
            </div>
        """.format(surl=shortened_url))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
