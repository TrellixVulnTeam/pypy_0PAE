# Migration path to py3

There are a lot of steps here, but they can be broadly broken into 3 categories:
-  Simple (e.g. `print(1)` vs `print 1`, affect of `__metaclass__`, `__non_zero__`)
-  Complex - int/long, bytecode ops
-  Very complex - string/unicode behaviour

Of these, I think only the `int/long` and `string/unicode` behaviour is hard to
implement in both a 2 and 3 compatible way.

## List of simple changes

In no particular order.

### Print statement

We should use `from __future__ import print_function` in all files except those
containing old-style print statement snippets for testing. We should also make the
print function valid rpython for compatibility.

### Tuple arguments

We would need to get rid of invalid syntax like `def foo((x, y), z)`. This can be done
with decorators for their usage in `pairtype` objects, and by unpacking via `*args` in
most other cases.

### Exception tuples

We should replace `raise Exc, Exc("bla")` with `raise Exc("bla")`.
It's also possible to set the traceback explicitly via `e.__traceback__ = tb`.
Whether this is strictly necessary in all the places we're reraising with a traceback
object I'm unsure.

### Exec statement

In Python 2 exec is a statement, in Python 3 it is a function. This will need
acomplishing by importing a helper function `execute` from `rpython.compat` and using
that.

### About Metaclasses

We should use an `@add_metaclass` decorator (this idea was lifted straight from the
`six` library), since Python 3 does not respect `__metaclass__` and Python 2 doesn't
understand `metaclass=` in class definitions.

### Comprehension differences

We should fix these as we find them. For instance:
- `[x for x in "foo", "bar"]` should be `[x for x in ("foo", "bar")]`
- variables don't leak from comprehensions any more

### Octal literals

We should write octal literals in the new style, i.e. `0o644` instead of `0644`.

### Long literals

There's no real need for long literals in Python 2.7. We should remove them from all
files except those used for testing our parsing/support of this syntax.

### No more xrange

We should just import this from an `rpython.compat` module.

### Raw unicode literals

We should remove these and replace them with carfully crafted unicode.

### Backticks

We should remove these and replace with `repr`.

### UserDict

We should replace with `collections.MutableMapping`.

### Iterator differences

We should use `__next__` rather than `next` to define iterators.

### Zero use of \_\_non_zero\_\_

We should define `__bool__ = __non_zero__` for any class which implements the latter.

### iteritems, itervalues, iterkeys

These should either be replaced with their non-"iter" versions, or for larger objects
where this would impact performance, use an `rpython.compat.iteritems` function.

We should keep these methods in some py2-only test snippets, to check we still support
them.

### Making a `\_\_hash\_\_` of it

If a class implements `__eq__` it will now need `__hash__` to end up in a dictionary or
set. I'd love to go with something like `hash(repr(self))`, but I think the inclusion of
the address in `repr` means that the hash could change during runtime. Possibly some
variant of `hash(tuple(self.__dict__.items()))` is a good default?

Note: we only need to implement this for things we want to hash. Some experimentation
is needed.

### Relative imports

We will probably need a few imports from `import foo` to `from . import foo`.

### \_\_builtin\_\_ vs builtins

A compatability hack is needed: `try import __builtin__` and if that fails, just
`import builtins`.

### No more os.tmpfile

We should replace current usage by `tempfile.TemporaryFile`. There is one use that I
have no idea about:
```python
redirect_function(os.tmpfile, 'rpython.rlib.rfile.create_temp_rfile')
```
We can `try` to do this and pass if it doesn't exist. I assume that means rpython3 code
can't use this function?

### All the things are iterators now

`items`, `map`, `zip`,`range`, .. you name it, it's an iterator. That means there will
be subtle semantic differences in `map(f, x) + map(g, y)` and some possible double-use
of empty iterators.

There are two ways to approach this:
1.  just wait and see what breaks, then fix it (e.g. by judicious application of `list`).
2.  fast-forward any breakage and test under Python 2 by using `imap`, `izip`, `xrange` etc.

Whether method 1 is justified depends on how much time we have playing around with a non
py3-compatible rpython. Presumably we'll have quite a lot of time and can do this at our
leisure.

## List of complex changes

Listed from simplest to most complex.

### Division

Ideally we would use new-style division in the existing codebase via
`from __future__ import division`. Because it's not feasible to find every use of the
`/` binary op, we'd have to rely on testing and real-world use to flag up any issues.
This can all be done under Python 2.

Step 1 would be to use old-style division in all test files and new-style division in
all non-test files, so that we're sure we haven't changed the tests. Step 2 is to fix
all the things that break (both in tests and real translations). Step 3 is to change the
test files - and fix the breakages there.

### Bytecode differences

We will probably need to rewrite `HostCode` and `FlowContext` to account for differences
in Python's in-built bytecode representation. Ideally we should use the builtin `dis`
library to help us with this. I suspect using `list(dis.Bytecode(code))` would prevent
us from having to write everything 2x and keep up with any further changes in the
internal bytecode representation.

## List of very complex changes

In (probably) increasing complexity.

### Int / Long confusion

I think that almost everywhere `long` is used in the py2 codebase, `int` would suffice
in the py3 codebase. There are some notable exceptions (this may not be a complete
list):
-  sizing for C types (in particular how to represent various ints)
-  any use of `sys.maxint` (which does not exist in Python 3)

In particular these cases will need careful inspection. I'm hopeful that comparing to
the system's max C int / long sizes will suffice for any sizing of integers. If we were
already doing so, then relying on Python's `int` being below a certain size is no longer
feasible.

The hardest part of all of this is probably cross-platform testing of any solution.

### String / Unicode mess

It's still unclear how to deal with this.

**Method 1** I've been operating under the assumption that everywhere that `str` is
currently used, we really mean `bytes`. However, the correctness of this assumption is
far from clear

If we operate under the above assumption then everywhere we use `str` we should try and
use `bytes`. Everywhere we use `unicode`, we will need to import it from
`rpython.compat` - under Python 2 this will resolve to the `unicode` type and under
Python 3 to `str`.

Assuming the above is correct, we need a compat version of `unichr` and have to replace
`cStringIO` with `io.BytesIO`. Then quite a lot of string literals will need to be
rewritten as bytes literals.

**Method 2** The alternative is to use the native `str`, whatever that may be, for most
things. This works for porting *most* codebases, where you only need to control the type
of the string during IO. However, we also have internal representations of all the types
that would need some careful thought.

For instance, the underlying type of `SomeString` and `SomeUnicodeString`. Should we
make these equal under Python3, and introduce `SomeByteString` which would equal
`SomeString` under Python 2, but not under Python 3?
