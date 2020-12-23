# Strings circular shifting

### Algorithm

Let `A` and `B` be given string and `N` - length of string

Choose `p` value for hashing

You calculate positional sum of chars for `A` and `B`:\
`a = p ^ 1 * A[1] + p ^ 2 * A[2] + ... + p ^ N * A[N]`\
`b = p ^ 1 * B[1] + p ^ 2 * B[2] + ... + p ^ N * B[N]`

From other side, if `B` is shifted `A` then `b` is shifted sum of `A`:\
`b = p ^ (1 + d) * A[1] + p ^ (2 + d) * A[2] + ... + p ^ (N + d) - p ^ N * SF`
where `SF` is sum of shifted chars:\
`SF = p ^ N * (A[N + 1 - d] + A[N + 2 - d] + ... + A[N]`)

It means that:\
`b = p ^ d * a - SF`

So you just iterate through possible shift values (`d: 1 -> N - 1`) and check if values are equal. If they are equal, that means that found shift value is correct

If none of possible shift values are matching, then `B` is not a shifted `A`

##### Formulas

<img src="https://github.com/no1sebomb/University-Labs/blob/master/resources/sem3-alg-lab6-1.png" width="200px"/>
