# Put any command that doesn't create a file here (almost all of the commands)
.PHONY: \
    help \
    usage \
    manage \
    test \
    migrations \
    migrate \
    shell \
    clear_cache \
    chown \

usage:
	@echo "Available commands:"
	@echo "manage					Run a Django management command"
	@echo "test						Run Django tests"
	@echo "migrations				Create Django migrations"
	@echo "migrate					Run Django migrations"
	@echo "shell					Run Django command line"
	@echo "clear_cache				Clear Django's cache"
	@echo "chown					Change ownership of files to own user"

help:
	$(MAKE) usage

manage:
	@docker-compose run --rm ${OPTIONS} web python3 ${PYTHON_ARGS} manage.py ${ARGS}

test:
	$(MAKE) manage ARGS="test ${ARGS}"

migrations:
	$(MAKE) manage ARGS="makemigrations ${ARGS}"

migrate:
	$(MAKE) manage ARGS="migrate ${ARGS}"

shell:
	$(MAKE) manage ARGS="shell_plus ${ARGS}"

clear_cache:
	$(MAKE) manage ARGS="clear_cache ${ARGS}"

chown:
	@docker-compose run --rm web chown -R "`id -u`:`id -u`" "/code/${ARGS}"
