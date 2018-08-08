help:
	@echo "Usage: "
	@echo "help           - Show this help"
	@echo "test           - Run the test suites"

test:
	HOME=/tmp py.test
