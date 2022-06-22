.PHONY:
init: down volume up
down:
	docker-compose down
volume:
	docker volume prune -f
pull:
	docker-compose pull
build:
	docker-compose build
up: pull build
	docker-compose up -d
	make ps
ps:
	docker-compose ps
test:
	docker-compose run --rm user python -m pytest tests/ -v -s
debug:
	docker-compose -f docker-compose.yml -f docker-compose.debug.yml up --build
prune:
	make down
	docker volume prune -f
	docker system prune -f
upgrade:
	docker-compose run --rm core flask db upgrade
