from fastapi import FastAPI, UploadFile
import base64
import datetime
import requests
import json
import random
import string
import os
import openai

def get_resume_recommendations(resume: UploadFile):

    base64str =  base64.b64encode(resume.file.read()).decode('UTF-8')
    lastModifiedDate = datetime.date.today().strftime("%Y-%m-%d") 

    positions = get_resume_highlights_and_improvements(base64str, lastModifiedDate)

    return {
        "data": positions
    }

def get_resume_highlights_and_improvements(base64str: str, lastModifiedDate: datetime.date):
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
            title = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

        highlights = description.split('\n')
        highlights_json = []
        for highlight in highlights:
            if highlight == '':
                continue
            if len(highlight) < 20:
                continue

            highlights_json.append({
                "highlight": highlight,
                "improvment_choices": generate_hightlight_improvment(highlight)
            })

        positions_json.append({'title': title, 'highlights': highlights_json})
    
    return positions_json

def generate_hightlight_improvment(highlight: str):
    # use open ai to generate improvment

    openai.api_key = "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"
    # gpt3 request 
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt="Rewrite this resume bullet point to make it sound more exciting and impactful by using more powerful verbs and highlighting key quantitative results and tools that were used. Don't use any pronouns and write everything in the past tense.\n\nBullet point: " + highlight,
        temperature=0.7,
        max_tokens=215,
        n=3,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    choices = [choice.text for choice in response['choices']]

    return choices