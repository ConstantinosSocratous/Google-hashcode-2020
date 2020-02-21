
import numpy as np
import operator

INPUT = "a"

GAMMA = 0.0


class Library:
    
    def __init__(self, id, books, days_signup, ship_per_day):
        self.id = id
        self.books = books
        self.signup = False
        self.days_signup = days_signup
        self.ship_per_day = ship_per_day


file = open(INPUT + ".txt", "r")

f_line = file.readline().replace("\n","").split(' ')
num_books, num_libraries, num_days = int(f_line[0]), int(f_line[1]), int(f_line[2])


s_line = file.readline().replace("\n","").split(' ')
books_id = []
books_score = []
books_scanned = []
for i,score in enumerate(s_line):
    books_id.append(i)
    books_score.append(int(score))
    books_scanned.append(False)


lst = [line.replace("\n", "").split(" ") for line in file.readlines()]

libraries = []
heuristics = {}
i=0
while i < (num_libraries * 2):
    
    num_of_books = int(lst[i][0])
    signup_days = int( lst[i][1])
    ship_per_day = int(lst[i][2])
    i+=1

    books_in_lib = [int(x) for x in lst[i]]

    if i != 0:
        lib_id = i/2
    else:
        lib_id = 0

    books_not_scanned_in_lib = 0
    for b in books_in_lib:
        if books_scanned[b] is False:
            books_not_scanned_in_lib += 1

    h = - signup_days# * ship_per_day
    heuristics[lib_id] = h
    libraries.append(Library(lib_id, books_in_lib,signup_days,ship_per_day))

    i+=1

# print heuristics
#OUTPUTS
libraries_signups = []
shippments = {}
######

# print heuristics
is_signing = False
day_started_signup = 0
day_stop_signup = 0
library_signing = None
for day in range(num_days):
    # print day
    if day == day_stop_signup and library_signing is not None:
        is_signing = False
        day_started_signup = 0
        day_stop_signup = 0

        # print "Library", library_signing, "finished sign up at day", day

        libraries_signups.append(library_signing)
        libraries[library_signing].signup = True

        del heuristics[library_signing]
        library_signing = None

        
    if not is_signing and len(heuristics) > 0:
        library_signing = max(heuristics.iteritems(), key=operator.itemgetter(1))[0]
        is_signing = True
        day_started_signup = day
        day_stop_signup = libraries[library_signing].days_signup + day_started_signup

        # print "Library", library_signing, "starting sign up at day", day

    for library in libraries:
        if library.signup == False:
            continue

        potential_books_to_ship = {}
        for book in library.books:
            if books_scanned[book]:
                continue
                    
            if potential_books_to_ship.get(book) == None:
                potential_books_to_ship[book] = []
            potential_books_to_ship[book] = books_score[book]


        for shipment in range(library.ship_per_day):    
            if len(potential_books_to_ship) > 0:
                max_score_book = max(potential_books_to_ship.iteritems(), key=operator.itemgetter(1))[0]

                #SHIP BOOK BRO
                if shippments.get(library.id) == None:
                    shippments[library.id] = []
                shippments[library.id].append(max_score_book)
                books_scanned[max_score_book] = True

                # print "Library", library.id, "sending book", max_score_book,\
                #     "at day", day
                
                del potential_books_to_ship[max_score_book]
            # else:
            #     break

        # # Update heuristics
        if heuristics.get(library.id) is not None:
            books_not_scanned_in_lib = 0
            for b in library.books:
                if books_scanned[b] is False:
                    books_not_scanned_in_lib += 1
            h = - library.days_signup + float(books_not_scanned_in_lib)/float(library.books)*100 #* library.ship_per_day + books_not_scanned_in_lib
            heuristics[library.id] = h



output_file = open(INPUT  + "OUTPUT.txt", "w")
output_file.write(str(len(libraries_signups)) + "\n")

for lib in libraries_signups:
    output_file.write(str(lib) + " " + str(len(shippments[lib])) + "\n")

    [output_file.write(str(b) + " ") for b in shippments[lib]]
    output_file.write("\n")


file.close()

output_file.close()
