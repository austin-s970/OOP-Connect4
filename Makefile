PLANTUML = java -jar ~/plantuml.jar
SHELL = /bin/bash

src = src/
test_dir = test/
documentation_dir = docs/

TEST = PYTHONPATH=$(src) python3 -m pytest
TEST_ARGS = -s --verbose --color=yes --cov=$(src) $(extra_test_args)
TYPE_CHECK = mypy --strict --allow-untyped-decorators --ignore-missing-imports
STYLE_CHECK = flake8
SHOW_COV = PYTHONPATH=$(src) python3 -m pytest --cov=$(src) --cov-report term-missing


.PHONY: all
all: check-style check-type run-test clean docs uml

.PHONY: check-type
check-type:
	time $(TYPE_CHECK) $(src)

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
	time $(TEST) $(TEST_ARGS) $(test_dir)

.PHONY: show-cov
show-cov:
	$(SHOW_COV)

.PHONY: docs
docs: $(documentation_dir)/index.html

$(documentation_dir)/index.html: src/*.py
	pdoc -o docs $^

.PHONY: uml
uml: docs
# use shell command which to check if java is installed and is in the $PATH
ifeq ($(shell which java), )
	$(error "No java found in $(PATH). Install java to run plantuml")
endif
# use wildcard function to check if file exists
ifeq ($(wildcard ~/plantuml.jar), )
	@echo "Downloading plantuml.jar in home folder..."
	curl -L -o ~/plantuml.jar https://sourceforge.net/projects/plantuml/files/plantuml.jar/download
endif
	$(PLANTUML) design-analysis/Process_View.plantuml
	$(PLANTUML) design-analysis/Logical_View.plantuml
	$(PLANTUML) design-analysis/Development_View.plantuml
	$(PLANTUML) design-analysis/Physical_View.plantuml
	$(PLANTUML) design-analysis/Context_View.plantuml
	@echo "Design Analysis (4+1 View) UML diagrams created and saved in design-analysis folder"

	$(PLANTUML) uml/FullError.plantuml
	$(PLANTUML) uml/MultiError.plantuml
	$(PLANTUML) uml/Game.plantuml
	$(PLANTUML) uml/Turns.plantuml
	$(PLANTUML) uml/Screen.plantuml
	$(PLANTUML) uml/Piece.plantuml
	$(PLANTUML) uml/Spot.plantuml
	$(PLANTUML) uml/BoardIterator.plantuml
	$(PLANTUML) uml/Board.plantuml
	$(PLANTUML) uml/Color.plantuml
	$(PLANTUML) uml/DrawMeta.plantuml
	$(PLANTUML) uml/Draw.plantuml
	$(PLANTUML) uml/Class-Interaction.plantuml
	@echo "UML class diagrams created and saved in uml folder"

.PHONY: clean
clean:
# remove all caches recursively
	rm -rf `find . -type d -name __pycache__` # remove all pycache
	rm -rf `find . -type d -name .pytest_cache` # remove all pytest cache
	rm -rf `find . -type d -name .mypy_cache` # remove all mypy cache
	rm -rf `find . -type d -name .hypothesis` # remove all hypothesis cache
	rm -rf `find . -type d -name .coverage` # remove all coverage cache

.PHONY: run
run:
	$(src)/main.py 2>/dev/null
