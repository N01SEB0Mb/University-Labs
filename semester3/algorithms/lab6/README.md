# Strings circular shifting

### Algorithm

Let `A` and `B` be given string and `N` - length of string

First, you calculate sum of chars:\
`s = A[1] + A[2] + ... + A[n]`

Then, you calculate positional sum of chars for `A` and `B`:\
`a = 1 * A[1] + 2 * A[2] + ... + N * A[N]`\
`b = 1 * B[1] + 2 * B[2] + ... + N * B[N]`

From other side, 'b' is shifted sum of 'A':\
`b = (1 + d) * A[1] + (2 + d) * A[2] + ... + (N + d) * A[N] - N * SF`
Where `SF` is sum of shifted chars:\
`SF = A[N + 1 - d] + A[N + 2 - d] + ... + A[N]`

It means that:\
`b - a = d * s - N * SF`

So you just iterate through possible shift values (`d: 1 -> N - 1`) and check if values are equal. If they are equal, that means that found shift value is correct

If none of possible shift values are matching, then `B` is not a shifted `A`

### Usage

Run program and follow instructions:
```
Type origin string: <Origin string>
Type shifted string: <String you want to check>
```

And you will get result.
 - If result == `-1`, that means that string is not shifted origin
 - If result >= `0`, that that means that result is shifting value of strings

### Examples

```
Type origin string:  abc
Type shifted string: cab
1
```

```
Type origin string:  abcabc
Type shifted string: bbcaac
-1
```

```
Type origin string:  351
Type shifted string: 351
0
```

```
Type origin string:  aaaaaaaaaabbbbbbbbbbbbcccccccccccccdddddddddddd
Type shifted string: bbbbbbbbbbbbcccccccccccccddddddddddddaaaaaaaaaa
37
```