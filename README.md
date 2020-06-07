<h1 align="center">covid19stats</h1>


 ![version](https://img.shields.io/badge/version-0.0.5-blue.svg)
 ![license](https://img.shields.io/github/license/orlovcs/Scrappy)
![GitHub issues open](https://img.shields.io/github/issues/orlovcs/Scrappy)
![Status](https://img.shields.io/website?label=dyno&up_message=online&url=https%3A%2F%2Fcorona-data-stats.herokuapp.com%2F)

![1](progress/2020-05-24.gif)

covid19stats is an app designed to help visualize the spread of COVID-19 in America. It also demonstrates how different technologies can all work together. Access the deployed app [here](http://corona-data-stats.herokuapp.com).

## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Development](#Development)
* [Docker](#Docker)
* [Heroku](#Heroku)
* [Todo](#Todo)
* [License](#License)
* [Acknowledgements](#Acknowledgements)


## About The Project

The app was initially used to simply import US infection data into PostgreSQL, overtime the data was made available to be visualized with a Flask web app. 

### Built With

* [PostgreSQL](https://www.postgresql.org/)
* [psycopg2](https://pypi.org/project/psycopg2/)
* [pandas](https://pandas.pydata.org/)
* [Flask](https://flask.palletsprojects.com)
* [Selenium](https://www.selenium.dev/)
* [Bootstrap](https://themewagon.com/themes/open-source-bootstrap-admin-template/)
* [Chart.js](https://www.chartjs.org/)
 

### Prerequisites

Install the required pip packages.

* virtualenv
```sh
pip install virtualenv
```

### Installation

[This](https://medium.com/@dushan14/create-a-web-application-with-python-flask-postgresql-and-deploy-on-heroku-243d548335cc) guide serves as a good foundation to initialize the project.

A postgresql server must be running with user ```postgres``` and password ```root```. A database named ```covid``` should be created.
 
Clone the repo.
```sh
git clone https://github.com/orlovcs/Scrappy.git
cd Scrappy
```
Head into the virtual env.
```sh
source env/bin/activate
```
Install all the requirements for pip.
```sh
pip3 install -r requirements.txt
```
Set the env vars from .env.
```sh
export APP_SETTINGS="config.DevelopmentConfig"
export DATABASE_URL="postgresql://postgres:root@localhost/covid"
```
The chrome driver used by selenium must be installed locally and the binary must be set to the GOOGLE_CHROME_SHIM env var:
```sh
export GOOGLE_CHROME_SHIM="path/to/chromedriver"
```


The app pulls data from datahub.io into a pandas df and uses it to create a table with information for each state/province as well as a table for the total cases for the country.

To refresh the table data, execute ```data.py``` :
```sh
python data.py
```
As of May 24, 2020, the original data is composed of nearly 380,000 rows while the the total row count for the tables generated by ```data.py```  come out to 7,257.

## Usage

After the tables are created the local server can be started in the virtual env by running:
```sh
python manage.py runserver
```
The main page gives an overview of the total data for the U.S. while the states page provide a searchable overview for each state.

If the command returns that the address is already in use, find and kill all existing instances:
```sh
ps -fA | grep python
kill -9 pid
python manage.py runserver

```
## Development

See [progress](https://github.com/orlovcs/Scrappy/tree/master/progress).

## Docker
The included Docker Compose files will allow you to run the app in a container with just the two following commands:
```sh
sudo docker-compose build
sudo docker-compose up
```

Initially there was an attempt to utilize the chromedriver container but it turned out to be easier to download Chrome 83 and the respective chromedriver directly into the base image using the package manager during the building process. This version of Chrome was isolated to work with the version of Selenium used. [This](https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/#postgres) was used as a initial reference for the Dockerfiles and [this](https://github.com/dimmg/dockselpy/blob/master/Dockerfile) was used to install the chromedriver correctly.


## Heroku

To deploy this app to Heroku, install heroku-cli
```sh
curl https://cli-assets.heroku.com/install.sh | sh
```
Log into the CLI and deploy the app by following [these](https://devcenter.heroku.com/articles/creating-apps) docs.

### Row Compliance
Since a free account is limited to 10,000 rows, the original dataset needed to be aggregated by precomputing and summing up the cases for each day and then specifying this data by state. With this reduction the app can exist and function normally with under 10,000 rows, instead pulling data from a table created for each state/province. However as the data continues to grow, eventually the tables would be forced to drop the top rows after checking if they are over row capacity.

### Chromedriver
The headless chromedriver must be installed as the following buildpacks for the dyno:
```sh
https://github.com/heroku/heroku-buildpack-chromedriver
https://github.com/heroku/heroku-buildpack-google-chrome
```
Locally the headless chromedriver used for selenium web scraping runs without issues. However, on the dyno the chromedriver is unstable and appears to crash the dyno for the first couple minutes of every new version. After some time passes, it no longer crashes.

### Data Refresh
The database tables can be refreshed from the upsteam repo by executing ```data.py``` on the dyno itself:
```sh
heroku run python data.py --app YOUR_APP_NAME_HERE
```
As well as dumping the local sql file and uploading it to the dyno manually:
```sh
pg_dump covid > updates.sql
heroku pg:psql --app YOUR_APP_NAME_HERE < updates.sql
```

## Todo

See [open issues](https://github.com/orlovcs/Scrappy/issues).


## License

Distributed under the GPL3 License.

## Acknowledgements

* [datahub.io](https://datahub.io/core/covid-19) for main csv data 
* [worldometers](https://www.worldometers.info/coronavirus/country/us/) for additional data

