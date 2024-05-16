from faker import Faker
import random

# Initialise Faker with the British localisation set.
fake = Faker('en_GB')

# Function to generate the dog walkers.
def generate_dummy_data():
    """Generate a single row of dummy data."""
    Forename = fake.first_name()
    Surname = fake.last_name()
    ExperienceStartDate = fake.date_between(start_date="-5y", end_date="today")
    AboutMe = fake.text(max_nb_chars=200) if random.choice([True, False]) else None
    Email = fake.ascii_free_email()  # Changed to ascii_free_email for more generic email generation
    City = fake.city()
    PostCode = fake.postcode()
    
    # Formatting AboutMe with single quotes for SQL insertion.
    if AboutMe is not None:
        AboutMe = AboutMe.replace("'", "''")  # Replace single quote with two single quotes for SQL.
        AboutMe = f"'{AboutMe}'"
    else:
        AboutMe = "NULL"

    return f"('{Forename}', '{Surname}', '{ExperienceStartDate}', {AboutMe}, '{Email}', '{City}', '{PostCode}')"

# Function to generate the dog owners.
def generate_dog_data():
    # List of dog breeds.
    breeds = ['Labrador Retriever', 'German Shepherd', 'Golden Retriever', 'French Bulldog', 
              'Bulldog', 'Poodle', 'Beagle', 'Rottweiler', 'Yorkshire Terrier', 'Cocker Spaniel'] 
    
    pet_name = fake.first_name()
    date_of_birth = fake.date_of_birth(minimum_age=0, maximum_age=15)  # Dog age range from 0 to 15 years.
    breed = random.choice(breeds)  # Randomly choose a breed.
    owner_name = fake.name()
    owner_email = fake.email()

    return f"('{pet_name}', '{date_of_birth.strftime('%Y-%m-%d')}', '{breed}', '{owner_name}', '{owner_email}')"


# Generate dummy data rows.
dummy_walkers = [generate_dummy_data() for _ in range(100)]
dummy_owners = [generate_dog_data() for _ in range(100)]

# SQL statement.
sql_insert_walkers = f"INSERT INTO dbo.Walker (Forename, Surname, ExperienceStartDate, AboutMe, Email, City, PostCode) VALUES\n" + ",\n".join(dummy_walkers) + ";"
sql_insert_dogs = f"INSERT INTO dbo.Pet (PetName, DateOfBirth, Breed, OwnerName, OwnerEmail) VALUES\n" + ",\n".join(dummy_owners) + ";"

# Save the SQL statement to a file.
data = [
    ['insert_walkers.sql',sql_insert_walkers],
    ['insert_dogs.sql',sql_insert_dogs]
]

# Save the mock data.
for item in data:
    with open(item[0], 'w') as file:
        file.write(item[1])

    print(f"SQL insert statement saved to {item[0]}")
