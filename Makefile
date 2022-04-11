run:
	./scripts/notes_pipeline

test:
	pytest -vv

build:
	docker build -t travel .

docker-run:
	docker run -d --name travel travel:latest
