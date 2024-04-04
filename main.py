"""CSC111 Project 2: Applications of trees and graphs

Description
===============================

This Python module contains the main code for Project 2. It contains all the code that
creates a gui for the user to interact with and draws from code in project2_part1.py.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC111 Teaching Team
"""
import doctest
import tkinter
from typing import Any
import project2_part1


def excute_choices(c: str, book_lst: set, p_info: list, g: project2_part1.Graph) -> Any:
    """
    Displays the information that the user requests from the choise they entered and through the respective function
    call.
    If the user enters an invalid choise, a message is displayed informing the user of such.
    """
    r = tkinter.Tk()
    if c == "get information":
        get_information_input(g, p_info, r)
    elif c == "all books":
        all_books(g, r)
    elif c == "all users":
        all_users(g, r)
    elif c == "books in":
        books_in_genre(g, r)
    elif c == "books by":
        books_by(g, r)
    elif c == "books read by":
        books_read_by(g, r)
    elif c == "book recommendations":
        book_rec(g, book_lst, r)
    elif c == "most popular":
        most_popular(g, r)
    else:
        choice_label = tkinter.Label(r, text="That is not a valid action!")
        choice_label.pack()


def get_information_input(g: project2_part1.Graph, p_info: list, r: tkinter.Tk) -> Any:
    """
    Displays a way for the user to enter what book they want to get information on and
    calls the function to get that information about that book.
    """
    book_label = tkinter.Label(r, text="Enter the book title: ")
    book_input = tkinter.Entry(r, bg="#F3CEFF", borderwidth=5)
    book_button = tkinter.Button(r, text='Submit', padx=50, fg="purple",
                                 command=lambda: get_info_check_book(g, p_info, book_input.get(), r))
    book_label.pack()
    book_input.pack()
    book_button.pack()


def get_info_check_book(g: project2_part1.Graph, p_info: list, book: Any, r: tkinter.Tk) -> Any:
    """
    Checks if the user had entered a valid book and displays a way for the user to enter the
    specific information that the user wants about the book
    """
    if book not in g.get_all_items('book'):
        book_return = tkinter.Label(r, text="That is not a valid book!")
        book_return.pack()
    else:
        wanted_info_intro = tkinter.Label(r, text="Possible information that can be requested: ")
        info_list_label = tkinter.Label(r, text=str(p_info))
        info_type_ask = tkinter.Label(r, text="Enter what you would like: ")
        info_type_entry = tkinter.Entry(r, bg="#F3CEFF", borderwidth=5)
        info_type_button = tkinter.Button(r, text='Submit', padx=50, fg="purple",
                                          command=lambda: get_info_output(g, book, str(info_type_entry.get()), r))
        wanted_info_intro.pack()
        info_list_label.pack()
        info_type_ask.pack()
        info_type_entry.pack()
        info_type_button.pack()


def get_info_output(g: project2_part1.Graph, b: Any, info_request: str, r: tkinter.Tk) -> Any:
    """
    Displays the information that the user wanted, info_request, about the book, b
    If the user asks for invalid information, displays a message informing the user of such
    """
    if info_request == "genre":
        info_label = tkinter.Label(r, text=str(g.get_book_info(b, 'genre')))
    elif info_request == "author":
        info_label = tkinter.Label(r, text=str(g.get_book_info(b, 'author')))
    elif info_request == "pages":
        info_label = tkinter.Label(r, text=str(g.get_book_info(b, 'pages')))
    elif info_request == "summary":
        info_label = tkinter.Label(r, text=str(g.get_book_info(b, 'blurb')))
    elif info_request == "reviews":
        info_label = tkinter.Label(r, text=str(g.get_reviews_for_book(b)))
    elif info_request == "average rating":
        info_label = tkinter.Label(r, text=str(g.get_book_info(b, 'average_rating')))
    elif info_request == "general information":
        info_label = tkinter.Label(r, text=str(g.get_book_info(b, '')))
    else:
        info_label = tkinter.Label(r, text="That is not valid information to get!")

    info_label.bind('<Configure>', lambda _unused_item: info_label.config(wraplength=info_label.winfo_width()))
    info_label.pack()


def all_books(g: project2_part1.Graph, r: tkinter.Tk) -> Any:
    """
    Displays all the books in the dataset
    """
    books_label = tkinter.Label(r, text=str(g.get_all_items('book')))
    books_label.bind('<Configure>', lambda _unused_item: books_label.config(wraplength=books_label.winfo_width()))
    books_label.pack()


def all_users(g: project2_part1.Graph, r: tkinter.Tk) -> Any:
    """
    Displays all the user in the dataset
    """
    users_label = tkinter.Label(r, text=str(g.get_all_items('user')))
    users_label.bind('<Configure>', lambda _unused_item: users_label.config(wraplength=users_label.winfo_width()))
    users_label.pack()


