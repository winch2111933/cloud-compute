import logging
import azure.functions as func
import pyodbc
import json
import os


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(
        "Python HTTP trigger function processed a request to add a dog walker."
    )

    try:
        # Parse incoming JSON data
        req_body = req.get_json()
        forename = req_body.get("forename")
        surname = req_body.get("surname")
        experience_start_date = req_body.get("experienceStartDate")
        about_me = req_body.get("aboutMe")
        email = req_body.get("email")
        city = req_body.get("city")
        postcode = req_body.get("postCode")

        # Validate mandatory fields
        if not all([forename, surname, experience_start_date, email, city, postcode]):
            return func.HttpResponse(
                json.dumps(
                    {"Bad request": "Missing required fields. All fields must be provided."}
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
                    {"Server error": "Database connection configuration error."}
                ),
                status_code=500,
                headers={"Content-Type": "application/json"},
            )

        # Insert data into the database
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            sql_query = """
            INSERT INTO dbo.Walker (Forename, Surname, ExperienceStartDate, AboutMe, Email, City, PostCode)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(
                sql_query,
                forename,
                surname,
                experience_start_date,
                about_me,
                email,
                city,
                postcode,
            )
            conn.commit()

        return func.HttpResponse(
            json.dumps(
                {"Success": f"Dog walker {forename} {surname} added successfully!"}
            ),
            status_code=201,
            headers={"Content-Type": "application/json"},
        )

    except json.JSONDecodeError:
        logging.error("Error decoding JSON.")
        return func.HttpResponse(
            json.dumps({"Bad request": "Invalid JSON format."}),
            status_code=400,
            headers={"Content-Type": "application/json"},
        )
    except pyodbc.Error as e:
        logging.error(f"Database error: {str(e)}")
        return func.HttpResponse(
            json.dumps({"Server error": "Unable to write to the database."}),
            status_code=500,
            headers={"Content-Type": "application/json"},
        )
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return func.HttpResponse(
            json.dumps({"Server error": "An unexpected error occurred."}),
            status_code=500,
            headers={"Content-Type": "application/json"},
        )
