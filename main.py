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
import sys
from project2_part1 import Graph
import doctest

if __name__ == '__main__':

    # The menu for all the actions that the user can do
    menu = ["get information (information)", "books in genre", "all books", "all users",
            "find books read by (user)", "similar (genre) (book1) (book2)", "books by (author)",
            "book recommendations (book)", "highest similar (book) (number)", "most popular", "quit"]

    # a list of possible information that the user can request from a book
    possible_info = ["author", "genre", "pages", "summary", "reviews", "average rating", "general information"]

    book_list = []

    end = True

    # prompts the user to select a choise
    while not end:
        print("What to do? \n")
        print("[menu]")
        for action in menu:
            print(action)
        choice = input("\nEnter action: ")

        if choice == "[menu]":
            print("Menu Options: \n")
            for option in menu:
                print(option)
            choice = input("\nChoose action: ")
        elif choice == "get information":

            book = input("Enter the book title: ")
            if book not in book_list:
                print("That is not a valid book!")

            print("Possible information that can be requested: \n")
            for info in possible_info:
                print(info)
            wanted_info = input("\nEnter what you would like: ")

            if wanted_info == "genre":
                ...
            elif wanted_info == "author":
                ...
            elif wanted_info == "pages":
                ...
            elif wanted_info == "summary":
                ...
            elif wanted_info == "reviews":
                ...
            elif wanted_info == "average rating":
                ...
            elif wanted_info == "general information":
                ...
            else:
                print("That is not valid information to get!")
        elif choice == "all books":
            ...
        elif choice == "all users":
            ...
        elif choice == "books in":

            genre = input("\nEnter genre:")
            if not ...:
                print("There is no books of that genre!")
            else:
                ...
        elif choice == "books by":

            author = input("\nEnter author: ")
            if not ...:
                print("That person has not written any of the books we have!")
            else:
                ...
        elif choice == "books read by":
            user = input("\n Enter the user id of the user: ")
            ...
        elif choice == "similar":

            book_one = input("\nEnter the first book: ")
            if book_one not in book_list:
                print("That is not a valid book!")

            book_two = input("\nEnter the second book: ")
            if book_two not in book_list:
                print("That is not a valid book!")
            ...
        elif choice == "book recommendations":
            book = input("Enter the book title: ")
            if book not in book_list:
                print("That is not a valid book!")
            ...
        elif choice == "highest similar":
            book = input("\nEnter the book title:")
            if book not in book_list:
                print("That is not a valid book!")
            ...
        elif choice == "most popular":
            ...
        elif choice == "quit":
            end = True
            sys.exit("Thank you for using our services! Hope you have a novel day!")
        else:
            print("That is not a valid action!")

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
    })
