import os 
import random 
import time

from flask import Flask, request, render_template, session, flash, redirect, \
    url_for, jsonify
from celery import Celery

from spiders import worldbank
from spiders import models


app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'


# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'


# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@celery.task(bind=True)
def search_task(self, *args, **kwargs):
    """Perform search for each search spider"""
    company_name = kwargs['company_name']
    crawler = ['worldbank']
    search_results = []
    message = ''
    total = len(crawler) 
    for i, spider in enumerate(crawler):
        message = "Searching {}".format(spider)
        self.update_state(state='PROGRESS',
                          meta={'current': 25, 'total': 100,
                                'status': message})
        results = worldbank.search(company_name=company_name)
        if results:
            search_results = results
        message = 'Searching CIA'.format(spider)
        self.update_state(state='PROGRESS',
                          meta={'current': 50, 'total': 100,
                                'status': message})
        time.sleep(3)
       
    return {'current': 100, 'total': 100, 'status': 'Search Complete',
            'result': search_results}


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    # process search request
    company_name = request.form['company_name']
    task = search_task.apply_async(kwargs={'company_name': company_name})
    return jsonify({}), 202, {'Location': url_for('taskstatus',
                                                  task_id=task.id)}


@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = search_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
