# Open Source Programs (Backend)

![Build Status](https://github.com/anitab-org/open-source-programs-backend/workflows/Tests%20Build/badge.svg)
[![project chat](https://img.shields.io/badge/zulip-join_chat-brightgreen.svg)](https://anitab-org.zulipchat.com/#narrow/stream/237907-open-source-progs)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)
[![Open Source Love](https://badges.frapsoft.com/os/v3/open-source.svg?v=103)](https://github.com/anitab-org/open-source-programs-backend/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/anitab-org/open-source-programs-backend)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)

Open Source Programs (OSP) is an application that simplifies the processing and selection procedure of Open Source Programs of AnitaB.org Open Source or other third-party programs. This is the Backend repo for OSP.

## Tech Stack
- Django 3.0.7
- Django REST Framework 3.11.0
- Python 3.7+

## API Documentation
- [Postman Docs](https://documenter.getpostman.com/view/11324046/Szzoaw1q?version=latest)

## Setup 
To setup the project locally go through [this wiki page](https://github.com/anitab-org/open-source-programs-web/wiki/Fork,-Clone,-Remote-and-Pull-Request).
Make sure you have installed the following:
* [pip](https://pip.pypa.io/en/stable/installing/)
* [virtualenv](https://pypi.org/project/virtualenv/)
* [PostgreSQL](https://www.postgresql.org/docs/9.5/install-procedure.html)

Next follow these instructions.

1. **Database Setup:** Before starting with the project create a db in you local using PostgreSQL with the following details. Refer to `main/settings.py` if you have any confusion.

    ```
    NAME: osp
    USER: osp
    PASSWORD: osp
    HOST: localhost
    ``` 
    You may run the following commands for local setup of DB in Linux:

    ```
    cd open-source-programs-backend
    sudo -i -u postgres
    createuser osp --pwprompt
    psql
    CREATE DATABASE osp;
    \c osp;
    GRANT ALL PRIVILEGES ON DATABASE osp to osp;
    ```
    You may run the following commands for local setup of DB in Windows:

    ```
    cd open-source-programs-backend
    psql -U postgres
    CREATE ROLE osp LOGIN PASSWORD 'osp' NOINHERIT CREATEDB;
    CREATE DATABASE osp;
    \c osp;
    GRANT ALL PRIVILEGES ON DATABASE osp to osp;
    ```
2. **Set the environment variables:** You need to download Zulip API key file from your user-settings on Zulip. The file you download is named as `download` or rename it to `download`. Place that download file in the project's directory. For more information follow [Environment Variables](#Environment-Variables) section.

3. Move into the project's directory.

    ```
    cd open-source-programs-backend
    ```
4. Create virtual environment (this is not a hard requirement, but its advisable)
    ```
    virtualenv venv
    ```
     Activating virtual environment for Linux users:
     ```
     source venv/bin/activate
     ```
     Activating virtual environment for Git Bash users:
     ```
     source ./venv/Scripts/activate
     ``` 
     Activating virtual environment for Windows users:   
     ``` 
     venv\Scripts\activate
     ```
5. To install dependencies:
    ```
    pip install -r requirements.txt
    ```	
6. To run the migrations run: 
   ```
   python manage.py migrate
   ```
7. To setup Social Auth for backend see [this](#Setup-Social-Auth).
8. To run the server:
    ```
    python manage.py runserver
    ```
8. Navigate to `http://localhost:8000/` in your browser.
9. To change the port you may run `python manage.py runserver <port_number>`
10. To run the migrations run: `python manage.py migrate`
11. You can terminate the process by `Ctrl+C` in your terminal.

Follow the given instructions for Login into the app.

1. You can register a new user by making a POST request on `/api/token_auth/register/`. After this confirmation e-mail will be sent to standard output (terminal). To receive confirmation e-mail using Sendgrid see [this](#environment-variables). The content of the request must be like this:
    ```json
    {
        "username":"< YOUR USERNAME >",
        "email":"< YOUR EMAIL >",
        "password":"< YOUR PASSWORD >",
        "confirm_password":"< YOUR PASSWORD >"  
    }
    ```


2. To create the superuser run:
   ```
   python manage.py createsuperuser
   ````
   Fill up the things it asked to and then Login into the app.

## Environment Variables

1. `Zulip API KEY file` - You can go [Zulip](https://anitab-org.zulipchat.com) and follow [these instructions to get your API KEY](https://zulip.com/api/api-keys#get-your-api-key). Download the file and save it in the root folder of the project with the name `download`.

2. `SENDGRID_API_KEY` - It is optional for development. To use this variable make `DEBUG=False` in `settings.py`. Follow the given steps to create a Sendgrid API key:

	1. Go to [Sendgrid's website](https://app.sendgrid.com/guide)
	2. Navigate to Settings on the left navigation bar, and then - select API Keys.
	3. Click Create API Key.
	4. Give your API key a name.
	5. Select Full Access, Restricted Access, or Billing Access. If you're selecting Restricted Access, or Billing Access, select the specific permissions to give each category. For more information, see API key permissions.
	6. Click Create & View.
	7. The API KEY is generated and displayed to you just once. So be sure to copy and save it somewhere.

Add it to your .env file as follows:
```
export SENDGRID_API_KEY=<your-sendgrid-api-key>
```
3. `GOOGLE_CALLBACK_URL` - For using Google authentication the **Callback URL** is required by Google API. Add this env variable in `.env` file or export it to use **Callback URL** which you used while setting Up Google App. The default value is: `http://localhost:3000/login`.

# Setup Social Auth

1. Create a Super User by running this command: `python manage.py createsuperuser`.
2. Login to [Django admin site](http://localhost:8000/admin/) using credentials of the previous step.
3. Go to **Sites dashboard** in admin site. (**URL**: http://localhost:8000/admin/sites/site/).
4. Click on `Add site` button and fill in the information as given in the image.

   ![site_id](https://user-images.githubusercontent.com/56037184/109974910-0fa79b00-7d20-11eb-9826-44fdf6d770f9.png)
   
   **Note**: After saving this if the site id is not `2` then change the `SITE_ID` in settings.py with the new site id.
5. After this go to **Social Applications Dashboard**. (**URL**: http://localhost:8000/admin/socialaccount/socialapp/).
6. Add the credentials that you get after creating the Google app. Fill in the information as given in the image.

   ![social_add](https://user-images.githubusercontent.com/44670961/110095166-9f058a80-7dc2-11eb-85eb-afb109f46663.png)
   **For creating Google App & Creating ClientId & Client Secret see [this docs](https://developers.google.com/adwords/api/docs/guides/authentication#create_a_client_id_and_client_secret).**
## Testing

To run the tests run: `python manage.py test`.

## QA Checks

Before creating a pull-request, always run QA checks to make your code more readable and error-free. Steps to run QA checks are:
1. Install QA checks dependencies:
    ```
    pip install black==20.8b1
    pip install isort==5.7.0
    pip install flake8==3.8.4
    ```
2. Run QA checks: `./osp-qa-checks`.

### Run with Docker

1. Make sure the latest version of docker and docker-compose are installed.

- For **docker** run ``docker -v`` from your terminal. If docker is not installed, install it from [here](https://docs.docker.com/engine/install/).
- For **docker-compose** run ``docker-compose -v`` from terminal. If it is not installed then install it by running ``pip install docker-compose`` or from [here](https://docs.docker.com/compose/install/).

2. Change Database HOST in ``settings.py``

- Go to ``main/settings.py``
- Under databases change host to db.

3. **Build docker image**

Execute ``sudo docker-compose run web`` to build the image.

4. **Run docker image**

Run ``sudo docker-compose up`` from the root directory of project. Navigate to `http://localhost:8000` in your browser.

**Note** 
- Run `docker-compose up --build` to rebuild the image.
- To **interact** with docker containers use ``docker exec -it {container id} bash`` from your terminal. Container id can be found using ``docker ps``.

## Documentation

- Read the [Meeting minutes](https://docs.google.com/document/d/1JSyAr9bO4hJJxFvThvn_LVjW0KcEspXpzvWULRC_xJE/edit) notes from our open sessions about the project.
- For setting up the project locally watch [this video](https://youtu.be/_b2RQGbYN9w).
- To learn about the project's initial features, watch the video of [project demonstration](https://youtu.be/3A746GppZ0Y).
- [Design and Mocks Google Drive folder](https://drive.google.com/drive/folders/1MybSH3f8peXGUSRxhDydDtoAi8WJL1th).
- [Timeline deliverables for the project during GSoC 2020](https://docs.google.com/document/d/1xl9F5kMZrKo4mNhnP0SKpk7WkQc8PLca1ym7EZMpjSc/edit).
- [GSoC 2020 Project Meeting Minutes](https://docs.google.com/document/d/1YF13IbBrU1ln4ZF1fOpgb-xGRgIF6tZLSjIBQgDmN7k/edit) [Old].

For more information, you can read [backend project wiki](https://github.com/anitab-org/open-source-programs-backend/wiki) and the [web project wiki](https://github.com/anitab-org/open-source-programs-web/wiki).

## Contributing
Please read the [Contributing guidelines](.github/CONTRIBUTING.md), [Code of Conduct](CODE_OF_CONDUCT.md) and [Reporting Guidelines](REPORTING_GUIDELINES.md)

## Contact
You can reach the admins, maintainers and our community on [AnitaB.org Open Source Zulip](https://anitab-org.zulipchat.com/). If you are interested in contributing to the OSP project, you may join the stream [#open-source-progs](https://anitab-org.zulipchat.com/#narrow/stream/237907-open-source-progs) and ask questions or intereact with the community. Join Us!
