WX_DATA_DIRECTORY ?= ../wx_data
DB_PATH ?= db/weather_data.sqlite
IMAGE_NAME ?= aws_account_id.dkr.ecr.region.amazonaws.com/weather-app:prod

create-tables:
	python3 create_tables.py --db_path=$(DB_PATH)

ingestion-job:
	python3 ingestion_job.py --wx_data_directory=$(WX_DATA_DIRECTORY) --db_path=$(DB_PATH)

data-analysis:
	python3 data_analysis.py --db_path=$(DB_PATH)

build-image:
	docker build . -t $(IMAGE_NAME)

push-image:
	docker push $(IMAGE_NAME)

deploy: build-image push-image
    # get image_name from prod.env and create a deployment in k8
    @export $(cat prod.env | xargs) && \
    envsubst < kubernetes-manifests/deployment.yaml | kubectl apply -f -

    # expose the service
    kubectl apply -f kubernetes-manifests/service.yaml

