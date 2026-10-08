# Rights Classification Tooling — Phase A

Reusable synthetic-only tooling for Work Item #10 Phase A, delivered under Work Item #15.

## Run tests

From this directory:

python -m unittest discover -s tests -v

No third-party packages are required.

## Guardrails

- does not open or scan the real corpus;
- does not accept Internet availability as rights evidence;
- separates underlying work from edition/file;
- A/B/C/D require evidence URLs;
- uncertain or unsupported cases become E;
- synthetic fixture URLs use example.invalid and contain no real catalog metadata.

Phase B is intentionally not executed here.
