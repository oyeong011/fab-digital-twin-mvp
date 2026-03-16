PYTHONPATH=src

install:
	python3 -m pip install -r requirements.txt

run:
	$(PYTHONPATH) python3 -m fab_sim.app --seed 7 --tools 12 --fab-name fab-beta

api:
	$(PYTHONPATH) python3 -m uvicorn fab_sim.api:app --reload

test:
	python3 -m unittest discover -s tests -v

docker-build:
	docker build -t fab-digital-twin-mvp .

docker-run:
	docker run --rm -p 8000:8000 fab-digital-twin-mvp
