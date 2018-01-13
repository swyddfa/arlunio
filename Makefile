
tests: lint test doctest

test:
	coverage run --source stylo setup.py test && coverage report

test_travis: test
	coveralls

lint:
	flake8 stylo/

doctest:
	cd docs && make doctest && rm *.png && cd ..
