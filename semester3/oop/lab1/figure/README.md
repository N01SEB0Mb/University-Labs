# Function shapes

This program calculates area of figures*,
that are given by the one function (between function graph and X-axis)
or two functions (between function graphs)

_*You need to manualy select left and right boundaries_

## Description

### Expression

[_**`Expression`**_](https://github.com/no1sebomb/University-Labs/blob/master/semester3/oop/lab1/figure/figure/expression/function.py#L17) class used to parse and store expressions.

It contains binary tree of operation nodes ([_**`ExpressionNode`**_](https://github.com/no1sebomb/University-Labs/blob/master/semester3/oop/lab1/figure/figure/expression/node.py#L16) class),
where value of node could be:
 - _`Callable`_ (node childrens is function arguments)
 - _`Float`_ (Constant value)
 - _`Bool`_ (Argument: positive if _`True`_, negative if _`False`_)
 
[_**`Expression`**_](https://github.com/no1sebomb/University-Labs/blob/master/semester3/oop/lab1/figure/figure/expression/function.py#L17) object must be initialized using string with expression

##### Examples:
```python
# Default function
Expression("x + sin(x - 5)")

# Lot of parentheses
Expression("x + (x + (x + (x - x)))")

# Other argument name
Expression("z - 5", argumentName="z")

# Constant function: f(x) = -3
Expression("-3")
```

If expression is invalid, it raises [_**`ExpressionError`**_](https://github.com/no1sebomb/University-Labs/blob/master/semester3/oop/lab1/figure/figure/expression/exceptions.py#L9)

After [_**`Expression`**_](https://github.com/no1sebomb/University-Labs/blob/master/semester3/oop/lab1/figure/figure/expression/function.py#L17) object was created, you can call it like a function*:
```python
squareFunc = Expression("x^2")

print(squareFunc(4))  # Prints '16.0'
print(squareFunc(-1.5))  # Prints '2.25'
```

*Accepts only [_**`Number`**_](https://github.com/no1sebomb/University-Labs/blob/master/semester3/oop/lab1/figure/figure/expression/number.py#L9) argument type (_`int`_ or _`float`_)

##### Supported operations:
 - **_a + b_** ([_**`addition`**_](https://github.com/no1sebomb/University-Labs/blob/master/semester3/oop/lab1/figure/figure/expression/operations.py#L19))
 - **_a - b_** ([_**`subtract`**_](https://github.com/no1sebomb/University-Labs/blob/master/semester3/oop/lab1/figure/figure/expression/operations.py#L38))
 - **_a * b_** ([_**`multiply`**_](https://github.com/no1sebomb/University-Labs/blob/master/semester3/oop/lab1/figure/figure/expression/operations.py#L58))
 - **_a / b_** ([_**`division`**_](https://github.com/no1sebomb/University-Labs/blob/master/semester3/oop/lab1/figure/figure/expression/operations.py#L77))
 - **_a % b_** ([_**`mod`**_](https://github.com/no1sebomb/University-Labs/blob/master/semester3/oop/lab1/figure/figure/expression/operations.py#L97))
 - **_a ^ b_** ([_**`power`**_](https://github.com/no1sebomb/University-Labs/blob/master/semester3/oop/lab1/figure/figure/expression/operations.py#L117))
 
##### Supported functions:
 - **_sin(a)_** ([_**`sin`**_](https://github.com/no1sebomb/University-Labs/blob/master/semester3/oop/lab1/figure/figure/expression/operations.py#L154))
 - **_cos(a)_** ([_**`cos`**_](https://github.com/no1sebomb/University-Labs/blob/master/semester3/oop/lab1/figure/figure/expression/operations.py#L168))
 - **_tan(a)_** ([_**`tan`**_](https://github.com/no1sebomb/University-Labs/blob/master/semester3/oop/lab1/figure/figure/expression/operations.py#L182))
 - **_cotan(a)_** ([_**`cotan`**_](https://github.com/no1sebomb/University-Labs/blob/master/semester3/oop/lab1/figure/figure/expression/operations.py#L196))
 - **_asin(a)_** ([_**`asin`**_](https://github.com/no1sebomb/University-Labs/blob/master/semester3/oop/lab1/figure/figure/expression/operations.py#L210))
 - **_acos(a)_** ([_**`acos`**_](https://github.com/no1sebomb/University-Labs/blob/master/semester3/oop/lab1/figure/figure/expression/operations.py#L224))
 - **_sqrt(a)_** ([_**`sqrt`**_](https://github.com/no1sebomb/University-Labs/blob/master/semester3/oop/lab1/figure/figure/expression/operations.py#L238))
 - **_ceil(a)_** ([_**`ceil`**_](https://github.com/no1sebomb/University-Labs/blob/master/semester3/oop/lab1/figure/figure/expression/operations.py#L252))
 - **_floor(a)_** ([_**`floor`**_](https://github.com/no1sebomb/University-Labs/blob/master/semester3/oop/lab1/figure/figure/expression/operations.py#L266))
 
You can add you own operation/function. Just add your method to class [_**`Operation`**_](https://github.com/no1sebomb/University-Labs/blob/master/semester3/oop/lab1/figure/figure/expression/operations.py#L13):
 - Method must accepts one argument (function) or few arguments (operation)
 - You should decorate it with [_**`@staticmethod`**_](https://github.com/no1sebomb/University-Labs/blob/master/semester3/oop/lab1/figure/figure/expression/decorator.py#L9) decorator (it is custom decorator)
 - Decorator parameters should be string with operation/function name (used in parsing)
 - If operation is not prior, like addition (function performs prior operations firsly, for example, multiplication instead of addition), you should set decorator parameter `prior=False`
 
### Functions

You can implement shape using two ways:
 - Between function graph and X-axis: [_**`AxisFigure`**_](https://github.com/no1sebomb/University-Labs/blob/master/semester3/oop/lab1/figure/figure/axisfigure.py#L8)
 - Between two function graphs: [_**`Figure`**_](https://github.com/no1sebomb/University-Labs/blob/master/semester3/oop/lab1/figure/figure/figure.py#L7)
 
Shapes must be initialized using [_**`Expression`**_](https://github.com/no1sebomb/University-Labs/blob/master/semester3/oop/lab1/figure/figure/expression/function.py#L17) instance
(one expression for [_**`AxisFigure`**_](https://github.com/no1sebomb/University-Labs/blob/master/semester3/oop/lab1/figure/figure/axisfigure.py#L8) and two expressions for [_**`Figure`**_](https://github.com/no1sebomb/University-Labs/blob/master/semester3/oop/lab1/figure/figure/figure.py#L7))

You can get / set / delete shape functions using _`.first`_ and _`.second`_ property

Figure has 2 methods:
 - height(x): Returns distance between first and second function at given x value
 - area(start, end, parts=1000): Calculates shape area (from start to end values) by dividing it into given number of parts

Examples:
```python
# Create expressions
first = Expression("x + 3")
second = Expression("sin(x - 5) - 1")

# Create figure
figure = Figure(first, second)

# Calculate area
area = figure.area(-1, 5)
```

## Using

You can use CLI ([_cli.py_](https://github.com/no1sebomb/University-Labs/blob/master/semester3/oop/lab1/figure/cli.py))

Simply run this command:
```
$ python3 cli.py
```

And run following commands.

Enter first function:
```
Type first expression: f(x) = <type expression>
```

Enter second function (or press `<Enter>` to use [_**`AxisFigure`**_](https://github.com/no1sebomb/University-Labs/blob/master/semester3/oop/lab1/figure/figure/axisfigure.py#L8)):
```
Type second expression (Or press <Enter> to create Axis Figure): g(x) = <type expression or press <Enter>>
```

Select area's start and end value:
```
Type shape start and end x: <Select start> <And end>
```

And you will get your area

Note - 
[_cli.py_](https://github.com/no1sebomb/University-Labs/blob/master/semester3/oop/lab1/figure/cli.py) uses multiprocessing to calculate area.

You can configurate parameters in [_config.json_](https://github.com/no1sebomb/University-Labs/blob/master/semester3/oop/lab1/figure/config.json) settings file:
 - `maxRecursionLimit`: n - Max limit of recursion in Python 3. It means that you are limiting binary-tree depth by n (Only less than 2^n operations and operators per exprssion could exists)
 - `parts`: p - Number of parts you want to use
 - `processes`: m - Number of processes you want to use (It divides shape by m processes, so final partition is m * p instead of p)
 