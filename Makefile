python_version=2.7
python_cmd=python${python_version}
venv_cmd=virtualenv -p ${python_cmd}
virtualenv=. env/bin/activate;
kivy=env/lib/python${python_version}/site-packages/kivy
PYTHONPATH=.buildozer/applibs

default: install dev-deps

env:
	${venv_cmd} env
	${virtualenv} pip install -U setuptools

dev-deps:
	${virtualenv} pip install flake8

kivy-deps:
	${virtualenv} pip install -r kivy-requirements.txt

${kivy}: kivy-deps
	${virtualenv} pip install -r requirements.txt

install-deps: env ${kivy}

install: install-deps
	${virtualenv} pip install -e .

app: env
	${virtualenv} python src/main.py

android: env
	${virtualenv} buildozer -v android debug deploy run

android-release: env
	${virtualenv} buildozer -v android release deploy run

lint:
	@${virtualenv} flake8 src

clean:
	@rm -rf env
	@rm -rf .buildozer
