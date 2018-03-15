# Makefile
init_project:
	docker-compose run --rm web python create_postgres_dockerfile.py
	docker-compose build
	docker-compose up -d
	docker-compose run --rm web python ./instance/db_create.py
#
init_db:
	docker-compose run --rm web python ./instance/db_create.py

dev:
	docker-compose -f docker-compose.yml -f docker-compose.development.yml up -d

prod:
	docker-compose -f docker-compose.yml up -d

migrate:
	flask db migrate -m '$(MESSAGE)'

test:
	# DO NOT USE - this is a work in progress.  The goal is to test using
	# an environment as similar as possible to production.  For now local
	# testing with `nose2` is the best option
	docker-compose -f docker-compose.yml -f docker-compose.test.yml run --rm web nose2 -s ./
