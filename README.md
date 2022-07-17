# Soodud

Soodud is a webapp that scrapes data from online stores with Python and then uses C++ hierarchical cluster analysis to form comparable products between stores that are stored in PostgreSQL. The resulting data is served by a Django REST API and then processed by a TailwindCSS & React frontend.

CI/CD is implemented through Github Actions and Docker Compose. Nginx & fail2ban are used to compress/cache/serve static files, provide rate limiting, and detect malicious bots. All commits are ran through flake8 and other pre-commit filters.

## Setup

1. Clone the project.
1. Create a valid `.env` file based on `.env.example`.
1. In order to contribute, first install the required git commit hooks with `cd django && pipenv run pre-commit install`.

### Development

1. Install dependencies using `cd client && npm install --dev` and `cd django && pipenv install`.
1. Build the C++ project and move `clustering/out/clustering.(so|pyd)` into the `django/data/stores/` directory.
1. Start the webpack dev server using `cd client && npm run server`
1. Start the Python virtual environment with `cd django && pipenv shell`.
1. Start the Django dev server with `tools/start_server.sh`.
1. To scrape new product data and form updated product clusters, run `tools/run_service.sh launch` and `tools/run_service.sh match` respectively.

### Production

1. If this is your initial configuration, temporarily disable HTTPS in `nginx/nginx.conf` by commenting out the `include`.
1. Run Docker Compose with `tools/compose.sh`.
1. Create a new cronjob with `tools/cron.txt` as a reference. This will ensure that the product database is updated once a day.
