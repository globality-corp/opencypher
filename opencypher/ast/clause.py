from typing import Union

from opencypher.ast.create import Create
from opencypher.ast.delete import Delete
from opencypher.ast.match import Match
from opencypher.ast.merge import Merge
from opencypher.ast.remove import Remove
from opencypher.ast.set import Set
from opencypher.ast.unwind import Unwind


"""
ReadingClause = Match
              | Unwind
              | InQueryCall
              ;

"""
ReadingClause = Union[
    Match,
    Unwind,
    # omitted: InQueryCall
]

"""
UpdatingClause = Create
               | Merge
               | Delete
               | Set
               | Remove
               ;

"""
UpdatingClause = Union[
    Create,
    Merge,
    Delete,
    Remove,
    Set,
]
