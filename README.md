# Soodud

Soodud is a webapp that scrapes data from online stores and uses C++ hierarchical cluster analysis to form comparable products between stores. The data is given by a Django REST API and then processed by a TailwindCSS & React frontend. CI/CD is implemented with Docker and static files are served by nginx.

## Setup

1. Clone the project.
2. Create a valid `.env` file based on `.env.example`.
3. If this is your initial configuration and you plan on using nginx, temporarily disable HTTPS in `nginx/nginx.conf`.
4. Install dependencies using `cd client && npm install --dev` and `cd django && pipenv install`.
5. If applicable, build the C++ project and move `clustering/out/clustering.(so|pyd)` into the `django/data/stores/` directory.
4. In development, run the servers using `cd client && npm run server` and `tools/start_server.sh`.
5. In production, run Docker Compose with `tools/compose.sh`.
6. To scrape new product data and form updated product clusters, run `tools/run_service.sh launch` and `tools/run_service.sh match` respectively.
7. In order to contribute, be sure to install the required git commit hooks with `cd django && pipenv run pre-commit install`.
