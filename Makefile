.PHONY: start
start:
	gunicorn

.PHONY: venv
venv:
	python3 -m venv venv --clear
