.PHONY: install-hooks
install-hooks:
	bin/venv_update.py \
		venv= -p python3 venv \
		install= -r requirements-dev.txt \
		bootstrap-deps= -r requirements-bootstrap.txt \
		>/dev/null
	venv/bin/pre-commit install --install-hooks

.PHONY: clean
clean:
	rm -rf ./venv
