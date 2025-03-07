from flask import Blueprint, request, jsonify
from .langchain_integration import run_model
from .batch_process import batch_model

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return "Hello, Flask!"

@main.route('/process', methods=['POST'])
def process():
    data = request.json
    resume = data.get('resume')
    job_description = data.get('job_description')

    response = run_model(resume, job_description)
    
    return jsonify(response)

@main.route('/evaluate', methods=['POST'])
def processes():
    data = request.json
    resume = data.get('resume')
    job_description = data.get('job_description')

    response = batch_model(resume, job_description)
    
    return jsonify(response)

@main.route('/apply', methods=['POST'])
def apply():
    data = request.json
    resume = data.get('resume')
    job_description = data.get('job_description')
    job_title = data.get('job_title')

    response = run_model(resume, job_description, job_title)
    
    return jsonify(response)
