# Put any command that doesn't create a file here (almost all of the commands)
.PHONY: \
	chown \
	clear_cache \
	help \
	manage \
	migrate \
	migrations \
	shell \
	test \
	usage \

usage:
	@echo "Available commands:"
	@echo "chown            Change ownership of files to own user"
	@echo "clear_cache      Clear Django's cache"
	@echo "help             Display available commands"
	@echo "manage           Run a Django management command"
	@echo "migrate          Run Django migrations"
	@echo "migrations       Create Django migrations"
	@echo "shell            Run Django command line"
	@echo "test             Run Django tests"
	@echo "usage            Display available commands"

chown:
	@docker-compose run --rm web chown -R "`id -u`:`id -u`" "/code/${ARGS}"

clear_cache:
	$(MAKE) manage ARGS="clear_cache ${ARGS}"

help:
	$(MAKE) usage

manage:
	@docker-compose run --rm ${OPTIONS} web python3 ${PYTHON_ARGS} manage.py ${ARGS}

migrate:
	$(MAKE) manage ARGS="migrate ${ARGS}"

migrations:
	$(MAKE) manage ARGS="makemigrations ${ARGS}"

shell:
	$(MAKE) manage ARGS="shell_plus ${ARGS}"

test:
	$(MAKE) manage ARGS="test ${ARGS}"
