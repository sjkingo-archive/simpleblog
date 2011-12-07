A filter, if actived, applies to the body of an entry before being passed to a
converter. Each filter must be a submodule (typically prefixed with 'f' i.e.
fmarkdown2 - this is to prevent conflicting names with other system-wide
modules) that defines a dict called `filter_register` with a required key
`callback`. This value of this is a method that takes a single argument (the
body text) and returns a modified version of it.

The following filters are known:

 * fmarkdown2 - converts body text using a port of John Gruber's markdown script