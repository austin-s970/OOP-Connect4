TEST = python -m pytest
TEST_ARGS = -s --verbose --color=yes
TYPE_CHECK = mypy --strict --allow-untyped-decorators --ignore-missing-imports
STYLE_CHECK = flake8

.PHONY: all
all: check-style fix-style check-type run-test clean

.PHONY: check-type
check-type:
	$(TYPE_CHECK) assignments/A0-sorttwonumbers

.PHONY: check-style
check-style:
	$(STYLE_CHECK) assignments/A0-sorttwonumbers

.PHONY: fix-style
fix-style:
	autopep8 --in-place --recursive --aggressive --aggressive assignments/A0-sorttwonumbers

# discover and run all tests
.PHONY: run-test
run-test:
	$(TEST) $(TEST_ARGS) assignments/A0-sorttwonumbers/tests/test.py


.PHONY: clean
clean:
	# remove all caches recursively
	rm -rf `find . -type d -name __pycache__` # remove all pycache
	rm -rf `find . -type d -name .pytest_cache` # remove all pytest cache
	rm -rf `find . -type d -name .mypy_cache` # remove all mypy cache
	rm -rf `find . -type d -name .hypothesis` # remove all hypothesis cache
	rm -rf `find . -type d -name .coverage` # remove all coverage cache 
	