def books_in_genre(g: project2_part1.Graph, r: tkinter.Tk) -> Any:
    """
    Displays a way to get the genre that the user wants all the books from
    """
    genre_get_label = tkinter.Label(r, text="Please enter what genre you would like to get books in:")
    genre_get_entry = tkinter.Entry(r, bg="#F3CEFF", borderwidth=5)
    genre_get_button = tkinter.Button(r, text='Submit', padx=50, fg="purple",
                                      command=lambda: b_in_g_output(g, str(genre_get_entry.get()), r))
    genre_get_label.bind('<Configure>',
                         lambda _unused_item: genre_get_label.config(wraplength=genre_get_label.winfo_width()))
    genre_get_label.pack()
    genre_get_entry.pack()
    genre_get_button.pack()


def b_in_g_output(g: project2_part1.Graph, genre: str, r: tkinter.Tk) -> Any:
    """
    Displays all the books in a specific genre
    If there are no books in the genre, displays an empty list
    """
    books_in_g_label = tkinter.Label(r, text=g.list_books_by_genre(genre))
    books_in_g_label.bind('<Configure>',
                          lambda _unused_item: books_in_g_label.config(
                              wraplength=books_in_g_label.winfo_width()))
    books_in_g_label.pack()


def books_read_by(g: project2_part1.Graph, r: tkinter.Tk) -> Any:
    """
    Displays a way to get the reviewer id of the person that the user wants their read books from
    and calls the function to get all those books
    """
    user_get_label = tkinter.Label(r, text="Please enter the reviewer:")
    user_get_entry = tkinter.Entry(r, bg="#F3CEFF", borderwidth=5)
    user_get_button = tkinter.Button(r, text='Submit', padx=50, fg="purple",
                                     command=lambda: user_book_reads(g, user_get_entry.get(), r))
    user_get_label.bind('<Configure>',
                        lambda _unused_item: user_get_label.config(wraplength=user_get_label.winfo_width()))
    user_get_label.pack()
    user_get_entry.pack()
    user_get_button.pack()


def user_book_reads(g: project2_part1.Graph, user_id: Any, r: tkinter.Tk) -> Any:
    """
    Displays all the books that the person, user_id, read
    If the person has not reviewed any books, display a message informing the user of such.
    """
    books_label = tkinter.Label(r, text=str(g.find_books_based_on_user_reads(user_id)))
    books_label.bind('<Configure>', lambda _unused_item: books_label.config(wraplength=books_label.winfo_width()))
    books_label.pack()


def books_by(g: project2_part1.Graph, r: tkinter.Tk) -> Any:
    """
    Displays a way to get the author that the user wants books by and calls the function to display those books
    """
    author_get_label = tkinter.Label(r, text="Please enter the name of the author:")
    author_get_entry = tkinter.Entry(r, bg="#F3CEFF", borderwidth=5)
    author_get_button = tkinter.Button(r, text='Submit', padx=50, fg="purple",
                                       command=books_by_output(g, str(author_get_entry.get()), r))
    author_get_label.bind('<Configure>',
                          lambda _unused_item: author_get_label.config(wraplength=author_get_label.winfo_width()))
    author_get_label.pack()
    author_get_entry.pack()
    author_get_button.pack()


def books_by_output(g: project2_part1.Graph, author: str, r: tkinter.Tk) -> Any:
    """
    Displays all the books that the author wrote
    """
    books_by_author_label = tkinter.Label(r, text=str(g.books_by_author(author)))
    books_by_author_label.bind('<Configure>',
                               lambda _unused_item: books_by_author_label.config(
                                   wraplength=books_by_author_label.winfo_width()))
    books_by_author_label.pack()


def book_rec(g: project2_part1.Graph, book_lst: set, r: tkinter.Tk) -> Any:
    """
    Displays a way to get all the books that the user wants to base a recommendation on and calls
    the function to display all the books that are recommended
    """
    book_get_label = tkinter.Label(r, text="Please enter the book title(s). If entering more than one book, "
                                           "please seperate each book with a #")
    book_get_entry = tkinter.Entry(r, bg="#F3CEFF", borderwidth=5)
    book_get_button = tkinter.Button(r, text='Submit', padx=100, fg="purple",
                                     command=lambda: books_rec_output(g, book_lst, str(book_get_entry.get()), r))
    book_get_label.bind('<Configure>', lambda _unused_item: book_get_label.config(
        wraplength=book_get_label.winfo_width()))
    book_get_label.pack()
    book_get_entry.pack()
    book_get_button.pack()


