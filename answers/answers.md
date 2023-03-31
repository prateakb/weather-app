## Question 1:

I chose sqlite and the corresponding python script that does so is at `src/create-tables.py` it can be run using `make create-tables`

## question 2:

the code is written at src/ingestion_job.py and can be run using `make ingestion-job`

## question 3:

the code is written at src/data_analysis.py and can be run using `make data-analysis`

## question 4:
the code is written at src/weather_api and can be run using python3 app.py on src/weather_api and accessed at `localhost:5000/apidocs`

## extra credit:

to deploy this first get your kubeconfig pointed to your k8 cluster. write your image-name at prod.env
type `make deploy`. It will use the kubernetes manifests to deploy the app and expose it. The service that is exposed can further be configured to have appropriate backend and dns configurations.