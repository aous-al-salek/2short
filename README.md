# 2short
This is a URL shortener Flask app. This app does not support statistics yet.

Requirements:
  - Ubuntu 20.04 LTS
  - Python 3.9
    - mysql-connector-python module
    - flask
    - urllib
    - random
    - string
  - MariaDB server 10
    - A database called "linkshortener"
    - A database user "database_user" with password "database_user_password"
    - Grant privileges to "database_user" over "linkshortener"
