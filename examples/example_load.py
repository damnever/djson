# -*- coding: utf-8 -*-

from djson import loads, JSONDecodeError


json_str = """
{
    "good": "bad",
    123: 456,
    "minus number": -2345,
    "arr": [1, 2, "3", 4.5],
    "none": null,
}
"""

bad_json_str = """
{
    "good": "bad",
    null
}
"""

bad_json_str2 = """
{
    "good": "bad",
    "bad": 12.3.4
}
"""

bad_json_str3 = """
{
    "good": "bad\\\\\""
    "bad": "good\\\\\\""
}
"""


if __name__ == "__main__":
    print(loads(json_str))

    print('--')
    try:
        print(loads(bad_json_str))
    except JSONDecodeError as e:
        print(e)

    print('--')
    try:
        print(loads(bad_json_str2))
    except JSONDecodeError as e:
        print(e)

    print('--')
    try:
        print(loads(bad_json_str3))
    except JSONDecodeError as e:
        print(e)
