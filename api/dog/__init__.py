import logging
import azure.functions as func
import pyodbc
import json
import os


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    try:
        # Parse incoming JSON data
        req_body = req.get_json()
        pet_name = req_body.get("petName")
        date_of_birth = req_body.get("dateOfBirth")
        breed = req_body.get("breed")
        owner_name = req_body.get("ownerName")
        owner_email = req_body.get("ownerEmail")

        # Check for required fields
        if not (pet_name and date_of_birth and breed and owner_name and owner_email):
            return func.HttpResponse(
                json.dumps(
                    {
                        "Bad request": "Missing one or more of the required fields: petName, dateOfBirth, breed, ownerName, ownerEmail."
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
                json.dumps({"Server error": "Unable to connect to the database."}),
                status_code=500,
                headers={"Content-Type": "application/json"},
            )

        # Execute the SQL query to insert data
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            sql_query = """
            INSERT INTO dbo.Pet (PetName, DateOfBirth, Breed, OwnerName, OwnerEmail)
            VALUES (?, ?, ?, ?, ?) 
            """
            cursor.execute(
                sql_query, pet_name, date_of_birth, breed, owner_name, owner_email
            )
            conn.commit()

        return func.HttpResponse(
            json.dumps({"Success": f"Dog {pet_name} added successfully!"}),
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
        logging.error("Database error: %s", e)
        return func.HttpResponse(
            json.dumps({"Server error": "Unable to write to the database."}),
            status_code=500,
            headers={"Content-Type": "application/json"},
        )
    except Exception as e:
        logging.error("Unexpected error: %s", e)
        return func.HttpResponse(
            json.dumps({"Server error": "An unexpected error occurred."}),
            status_code=500,
            headers={"Content-Type": "application/json"},
        )
