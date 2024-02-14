pre-commit-check-chameleon
==========================

Purpose: Check for syntax and accessibility misuse in Chameleon templates.

Usage in ``.pre-commit-config.yaml``::

    - repo: https://github.com/minddistrict/pre-commit-check-chameleon
      rev: 1.0
      hooks:
      - id: check-chameleon
