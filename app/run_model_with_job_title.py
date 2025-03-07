from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from groq import APIConnectionError
import logging
import os
import httpx
import re
import json

def run_model(resume, job_description, job_title):
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    os.environ['HTTPX_DISABLE_CERT_VERIFICATION'] = '1'
    
    # Define prompts based on job titles
    prompts = {
        "Software Engineer": "Please evaluate the resume for a Software Engineer position.",
        "Data Scientist": "Please evaluate the resume for a Data Scientist position.",
        "Product Manager": "Please evaluate the resume for a Product Manager position.",
        # Add more job titles and their corresponding prompts as needed
    }

    prompt_message = prompts.get(job_title, "Please evaluate the resume for a general position.")

    try:
        chat = ChatGroq(temperature=0, groq_api_key="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", model_name="mixtral-8x7b-32768")

        system = """
        I want you to assess the compatibility between the given resume and job description.
        Your output must strictly be a JSON object with the following fields:
        - "name": The candidate's name (string).
        - "email": The candidate's email (string).
        - "matchingSkills": A list of skills present in both the resume and the job description (array of strings).
        - "missingSkills": A list of skills in the job description that are not found in the resume (array of strings).
        - "compatibility": The compatibility percentage between the resume and job description (numerical value between 0 and 100).

        Ensure your output strictly matches this format, and all fields are accurate based on the input.
        """

        human = f"""
        Resume:
        {resume}

        Job Description:
        {job_description}

        Job Title:
        {job_title}

        Additional Prompt:
        {prompt_message}
        """

        prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

        chain = prompt | chat

        resp = chain.invoke({"resume": resume, "job_description": job_description})
        
        # Extract core JSON content using regular expressions
        match = re.search(r"{.*?}", resp.content, re.DOTALL)
        if match:
            json_content = match.group(0)
        else:
            print("Error: Could not extract JSON content from response.")
            exit(1)
 
        return json.loads(json_content)
    except APIConnectionError as e:
        logging.error("Connection error: %s", e)
        return {"error": "Failed to connect to the Groq API. Please try again later."}
