SHELL := /bin/bash
ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
PYTHONPATH := $(ROOT)
SCENE ?= room
INSTRUCTION ?= Go to the red bin, avoid the chair, inspect the table, then return home.
ALLOW_PROXY ?= 0
ALLOW_KINEMATIC ?= 0
ALLOW_RULE_PLANNER ?= 0

export PYTHONPATH

.PHONY: setup-brev check-gpu check-isaac check-livestream build live-demo recorded-demo api vla dashboard eval test integration-test clean

setup-brev:
	bash scripts/setup_brev.sh

check-gpu:
	bash scripts/check_gpu.sh

check-isaac:
	bash scripts/check_isaac.sh

check-livestream:
	bash scripts/check_livestream.sh

build:
	docker compose -f docker/docker-compose.yaml build

live-demo:
	bash scripts/run_live_demo.sh "$(SCENE)" "$(INSTRUCTION)" "$(ALLOW_PROXY)" "$(ALLOW_KINEMATIC)" "$(ALLOW_RULE_PLANNER)"

recorded-demo:
	bash scripts/run_headless_recorded_demo.sh "$(SCENE)" "$(INSTRUCTION)" "$(ALLOW_PROXY)" "$(ALLOW_KINEMATIC)" "$(ALLOW_RULE_PLANNER)"

api:
	bash scripts/start_api.sh

vla:
	bash scripts/start_vla.sh

dashboard:
	bash scripts/start_dashboard.sh

eval:
	bash scripts/run_eval.sh

test:
	python3 -m pytest tests -m "not integration"

integration-test:
	python3 -m pytest tests -m integration

clean:
	find outputs -mindepth 1 -maxdepth 1 ! -name .gitkeep -exec rm -rf {} +
