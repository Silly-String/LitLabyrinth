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
from typing import Any, List, Optional, Union


# TODO: a lot of this module is copy pasted, so just check each one to make sure the implementations fit
#  the changes we've made to our class attributes, and check the docstrings for the same
#  reason (as well as to remove things like  "check the handout for..."). And especially keep an eye out for
#  set methods being used on a dict. That was one of the changes we made for this project and it's probably going to
#  pop up a lot
#  Most fo these jsut need to be double checked to make sure nothing got missed and tha tthe implemetations make sense.

class _Vertex:
    """A vertex in a graph.

    Instance Attributes:
        - item: The data stored in this vertex.
        - kind: either 'book' or 'user' to help run checks when working with vertices
        - reviews: a dictionary of books/users mapped to their corresponding reviews.
        - neighbours: The vertices that are adjacent to this vertex; mapped to their corresponding review amount.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
        - self.kind in {'book', 'user'}
    """
    item: Any
    kind: str
    reviews: dict[str, str]
    neighbours: dict[_Vertex, Union[int, float]]

    def __init__(self, item: Any, kind: str) -> None:
        """Initialize a new vertex with the given item and neighbours."""
        self.item = item
        self.kind = kind
        self.reviews = {}
        self.neighbours = {}

    def degree(self) -> int:
        """Return the degree of this vertex."""
        return len(self.neighbours)

    def check_connected_path(self, target_item: Any, visited: set[_Vertex]) -> Optional[list]:
        """Return a path between self and the vertex corresponding to the target_item,
        WITHOUT using any of the vertices in visited.

        The returned list contains the ITEMS stored in the _Vertex objects, not the _Vertex
        objects themselves. The first list element is self.item, and the last is target_item.
        If there is more than one such path, any of the paths is returned.

        Return None if no such path exists (i.e., if self is not connected to a vertex with
        the target_item). Note that this is very similar to _Vertex.check_connected, except
        this method returns an Optional[list] instead of a bool.

        Preconditions:
            - self not in visited

        >>> v1 = _Vertex(1, set())
        >>> v2 = _Vertex(2, set())
        >>> v3 = _Vertex(3, set())
        >>> v4 = _Vertex(4, set())
        >>> v1.neighbours = {v2, v3}
        >>> v2.neighbours = {v4}
        >>> v1.check_connected_path(4, set())
        [1, 2, 4]
        >>> v1.check_connected_path(4, {v2}) is None
        True
        """
        # TODO: adjust code to fit the specifications for our version of the vertex class
        if self.item == target_item:
            return [self.item]

        visited.add(self)

        for neighbour in self.neighbours:
            if neighbour not in visited:
                path = neighbour.check_connected_path(target_item, visited)

                if path is not None:
                    return [self.item] + path

        return None

    def check_connected_distance(self, target_item: Any, visited: set[_Vertex], d: int) -> bool:
        """Return whether this vertex is connected to a vertex corresponding to the target_item,
        WITHOUT using any of the vertices in visited, by a path of length <= d.

        Preconditions:
            - self not in visited
            - d >= 0

        >>> v1 = _Vertex(1, set())
        >>> v2 = _Vertex(2, set())
        >>> v3 = _Vertex(3, set())
        >>> v4 = _Vertex(4, set())
        >>> v5 = _Vertex(5, set())
        >>> v1.neighbours = {v2, v3}
        >>> v2.neighbours = {v3}
        >>> v3.neighbours = {v4}
        >>> v4.neighbours = {v5}
        >>> v1.check_connected_distance(5, set(), 3)  # Returns True: v1, v3, v4, v5
        True

        Implementation note (IMPORTANT):
            - Unlike check_connected, you should NOT mutate visited here (but instead
              create a new set that adds self, using set.union for example).
              This is less efficient, but also required to not introduce bugs.
              (Keep reading for details, but it's not required for implementing this method.)

              To see why, consider the doctest example.
              Since v1 has two neighbours (v2 and v3) stored in a set, the choice of which
              one to recurse on first is up to the Python interpreter. If we recurse on
              v2 first, then that recursive call will return False (since the path
              v1, v2, v3, v4, v5 is too long). But if we have every recursive call mutate
              visited, then when we're back to the original call v1.check_connected_distance,
              the loop will skip over v3, and fail to "find" the path v1, v3, v4, v5.

              This is subtle because this error would only happen if we make the first recursive
              call on v2---if we recurse on v3, the doctest would pass!
        """
        # TODO: adjust code to fit the specifications for our version of the vertex class
        if d == 0 and self.item == target_item:
            return True

        elif d > 0:
            new_visited = visited.union({self})

            for neighbour in self.neighbours:
                if neighbour not in new_visited:
                    if neighbour.check_connected_distance(target_item, new_visited, d - 1):
                        return True

        return False

    def similarity_score_unweighted(self, other: _Vertex) -> float:
        """Return the unweighted similarity score between this vertex and other.

        The unweighted similarity score is calculated in the same way as the
        similarity score for _Vertex (from Exercise 3). That is, just look at edges,
        and ignore the weights.
        """
        # TODO: check docstring and remove anything refering to the handout.
        #  Replace with additional details or omit entirely
        if self.degree() == 0 or other.degree() == 0:
            return 0

        self_keys = set(self.neighbours.keys())
        other_keys = set(other.neighbours.keys())

        intersection = {u for u in self_keys if u in other_keys}
        union = self_keys | other_keys

        if len(union) == 0:
            return 0
        else:

            return len(intersection) / len(union)

    def similarity_score_strict(self, other: _Vertex) -> float:
        """Return the strict weighted similarity score between this vertex and other.

        See Exercise handout for details.
        """
        # TODO: check docstring and remove anything refering to the handout.
        #  Replace with additional details or omit entirely
        if self.degree() == 0 or other.degree() == 0:
            return 0

        self_keys = set(self.neighbours.keys())
        other_keys = set(other.neighbours.keys())

        intersection = {u for u in self_keys if u in other_keys}
        specific_intersection = {v for v in intersection if self.neighbours[v] == other.neighbours[v]}
        union = self_keys | other_keys

        if len(union) == 0:
            return 0
        else:

            return len(specific_intersection) / len(union)


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
    reviews: dict[str, str]
    neighbours: dict[_Vertex, Union[int, float]]

    def __init__(self, item: str, genre: str, author: str, blurb: str = '') -> None:
        """Initialize a new vertex with the given item and neighbours."""
        super().__init__(item, 'book')
        self.genre = genre
        self.author = author
        self.blurb = blurb

    def average_rating(self) -> Optional[float]:
        """Calculate the average rating for the book based on its reviews.

        Return None if there are no reviews for the book.
        (use the reviews dictionary)
        """
        # TODO: implement


