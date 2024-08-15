# chatterfang
A POC for creating a chatterfang REST service with django

To run a dev environment:
1. Install python3 (see https://www.python.org/)
2. cd into project root directory
3. create a virtual env (see https://docs.python.org/3/library/venv.html for more details)

    `python3 -m venv .venv`
4. activate the virtual env

    on mac zsh: `source .venv/bin/activate`

    on windows powershell: `<venv>\Scripts\Activate.ps1`
5. install project dependencies

    `pip install -r requirements.txt`

6. run server and view on localhost:8000/

    `python3 manage.py runserver`