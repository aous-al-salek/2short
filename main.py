import string
import random
import mysql.connector

def main():

    def shorten():
        original_url = input("Please enter the original URL: ")

        sql_connection = mysql.connector.connect(host="localhost", user="database_user", passwd="database_user_password", database="linkshortner")
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

        print("The shortened link is: https://example.com/" + shuffled_string)

    def retrieve():
        shortened_url = input("Please enter the shortened URL: ")
        shortened_url = shortened_url.split("/")
        shuffled_string = shortened_url[-1]

        sql_connection = mysql.connector.connect(host="localhost", user="database_user", passwd="database_user_password", database="linkshortner")
        sql_cursor = sql_connection.cursor()
        sql_cursor.execute("SELECT * FROM shortslinks WHERE shorts = '"+shuffled_string+"';")
        query_results = sql_cursor.fetchall()
        try:
            print("The original link is:", query_results[0][1])
        except:
            print("The link you entered does not exist!")

    choice = input("Do you want to shorten or retrieve? s/r ")
    if choice.lower() == "s":
        shorten()
    elif choice.lower() == "r":
        retrieve()
    else:
        print("Please enter a valid choice!")
        main()

if __name__ == "__main__":
    main()
