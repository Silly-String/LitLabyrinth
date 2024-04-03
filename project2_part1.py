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
import csv

import networkx as nx


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
        """Initialize a new vertex with the given item and kind.
        self.reviews and self.neighbours is automatically set to an empty dictionary."""
        self.item = item
        self.kind = kind
        self.reviews = {}
        self.neighbours = {}

    def degree(self) -> int:
        """Return the degree of this vertex."""
        return len(self.neighbours)

    def check_connected_path(self, target_item: Any, visited: set[_Vertex]) -> Optional[list]:
        """Return a path between self and the vertex corresponding to the target_item,
        without using any of the vertices in visited.

        The returned list contains the items stored in the _Vertex objects, not the _Vertex
        objects themselves. The first list element is self.item, and the last is target_item.
        If there is more than one such path, any of the paths is returned.

        Return None if no such path exists (i.e., if self is not connected to a vertex with
        the target_item).

        Preconditions:
            - self not in visited

        >>> b1 = _Book("Nush On the Shore", 7)
        >>> u2 = _User("ala")
        >>> b3 = _Book("Nelle On the Shore", 8)
        >>> u4 = _User("illy")
        >>> b1.neighbours = {u2: 3, u4: 5}
        >>> u2.neighbours = {b3: ""}
        >>> b1.check_connected_path("Nelle On the Shore", set())
        ['Nush On the Shore', 'ala', 'Nelle On the Shore']
        >>> b1.check_connected_path("Nelle On the Shore", {u2}) is None
        True
        """
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
        without using any of the vertices in visited, by a path of length <= d.

        Preconditions:
            - self not in visited
            - d >= 0

        >>> b1 = _Book("Nush On the Shore", 7)
        >>> u2 = _User("ala")
        >>> b3 = _Book("Nelle On the Shore", 8)
        >>> u4 = _User("illy")
        >>> b1.neighbours = {u2: 3, u4: 5}
        >>> u2.neighbours = {b3: ""}
        >>> b1.check_connected_distance("Nelle On the Shore", set(), 3)  # Returns True: v1, v3, v4, v5
        True
        """
        if d >= 0 and self.item == target_item:
            return True

        elif d > 0:
            new_visited = visited.union({self})

            for neighbour in self.neighbours:
                if neighbour not in new_visited and neighbour.check_connected_distance(target_item, new_visited, d - 1):
                    return True

        return False

    def similarity_score_unweighted(self, other: _Vertex) -> float:
        """Return the unweighted similarity score between this vertex and other.

        The unweighted similarity score is calculated by dividing the total number of neighbours that are
        adjacent to both the vertices by the total number of neighbours that are adjacent to either one or
        both  of them. In the case that the degree of either vertex is found to be 0, the unweighted
        similarity score is computed as 0.
        """
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
        This function calculates the similarity score in a similar manner as the function
        similarity_score_unweighted; however, the numerator only counts common neighbours
        that have the same weight on the corresponding edges. When comparing two books,
        this means we only count the common users that gave the books the exact same
        review score.

        """
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
        - self.reviews is None and self.neighbours is None
    """
    item: str
    kind: str
    genre: set[str]
    author: set[str]
    pages: int
    blurb: str
    reviews: dict[str, str]
    neighbours: dict[_Vertex, Union[int, float]]

    def __init__(self, item: str, pages: int, blurb: str = '') -> None:
        """Initialize a new vertex with the given item and neighbours."""
        super().__init__(item, 'book')
        self.genre = set()
        self.author = set()
        self.blurb = blurb
        self.pages = pages

    def average_rating(self) -> Optional[float]:
        """Calculate the average rating for the book based on its reviews.

        Return None if there are no reviews for the book.
        """
        total_rating = 0
        num_reviews = len(self.neighbours)

        if num_reviews == 0:
            return None

        for rating in self.neighbours.values():
            total_rating += rating

        return total_rating / num_reviews


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

    def add_vertex(self, item: Any, kind: str, pages: Optional[int] = None, blurb: Optional[str] = None) -> None:
        """Add a vertex with the given item and kind to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.

        Preconditions:
            - kind in {'user', 'book'}
        """
        if item not in self._vertices:
            if kind == 'book':
                self._vertices[item] = _Book(item, pages, blurb)
            elif kind == 'user':
                self._vertices[item] = _User(item)
            else:
                raise ValueError("Invalid kind. Kind must be either 'user' or 'book'.")

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
            raise ValueError("This item is not in the graph")

    def get_all_items(self, kind: str = '') -> set:
        """Return a set of all vertex items in this graph.

        If kind != '', only return the items of the given vertex kind.

        Preconditions:
            - kind in {'', 'user', 'book'}
        """
        if kind != '':
            return {v.item for v in self._vertices.values() if v.kind == kind}
        else:
            return set(self._vertices.keys())

    def get_all_vertices(self, kind: str = '') -> set:
        """Return a set of all vertices in this graph.

        If kind != '', only return the vertices of the given kind.

        Preconditions:
            - kind in {'', 'user', 'book'}
        """
        if kind != '':
            return {v for v in self._vertices.values() if v.kind == kind}
        else:
            return set(self._vertices.values())

    def connected_path(self, item1: Any, item2: Any) -> Optional[list]:
        """Return a path between item1 and item2 in this graph.

        The returned list contains the ITEMS along the path.
        Returns None if no such path exists, including when item1 or item2
        do not appear as vertices in this graph.
        """
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
        in function docstrings.

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

    def get_book_info(self, book_item: Any, info_type: str = '') -> Union[dict, Union[str, set]]:
        """Retrieve information about a particular book in this graph.

        Return a dictionary containing the book information if the book is found in the graph.
        Return a string message if the book is not found in the graph.
        If info_type is specified, return the requested piece of information about the book.
        """
        book_vertex = self._vertices.get(book_item)
        if isinstance(book_vertex, _Book):
            book_info = {
                'title': book_vertex.item,
                'author': ', '.join(book_vertex.author),
                'genre': ', '.join(book_vertex.genre),
                'blurb': book_vertex.blurb,
                'average_rating': self.average_rating_for_book(book_item),
                'pages': book_vertex.pages
            }
            # If info_type is specified, return the requested piece of information
            if info_type:
                return book_info.get(info_type, "Invalid info type specified.")
            else:
                return book_info
        else:
            # The item corresponds to a user, not a book
            return "The specified item does not correspond to a book."

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
                    formatted_reviews = _format_reviews(reviews_list, max_reviews)
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
        """Find books based on a specific user's reading history in this graph.

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
                                 max_books: Optional[int] = 5) -> Union[str, dict[str, list]]:
        """Get book recommendations based on a list of liked books.

        Given a list of liked_books, find books that share features with those liked books.
        book list is decided based on [...]?
        Optionally filter the recommended books by a minimum average rating.
        Limit the maximum number of recommended books returned to max_books, with a default of 10 unless otherwise
        specified.
        """
        if not liked_books:
            return "No liked books provided."

        recommendations = {'books with similar genre': [], 'books with similar author': []}

        for book in liked_books:
            genre_similar_books = self.highest_genre_similarity(book, 20)
            author_similar_books = self.highest_author_similarity(book, 20)

            # Filter by minimum rating if provided
            if min_rating is not None:
                genre_similar_books = [b for b in genre_similar_books
                                       if self.average_rating_for_book(book) >= min_rating]
                author_similar_books = [b for b in author_similar_books
                                        if self.average_rating_for_book(book) >= min_rating]

            # Limit the number of recommended books
            genre_similar_books = genre_similar_books[:max_books]
            author_similar_books = author_similar_books[:max_books]

            # Add recommendations to the dictionary
            recommendations['books with similar genre'].append(genre_similar_books)
            recommendations['books with similar author'].append(author_similar_books)

        return recommendations

    def find_books_by_genre(self, genre: str, max_books: Optional[int] = 10) -> list:
        """Find books based on the specified genre.

        Return a list of books that belong to the specified genre.
        Limit the maximum number of books returned to max_books, with a default of 10 unless otherwise specified.
        """
        # Initialize an empty list to store books of the specified genre
        books_in_genre = []

        # Iterate over all vertices in the graph
        for vertex in self._vertices.values():
            # Check if the vertex represents a book and belongs to the specified genre
            if isinstance(vertex, _Book) and genre in vertex.genre:
                books_in_genre.append(vertex.item)

                # Check if the maximum number of books has been reached
                if len(books_in_genre) == max_books:
                    break

        return books_in_genre

    def genre_similarity_score(self, book_item1: Any, book_item2: Any) -> float:
        """Compute the genre similarity score between two books.

        Return a score representing the similarity of genres between the two books.
        The score is computed as the number of common genres divided by the minimum number of genres between the two
        books.
        """
        # Retrieve the book vertices corresponding to the given book items
        book_vertex1 = self._vertices.get(book_item1)
        book_vertex2 = self._vertices.get(book_item2)

        # If either book is not found in the graph or is not a book vertex, return 0
        if (not book_vertex1 or not book_vertex2 or not isinstance(book_vertex1, _Book)
                or not isinstance(book_vertex2, _Book)):
            return 0.0

        # Compute the number of common genres between the two books
        common_genres = len(book_vertex1.genre & book_vertex2.genre)

        # Compute the minimum number of genres between the two books
        min_num_genres = min(len(book_vertex1.genre), len(book_vertex2.genre))

        # Avoid division by zero
        if min_num_genres == 0:
            return 0.0

        # Compute the genre similarity score
        similarity_score = common_genres / min_num_genres

        return similarity_score

    def highest_genre_similarity(self, book_item: str, num_books: int = 10) -> List[str]:
        """Get a list of books with the highest genre similarity scores to the specified book.

        Return a list of book items with the highest genre similarity scores to the specified book.
        """
        # Retrieve the book vertex corresponding to the given book item
        book_vertex = self._vertices.get(book_item)

        # If the book is not found in the graph or is not a book vertex, return an empty list
        if not book_vertex or not isinstance(book_vertex, _Book):
            return []

        # Initialize a list to store book items with the highest similarity scores
        similar_books = []

        # Initialize a dictionary to store book items and their similarity scores
        similarity_scores = {}

        # Iterate over all other book vertices in the graph
        for other_book_item, other_book_vertex in self._vertices.items():
            # Skip the same book or non-book vertices
            if other_book_item == book_item or not isinstance(other_book_vertex, _Book):
                continue

            # Compute the genre similarity score between the specified book and the other book
            similarity_score = self.genre_similarity_score(book_item, other_book_item)

            # Store the similarity score for the other book
            similarity_scores[other_book_item] = similarity_score

        # Sort the dictionary by similarity score in descending order
        sorted_scores = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)

        # Extract the book items from the sorted list
        for book, _unused_item in sorted_scores[:num_books]:
            similar_books.append(book)

        # Return the list of book items with the highest similarity scores
        return similar_books

    def author_similarity_score(self, book_item1: Any, book_item2: Any) -> float:
        """Compute the author similarity score between two books.

        Return a score representing the similarity of authors between the two books.
        The score is computed as the number of common authors divided by the minimum number of authors between the two
        books.
        """
        # Retrieve the book vertices corresponding to the given book items
        book_vertex1 = self._vertices.get(book_item1)
        book_vertex2 = self._vertices.get(book_item2)

        # If either book is not found in the graph or is not a book vertex, return 0
        if (not book_vertex1 or not book_vertex2 or not isinstance(book_vertex1, _Book)
                or not isinstance(book_vertex2, _Book)):
            return 0.0

        # Compute the number of common authors between the two books
        common_authors = len(book_vertex1.author & book_vertex2.author)

        # Compute the minimum number of authors between the two books
        min_num_authors = min(len(book_vertex1.author), len(book_vertex2.author))

        # Avoid division by zero
        if min_num_authors == 0:
            return 0.0

        return common_authors / min_num_authors

    def highest_author_similarity(self, book_item: str, num_books: int = 10) -> List[str]:
        """Get a list of books with the highest author similarity scores to the specified book.

        Return a list of book items with the highest author similarity scores to the specified book.
        """
        # Retrieve the book vertex corresponding to the given book item
        book_vertex = self._vertices.get(book_item)

        # If the book is not found in the graph or is not a book vertex, return an empty list
        if not book_vertex or not isinstance(book_vertex, _Book):
            return []

        # Initialize a list to store book items with the highest similarity scores
        similar_books = []

        # Initialize a dictionary to store book items and their similarity scores
        similarity_scores = {}

        # Iterate over all other book vertices in the graph
        for other_book_item, other_book_vertex in self._vertices.items():
            # Skip the same book or non-book vertices
            if other_book_item == book_item or not isinstance(other_book_vertex, _Book):
                continue

            # Compute the author similarity score between the specified book and the other book
            similarity_score = self.author_similarity_score(book_item, other_book_item)

            # Store the similarity score for the other book
            similarity_scores[other_book_item] = similarity_score

        # Sort the dictionary by similarity score in descending order
        sorted_scores = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)

        # Extract the book items from the sorted list
        for book, _unused_item in sorted_scores[:num_books]:
            similar_books.append(book)

        # Return the list of book items with the highest similarity scores
        return similar_books

    def books_by_author(self, author: str, num_books: int = 10) -> List[str]:
        """Retrieve books by the given author, up to a default of 10.

        Return a list of book items written by the specified author, up to a default of 10.
        """
        # Initialize a list to store books by the given author
        books_by_author = []

        # Initialize a counter to keep track of the number of books found
        count = 0

        # Iterate over all book vertices in the graph
        for book_item, book_vertex in self._vertices.items():
            # Check if the vertex corresponds to a book and if the given author is in the set of authors
            if isinstance(book_vertex, _Book) and author in book_vertex.author:
                # Add the book item to the list
                books_by_author.append(book_item)
                count += 1

                # If the desired number of books is reached, stop iterating
                if count >= num_books:
                    break

        # Return the list of books by the given author
        return books_by_author

    def most_popular_books(self, num_books: int = 10) -> List[str]:
        """Find the most popular books based on the ratio of 5-star reviews to total number of reviews.

        Return a list of book items representing the most popular books, up to a default of 10.
        """
        # Initialize a list to store book items and their popularity scores
        book_popularity = []

        # Iterate over all book vertices in the graph
        for book_item, book_vertex in self._vertices.items():
            # Check if the vertex corresponds to a book
            if isinstance(book_vertex, _Book):
                # Calculate the ratio of 5-star reviews to total number of reviews
                five_star_reviews = sum(1 for _, rating in book_vertex.neighbours.items() if rating == 5)
                total_reviews = len(book_vertex.neighbours)
                popularity_score = five_star_reviews / total_reviews if total_reviews > 0 else 0

                # Append the book item and popularity score to the list
                book_popularity.append((book_item, popularity_score, total_reviews))

        # Sort the list by popularity score in descending order, with ties broken by total number of reviews
        book_popularity.sort(key=lambda x: (x[1], x[2]), reverse=True)

        # Extract the book items from the sorted list
        popular_books = [book[0] for book in book_popularity[:num_books]]

        # Return the list of most popular books
        return popular_books

    def to_networkx(self, max_vertices: int = 5000) -> nx.Graph:
        """Convert this graph into a networkx Graph.

        max_vertices specifies the maximum number of vertices that can appear in the graph.
        (This is necessary to limit the visualization output for large graphs.)

        Note that this method is provided for you, and you shouldn't change it.
        """
        graph_nx = nx.Graph()
        for v in self._vertices.values():
            graph_nx.add_node(v.item, kind=v.kind)

            for u in v.neighbours:
                if graph_nx.number_of_nodes() < max_vertices:
                    graph_nx.add_node(u.item, kind=u.kind)

                if u.item in graph_nx.nodes:
                    graph_nx.add_edge(v.item, u.item)

            if graph_nx.number_of_nodes() >= max_vertices:
                break

        return graph_nx


