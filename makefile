docker-up:
	docker-compose -f docker-compose.dev.yml up --build --abort-on-container-exit

docker-down:
	docker-compose -f docker-compose.dev.yml down