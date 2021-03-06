#Pull Python 3.6
FROM python:3.6-buster
#Set work dir
WORKDIR /usr/src/app
#Set env vars
ENV APP_SETTINGS config.DevelopmentConfig
ENV DATABASE_URL postgresql://postgres:root@localhost/covid
#Install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
#Install Chrome dependencies
RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 \
    libnspr4 libnss3 lsb-release xdg-utils libxss1 libdbus-glib-1-2 libgbm1 \
    curl unzip wget \
    xvfb
#ISOLATE CHROME 83 FOR CHROME AND DRIVER
RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    wget https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip -d /usr/bin && \
    chmod +x /usr/bin/chromedriver && \
    rm chromedriver_linux64.zip
RUN CHROME_SETUP=google-chrome.deb && \
    wget -O $CHROME_SETUP "http://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_83.0.4103.97-1_amd64.deb" && \
    dpkg -i $CHROME_SETUP && \
    apt-get install -y -f && \
    rm $CHROME_SETUP

#Copy current directory to container work dir
COPY . /usr/src/app/
