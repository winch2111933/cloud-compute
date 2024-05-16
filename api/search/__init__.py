import logging
import azure.functions as func
import pyodbc
import json
import os


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(
        "Python HTTP trigger function processed a request to find dog walkers."
    )

    # Retrieve 'location' parameter from the query string or the request body.
    location = req.params.get("location")
    if location is None:
        try:
            req_body = req.get_json()
            location = req_body.get("location")
        except ValueError:
            return func.HttpResponse(
                json.dumps({"Bad request": "Invalid JSON input or missing 'location'."}),
                status_code=400,
                headers={"Content-Type": "application/json"},
            )

    if not location:
        return func.HttpResponse(
            json.dumps(
                {
                    "Bad Request": "Please pass a location on the query string or in the request body."
                }
            ),
            status_code=400,
            headers={"Content-Type": "application/json"},
        )

    # Access the connection string from environment variables
    conn_str = os.getenv("SqlConnectionString")
    if not conn_str:
        logging.error("SQL connection string is not set.")
        return func.HttpResponse(
            json.dumps(
                {"Server error": "SDatabase connection configuration error."}
            ),
            status_code=500,
            headers={"Content-Type": "application/json"},
        )

    try:
        # Connect to the database and execute the query
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            sql_query = """
            SELECT Forename, Surname, ExperienceStartDate, Email
            FROM dbo.Walker
            WHERE City LIKE ? OR Postcode LIKE ?
            """
            like_location = f"%{location}%"
            cursor.execute(sql_query, like_location, like_location)
            rows = cursor.fetchall()

            # Prepare the data for JSON response
            walkers = [
                {
                    "forename": row[0],
                    "surname": row[1],
                    "experience_start_date": row[2].strftime("%Y-%m-%d"),
                    "email": row[3],
                }
                for row in rows
            ]

            return func.HttpResponse(
                json.dumps(walkers, ensure_ascii=False),
                status_code=200,
                mimetype="application/json",
            )

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return func.HttpResponse(
            json.dumps({"Server error": "Failed to fetch data from the database."}),
            status_code=500,
            headers={"Content-Type": "application/json"},
        )
