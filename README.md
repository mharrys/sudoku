[![Build Status](https://travis-ci.org/mharrys/sudoku.svg?branch=master)](https://travis-ci.org/mharrys/sudoku)

# Sudoku solver using Dancing Links (DLX)
Sudoku can be reduced to a exact cover problem which is known to be
NP-complete. The classification of NP-complete is only for a generalized nxn
Sudoku and not a 9x9 Sudoku because it is a finite instance.

The exact cover problem is a decision problem where the objective is to find a
exact cover. Given a set S and another set where each element is a subset to
S, is is possible to select a set of subsets such that every element in S
exist in exactly one of the selected sets? This selection of sets is said to
be a cover of the set S.

Algorithm X (ALX) created by Donald Knuth can be used to find all solutions to
a exact cover problem. Dancing Links (DLX) is the technique suggested by
Knuth for implementing Algorithm X efficiently.

This solver implements the DLX algorithm as described by Knuth but the
reduction of a Sudoku to a exact cover problem is not truly a full reduction
because its reduced directly to the links used in DLX. The full reduction would
have been to first reduce the Sudoku to a binary matrix and then create the
links used in DLX. The only reason for this is gain in performance but it is
less flexible since this reduction can only be used with DLX.

## License
Licensed under GNU GPL v3.0.

## Installation
The solver depends on [numpy](http://www.numpy.org/) and can be installed as
described below with a virtual environment and pip or by installing [scipy](http://www.scipy.org/).
The second dependency [nose](https://nose.readthedocs.org/en/latest/) is only
required if you wish to run the test code.

Click [here](http://www.pip-installer.org/en/latest/index.html) for more
information on using pip and installing a virtual environment.

    $ virtualenv venv
    $ source venv/bin/activate
    (venv)$ pip install -r requirements.txt

## Run all tests

    (venv)$ nosetests

### Note on test data
There are tons of test data available in `tests/data/collections`, most
notably `all_17` which contains 49151 Sudoku challenges with 17 clues and
allegedly this is all possible challenges with 17 clues. Note that 17 clues
does not mean longest solving time. A second huge file  `random` contains
21460 different Sudoku challenges of varying (human) difficulty rating.
Specify `-v` to validate the solution and to search for more than one solution.

## Run
Show the argument options

    (venv)$ python sudoku.py -h
    Usage: sudoku.py [options]

    Options:
      -h, --help      show this help message and exit
      -v, --validate  validate solution (longer search time)
      -p, --pretty    pretty print solution

You can either provide the solver from stdin or by file. The input must be on
the following form

    .......12........3..23..4....18....5.6..7.8.......9.....85.....9...4.5..47...6...

each line represents a new Sudoku challenge. For instance

    $ python sudoku.py tests/data/platinum_blonde
    839465712146782953752391486391824675564173829287659341628537194913248567475916238

    $ python sudoku.py < tests/data/platinum_blonde
    839465712146782953752391486391824675564173829287659341628537194913248567475916238

    $ cat tests/data/platinum_blonde | python sudoku.py
    839465712146782953752391486391824675564173829287659341628537194913248567475916238

or on a more human readable form

    $ python sudoku.py --pretty tests/data/platinum_blonde
    +-------+-------+-------+
    | 8 3 9 | 4 6 5 | 7 1 2 |
    | 1 4 6 | 7 8 2 | 9 5 3 |
    | 7 5 2 | 3 9 1 | 4 8 6 |
    +-------+-------+-------+
    | 3 9 1 | 8 2 4 | 6 7 5 |
    | 5 6 4 | 1 7 3 | 8 2 9 |
    | 2 8 7 | 6 5 9 | 3 4 1 |
    +-------+-------+-------+
    | 6 2 8 | 5 3 7 | 1 9 4 |
    | 9 1 3 | 2 4 8 | 5 6 7 |
    | 4 7 5 | 9 1 6 | 2 3 8 |
    +-------+-------+-------+

or a file with multiple Sudoku challenges

    $ python sudoku.py tests/data/collections/hardest
    123456789457189236869273154271548693346921578985637412512394867698712345734865921
    129385764348627195765914823672491538483562971951738246894256317216873459537149682
    123456789457189236968327154249561873576938412831742695314275968695814327782693541
    128465379374219856956837142765198423249673581813542967592386714487921635631754298
    562987413471235689398146275236819754714653928859472361187324596923568147645791832
    751846239892371465643259871238197546974562318165438927319684752527913684486725193
    123456789457189236896372514249518367538647921671293845364925178715834692982761453
    125374896479618325683952714714269583532781649968435172891546237257893461346127958
    128396754495271638376845921689124375714539862253768419862457193547913286931682547
    839465712146782953752391486391824675564173829287659341628537194913248567475916238
    126395784359847162874621953985416237631972845247538691763184529418259376592763418

## References
1. Donald Knuth. Dancing links. Millenial Perspectives in Computer Science, pages 187–214, 2000.
