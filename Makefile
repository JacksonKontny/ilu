# Makefile
init:
	docker-compose run --rm web python create_postgres_dockerfile.py
	docker-compose build
	docker-compose up -d
	docker-compose run --rm web python ./instance/db_create.py

init_db:
	docker-compose run --rm web python ./instance/db_create.py

dev:
	docker-compose -f docker-compose.yml -f docker-compose.development.yml up -d
	docker attach --sig-proxy=false ilu_web_1

prod:
	docker-compose -f docker-compose.yml up -d

migrate:
	docker-compose -f docker-compose.yml -f docker-compose.development.yml run --rm web flask db upgrade
	docker-compose -f docker-compose.yml -f docker-compose.development.yml run --rm web flask db migrate -m '$(MESSAGE)'
	docker-compose -f docker-compose.yml -f docker-compose.development.yml run --rm web flask db upgrade

test:
	# DO NOT USE - this is a work in progress.  The goal is to test using
	# an environment as similar as possible to production.  For now local
	# testing with `nose2` is the best option
	docker-compose -f docker-compose.test.yml build
	docker-compose -f docker-compose.test.yml up -d postgres
	docker-compose -f docker-compose.test.yml run --rm web nose2 -s ./ --with-coverage --coverage-config=./.coveragerc
