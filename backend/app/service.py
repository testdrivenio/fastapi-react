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


        employer_name = ''
        if 'Employer' in position:
            employer_name = position['Employer']['Name']['Normalized']
        else:
            employer_name = 'Unknown Employer'


        def get_end_date(end_date):
            if is_current:
                return 'Current'
            else:
                return datetime.datetime.strptime(end_date, '%Y-%m-%d').strftime('%B %Y')

        start_date = position['StartDate']['Date']
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').strftime('%B %Y')
        end_date = get_end_date(position['EndDate']['Date'])

        title = ''
        if 'JobTitle' in position:
            title = position['JobTitle']['Normalized']
        else:
            title = 'No Job Title Found'

        highlights = description.split('\n')
        highlights = list(filter(lambda x: len(x) > 20, highlights))

        def remove_bullets(highlight):
            first_char = highlight.find(next(filter(str.isalpha or str.isnumeric, highlight)))
            return highlight[first_char:]

        highlights = list(map(remove_bullets, highlights))
        positions_json.append({'title': title, 'employerName': employer_name, 'highlights': highlights, 'startDate': start_date, 'endDate': end_date})
    
    return positions_json

def generate_highlight_improvment(highlight: str):
    openai.api_key_path = '.env'
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt="Rewrite this resume bullet point to make it sound more exciting and impactful by using more powerful verbs and highlighting key quantitative results and tools that were used. Don't use any pronouns and write everything in the past tense.\n\nBullet point: " + highlight,
        temperature=0.7,
        max_tokens=215,
        n=2,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    choices = [choice.text for choice in response['choices']]

    return {
        "data": choices
    }

## function that adds and multiplies two numbers

