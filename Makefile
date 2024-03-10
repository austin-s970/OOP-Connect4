src = src/
test_dir = test/
documentation_dir = docs/

TEST = PYTHONPATH=$(src) python3 -m pytest
TEST_ARGS = -s --verbose --color=yes --cov=$(src)
TYPE_CHECK = mypy --strict --allow-untyped-decorators --ignore-missing-imports
STYLE_CHECK = flake8


.PHONY: all
all: check-style check-type run-test clean docs

.PHONY: check-type
check-type:
	$(TYPE_CHECK) $(src)

.PHONY: check-style
check-style:
	$(STYLE_CHECK) $(src)

.PHONY: fix-style
fix-style:
	autopep8 --in-place --recursive --aggressive --aggressive $(src)

.PHONY: test # alias for run-test
test: run-test

# discover and run all tests
.PHONY: run-test
run-test:
	$(TEST) $(TEST_ARGS) $(test_dir)

.PHONY: docs
docs: $(documentation_dir)/index.html

$(documentation_dir)/index.html: src/*.py
	pdoc -o docs $^




.PHONY: clean
clean:
# remove all caches recursively
	rm -rf `find . -type d -name __pycache__` # remove all pycache
	rm -rf `find . -type d -name .pytest_cache` # remove all pytest cache
	rm -rf `find . -type d -name .mypy_cache` # remove all mypy cache
	rm -rf `find . -type d -name .hypothesis` # remove all hypothesis cache
	rm -rf `find . -type d -name .coverage` # remove all coverage cache
