

class Cell(object):
    def __init__(self):
        self.value = '.'
        self.exclude = {}
        self.poss = {}
        self.fixed = False

    def __str__(self):
        return self.value

    def set(self, val, f=False):
        if self.fixed:
            raise "modify fixed"

        self.value = str(val)
        if val != '.':
            self.fixed = f

    def add_poss(self, v):
        v=str(v)
        if v not in self.poss:
            self.poss[v] = 'T'

    def add_excl(self, v):
        v = str(v)
        self.exclude[v] = 'T'

    def rem_poss(self, v):
        v = str(v)
        self.poss[v] = 'F'

    def possible(self, v):
        v = str(v)
        if v in self.poss:
            return self.poss[v] == 'T'
        return False

    def poss_list(self):
        out = []
        for p in self.poss:
            if self.poss[p] == 'T':
                out.append(p)
        return out


class Nine(object):
    def __init__(self, autoCreate=False):
        self.cells = []
        if autoCreate:
            self._auto_create()

    def _auto_create(self):
        for i in range(9):
            self.cells.append(Cell())

    # Must be called in sequential order
    def init(self, c):
        self.cells.append(c)

    def populate(self, r):
        cell_num=0
        for c in r:
            self.cells[cell_num].set(c, True)
            cell_num += 1

    def cell(self, n):
        return self.cells[n]

    def __str__(self):
        q = list(map(lambda x: str(x), self.cells))
        return str(q)

    def contains(self, n):
        n = str(n)
        for c in self.cells:
            if c.value == n:
                return True
        return False

    def get_poss(self):
        for rows in range(3):
            outr = []
            for c in self.cells:
                for n in range(rows*3+1,rows*3+3+1):
                    if c.possible(n):
                        outr.append(str(n))
                    else:
                        outr.append('.')
                outr.append(' ')
            outr.append('\n')
        return ''.join(outr)


class Square(Nine):
    def __init__(self, autoCreate=False):
        super().__init__(autoCreate)

class Col(Nine):
    def __init__(self, autoCreate=False):
        super().__init__(autoCreate)

class Row(Nine):
    def __init__(self, autoCreate=False):
        super().__init__(autoCreate)

class Board(object):
    def __init__(self):
        self.rows = []
        self.cols = []
        self.squares = []
        for i in range(9):
            self.rows.append(Row(True))

        for i in range(9):
            c = Col()
            for n in range(9):
                c.init(self.rows[n].cells[i])
            self.cols.append(c)

        for n in range(9):
            s = Square()
            c = n % 3
            r = int(n / 3)*3
            for n in range(3):
                s.init(self.rows[r].cells[(c*3)+n])
            for n in range(3):
                s.init(self.rows[r+1].cells[(c*3)+n])
            for n in range(3):
                s.init(self.rows[r+2].cells[(c*3)+n])
            self.squares.append(s)

    def populate(self, b):
        row_num = 0
        for r in b:
            self.rows[row_num].populate(r)
            row_num += 1

    def row(self, n):
        return self.rows[n]

    def col(self, n):
        return self.cols[n]

    def square(self, n):
        return self.squares[n]

    def __str__(self):
        out = []
        row_count = 0
        for r in self.rows:
            col_count = 0
            for c in r.cells:
                out.append(str(c))
                col_count += 1
                if col_count == 3:
                    out.append(' ')
                    col_count = 0
            row_count += 1
            if row_count == 3:
                out.append('\n')
                row_count = 0

            out.append('\n')
        return ''.join(out)

    def print_possibles(self):
        for r in self.rows:
            print(r.get_poss())
            print("\n")


b1 = ['123456789',
      'abcdefghi',
      'ABCDEFGHI',

      'jklmnopqr',
      'JKLMNOPQR',
      '!"p$%^&*('

      'stuvwxyz#',
      'STUVWXYZ~',
      '[]{};;@,.']


b2 = ['85.6...7.',
      '.91.7.8.6',
      '7.6.....3',

      '.1..3..92',
      '..2..73.8',
      '.8....51.',

      '57....6.9',
      '1..2.5..7',
      '.3.7.91..']

b3 = ['3......27',
      '8.72.9...',
      '.....7...',

      '.........',
      '6..87...5',
      '12..6..8.',

      '..4......',
      '.38.92...',
      '....5..31']

def quick_check(q):
    for c in q.cells:
        if c.value == '.':
            for n in range(1, 10):
                if not q.contains(n):
                    c.add_poss(n)
                else:
                    c.rem_poss(n)
                    c.add_excl(n)


def quick_eval(q):
    changed_count = 0
    for c in q.cells:
        if c.value == '.':
            pl = c.poss_list()
            if len(pl) == 1:
                for z in pl:
                    c.set(z)
                    changed_count += 1
    return changed_count


def main():
    board = Board()

    # board.populate(b1)
    # print(board.row(1))
    # print(board.col(2))
    # print(board.square(2))
    # print(board.square(8))
    # print(board)

    board.populate(b3)
    print(board)


    count = 0
    ch = 1
    while ch != 0:
        count += 1
        for r in board.rows:
            quick_check(r)

        for c in board.cols:
            quick_check(c)

        for s in board.squares:
            quick_check(s)

        ch = 0
        for r in board.rows:
            ch += quick_eval(r)

    print(board)
    print(count)

    board.print_possibles()

main()


