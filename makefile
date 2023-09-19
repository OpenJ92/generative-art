clean:
	rm -rf __pycache__

black: black-diff
	black --target-version=py310 py-gen

black-diff:
	black --target-version=py310 --diff --color py-gen

