TAG        := $(shell git describe --tags --long --abbrev=8)
REGISTRY   := ghcr.io/sbostick
APP_NAME   := amrad-sota
IMAGE      := ${REGISTRY}/${APP_NAME}:${TAG}
BUILD_TIME := $(shell date "+%F %H:%M:%S %Z (%z)")
SHELL      := /bin/bash

LAST_KNOWN_GOOD := v0.0.0

tag:
	@echo ${TAG}

lint: pycodestyle pyruff pylint

# https://pycodestyle.pycqa.org/en/latest/intro.html#error-codes
# E128 continuation line under-indented for visual indent
# E501 line too long (85 > 79 characters)
# E203 whitespace before ':'
# E402 module level import not at top of file
# E266 too many leading '#' for block comment
pycodestyle:
	@echo "+ Checking source with pycodestyle"
	pycodestyle --ignore E128,E501,E203,E402,E266 --verbose ./src/*.py
	@echo

# https://pypi.org/project/ruff/0.0.47/
# E402 Module level import not at top of file
pyruff:
	@echo "+ Checking source with ruff (linter written in Rust)"
	ruff --verbose --ignore E402 --cache-dir /tmp/ruff_cache .
	@echo

# https://pylint.org/
# https://pylint.pycqa.org/en/latest/
pylint:
	@echo "+ Checking source with pylint (most comprehensive and popular)"
	@[[ -e pylintrc ]] || pylint --generate-rcfile > pylintrc
	pylint --rcfile pylintrc ./src/*.py
	@echo

.PHONY: test
test: unit-tests func-tests

.PHONY: unit-tests
unit-tests:
	@PYTHONPATH=${PWD}/src python3 -m unittest discover \
		-s ./src/modules -p "*_test.py" -vv

.PHONY: func-tests
func-tests:
	@PYTHONPATH=${PWD}/src python3 -m unittest discover \
		-s ./test/ -p "*_test.py" -vv

run-native:
	./src/main.py --project foo --self-test 42

# https://docs.docker.com/engine/reference/commandline/buildx_build/
# Use --load to load images into local container store
# Use --push to push images into remote container registry
docker-build:
	docker buildx build \
		--platform linux/amd64,linux/arm64 \
		--tag ${REGISTRY}/${APP_NAME}:${TAG} \
		--tag ${REGISTRY}/${APP_NAME}:latest \
		--build-arg APP_VERSION=${TAG} \
		--build-arg BUILD_TIME="${BUILD_TIME}" \
		--file Dockerfile --push .
	docker buildx imagetools inspect ${REGISTRY}/${APP_NAME}:${TAG}

ci-build:
	docker build \
		--pull \
		--tag ${REGISTRY}/${APP_NAME}:latest \
		--tag ${REGISTRY}/${APP_NAME}:${TAG} \
		--build-arg APP_VERSION=${TAG} \
		--build-arg BUILD_TIME="${BUILD_TIME}" \
		--file Dockerfile .
	docker push ${REGISTRY}/${APP_NAME}:latest
	docker push ${REGISTRY}/${APP_NAME}:${TAG}

docker-inspect:
	docker inspect ${REGISTRY}/${APP_NAME}:${TAG}

docker-run:
	docker run -it --rm --name "${APP_NAME}" "${IMAGE}"

docker-run-shell:
	docker run -it --rm --name "${APP_NAME}" --entrypoint "" "${IMAGE}" sh

update-image-ver:
	@perl -p -i -e 's/^(LAST_KNOWN_GOOD)( := ).*/\1\2${TAG}/g' Makefile
	@git diff Makefile

# NOTE: fails over VPN due to disallowed ip-block
pull-summitslist-csv:
	curl -sLo data/summitslist.csv "https://storage.sota.org.uk/summitslist.csv"

filter-region-w7w:
	@./scripts/filter-w7w.sh

filter-region-w7w-kg:
	@./scripts/filter-w7w-kg.sh
