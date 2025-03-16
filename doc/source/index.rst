fractaltext documentation
=========================

**FractalText** is a dead-simple, recursive plaintext data format
which aims to alternate TOML or YAML.

See `official specification <https://github.com/0y2k/fractaltext-spec>`_.

This document is about fractaltext-|version|.

Annotated and Naked
-------------------

Annotated document (DocumentA) keeps blank lines and comment lines.
Naked document (Item) drops these lines.

fractaltext
-----------

.. autoclass:: fractaltext.DocumentA
.. autoclass:: fractaltext.ItemA
.. autofunction:: fractaltext.from_dict
.. autofunction:: fractaltext.to_dict
.. autoexception:: fractaltext.FractalTextParseError
.. autofunction:: fractaltext.load
.. autofunction:: fractaltext.parse
.. autofunction:: fractaltext.dump
.. autofunction:: fractaltext.serialize
.. autofunction:: fractaltext.itself
.. autofunction:: fractaltext.lookup
.. autofunction:: fractaltext.delete
.. autofunction:: fractaltext.exists
.. autofunction:: fractaltext.insert
.. autofunction:: fractaltext.update

* :doc:`fractaltext.naked <./fractaltext.naked>`
* :doc:`changelog <./changelog>`
* :ref:`search`
