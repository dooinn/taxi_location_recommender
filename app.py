from flask import Flask, request, jsonify
import pymysql
import json
from datetime import date, timedelta


app = Flask(__name__)



@app.route("/")
def home():
    return "Home"





def fetch_all_data(table_name):
    try:
        # Connection to the database
        db_conn = pymysql.connect(host="127.0.0.1", user="root", passwd="password", database="chicago_taxi",
                                  cursorclass=pymysql.cursors.DictCursor)
        with db_conn.cursor() as cursor:
            # Fetch all data from the specified table
            cursor.execute(f"SELECT * FROM {table_name}")
            data = cursor.fetchall()
        db_conn.close()

        # Check if data is found
        if data:
            return jsonify(data)
        else:
            return f"No data found in table {table_name}", 404

    except pymysql.MySQLError as e:
        print(f"Error connecting to the MySQL database: {e}")
        return "Internal Server Error", 500





def fetch_paginated_data(table_name, page, page_size):
    try:
        # Calculate offset
        offset = (page - 1) * page_size

        # Connection to the database
        db_conn = pymysql.connect(host="127.0.0.1", user="root", passwd="password", database="chicago_taxi",
                                  cursorclass=pymysql.cursors.DictCursor)
        with db_conn.cursor() as cursor:
            # Count total records
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            total_records = cursor.fetchone()['COUNT(*)']

            # Fetch paginated data
            cursor.execute(f"SELECT * FROM {table_name} LIMIT {page_size} OFFSET {offset}")
            data = cursor.fetchall()
        db_conn.close()

        # Calculate total pages
        total_pages = (total_records + page_size - 1) // page_size

        # Check if data is found
        if data:
            return jsonify({
                "data": data,
                "total_records": total_records,
                "total_pages": total_pages,
                "current_page": page,
                "page_size": page_size
            })
        else:
            return f"No data found in table {table_name} for the specified page", 404

    except pymysql.MySQLError as e:
        print(f"Error connecting to the MySQL database: {e}")
        return "Internal Server Error", 500




@app.route("/community")
def community():
    return fetch_all_data("community")

@app.route("/taxi")
def taxi():
    return fetch_all_data("taxi")

@app.route("/company")
def company():
    return fetch_all_data("company")

@app.route("/location")
def location():
    return fetch_all_data("location")

@app.route("/trips")
def trips():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)

    return fetch_paginated_data("trips", page, page_size)





    
if __name__ == "__main__":
    app.run(debug=True)

