.PHONY: build
build:
		docker-compose up --build -d

.PHONY: test
test:
		docker-compose exec backend sh -c "pytest /app/tests/learn/test_learn.py"

.PHONY: down
down:
		docker compose down
