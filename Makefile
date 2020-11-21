PYTHON := python3
MODULE_NAME := update_notifier
DIR_SRC := ./${MODULE_NAME}

.PHONY: test
test: lint
	${PYTHON} -m pytest -vv

.PHONY: lint
lint:
	${PYTHON} -m flake8 \
		--ignore=E501 \
		${DIR_SRC}
	${PYTHON} -m vulture \
		--exclude version.py \
		vulture-whitelist.py \
		${DIR_SRC}
	${PYTHON} -m mypy \
		--allow-redefinition \
		--ignore-missing-imports \
		${DIR_SRC}

.PHONY: setup
setup:
	pipenv install --dev

.PHONY: clean
clean:
	find -type d -name '.mypy_cache' -exec rm -rf {} +;
	find -type d -name '.pytest_cache' -exec rm -rf {} +;
	find -type d -name '__pycache__' -exec rm -rf {} +;
	rm -f ./tags

.PHONY: run
run:
	${PYTHON} -m ${MODULE_NAME}

.PHONY: tags
tags:
	ctags -R \
		--extra=+f \
		--languages=Python \
		--sort=yes \
		--totals=yes \
		${DIR_SRC}
