# arcanis

A POC for Arcanis, a django REST service replacement for chatterfang

To run a dev environment:

1. Install python3 (see https://www.python.org/)
2. Install postgres (pg_config required to compile dependencies)
3. Install docker (required to run the dev database)
2. cd into project root directory
3. create a virtual env (see https://docs.python.org/3/library/venv.html for more details)

   `python3 -m venv .venv`

4. activate the virtual env

   on mac zsh: `source .venv/bin/activate`

   on windows powershell: `<venv>\Scripts\Activate.ps1`

5. install project dependencies

   `just install`

6. create and run database docker container

   `just db_reset`

6. run server and view on localhost:8000/

   `just server_start`


Check out the justfile for more commands that may improve your dev experience.


## Git Commit Message Guidelines

To maintain consistency and clarity in our commit history, all commit messages must follow these guidelines:

- **Start with a verb**: The first word of your commit message should always be a verb that describes the action taken. This helps clearly convey what the commit accomplishes.
- **Capitalize the first word**: The first word in the commit message should be capitalized to maintain a professional and consistent format.

**Example:** `Update gitignore to exclude temporary files` By adhering to these guidelines, we ensure that our commit history remains clean and easy to understand. --- This should help your team maintain clear and professional commit messages!
