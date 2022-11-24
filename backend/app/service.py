from fastapi import FastAPI, UploadFile
import base64
import datetime
import requests
import json
import os
import openai

def get_resume_recommendations(resume: UploadFile):

    base64str =  base64.b64encode(resume.file.read()).decode('UTF-8')
    lastModifiedDate = datetime.date.today().strftime("%Y-%m-%d") 

    positions = get_resume_highlights(base64str, lastModifiedDate)

    return {
        "data": positions
    }

def get_resume_highlights(base64str: str, lastModifiedDate: datetime.date):
    # Using Sovren API to get resume highlights
    url = "https://rest.resumeparsing.com/v10/parser/resume"
    payload = {
        'DocumentAsBase64String': base64str,
        'DocumentLastModified': lastModifiedDate
    #other options here (see https://sovren.com/technical-specs/latest/rest-api/resume-parser/api/)
    }
    
    headers = {
        'accept': "application/json",
        'content-type': "application/json",
        'sovren-accountid': "37306374",
        'sovren-servicekey': "8qWxcGqr0OdDUisjCDNWxWdKrftMQR/fyovdtvwn",
    }

    # print(payload)

    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    responseJson = json.loads(response.content)
    
    #grab the ResumeData
    resumeData = responseJson['Value']['ResumeData']
    # print(resumeData)
    
    #access the ResumeData properties with simple JSON syntax

    #get description for all jobs and then run them through Open AI
    positions = resumeData['EmploymentHistory']['Positions']
    positions_json = []

    for position in positions:
        is_current = position['IsCurrent']

        if 'Description' not in position:
            continue

        description = position['Description']

        title = ''
        if 'JobTitle' in position:
            title = position['JobTitle']['Normalized']
        else:
            # generate string with random chars
            title = 'No Job Title Found'

        highlights = description.split('\n')
        highlights = list(filter(lambda x: len(x) > 20, highlights))

        positions_json.append({'title': title, 'highlights': highlights})
    
    return positions_json

def generate_highlight_improvment(highlight: str):
    openai.api_key_path = '.env'
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt="Rewrite this resume bullet point to make it sound more exciting and impactful by using more powerful verbs and highlighting key quantitative results and tools that were used. Don't use any pronouns and write everything in the past tense.\n\nBullet point: " + highlight,
        temperature=0.7,
        max_tokens=215,
        n=1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    choices = [choice.text for choice in response['choices']]

    return {
        "data": choices
    }