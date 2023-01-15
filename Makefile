default: | help

SRC_DIR=.

format: ## format codes
	poetry run autoflake -ri --remove-all-unused-imports --ignore-init-module-imports --remove-unused-variables ${SRC_DIR} && \
	poetry run isort ${SRC_DIR} && \
	poetry run black ${SRC_DIR}