def _format_reviews(reviews_list: list, max_reviews: Optional[int]) -> str:
    """Format the list of reviews.

    Args:
        reviews_list (list): List of tuples containing user and review.
        max_reviews (int, optional): Maximum number of reviews to include.

    Returns:
        str: Formatted reviews string.
    """
    if max_reviews is not None:
        reviews_list = reviews_list[:max_reviews]

    formatted_reviews = "\n".join([f"{user}: {review}" for user, review in reviews_list])
    return formatted_reviews


def load_graph(user_reviews_file: str, book_file: str) -> Graph:
    """
    Return a book review system as graph corresponding to the given datasets.
    The Users and Books are the vertices of this graph. Edges can only exist
    between books and users (i.e. an edge cannot exist between two vertices
    of the same kind).

    Preconditions:
        - user_reviews_file is the path to a CSV file corresponding to the book review data
          format
        - book_file is the path to a CSV file corresponding to the book data
          format

    """
    gr = Graph()

    with open(book_file, 'r') as file:
        book_data = csv.reader(file)
        # Skipping the header
        next(book_data)
        for line in book_data:
            book_title = line[0]
            authors = [author.strip() for author in line[1].split(',')]
            pages = int(line[2])
            genres = [genre.strip() for genre in line[3].split(',')]
            summary = line[4]

            _add_book_to_graph(gr, (book_title, pages), authors, genres, summary)

    with open(user_reviews_file, 'r') as file:
        user_data = csv.reader(file)
        # Skipping the header
        next(user_data)
        for line in user_data:
            user_id = line[0]
            book_title = line[1]
            review = line[3]
            rating = int(line[2])

            _add_user_review_to_graph(gr, user_id, book_title, review, rating)

    return gr


