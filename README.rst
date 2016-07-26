A JSON parser written in Python
===============================


WTF
---

:cry: :

.. code:: python

    import json
    json.loads(r"""{"a": "good", 123: "fuck!", false: "fuck!!", null: "fuck!!!"}""")



:kissing_heart: :

.. code:: python

    import djson
    djson.loads(r"""{"a": "good", 123: "well done!", true: "excellent!!", null: "I love djson!!!"}""")



APIs
----

 - load(str) -> dict()
 - loads(fd) -> dict(): fd is a iterable file-like object.
 - dump(obj, fd=sys.stdout, encoder=Encoder): Rewrite Encoder to support custom object. NOTE: returned string must like this: ``'"string"'``.
 - dumps(obj, encoder=Encoder) -> str


Examples
--------

See `examples/ <https://github.com/Damnever/djson/tree/master/examples>`_


TODO
----

 - testcases(corner cases..)


LICENSE
-------

`The BSD 3-Clause License <https://github.com/Damnever/pigar/blob/master/LICENSE>`_
