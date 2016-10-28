.PHONY: docker-image docker-push docker-pull docker-test docker-ft build-app functional-tests deploy-staging

PROJECT=nextchef
TAG=latest
REGISTRY=docker.apiumtech.io
IMAGE=$(REGISTRY)/$(PROJECT):$(TAG)

ENV_VARS=TAG=$(TAG) REGISTRY=$(REGISTRY)

DC_TEST=$(ENV_VARS) docker-compose -p nextcheftest -f compose/base.yml -f compose/integration-test.yml
DC_FT=$(ENV_VARS) docker-compose -p nextchefft -f compose/base.yml -f compose/functional-test.yml
DC_STAGING=$(ENV_VARS) docker-compose -p nextchefft -f compose/base.yml -f compose/staging.yml
DC_QA=$(ENV_VARS) docker-compose -p nextchefqa -f compose/base.yml -f compose/qa.yml
DC_DEV=$(ENV_VARS) docker-compose -p nextchefdev -f compose/base.yml -f compose/dev.yml
DC_PRODUCTION=$(ENV_VARS) docker-compose -p nextchefft -f compose/base.yml -f compose/production.yml

docker-image:
	docker build -t $(IMAGE) .

docker-push:
	docker push $(IMAGE)

docker-pull:
	docker pull $(IMAGE)

docker-test:
	$(DC_TEST) down || true
	$(DC_TEST) build
	$(DC_TEST) run --rm web
	$(DC_TEST) run --rm frontend_tests
	$(DC_TEST) down

docker-ft:
	$(DC_FT) down || true
	$(DC_FT) run --rm jmeter
	$(DC_FT) down

build-app: docker-image docker-test docker-push

functional-tests: docker-pull docker-ft

deploy-production:
	$(DC_PRODUCTION) down || true
	$(DC_PRODUCTION) pull
	$(DC_PRODUCTION) up -d
deploy-staging:
	$(DC_STAGING) down || true
	$(DC_STAGING) pull
	$(DC_STAGING) up -d

task-migrate:
	$(DC_$(TASK_ENV)) -f compose/tasks.yml run managepy migrate