def _add_book_to_graph(graph: Graph, book_title_pages: tuple[str, int], authors: List[str], genres: List[str],
                       summary: str) -> None:
    """
    Add book information to the graph.

    Args:
        - graph (Graph): The graph object to which the book information will be added.
        - book_title_pages tuple[str, int]: The title of the book, coupled with the page count.
        - authors (List[str]): List of authors of the book.
        - genres (List[str]): List of genres associated with the book.
        - summary (str): Summary or blurb of the book.

    Returns:
        - None
    """
    graph.add_vertex(item=book_title_pages[0], kind="book", pages=book_title_pages[1], blurb=summary)
    for vert in graph.get_all_vertices("book"):
        if vert.item == book_title_pages[0]:
            vert.author.update(authors)
            vert.genre.update(genres)


def _add_user_review_to_graph(graph: Graph, user_id: str, book_title: str, review: str, rating: int) -> None:
    """
    Add user review information to the graph.

    Args:
        - graph (Graph): The graph object to which the user review information will be added.
        - user_id (str): The ID of the user.
        - book_title (str): The title of the book being reviewed.
        - review (str): The review text.
        - rating (int): The rating given by the user.

    Returns:
        - None
    """
    graph.add_vertex(item=user_id, kind="user")
    for vert in graph.get_all_vertices("user"):
        if vert.item == user_id:
            vert.reviews[book_title] = review
            _update_book_reviews(graph, book_title, user_id, review)
    graph.add_edge(user_id, book_title, rating)


def _update_book_reviews(graph: Graph, book_title: str, user_id: str, review: str) -> None:
    """
    Update the review dictionary of a book vertex with a new user review.

    Args:
        graph (Graph): The graph object containing the book vertex.
        book_title (str): The title of the book being reviewed.
        user_id (str): The ID of the user who provided the review.
        review (str): The review text.

    Returns:
        None
    """
    for book_vertex in graph.get_all_vertices("book"):
        if book_vertex.item == book_title:
            book_vertex.reviews[user_id] = review


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ["csv", "networkx"],
        'allowed-io': ['load_graph'],
        'max-line-length': 120,
    })
