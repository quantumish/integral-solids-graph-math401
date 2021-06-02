run: 
	mypy --pretty --strict --ignore-missing-imports --disallow-any-explicit --disallow-any-decorated threed.py
	python3.9 threed.py
