A different JSON parser for Python
==================================


WTF
---

-_-# :

.. code:: python

    import json
    json.loads(r"""{"a": "good", 123: "fuck!", false: "fuck!!", null: "fuck!!!"}""")



^_^ :

.. code:: python

    import djson
    djson.loads(r"""{"a": "good", 123: "well done!", true: "excellent!!", null: "I love djson!!!"}""")



APIs
----

 - load(str) -> dict()
 - loads(file) -> dict(): file is a iterable file-like object.
 - dump(obj, file=sys.stdout, encoder=JSONEncoder): Rewrite JOSNEncoder to support custom object. **NOTE**: returned string must like this: ``'"string"'``.
 - dumps(obj, encoder=JSONEncoder) -> str


Examples
--------

See `examples/ <https://github.com/Damnever/djson/tree/master/examples>`_


TODO
----

 - testcases(corner cases..)


LICENSE
-------

`The BSD 3-Clause License <https://github.com/Damnever/pigar/blob/master/LICENSE>`_
