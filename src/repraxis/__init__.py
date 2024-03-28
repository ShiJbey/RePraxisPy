"""Re:Praxis

Re:Praxis is an in-memory database solution for creating simple databases for games and
applications. It is a reconstruction of Praxis, the exclusion logic-based language used
by the [Versu social simulation engine](https://versu.com/). Users store information
using strings called *sentences*, and the system parses these to create an internal
database tree. Users can then query for patterns in the data using the same syntax used
to store information.

"""

from repraxis.database import RePraxisDatabase
from repraxis.query import DBQuery

MAJOR_VERSION = 1
MINOR_VERSION = 4
PATCH_VERSION = 0
__version__ = f"{MAJOR_VERSION}.{MINOR_VERSION}.{PATCH_VERSION}"

__all__ = ["RePraxisDatabase", "DBQuery"]
