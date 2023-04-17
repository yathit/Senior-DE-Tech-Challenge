## Server setup

Install and setup Docker Swarm

Install docker using Docker Inc's script.
https://github.com/docker/docker-install

    curl -fsSL https://get.docker.com -o get-docker.sh
    sh ./get-docker.sh | tee "docker-install_$(hostname)_$(date +'%Y-%m-%d').txt"

Run in swarm mode for scalability 

    docker swarm init

Check

    docker info

## Airflow setup 

Setup Airflow following [the official instruction](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html), here brief snippets are shown for quick following.

    curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.5.3/docker-compose.yaml'

Send files to test server

    rsync -av . dev:~/airflow/

Setting the right Airflow user

```bash 
mkdir -p ./dags ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)" > .env
source .env
```

Then, follow Airflow docker compose installation.

