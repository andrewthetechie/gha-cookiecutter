.DEFAULT_GOAL := help

# This help function will automatically generate help/usage text for any make target that is commented with "##".
# Targets with a singe "#" description do not show up in the help text
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-40s\033[0m %s\n", $$1, $$2}'

setup-dev:  pyenv-setup install-requirements setup-pre-commit ## Uses pyenv to setup a virtualenv and install requirements

pyenv-setup:
	pyenv virtualenv 3.11 gha-cookiecutter
	pyenv local gha-cookiecutter

install-requirements:  ## Pip installs our requirements
	pip install -r Docker/builder/rootfs/requirements.txt
	pip install -r requirements-dev.txt

setup-pre-commit:
	pre-commit install

build: ## build a docker image locally
	docker build -t gha-cookiecutter -f Docker/Dockerfile .

generate-inputs: ## Generate a dict of inputs from actions.yml into repo_manager/utils/__init__.py
	./.github/scripts/replace_inputs.sh

install-action-lint-mac: ## Install actionlint (used in pre-commit) on a mac using homebrew
	brew install actionlint

install-action-lint: ## Install actionlint (used in pre-commit) using go install
	go install github.com/rhysd/actionlint/cmd/actionlint@latest

actionlint: ## run actionlint with our ignores
	# https://github.com/rhysd/actionlint/issues/152
	actionlint -ignore 'property \".+\" is not defined in object type'

test: ## Run our unit tests
	pytest
