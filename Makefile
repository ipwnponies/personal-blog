.PHONY: venv
venv:
	bin/venv_update.py \
		venv= -p python3 venv \
		install= -r requirements-dev.txt \
		bootstrap-deps= -r requirements-bootstrap.txt \
		>/dev/null

.PHONY: install-hooks
install-hooks: venv
	venv/bin/pre-commit install --install-hooks

.PHONY: clean
clean:
	rm -rf ./venv
