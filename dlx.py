from numpy import inf


class DataObject(object):
    """Describes a data object in the Dancing Links algorithm.
    """

    def __init__(self, C, ID):
        self.C = C     # head column object
        self.ID = ID   # symbolic name
        self.U = self  # up
        self.D = self  # down
        self.L = self  # left
        self.R = self  # right


class ColumnObject(DataObject):
    """Describes a column object in the Dancing Links algorithm.
    """

    def __init__(self, ID):
        DataObject.__init__(self, self, ID)
        self.S = 0


class DLX(object):
    """Solves exact cover problems using the Dancing Links algorithm.
    """

    def __init__(self, h, callback):
        """Create links from specfied root node h and solution callback.
        """
        self.h = h
        self.callback = callback

    @classmethod
    def from_matrix(cls, M, callback):
        """Create links from specified binary matrix (numpy array). Callback
        is called when a solution is found.

        For a mxn matrix.
        O(n + m + n) = O(2n + m) ~ O(max(n, m))

        """
        rows, cols = M.shape
        # root
        h = ColumnObject('h')
        # create column objects
        for col in range(cols):
            c = ColumnObject(col)
            # last column object wraps to root
            c.R = h
            # swap current last column object with this column object
            c.L = h.L
            h.L.R = c
            h.L = c
        # create data objects
        for row in range(rows):
            # for every new row, begin at the first non-root column
            c = h.R
            # first data object for this row
            first = None
            for col in range(cols):
                cell = M[row][col]
                # only positive numbers are of interest
                if cell > 0:
                    d = DataObject(c, row)
                    # adjust size for added data object
                    c.S += 1
                    # last data object wraps to column object
                    d.D = c
                    # swap current last data object with this data object
                    d.U = c.U
                    c.U.D = d
                    c.U = d
                    # link rows
                    if first:
                        d.L = first.L
                        d.R = first
                        first.L.R = d
                        first.L = d
                    else:
                        first = d
                c = c.R  # next

        return cls(h, callback)

    @classmethod
    def from_sudoku(cls, grid, callback):
        """Create links from specified 9x9 grid (numpy array). Callback is
        called when a solution is found.

        Skip the step of reducing the sudoku to a binary matrix and instead
        create the links directly from the grid. This is achieved by storing
        the column objects in a array so that each column object can be
        accessed in O(1). Since each column object always has a reference to
        the last row element, we can always quickly append new row elements by
        using said array.

        """
        cols = []
        # root
        h = ColumnObject('h')
        # create column objects and store them all in the array
        for col in range(324):
            c = ColumnObject(col)
            # last column object wraps to root
            c.R = h
            # swap current last column object with this column object
            c.L = h.L
            h.L.R = c
            h.L = c
            cols.append(c)
        # define column position for our constraints
        pos_constraint = lambda x, y, k: x * 9 + y
        row_constraint = lambda x, y, k: 81 + x * 9 + k
        col_constraint = lambda x, y, k: 162 + y * 9 + k
        box_constraint = lambda x, y, k: 243 + (3 * (x / 3) + y / 3) * 9 + k
        row_num = lambda x, y, k: x * 81 + y * 9 + k

        def link_rows(a, b, c, d):
            """Helper function for linking row elements a,b,c and d together.
            """
            a.R = b
            b.R = c
            c.R = d
            d.R = a
            a.L = d
            d.L = c
            c.L = b
            b.L = a

        def link_row_to_column(d):
            """Helper function for linking row element to its column.
            """
            c = d.C
            c.S += 1
            # last data object wraps to column object
            d.D = c
            # swap current last data object with this data obejct
            d.U = c.U
            c.U.D = d
            c.U = d

        def create_links(x, y, k):
            """Helper function for creating links from specified row.
            """
            # create row link
            pos = DataObject(cols[pos_constraint(x, y, k)], row_num(x, y, k))
            row = DataObject(cols[row_constraint(x, y, k)], row_num(x, y, k))
            col = DataObject(cols[col_constraint(x, y, k)], row_num(x, y, k))
            box = DataObject(cols[box_constraint(x, y, k)], row_num(x, y, k))
            # create links for entire row
            link_rows(pos, row, col, box)
            # insert links to correct column
            link_row_to_column(pos)
            link_row_to_column(row)
            link_row_to_column(col)
            link_row_to_column(box)

        # create data objects
        for x in range(9):
            for y in range(9):
                if grid[x][y] == 0:
                    # add all possible rows
                    for k in range(9):
                        create_links(x, y, k)
                else:
                    # given clue
                    k = grid[x][y] - 1  # zero-based
                    create_links(x, y, k)
        return cls(h, callback)

    def cover(self, c):
        """Cover specified column c.

        Removes c from the header list and removes all rows in the list of c
        from the other column lists they are in.

        """
        c.R.L = c.L
        c.L.R = c.R
        i = c.D
        while i != c:
            j = i.R
            while j != i:
                j.D.U = j.U
                j.U.D = j.D
                j.C.S -= 1
                j = j.R  # next column
            i = i.D  # next row

    def uncover(self, c):
        """Uncover specified column c.
        """
        i = c.U
        while i != c:
            j = i.L
            while j != i:
                j.C.S += 1
                j.D.U = j
                j.U.D = j
                j = j.L  # next column
            i = i.U  # next row
        c.R.L = c
        c.L.R = c

    def choose_column_object(self):
        """Return choosen column object.

        The first column with fewest number of 1s is chosen, this will
        minimize the branching factor.

        """
        c = None
        s = inf
        j = self.h.R
        while j != self.h:
            if j.S < s:
                c = j
                s = j.S
            j = j.R  # next column
        return c

    def search(self, s):
        """Search for a exact cover solution from links specified in list s.
        """
        if not self.find_all and self.solutions > 0:
            return

        if self.h == self.h.R:
            # one possible solution found
            self.solutions += 1
            self.callback(self.solutions, s)
            return
        else:
            c = self.choose_column_object()
            self.cover(c)

            # for each row in this column
            r = c.D
            while r != c:
                s.append(r)
                # for each column on this row
                j = r.R
                while j != r:
                    self.cover(j.C)
                    j = j.R  # next column

                self.search(s)

                r = s.pop()
                c = r.C
                # for each column on this row
                j = r.L
                while j != r:
                    self.uncover(j.C)
                    j = j.L  # next column
                r = r.D  # next row
            self.uncover(c)
            return

    def run(self, find_all):
        # we only perform a search if there is at least one column object
        if self.h != self.h.R:
            self.solutions = 0
            self.find_all = find_all
            self.search([])
