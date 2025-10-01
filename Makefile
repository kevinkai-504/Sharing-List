.PHONY: build
build:
		docker compose up --build -d

.PHONY: test
test:
		docker compose exec backend sh -c "export PYTHONPATH=\"/app\" && pytest --html=./reports/reoprt.html --self-contained-html /app/tests"

.PHONY: down
down:
		docker compose down

.PHONY: query_db
query_db:
		docker compose exec backend python /app/query_db.py
