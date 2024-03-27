import psycopg2
import requests
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# PostgreSQL Connection Details
pg_host = 'localhost'
pg_port = ''
pg_db = 'postgres'
pg_user = 'postgres'
pg_password = ''

# Zoho CRM API Details
zoho_crm_api_endpoint = ''
zoho_crm_auth_token = '' 

# Check Zoho CRM Auth Token
if not zoho_crm_auth_token:
    logger.error("Zoho CRM Auth Token is missing. Please update the script with a valid API Key.")
    exit()

# Connect to PostgreSQL
try:
    conn = psycopg2.connect(
        host=pg_host,
        port=pg_port,
        database=pg_db,
        user=pg_user,
        password=pg_password
    )
    cursor = conn.cursor()
except psycopg2.Error as e:
    logger.error(f"Error connecting to PostgreSQL: {e}")
    exit()

# Fetch data from PostgreSQL
try:
    cursor.execute("SELECT * FROM Leads")
    rows = cursor.fetchall()
except psycopg2.Error as e:
    logger.error(f"Error executing SQL query: {e}")
    exit()

# Iterate through rows and push data to Zoho CRM
for row in rows:
    # Prepare data for Zoho CRM API
    zoho_crm_data = {
        'data': [{
            'Lead Name': f"{row[1]} {row[2]}",
            'Last_Name': row[2],
            'Lead Owner': 'test',
            'Lead Source': 'test',
            'Lead Status': 'לא רלוונטי',
            'Association': ['test'],
            'Description': 'test',
            'Last Activity Time': datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z'),
            'Created Time': datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z'),
            'Email': row[3],
            'Phone': row[4],
            'Company': row[5]
        }]
}

    # Make API request to Zoho CRM
    try:
        response = requests.post(
            zoho_crm_api_endpoint,
            headers={'Authorization': f'Zoho-oauthtoken {zoho_crm_auth_token}'},
            json=zoho_crm_data
        )
        response_json = response.json()
        if 'data' in response_json and 'code' in response_json['data']:
            if response_json['data']['code'] == 3000:
                logger.info(f"Successfully pushed data to Zoho CRM for record {row[0]}")
            else:
                logger.error(f"Error pushing data to Zoho CRM for record {row[0]}: {response_json}")
        else:
            logger.error(f"Unexpected response from Zoho CRM API: {response_json}")
    except requests.RequestException as e:
        logger.error(f"Error making API request to Zoho CRM: {e}")

# Close PostgreSQL connection
conn.close()