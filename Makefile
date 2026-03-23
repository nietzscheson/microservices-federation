.PHONY:
init: down volume up
down:
	docker compose down
volume:
	docker volume prune -f
pull:
	docker compose pull
build:
	docker compose build
up: pull build
	docker compose up -d
	make ps
ps:
	docker compose ps
test: test.user test.product test.order
test.user:
	@docker compose run -T --rm user uv run pytest tests/ -v -s
test.product:
	@docker compose run -T --rm product uv run pytest tests/ -v -s
test.order:
	@docker compose run -T --rm order uv run pytest tests/ -v -s
debug:
	docker compose -f docker compose.yml -f docker compose.debug.yml up --build
prune:
	make down
	docker volume prune -f
	docker system prune -f
upgrade: upgrade.user upgrade.product upgrade.order
upgrade.user:
	@docker compose run -T --rm user uv run alembic upgrade head
upgrade.product:
	@docker compose run -T --rm product uv run alembic upgrade head
upgrade.order:
	@docker compose run -T --rm order uv run alembic upgrade head
fixtures: fixtures.user fixtures.product fixtures.order
fixtures.user:
	@docker compose run -T --rm user uv run python -m src.fixtures
fixtures.product:
	@docker compose run -T --rm product uv run python -m src.fixtures
fixtures.order:
	@docker compose run -T --rm order uv run python -m src.fixtures
migrate:
	docker compose run -T --rm user uv run alembic revision --autogenerate
	docker compose run -T --rm product uv run alembic revision --autogenerate
	docker compose run -T --rm order uv run alembic revision --autogenerate
