Filters
=======

Overview
--------

A filter, if enabled (see below), applies to an entry at various points during
generation. There are two points that a filter may register to be applied to:

* `entry_body`: passes the filter over each entry's body before it is templated
* `html_file`: passes the filter over the generated HTML file

Each filter takes a string argument, (optionally) makes some modifications to
it, and returns a transformed version of the string.

Stock filters
-------------

One filter is shipped with simpleblog and is enabled by default:

* `fmarkdown2` converts each entry's body text from [Markdown](http://daringfireball.net/projects/markdown/syntax) to HTML

Filters may be disabled by setting its `enabled` attribute to `False` (more on
this below). They are typically named with an `f` at the start; this is to
prevent name conflicts with other Python modules on the import path.

Internals of a filter
---------------------

Each filter is a Python module located in the `filters/` subdirectory. It
contains at least one file (`__init__.py`) and must define a dictionary called
`filter_register`. An example dictionary is given below:

```python
filter_register = {
    'enabled': True,
    'callback': run_filter,
    'apply_to': 'entry_body'
}
```

The `filter_register` dictionary contains three required keys:

* `enabled` must be a boolean and can be used to disable a filter from running
  (if set to `False`).
* `callback` is the callable object that will be called when the filter is run.
  It must take a single argument (the input) and return an (optionally)
  transformed output. It may be any object that can be called with an argument
  (e.g. method, class)
* `apply_to` defines when the filter shall be run. It must be one of
  `entry_body` or `html_file`, described at the top of this document.

An example callback (`run_filter`, from above) could transform the body text
into uppercase:

```python
def run_filter(s):
    return s.upper()
```
