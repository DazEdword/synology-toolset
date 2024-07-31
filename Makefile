.PHONY: permissions
permissions:
	find . -type f -iname "*.sh" -exec chmod +x {} \;
	find docker/scripts/ -type f -exec chmod +x {} \;

.PHONY: test/unit
test/unit:
	docker-compose build tests
	docker-compose run --rm tests docker/scripts/tests

.PHONY: test/scripts
test/scripts:
	docker-compose build tests
	docker-compose run --rm tests docker/scripts/scripts-tests

.PHONY: test/integration
test/integration:
	docker-compose build tests
	docker-compose run --rm tests docker/scripts/integration-tests