def books_rec_output(g: project2_part1.Graph, book_lst: set, books: str, r: tkinter.Tk) -> Any:
    """
    Displays all the recommended books based on the books in book_lst
    """
    books = books.split('#')
    books_valid = True
    for book in books:
        if book not in book_lst:
            books_valid = False
    if not books_valid:
        recommended_books_label = tkinter.Label(r, text="There are invalid books that you entered!")
    else:
        recommended_books_label = tkinter.Label(r, text=str(g.get_book_recommendations(books)))
    recommended_books_label.bind('<Configure>', lambda _unused_item: recommended_books_label.config(
        wraplength=recommended_books_label.winfo_width()))
    recommended_books_label.pack()


def most_popular(g: project2_part1.Graph, r: tkinter.Tk) -> Any:
    """
    Displays a way to get the number of popular books
    """
    num_books_label = tkinter.Label(r, text="Please enter the number of popular books you would like (up to 10): ")
    num_books_entry = tkinter.Entry(r, bg="#F3CEFF", borderwidth=5)
    num_books_button = tkinter.Button(r, text='Submit', padx=50, fg="purple",
                                      command=lambda: most_popular_with_num(g, int(num_books_entry.get()), r))
    num_books_label.bind('<Configure>', lambda _unused_item: num_books_label.config(
        wraplength=num_books_label.winfo_width()))
    num_books_label.pack()
    num_books_button.pack()
    num_books_button.pack()


def most_popular_with_num(g: project2_part1.Graph, num: int, r: tkinter.Tk) -> Any:
    """
    Displays num amount of the most popular books
    If num is greater than 10 or less than 1, then display a message informing the user that they have entered
    an invalid number of books.
    """
    if num <= 10 and num > 0:
        popular_books = tkinter.Label(r, text=str(g.most_popular_books(num)))
    else:
        popular_books = tkinter.Label(r, text="That is not a valid amount of books!!")
    popular_books.bind('<Configure>', lambda _unused_item: popular_books.config(wraplength=popular_books.winfo_width()))
    popular_books.pack()


if __name__ == '__main__':
    my_graph = project2_part1.load_graph('User testing file.csv', 'Book testing file.csv')

    root = tkinter.Tk()
    root.title("LitLabyrinth: Your Next Reading Adventure")

    # The menu for all the actions that the user can do
    menu = ["get information (information)", "books in genre", "all books", "all users",
            "find books read by (user)", "books by (author)", "book recommendations (book)", "most popular"]

    # a list of possible information that the user can request from a book
    possible_info = ["author", "genre", "pages", "summary", "reviews", "average rating", "general information"]

    book_set = my_graph.get_all_items('book')

    end = False
    menu_intro_label = tkinter.Label(root, text="Please select from these options: ")
    menu_label = tkinter.Label(root, text=str(menu))
    menu_clarification = tkinter.Label(root, text="CLARIFICATION: You do not have to and should not type "
                                                  "the part of the option that is in (). This is just so you know what "
                                                  "you may need to submit after typing in that choice!!")
    exit_clarification = tkinter.Label(root, text="To quit, click the red x in the top right. In other words, close all"
                                                  " windows to quit.")
    error_clarification = tkinter.Label(root, text="If blank windows pop up, please close these!! They are not windows "
                                                   "that you need to concern yourself with and they will not "
                                                   "impact your usage of this interface!")
    after_command_clarification = tkinter.Label(root, text="After every option you select, "
                                                           "feel free to close out the additional windows."
                                                           "The program should not quit entirely"
                                                           " unless you close out of this window!")

    menu_intro_label.bind('<Configure>',
                          lambda _unused_item: menu_intro_label.config(wraplength=menu_intro_label.winfo_width()))
    menu_label.bind('<Configure>', lambda _unused_item: menu_label.config(wraplength=menu_label.winfo_width()))
    menu_clarification.bind('<Configure>',
                            lambda _unused_item: menu_clarification.config(wraplength=menu_clarification.winfo_width()))
    exit_clarification.bind('<Configure>',
                            lambda _unused_item: exit_clarification.config(wraplength=exit_clarification.winfo_width()))
    error_clarification.bind('<Configure>',
                             lambda _unused_item: error_clarification.config(
                                 wraplength=error_clarification.winfo_width()))
    after_command_clarification.bind('<Configure>', lambda _unused_item: after_command_clarification.config(
        wraplength=after_command_clarification.winfo_width()))

    menu_intro_label.pack()
    menu_label.pack()
    menu_clarification.pack()
    exit_clarification.pack()
    error_clarification.pack()
    after_command_clarification.pack()

    e = tkinter.Entry(root, bg="#F3CEFF", borderwidth=5)
    e.pack()

    submit_button = tkinter.Button(root, text='Submit', padx=50, fg="purple",
                                   command=lambda: excute_choices(str(e.get()), book_set, possible_info, my_graph))
    submit_button.pack()

    root.mainloop()

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['sys', 'project2_part1', 'tkinter', 'networkx', 'typing'],
        'max-line-length': 120,
    })
