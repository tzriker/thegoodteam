
// Extracts UTM parameters from the URL
function getUTMParams(url) {
    // Parses the URL
    const params = new URLSearchParams(url.split('?')[1]);
    // Gets the UTM source parameter
    const source = params.get('utm_source') || 'Unknown'; // 'Unknown' if the parameter doesn't exist

    // Returns an object with the UTM data
    return {
      source,
    };
  }
  
  // Sends lead data to the database
  async function sendLeadData(leadData) {
    // Creates a request body
    const body = {
      ...leadData,
    };
    // Sends the lead data
    const response = await fetch('https://api.wix.com/v1/sites/<YOUR_SITE_ID>/leads', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer <YOUR_ACCESS_TOKEN>`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(body)
    });
    // Handles the response
    if (response.status === 200) {
      console.log('Lead data sent successfully!');
    } else {
      console.error('Error sending lead data:', response.statusText);
    }
  }
  // Updates the lead source field in the Wix Leads table
  async function updateLeadSource(leadId, source) {
    // Creates a request body
    const body = {
      source,
    };

    // Updates the lead source field
    const response = await wixData.update('leads', leadId, body);
    // Handles the response
    if (response.status === 200) {
      console.log('Lead source updated successfully!');
    } else {
      console.error('Error updating lead source:', response.statusText);
    }
  }

  // Gets the current page URL
  const url = window.location.href;
  // Extracts the UTM parameter
  const { source } = getUTMParams(url);
  // Creates a lead data object
  const leadData = {
    source,
    // Add additional lead data
  };
  // Sends the lead data to the database
  sendLeadData(leadData);
  // Gets the current lead ID
  const leadId = wixLocation.query['leadId'];
  // Updates the lead source field
  updateLeadSource(leadId, source);
  