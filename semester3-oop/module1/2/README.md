### Solution of task using Python3

Solution defined using 3 different methods:
 * **CalcFunc** ([_func.py_](https://github.com/no1sebomb/University-Labs/blob/master/semester3-oop/module1/2/calculate/func.py)):
 default python function using dict with variants,
 that is more compact, unlike `if/elif/else` condions.
 Dict keys are lambda-funcs that checks if `x` suits to condition of types.
 Dict values are lambda-funcs with result of calculations for every type.
    * Pluses:
        1. Less memory usage
        2. Less code
        3. Better type checking construction
    * Minuses:
        1. Less versatility
 * **CalcCall** ([_call.py_](https://github.com/no1sebomb/University-Labs/blob/master/semester3-oop/module1/2/calculate/call.py)):
 python class with `__call__` method.
 Unlike CalcFunc, uses different method for every `x` type.
 Inherits [`CalculatorABC`](https://github.com/no1sebomb/University-Labs/blob/master/semester3-oop/module1/2/calculate/basecalc.py#L28) class with defined method for most of types.
 Checking of type is realised using `try/except` construction:
 If `x` type is not suits method type, it raises [`CalculatorTypeError`](https://github.com/no1sebomb/University-Labs/blob/master/semester3-oop/module1/2/calculate/basecalc.py#L10).
 Object looping over all it's methods until succeed (No exception raised).
    * Pluses
        1. More versatility
        2. Different methods for every type
    * Minuses
        1. More code
        2. More memory
        3. First you need to create CalcCall instance, then you should call it
 * **CalcNew** ([_new.py_](https://github.com/no1sebomb/University-Labs/blob/master/semester3-oop/module1/2/calculate/new.py)):
 python class similar to previous, but it simulates function using `__new__` method:
 This method is constructor that returns new object instance, but this class returns calculation answer.
    * Pluses
        1. More versatility
        2. Different methods for every type
        3. You don't need to create object instance
    * Minuses:
        1. More code
        2. More memory
        3. Strange and unwanted usage of OOP
        
This solutions are defined in [calculate](https://github.com/no1sebomb/University-Labs/tree/master/semester3-oop/module1/2/calculate) package.

### Usage

Run following command:

`$ python3 run.py`

And follow instructions in the console:

`Type value to calculate or <Enter> to exit: <Type your value*>`

*Value must follow Python 3 syntax.
Pair type is tuple with 2 elements.

Get the result:

```
CalcFunc(<your value>) = <result>
CalcCall(<your value>) = <result>
CalcNew(<your value>)  = <result>
```

Program works in infinite loop, so you can test it until you get bored.
Whenever you want to exit, just click `<Enter>`

### Examples

```
Type value to calculate or <Enter> to exit: 3.
CalcFunc(3.0) = 8.0
CalcCall(3.0) = 8.0
CalcNew(3.0)  = 8.0

Type value to calculate or <Enter> to exit: -5
CalcFunc(-5) = 116
CalcCall(-5) = 116
CalcNew(-5)  = 116

Type value to calculate or <Enter> to exit: 'ABcCb'
CalcFunc(ABcCb) = 3
CalcCall(ABcCb) = 3
CalcNew(ABcCb)  = 3

Type value to calculate or <Enter> to exit: [7, [8, 9]]
CalcFunc([7, [8, 9]]) = 207
CalcCall([7, [8, 9]]) = 207
CalcNew([7, [8, 9]])  = 207

Type value to calculate or <Enter> to exit: (8, 8)
CalcFunc((8, 8)) = 2
CalcCall((8, 8)) = 2
CalcNew((8, 8))  = 2

Type value to calculate or <Enter> to exit: {1: 2}
CalcFunc({1: 2}) = 8941
CalcCall({1: 2}) = 8941
CalcNew({1: 2})  = 8941

Type value to calculate or <Enter> to exit: 

Process finished with exit code 0

```

<img src="https://media1.tenor.com/images/2f5c3a840c4ce399bd93f3990c203b6b/tenor.gif"/>
