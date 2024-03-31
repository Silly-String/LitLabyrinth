"""CSC111 Project 2: Applications of trees and graphs

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 2. Please consult
the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC111 Teaching Team
"""
from __future__ import annotations
from typing import Any, Union


class _Vertex:
    """A vertex in a graph.

    Instance Attributes:
        - item: The data stored in this vertex.
        - kind: either 'book' or 'user' to help run checks when working with vertices
        - neighbours: The vertices that are adjacent to this vertex; mapped to their corresponding review amount.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
        - self.kind in {'book', 'user'}
    """
    item: Any
    kind: str
    neighbours: dict[_Vertex, Union[int, float]]

    def __init__(self, item: Any, kind: str) -> None:
        """Initialize a new vertex with the given item and neighbours."""
        self.item = item
        self.kind = kind
        self.neighbours = {}


class _Book(_Vertex):
    """A vertex in a graph.

    Instance Attributes:
        - item: The data stored in this vertex.
        - kind: 'book' to help run checks when working with vertices
        - genre: The genre of the book
        - author: The author of the book
        - blurb: A short summary of the book
        - reviews: a dictionary of users mapped to their corresponding reviews for the particular books.
        - neighbours: The vertices that are adjacent to this vertex; mapped to their corresponding review amount.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
    """
    item: str
    kind: str
    genre: str
    author: str
    blurb: str
    reviews: dict
    neighbours: dict[_Vertex, Union[int, float]]

    def __init__(self, item: str, genre: str, author: str, blurb: str = '') -> None:
        """Initialize a new vertex with the given item and neighbours."""
        super().__init__(item, 'book')
        self.genre = genre
        self.author: author
        self.blurb: blurb
        self.reviews = {}


class _User(_Vertex):
    """A vertex in a graph.

    Instance Attributes:
        - item: The data stored in this vertex.
        - kind: 'user' to help run checks when working with vertices
        - neighbours: The vertices that are adjacent to this vertex; mapped to their corresponding review amount.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
    """
    item: str
    kind: str
    neighbours: dict[_Vertex, Union[int, float]]

    def __init__(self, item: Any, neighbours: set[_Vertex]) -> None:
        """Initialize a new vertex with the given item and neighbours."""
        super().__init__(item, 'user')


class Graph:
    """A graph.

    Representation Invariants:
        - all(item == self._vertices[item].item for item in self._vertices)
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _Vertex object.
    _vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    # You can use "Run file in Python Console" to run PythonTA,
    # and then also test your methods manually in the console.
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
    })
