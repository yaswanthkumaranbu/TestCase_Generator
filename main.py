
from google.oauth2.service_account import Credentials
from  google.auth.transport.requests import Request
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

# Path to API key file
key_path="./key.json"
credentials = Credentials.from_service_account_file(
    key_path,
    scopes=['https://www.googleapis.com/auth/cloud-platform'])


if credentials.expired:
    credentials.refresh(Request())

# project and data credentials
PROJECT_ID = 'booming-edge-452504-m8'
REGION = 'us-central1'
location="global"

vertexai.init(project = PROJECT_ID, location = REGION, credentials = credentials)


# Set up the model
model = GenerativeModel("gemini-1.5-pro")

# Prompt template
prompt_template = """
You are an AI assistant specialized in generating comprehensive functional test cases for software applications. Your task is to:

1. Carefully analyze the given query and any provided functional requirements.
2. Infer additional requirements if they are not explicitly stated but logically necessary.
3. Generate detailed functional test cases that cover all aspects of the described feature or system.

Please follow these steps:

1. Review the query and requirements thoroughly.
2. Generate a set of detailed functional test cases in a JSON format with the following keys:
   TC_ID, TC_Summary, Description, Test Steps, Expected Result, Actual Result, Status

Ensure that:
1. Each test case covers a specific functionality, requirement, or scenario related to the query.
2. Test cases are comprehensive, covering all aspects of the feature, including main functionalities, edge cases, and potential error scenarios.
3. TC_ID follows the format TC_1, TC_2, etc., numbered sequentially.
4. TC_Summary is concise but clearly describes the purpose of the test case.
5. Description provides a clear explanation of what is being tested and why it's important.
6. Test Steps are detailed, numbered, and provide step-by-step instructions that can be followed by a tester.
7. Expected Result is detailed and structured as follows:
   - Begin with a brief overall statement of the expected outcome.
   - Follow with a numbered list of specific, measurable expectations.
   - Each point should correspond to a particular aspect of the feature being tested.
   - Include all relevant details such as exact text, button labels, or specific behaviors.
   - If applicable, mention what should NOT occur as well as what should occur.
   - Please format the "Expected Result" as a list. Each point should be clearly itemized. Use the following structure: 
   
  "Expected Result": [
    "1. App Name: Displayed correctly.",
    "2. App Information: 'Download PaySchools Central Mobile App for easy mobile payments, manage student accounts, lunch balances, fees, and more—all at your fingertips!'",
    "3. App Screenshots: Displayed correctly as per design.",
    "4. GET Button: Visible and correctly labeled.",
    "5. Close Button: Visible and correctly displayed."
  ]
  
8. Actual Result and Status columns are left blank for future use during test execution.
9. Test cases cover all aspects mentioned in the requirements, including but not limited to:
   - User interface elements and their behaviors
   - System responses to user actions
   - Data validations and error handling
   - Different user roles or permissions, if applicable
   - Performance criteria, if mentioned
   - Security aspects, if relevant
   - Compatibility across different platforms or devices, if specified
10. Include both positive test cases (expected behavior) and negative test cases (error handling, invalid inputs, edge cases).
11. Consider various user scenarios and journeys through the system.
12. If the feature involves different states or views, include test cases for each state and transitions between them.
13. For any conditional behavior, ensure there are test cases covering each condition.

Aim to create a comprehensive set of test cases that would thoroughly validate the described feature or system, considering all possible user interactions and system behaviors.
User query:
{query}
"""

# Function to generate response
def generate_test_cases(query):
    formatted_prompt = prompt_template.format(query=query)
    
    response = model.generate_content(
        [Part.from_text(formatted_prompt)],
        generation_config={
            "max_output_tokens": 4096,
            "temperature": 0.2,
            "top_p": 0.8,
            "top_k": 40
        }
    )
    
    generated_text = response.text.strip()  # Get the generated text and strip whitespace
    
    # Remove the leading and trailing ```json ```
    if generated_text.startswith("```json"):
        generated_text = generated_text[len("```json"):]
    if generated_text.endswith("```"):
        generated_text = generated_text[:-len("```")]
    
    return generated_text.strip()



# Example usage 
query = """
Description
A smart banner will be displayed on the login screen when users open the PSC application in a mobile browser. The banner will provide information about the PSM mobile application and will feature an "Install" button for Android users and a "GET" button for iOS users. If the user already has the PSM app installed, an "Open" button will be displayed instead.

Functional Requirements
1. Display Criteria:
The smart banner will be displayed when the PSC application is accessed via a mobile browser.
The banner will not be displayed when accessing PSC from web/desktop browsers.
The banner will not be displayed within the PSM mobile application.

2. Banner Content:

The smart banner will include:

App name
App information (Content : Download PaySchools Central Mobile App for easy mobile payments, manage student accounts, lunch balances, fees, and more—all at your fingertips! )
App screenshots ( Attached below )
An "Install" button for Android devices
A "GET" button for iOS devices
An "Open" button if the PSM app is already installed
A close (x) button to dismiss the banner
3. Banner Behavior:

The banner will have an expanded and collapsed view:

Expanded View: Shows app name, buttons, app information, and app screenshots.
Collapsed View: Shows only app name and buttons.
By default, the banner will be in the expanded view upon loading.
Users can manually expand or collapse the banner at any time.
The close (x) button will be available in both views to dismiss the banner.
4. User Interaction:

Install/GET Button:

If the banner is displayed on an Android device, the "Install" button will direct the user to the Google Play Store.
If the banner is displayed on an iOS device, the "GET" button will direct the user to the Apple App Store.
Collapse icon: 

If clicked, banner should be collapsed to display collapsed view
Open Button:

If the PSM app is already installed on the device, the banner will display an "Open" button.
Clicking the "Open" button will direct the user to the PSM application.

Buttons

"Install" button (Android): Directs the user to the Google Play Store.
"GET" button (iOS): Directs the user to the Apple App Store.
"Open" button (if PSM app is installed): Directs the user to the PSM application.
“Close” button: Closes the banner



Rules and Validation:

1. The smart banner will be displayed only when accessing PSC through mobile browsers.
2. There should be no time limit for how long the banner is displayed.
3. Ensure the banner is not displayed within the PSM mobile application.
"""


if __name__ == '__main__':
    response = generate_test_cases(query)
    print(response)  

