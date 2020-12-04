# coding=utf-8

from typing import Optional, Union, List

Number = Union[int, float]
isNum = lambda value: isinstance(value, int) or isinstance(value, float)


class Stats:
    __slots__ = [
        "__table",
        "__width", "__height",
        "__rows", "__columns"
    ]

    YATES_CORRECTION = 0.5

    def __init__(
            self,
            table: List[List[Number]],
            rows: Optional[List[str]] = None,
            columns: Optional[List[str]] = None
    ) -> None:
        """
        __init__ method override. Initializes Stats object

        Args:
            table (List[List[Number]]): Stats table
            rows (Optional[List[str]]): Name of rows
            columns (Optional[List[str]]): Name of columns

        Raises:
            TypeError: If invalid 'table' argument given
            TypeError: If invalid 'rows'/'columns' argument type
            ValueError: If number of columns does not match
            ValueError: If 'rows'/'columns' argument length does not match table sizes
            ValueError: If invalid 'rows'/'columns' argument given
        """

        if not isinstance(table, List):  # If table is not a list
            raise TypeError("Wrong table type")
        elif not table:  # If table is empty
            raise TypeError("Empty table given")

        # Table sizes
        self.__width = None
        self.__height = len(table)

        # Check types and sizes
        for row in table:
            if self.__width is None:
                self.__width = len(row)
            else:
                if self.__width != len(row):
                    raise ValueError("Invalid table format")

            if not all(map(isNum, row)):
                raise TypeError("Wrong table values given")

        self.__table = table

        # Rows name
        if isinstance(rows, List):
            if all(map(lambda row: isinstance(row, str), rows)) and len(rows) == self.__height:
                self.__rows = rows
            else:
                raise ValueError("Wrong rows given")
        elif rows is None:
            self.__rows = [chr(97 + number % 26) * (number // 26) for number in range(self.__height)]
        else:
            raise TypeError("Wrong rows type")

        # Columns name
        if isinstance(columns, List):
            if all(map(lambda column: isinstance(column, str), columns)) and len(columns) == self.__width:
                self.__columns = columns
            else:
                raise ValueError("Wrong columns given")
        elif columns is None:
            self.__columns = [chr(65 + number % 26) * (number // 26) for number in range(self.__width)]
        else:
            raise TypeError("Wrong columns type")

    def expected(self) -> 'Stats':
        """
        Get expected stats

        Returns:
            Stats: expected stats
        """

        # Calculate totals of each row and column
        totalColumn = [sum(row) for row in self.__table]
        totalRow = [0] * self.__width
        total = sum(totalColumn)

        # Calculate totalRow
        for row in self.__table:
            for index, number in enumerate(row):
                totalRow[index] += number

        # Generate average values
        return Stats(
            [[row * column / total for column in totalRow] for row in totalColumn],
            rows=self.__rows,
            columns=self.__columns
        )

    def ChiSquare(
            self,
            yatesCorrection: Optional[bool] = False
    ) -> float:
        """
        Chi-squared test

        Args:
            yatesCorrection (Optional[bool]): Yates correction

        Returns:
            float: Chi-square test
        """

        expectedTable = self.expected().table
        correction = self.YATES_CORRECTION if yatesCorrection else 0.0

        result = 0.0

        # Summands
        for rowNumber in range(self.__height):
            for rowColumn in range(self.__width):
                tableValue = self.__table[rowNumber][rowColumn]
                expectedValue = expectedTable[rowNumber][rowColumn]

                result += (abs(tableValue - expectedValue) - correction) ** 2 / expectedValue

        return result

    @property
    def table(self) -> List[List[Number]]:
        """
        Get table

        Returns:
            List[List[Number]]: Return table
        """

        return self.__table

    @property
    def width(self) -> int:
        """
        Get table width

        Returns:
            int: Table width
        """

        return self.__width

    @property
    def height(self) -> int:
        """
        Get table height

        Returns:
            int: Table height
        """

        return self.__height

    def __str__(self) -> str:
        """
        __str__ method override. Used to convert object to str

        Returns:
            str: Formatted table
        """

        def genRows():
            def getNumbers(row):
                for numberIndex, numberValue in enumerate(row):
                    numberStr = "%.3f" % numberValue
                    yield numberStr + " " * (maxColumns[numberIndex] - len(numberStr))

            for row in self.__table:
                yield " ".join(getNumbers(row))

        maxColumns = [0] * self.__width

        for row in self.__table:
            for columnNumber, columnValue in enumerate(row):
                if maxColumns[columnNumber] < len("%.3f" % columnValue):
                    maxColumns[columnNumber] = len("%.3f" % columnValue)

        return "\n".join(genRows())
