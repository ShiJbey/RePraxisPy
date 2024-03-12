"""Re:Praxis

Re:Praxis is an in-memory database solution for creating simple databases for games and
applications. It is a reconstruction of Praxis, the exclusion logic-based language used
by the [Versu social simulation engine](https://versu.com/). Users store information
using strings called *sentences*, and the system parses these to create an internal
database tree. Users can then query for patterns in the data using the same syntax used
to store information.

"""

from repraxis.__version__ import VERSION
from repraxis.database import RePraxisDatabase

# from repraxis.query

__all__ = ["VERSION", "RePraxisDatabase"]