class _User(_Vertex):
    """A vertex in a graph.

    Instance Attributes:
        - item: The data stored in this vertex.
        - kind: 'user' to help run checks when working with vertices
        - reviews: a dictionary of books for which the user made a review mapped to their corresponding reviews.
        - neighbours: The vertices that are adjacent to this vertex; mapped to their corresponding review amount.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
    """
    item: str
    kind: str
    reviews: dict[str, str]
    neighbours: dict[_Vertex, Union[int, float]]

    def __init__(self, item: Any) -> None:
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

    def add_vertex(self, item: Any, kind: str) -> None:
        """Add a vertex with the given item and kind to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.

        Preconditions:
            - kind in {'user', 'book'}
        """
        if item not in self._vertices:
            self._vertices[item] = _Vertex(item, kind)

    def add_edge(self, item1: Any, item2: Any, weight: Union[int, float] = 1) -> None:
        """Add an edge between the two vertices with the given items in this graph,
        with the given weight.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            # Add the new edge
            v1.neighbours[v2] = weight
            v2.neighbours[v1] = weight
        else:
            # We didn't find an existing vertex for both items.
            raise ValueError

    def adjacent(self, item1: Any, item2: Any) -> bool:
        """Return whether item1 and item2 are adjacent vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            return any(v2.item == item2 for v2 in v1.neighbours)
        else:
            return False

    def get_neighbours(self, item: Any) -> set:
        """Return a set of the neighbours of the given item.

        Note that the *items* are returned, not the _Vertex objects themselves.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item in self._vertices:
            v = self._vertices[item]
            return {neighbour.item for neighbour in v.neighbours}
        else:
            raise ValueError

    def get_all_vertices(self, kind: str = '') -> set:
        """Return a set of all vertex items in this graph.

        If kind != '', only return the items of the given vertex kind.

        Preconditions:
            - kind in {'', 'user', 'book'}
        """
        if kind != '':
            return {v.item for v in self._vertices.values() if v.kind == kind}
        else:
            return set(self._vertices.keys())

    def connected_path(self, item1: Any, item2: Any) -> Optional[list]:
        """Return a path between item1 and item2 in this graph.

        The returned list contains the ITEMS along the path.
        Return None if no such path exists, including when item1 or item2
        do not appear as vertices in this graph.
        """
        # TODO: adjust code to fit the specifications for our version of the vertex/graph class
        #  (dependent on an unadjusted method above in the vertex class)
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            return v1.check_connected_path(item2, set())
        else:
            return None

    def connected_distance(self, item1: Any, item2: Any, d: int) -> bool:
        """Return whether items1 and item2 are connected by a path of length <= d.

        Return False if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - d >= 0
        """
        # TODO: adjust code to fit the specifications for our version of the vertex/graph class
        #  (dependent on an unadjusted method above in the vertex class)
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            return v1.check_connected_distance(item2, set(), d)
        else:
            return False

    def get_similarity_score(self, item1: Any, item2: Any,
                             score_type: str = 'unweighted') -> float:
        """Return the similarity score between the two given items in this graph.

        unweighted: determines books that have simular users
        strict: detemins books with simular users and reviews

        score_type is one of 'unweighted' or 'strict', corresponding to the
        different ways of calculating weighted graph vertex similarity, as described
        on the assignment handout.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - score_type in {'unweighted', 'strict'}
        """
        if item1 not in self._vertices or item2 not in self._vertices:
            raise ValueError

        v1 = self._vertices[item1]
        v2 = self._vertices[item2]

        if score_type == 'unweighted':
            return v1.similarity_score_unweighted(v2)

        else:
            return v1.similarity_score_strict(v2)

    def average_rating_for_book(self, book_item: Any) -> Union[float, str]:
        """Calculate the average rating for the specified book in this graph.

        Return a string message if the book is not found in the graph or if there are no reviews for the book.
        """
        if book_item in self._vertices:
            book_vertex = self._vertices[book_item]

            # Check if the vertex represents a book
            if isinstance(book_vertex, _Book):
                average_rating = book_vertex.average_rating()
                if average_rating is None:
                    return "No reviews available for this book."
                else:
                    return average_rating
            else:
                # The item corresponds to a user, not a book
                raise ValueError("The specified item does not correspond to a book.")
        else:
            # Book not found in the graph
            raise ValueError("Book not found in the graph.")

    def get_book_info(self, book_item: Any, info_type: str = '') -> Union[dict, str]:
        """Retrieve information about a particular book in this graph.

        Return a dictionary containing the book information if the book is found in the graph.
        Return a string message if the book is not found in the graph.
        If info_type is specified, return the requested piece of information about the book.
        """
        try:
            average_rating = self.average_rating_for_book(book_item)
        except ValueError as e:
            return str(e)

        if isinstance(average_rating, float):
            book_vertex = self._vertices.get(book_item)

            # Check if the vertex represents a book
            if isinstance(book_vertex, _Book):
                book_info = {
                    'title': book_vertex.item,
                    'genre': book_vertex.genre,
                    'author': book_vertex.author,
                    'blurb': book_vertex.blurb,
                    'average_rating': average_rating
                }

                # If info_type is specified, return the requested piece of information
                if info_type:
                    return book_info.get(info_type, "Invalid info type specified.")
                else:
                    return book_info
            else:
                # The item corresponds to a user, not a book
                return "The specified item does not correspond to a book."
        else:
            # Book not found in the graph or no reviews available
            return average_rating

    def get_reviews_for_book(self, book_item: Any, max_reviews: Optional[int] = 10) -> Union[str, list]:
        """Retrieve the list of reviews for a particular book in this graph.

        Return a string containing the formatted reviews if the book is found in the graph and has reviews.
        Return a string message if the book is not found in the graph or if there are no reviews for the book.
        If max_reviews is specified, limit the number of reviews printed to that maximum number. The auto-limit is 10.
        """
        if book_item in self._vertices:
            book_vertex = self._vertices[book_item]

            # Check if the vertex represents a book
            if isinstance(book_vertex, _Book):
                if book_vertex.reviews:
                    reviews_list = list(book_vertex.reviews.items())

                    # Limit the number of reviews if max_reviews is specified
                    if max_reviews is not None:
                        reviews_list = reviews_list[:max_reviews]

                    formatted_reviews = "\n".join([f"{user}: {review}" for user, review in reviews_list])
                    return formatted_reviews
                else:
                    return "No reviews available for this book."
            else:
                # The item corresponds to a user, not a book
                return "The specified item does not correspond to a book."
        else:
            # Book not found in the graph
            return "Book not found in the graph."

    def list_books_by_genre(self, genre: str, amount: Optional[int] = 10) -> Union[str, list]:
        """List books falling into a particular genre in this graph.

        Return a list containing the titles of books falling into the specified genre.
        Limit the number of books listed to the specified amount, with a default of 10.
        """
        # Create an empty list to store book titles
        book_titles = []

        # Iterate over all vertices in the graph
        for vertex in self._vertices.values():
            # Check if the vertex represents a book and if its genre matches the specified genre
            if isinstance(vertex, _Book) and vertex.genre == genre:
                # Add the book title to the list
                book_titles.append(vertex.item)

                # Check if the specified amount of books has been reached
                if len(book_titles) == amount:
                    break

        # Return the list of book titles
        return book_titles

    def find_books_based_on_user_reads(self, user_item: Any, min_rating: Optional[int] = None,
                                       max_books: Optional[int] = 10) -> Union[str, list]:
        """Find books based on a specific user's reads in this graph.

        Return a list of books read by the specified user, optionally filtered by a minimum rating.
        If min_rating is specified, only return books with ratings greater than or equal to min_rating.
        Limit the maximum number of books returned to max_books, with a default of 10 unless otherwise specified.
        """
        # Check if the user exists in the graph
        if user_item not in self._vertices:
            return "User not found in the graph."

        # Retrieve the user's neighbors and their corresponding ratings
        user_vertex = self._vertices[user_item]
        user_neighbors = user_vertex.neighbours

        # Filter books based on the minimum rating (if provided)
        filtered_books = []
        for neighbor, rating in user_neighbors.items():
            # Check if the rating meets the filter criteria (if provided)
            if min_rating is None or rating >= min_rating:
                filtered_books.append(neighbor.item)

                # Check if the maximum number of books has been reached
                if len(filtered_books) == max_books:
                    break

        return filtered_books

    def get_book_recommendations(self, liked_books: List[Any], min_rating: Optional[int] = None,
                                 max_books: Optional[int] = 10) -> Union[str, list]:
        """Get book recommendations based on a list of liked books.

        Given a list of liked_books, find books that share features with those liked books.
        book list is decided based on [...]?
        Optionally filter the recommended books by a minimum average rating.
        Limit the maximum number of recommended books returned to max_books, with a default of 10 unless otherwise
        specified.
        """
        # TODO: implement
        #  I'm not 100% sure how to go about the implementation of this one, so if it gets too much, we can scrap it.
        #  This would be the function for the main recomending feature of our project, but we still have a bunch of
        #  other festures, so loosing one won't hurt too much.
        #  I know this is a tough one so I tried to get some of the other functions out of the way.


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
