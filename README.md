Weather App
===========

This is a simple weather application that ingests weather data, stores it in a SQLite database, and exposes it via a REST API.

Prerequisites
-------------

- Python 3.7 or higher
- Docker
- Kubernetes

Getting Started
---------------

1. Clone the repository:


2. Install the required Python packages:

```
pip3 install -r requirements.txt
```

3. Create the database tables:

```
make create-tables
```

4. Ingest data into the database:

```
 WX_DATA_DIRECTORY=/path/to/weather/data && make ingestion-job
```

5. Analyze the data:

```
make data-analysis
```

6. Build and deploy the application to Kubernetes:

make sure your kubectl is configured to point to the cluster where you want to deploy the application to

```
make deploy
```

This will build a Docker image, push it to an AWS ECR repository, and deploy the application to a Kubernetes cluster. The Kubernetes deployment will be configured using the `prod.env` file.

## Endpoints
---------

The REST API exposes the following endpoints:

- `/api/weather`: Retrieve weather data.
- `/api/weather/stats`: Retrieve weather statistics.

Both endpoints support filtering by date and station ID using query parameters. Data is returned in JSON format

## Swagger/OpenAPI
---------------

The REST API includes an automatically generated Swagger/OpenAPI endpoint that provides documentation for the API. This is accessible at the following URL:

- `http://localhost:5000/apidocs/`

## License
-------

This project is licensed under the MIT License. See the `LICENSE` file for details.