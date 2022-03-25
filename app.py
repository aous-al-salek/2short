from flask import Flask
from flask import request, escape
import string
import random
import mysql.connector

app = Flask(__name__)

@app.route("/")
def index():
        original_url = str(escape(request.args.get("URL", "")))
        if original_url:
            shortened_url = shorten(original_url)
        else:
            shortened_url = ""
        return( """
                    <!doctype html>
                    <html>
                        <Title>URL Shortener</Title>
                        <head>URL Shortener</head>
                        <body>
                            <form action="" method="get">
                                <input type="text" name="URL">
                                <input type="submit" value="Shorten">
                            </form>
                        </body>
                    </html>
                """
                + "Shortened URL: "
                + shortened_url
        )

@app.route("/<original_url>")
def shorten(original_url):
    original_url = original_url

    sql_connection = mysql.connector.connect(host="localhost", user="database_user", passwd="database_user_password", database="linkshortener")
    sql_cursor = sql_connection.cursor()

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
    return("<a href="+shortened_url+">"+shortened_url+"</a>")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
