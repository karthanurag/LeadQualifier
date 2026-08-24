#LeadQualifierProject
from pathlib import Path
from google import genai
import json
from pydantic import BaseModel
from dotenv import load_dotenv
from google.genai import types
load_dotenv()
no = int(input("Enter number of inputs: "))
usertotal = []
for i in range(no):
    user = input(f"What does Lead {i+1} want? ")
    usertotal.append(user)
all_leads = f"""
Lead : {usertotal}
"""
client=genai.Client()
class Lead(BaseModel):
    score:int
    budget:str
    location:str
    reason:str
class Leads(BaseModel):
    leads: list[Lead]
response=client.models.generate_content(
    model="gemini-3.6-flash",
    contents=str(usertotal),
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
                response_schema=Leads,
                system_instruction=("You are a Real Estate AI Assistant. Your job is to score candidates based on their level of importance on a scale from 1-10,based on how well there budget amtches with the actual price of the flat in that location")
            )
    )
print(response.text)
# {"leads":[{"score":4,"budget":"500,000 AED","location":"Dubai Marina","reason":"500k AED is significantly below the average market price of 900k to 1.3M AED for a 1BHK in Dubai Marina."},{"score":9,"budget":"5 Crore INR","location":"Juhu","reason":"A budget of 5 Cr INR matches the typical price range of 3.5 Cr to 6 Cr INR for a 2BHK in Juhu."}]}
data=json.loads(response.text)
for item in data['leads']:
    score=item['score']
    print("Lead:")
    print("Budget:",item['budget'])
    print("Location:",item['location'])

    if score >= 8:
        print("Score is" ,score," and its HOT")
    elif score >= 5:
        print("Score is" ,score," and its MEDIUM")
    else:
        print("Score is" ,score," and its COLD")
    
folder1=Path("PYCODE")
folder1.mkdir(exist_ok=True)
file1=folder1/'LeadQualify.txt'
with open('LeadQualify.txt','w') as f:
    f.write(response.text)


print(data)