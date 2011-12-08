A filter, if actived, applies to the body of an entry before being passed to a
converter. Each filter must be a submodule (typically prefixed with 'f' i.e.
fmarkdown2 - this is to prevent conflicting names with other system-wide
modules) that defines a dict called `filter_register`. The required attributes 
are given below:

* `callback`: a method that takes a single argument (the body text) and returns a modified version of it
* `when`: one of `start` or `end`, denoting whether the body text should be passed through before applying to the template (`start`) or after the template has been generated (`end`)

The following filters are known:

* fmarkdown2 - converts body text using a port of John Gruber's markdown script
* fprettify - reformats the final HTML output prettily
