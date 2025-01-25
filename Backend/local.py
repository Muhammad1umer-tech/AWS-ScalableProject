from dotenv import load_dotenv
import pandas as pd
import psycopg2
import json
import fsspec
import os
import s3fs
import boto3

load_dotenv()

def retrieve_data_from_s3():
    #a session using the instance's role (boto3 automatically uses instance metadata credentials)
    session = boto3.Session()

    # Create an S3 client using the session
    s3 = session.client('s3')

    # Get the S3 path from environment variable
    s3_path = os.getenv("CSV_FILE_PATH")

    # Extract bucket name and key from the S3 path (e.g., s3://bucket-name/path/to/file.csv)
    bucket_name = s3_path.split('/')[2]
    object_key = '/'.join(s3_path.split('/')[3:])

    # Read the content of the file from S3
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    content = response['Body'].read().decode('utf-8')

    # Print the content of the file
    #print("hahah",content)
    return content

def retrieve_data_from_s3_2():
    data = ''
    url = os.getenv("CSV_FILE_PATH")
        
    with fsspec.open(url, mode="r") as f:
        # Load JSON data
        data = json.load(f)
    return data

def check_file():
    file_path = os.getenv("CSV_FILE_PATH")
    print(file_path)
    df = pd.read_csv(file_path)
    print("check_file: ",df)

def create_db():
    try:
        # Get connection details from environment variables
        postgres_user = os.getenv("POSTGRES_USER")
        postgres_password = os.getenv("POSTGRES_PASSWORD")
        postgres_db = os.getenv("POSTGRES_DB")
        postgres_endpoint = os.getenv("POSTGRES_ENDPOINT")
        postgres_port = os.getenv("POSTGRES_PORT")
        conn = psycopg2.connect(
            dbname=postgres_db,
            user=postgres_user,
            password=postgres_password,
            host=postgres_endpoint,
            port=postgres_port)
        
        cursor = conn.cursor()
        
        # Step 1: Create the table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS data (
            id SERIAL PRIMARY KEY,
            question TEXT NOT NULL,
            answer TEXT NOT NULL
        );
        """
        cursor.execute(create_table_query)
        
        #Step 2: Add data
        datas = retrieve_data_from_s3()
        insert_query = "INSERT INTO data (question, answer) VALUES (%s, %s)"
        for item in datas:
            for question, answer in item.items():
                print(question)
                cursor.execute(insert_query, (question, answer))
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Data inserted successfully.")
    except Exception as e:
        print("Error while inserting to database: ",e)


def input_to_response(question):
    try:
        # Get connection details from environment variables
        postgres_user = os.getenv("POSTGRES_USER")
        postgres_password = os.getenv("POSTGRES_PASSWORD")
        postgres_db = os.getenv("POSTGRES_DB")
        postgres_endpoint = os.getenv("POSTGRES_ENDPOINT")
        postgres_port = os.getenv("POSTGRES_PORT")
        conn = psycopg2.connect(
            dbname=postgres_db,
            user=postgres_user,
            password=postgres_password,
            host=postgres_endpoint,
            port=postgres_port)
        
        cursor = conn.cursor()
        
        select_query = "SELECT answer FROM data WHERE question = %s"
        cursor.execute(select_query, (question,))

        # Fetch the result
        result = cursor.fetchone()
        print(result)
        if result:
            return result[0]
        else:
            return "Question not found in the database."
    except Exception as e:
        print("Error while retrieving data from DB", e)
        return "Error while retrieving data from DB"

print(retrieve_data_from_s3())
#create_db()    
input_to_response("are you familiar with python")
