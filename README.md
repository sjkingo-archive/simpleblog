simpleblog
==========

simpleblog is a blogging platform that is intented to be have a low barrier to
setup and entry, and to make publishing blog entries simple and trivial to do.

It takes input as a series of MIME-type text files describing the entry and its
content (see `example-entries/`) and applies gemerates an output of HTML, ready to
be published (see `publishers/`).

A lot of the ideas for simpleblog are taken from a fellow blogging platform
called [constance](http://github.com/danc86/constance). The primary purpose of
this system is to provide extensibility via filters. Filters can be defined as
submodules to alter the text as it is processed (such as converting from
markdown to HTML).

To get started with the file publisher (writes to .html files), make sure all 
of the `DEPENDS` are satisfied and run:

    publishers/file.py -f entry.txt -i

You can also run the publisher over more than one entry by specifying a directory:

    publishers/file.py -d directory_full_of_entries/ -i

The published HTML file will be placed in the same directory as the input entry.

The `-i` option tells the publisher to write an `index.html` file in the same
directory.
