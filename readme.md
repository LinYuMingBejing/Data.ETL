# How to run ETL.py on Ubuntu?


### Install Docker

* sudo apt-get update

* sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common

* curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

* sudo apt-key fingerprint 0EBFCD88

* sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

* sudo apt-get update

* sudo docker run --name redis redis-lab -p 6379:6379 -d redis


### Install Redis

* sudo docker pull redis
* sudo docker run --name redis redis-lab -p 6379:6379 -d redis


### Install Python Packages

* pip install --no-cache-dir -r requirements.txt

### Run ETL.py

* python3 ETL.py
