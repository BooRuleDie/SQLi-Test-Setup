up:
	docker compose up -d

down:
	docker compose down

status:
	docker container ls -a

install:
	pip install "fastapi[all]"