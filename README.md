# Soodud

Soodud is a webapp that scrapes data from online stores with Python and then uses C++ hierarchical cluster analysis to form comparable products between stores that are stored in PostgreSQL. The resulting data is served by a Django REST API and then processed by a TailwindCSS & React frontend.

CI/CD is implemented through Github Actions and Docker Compose. Nginx & fail2ban are used to serve static files, provide rate limiting, and detect malicious bots. All commits are ran through flake8 and other pre-commit filters.

## Setup

1. Clone the project.
2. Create a valid `.env` file based on `.env.example`.
3. If this is your initial configuration and you plan on using nginx, temporarily disable HTTPS in `nginx/nginx.conf`.
4. Install dependencies using `cd client && npm install --dev` and `cd django && pipenv install`.
5. If applicable, build the C++ project and move `clustering/out/clustering.(so|pyd)` into the `django/data/stores/` directory.
6. In development, run the servers using `cd client && npm run server` and `tools/start_server.sh`.
7. In production, run Docker Compose with `tools/compose.sh`.
8. To scrape new product data and form updated product clusters, run `tools/run_service.sh launch` and `tools/run_service.sh match` respectively.
9. Alternatively, create a new cronjob with `tools/cron.txt` as a reference. This will assure that the product database is updated once a day.
10. In order to contribute, be sure to install the required git commit hooks with `cd django && pipenv run pre-commit install`.
