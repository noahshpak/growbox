create_venv:
	python3 -m venv venv
	. venv/bin/activate && \
	pip3 install -r requirements.txt

remove_venv:
	rm -r venv

black:
	black -l 125 --exclude "/(venv)/" .

isort:
	. venv/bin/activate && \
	isort --recursive *.py
