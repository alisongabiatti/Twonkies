redis-run:
	bin/redis-server bin/redis.conf

deploy:
	tsuru app-deploy . -a poc-chaos

run-server:
	python api-server/server.py 
