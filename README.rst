pre-commit-check-chameleon
==========================

Purpose
-------

Check for syntax and accessibility misuse in Chameleon templates.



Usage
-----

In ``.pre-commit-config.yaml`` add:

.. code:: yaml

    - repo: https://github.com/minddistrict/pre-commit-check-chameleon
      rev: 1.0
      hooks:
      - id: check-chameleon

Options
-------

a11y-lint-exclude
+++++++++++++++++

Exclude files in the given path from the accessibility checks, so they just get
checked for correct XML syntax.

Example:

.. code:: yaml

    - repo: https://github.com/minddistrict/pre-commit-check-chameleon
      rev: 1.0
      hooks:
      - id: check-chameleon
        args: [--a11y-lint-exclude=src/module_a/module_b/templates]
