class Grid:
    def __init__(self, begin_x, begin_y, width, height, n_columns, n_rows):
        self.n_rows = n_rows
        self.n_columns = n_columns
        self.height = height
        self.width = width
        self.begin_y = begin_y
        self.begin_x = begin_x

        self.cells = [[[0, 0]] * n_columns] * n_rows

        self.delta_x = width / float(n_columns)
        self.delta_y = height / float(n_rows)

    def set(self, i, j, value):
        """
        Set value to grid.
        :param i: row
        :param j: column
        :param value: value
        """
        self.cells[i][j] = value

    def get(self, i, j):
        return self.cells[i][j]

    def cell_points(self, i, j):
        """
        Compute the bounding points of a cell.
        :param i: y
        :param j: x
        :return: four points.
        """
        p1 = (self.begin_x + j * self.delta_x, self.begin_y + i * self.delta_y)
        p2 = (self.begin_x + (j + 1) * self.delta_x, self.begin_y + i * self.delta_y)
        p3 = (self.begin_x + j * self.delta_x, self.begin_y + (i + 1) * self.delta_y)
        p4 = (self.begin_x + (j + 1) * self.delta_x, self.begin_y + (i + 1) * self.delta_y)

        return [p1, p2, p3, p4]

    def cell_center(self, i, j):
        """
        Get the center point of the cell
        :param i: y
        :param j: x
        :return: four points.
        """
        x = self.begin_x + j * self.delta_x + self.delta_x / 2.0
        y = self.begin_y + i * self.delta_y + self.delta_y / 2.0

        return x, y
