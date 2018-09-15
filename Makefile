help:
	@echo "Usage: "
	@echo "help           - Show this help"
	@echo "test           - Run the test suites"
	@echo "build          - Build the package"

test:
	HOME=/tmp py.test

build:
	python setup.py build
	python setup.py sdist
