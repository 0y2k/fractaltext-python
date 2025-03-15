###########
FractalText
###########

Python implementation of `FractalText <https://github.com/0y2k/fractaltext-spec>`_.
FractalText is a recursive plaintext data format.

***************
Install and Run
***************

build
  ::

    uv build
test
  ::

    uv run --group test pytest

***********
Development
***********

install pre-commit
  ::

    uv run pre-commit install
lint and format
  ::

    uv run pre-commit run -a
generate doc
  ::

    uv run --group doc make -C doc html
