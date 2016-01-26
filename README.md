#Tieba-Tools

A web application about Daidu Tieba, used to
signing, watering, administrator utils, etc.

Quick Setup
-----------

1. have installed python3.4+ and redis
2. Clone this repository.
3. cd to the directory,  and create a virtualenv with 

    pyvenv venv

4. install the requirements, execute 

    venv/bin/pip install -r requirements.txt

5. Open a second terminal window and start a local Redis server .
   on linux, execute

       redis-server

6. Open a third terminal window and start a Celery worker: 

    venv/bin/celery worker -B -A TiebaTools.cel --loglevel=info

7. Start the Flask application on your original terminal window: 

    venv/bin/python run.py

8. Go to `http://localhost:5000/` and enjoy this application!

Customize
-----------

There are some default config in `config.py`. If you want to customize
it , do not modify it .Instead, create a directory named `instance` in 
root of project, and a file named `config.py` in `instance` directory.
Then put what you want to customize in it.
When application starts, it will get all-uppercase vars of 'config.py'
and 'instance/config.py' as config of application Sequentially. 

todo
TiebaTools/static/js/sign.js
