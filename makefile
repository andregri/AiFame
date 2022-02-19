docker-up:
	docker-compose -f docker-compose.dev.yml up --build --abort-on-container-exit

docker-down:
	docker-compose -f docker-compose.dev.yml down

docker-down-volume:
	docker-compose -f docker-compose.dev.yml down -v

create-tables:
	docker-compose -f docker-compose.dev.yml up --build -d
	docker-compose -f docker-compose.dev.yml exec aifame-app python manage.py create_db
	docker-compose -f docker-compose.dev.yml down

shell-db:
	docker-compose -f docker-compose.dev.yml exec aifame-db psql --username=aifame-admin --dbname=user_db