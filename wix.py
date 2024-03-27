import requests
import json

# Replace these values with your actual Wix site's information
wix_site_id = ''
access_token = ''

def import_leads_from_wix():
    url = f'https://www.wixapis.com/crm/v1/sites/{wix_site_id}/leads'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        leads_data = response.json()

        # Process leads data as per your requirement
        for lead in leads_data['leads']:
            # Example: print lead's name and email
            print(f"Lead Name: {lead['contactInfo']['name']}, Email: {lead['contactInfo']['emails'][0]['email']}")

        print("Leads imported successfully!")
    except requests.exceptions.HTTPError as e:
        print(f"Error occurred: {e}")

import_leads_from_wix()