from flask import Flask, request, jsonify
import pymysql
import json
from datetime import date, timedelta

app = Flask(__name__)


def fetch_all_data(table_name):
    try:
        db_conn = pymysql.connect(host="127.0.0.1", user="root", passwd="password", database="chicago_taxi",
                                  cursorclass=pymysql.cursors.DictCursor)
        with db_conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table_name}")
            data = cursor.fetchall()
        db_conn.close()
        if data:
            return jsonify(data)
        else:
            return f"No data found in table {table_name}", 404

    except pymysql.MySQLError as e:
        print(f"Error connecting to the MySQL database: {e}")
        return "Internal Server Error", 500


def fetch_data_with_filters(company_id, start_date, end_date, page, page_size):
    try:

        db_conn = pymysql.connect(host="127.0.0.1", user="root", passwd="password", database="chicago_taxi",
                                  cursorclass=pymysql.cursors.DictCursor)
        with db_conn.cursor() as cursor:
            count_query = "SELECT COUNT(*) FROM trips WHERE company_id = %s"

            # Add date filters if provided for the count query
            count_params = [company_id]
            if start_date and end_date:
                count_query += " AND trip_start_timestamp BETWEEN %s AND %s"
                count_params.extend([start_date, end_date])

            # Execute the count query
            cursor.execute(count_query, count_params)
            total_records = cursor.fetchone()['COUNT(*)']

            # Calculate total pages
            total_pages = (total_records + page_size - 1) // page_size

            # Prepare the data query with filters and pagination
            data_query = "SELECT * FROM trips WHERE company_id = %s"
            data_params = [company_id]
            if start_date and end_date:
                data_query += " AND trip_start_timestamp BETWEEN %s AND %s"
                data_params.extend([start_date, end_date])

            # Add pagination
            offset = (page - 1) * page_size
            data_query += " LIMIT %s OFFSET %s"
            data_params.extend([page_size, offset])

            # Execute the data query
            cursor.execute(data_query, data_params)
            data = cursor.fetchall()
        db_conn.close()

        # Check if data is found
        if data:
            return jsonify({
                "current_page": page,
                "total_records": total_records,
                "total_pages": total_pages,
                "page_size": page_size,
                "data": data
            })
        else:
            return "No data found for the given filters", 404

    except pymysql.MySQLError as e:
        print(f"Error connecting to the MySQL database: {e}")
        return "Internal Server Error", 500

# Routes
@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chicago Taxi Data API</title>
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        .api-endpoint {
            margin-bottom: 30px;
        }
        .api-url {
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h1>Chicago Taxi Data API</h1>
    <p>Welcome to the Chicago Taxi Data API. Use the following endpoints to access data about the Chicago Taxi ecosystem.</p>

    <div class="api-endpoint">
        <h2>Community</h2>
        <p>Retrieves all community data.</p>
        <p><span class="api-url">GET /community</span></p>
    </div>

    <div class="api-endpoint">
        <h2>Taxi</h2>
        <p>Retrieves all taxi data.</p>
        <p><span class="api-url">GET /taxi</span></p>
    </div>

    <div class="api-endpoint">
        <h2>Company</h2>
        <p>Retrieves all company data.</p>
        <p><span class="api-url">GET /company</span></p>
    </div>

    <div class="api-endpoint">
        <h2>Location</h2>
        <p>Retrieves all location data.</p>
        <p><span class="api-url">GET /location</span></p>
    </div>

    <div class="api-endpoint">
        <h2>Filtered Trips</h2>
        <p>Retrieves trip data for a specific company within an optional date range. Pagination is supported through query parameters.</p>
        <p><span class="api-url">GET /trips/&lt;company_id&gt;/&lt;start_date&gt;/&lt;end_date&gt;</span></p>
        <p>Parameters:</p>
        <ul>
            <li><strong>company_id</strong> (path parameter): The ID of the company.</li>
            <li><strong>start_date</strong> (path parameter, optional): The start date for filtering trips.</li>
            <li><strong>end_date</strong> (path parameter, optional): The end date for filtering trips.</li>
            <li><strong>page</strong> (query parameter, optional): The page number for pagination (default is 1).</li>
            <li><strong>page_size</strong> (query parameter, optional): The number of records per page (default is 10000).</li>
        </ul>
        <p>Example: <span class="api-url">GET /trips/1/2023-01-01/2023-01-31?page=1&page_size=100</span></p>
    </div>

</body>
</html>
"""



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

@app.route("/trips/<int:company_id>/", defaults={'start_date': None, 'end_date': None})
@app.route("/trips/<int:company_id>/<start_date>/<end_date>")
def filtered_trips(company_id, start_date, end_date):
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10000, type=int)
    return fetch_data_with_filters(company_id, start_date, end_date, page, page_size)

    
if __name__ == "__main__":
    app.run(debug=True)

