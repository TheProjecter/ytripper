# Headers #

The file headers should look like this:

```
#!/usr/bin/python

# Copyright (c) 2005 by <author> - <email>
#
# Generated: Fr 8. Okt 15:10:26 CEST 2010
#
# GNU General Public Licence (GPL)
# 
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA  02111-1307  USA
#

<local imports>

<imports>


```

If you have more than one programmer per file, change the header as follows:
```
# Copyright (c) 2005 by <author> - <email>, <second-author> - <mail>
```

And if it gets longer than approx. 90 chars, write the author/s in a new line.

And so forth ;)

# Code format #
## Variables ##
```
foo_bar = None
really_long_var = True
```

## Functions ##
```
def example_function():
```

## Classes ##
```
class everyLeadingCharUppercase:
```
(Except the first letter)

## Attributes and Methods ##
Private data:
```
def __private_function(self):
# ...

class __internUsedObject:
```

Everything else is written as follows:
```
something_not_listed
```
## Kommentierung ##
One-line-comments should be written below the referred line of code:
```
do_smth()
# does something
```

If you have a bigger comment use a block comment:class makesSomething:
    """
       This class does something.

       Sub-classes: __subOne, __subTwo
    """```