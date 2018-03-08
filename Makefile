# Makefile
#
create_db:
	docker-compose run --rm web python ./instance/db_create.py

dev:
	docker-compose up -d

prod:
	docker-compose -f docker-compose.yml up -d
