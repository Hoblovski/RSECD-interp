# Recursive SECD machine interactive interpreter
A stupid, unsafe, untyped but small implementation.

> Actually it's very simple but somehow it took me days to figure out. Mysterious.

# Usage
Ensure all `imports` are installed, then

```
vim secdinterpexamples.py
# choose one example, just uncomment it. default is (add 11 23)
# note some examples are diverging and thus you must only run them under interactive mode.

python secdinterp.py [-i]
```

* `[-i]`: interactive mode.
  - `n`: one step forward. Just hitting `<Enter>` is the same.
  - `p`: one step backward
  - `q`: quit

# The RSECD machine
The SECD machine is a classical functional abstract machine.

Only instructions are listed; their semantics should be obvious given the `step` function.

All closures take exactly one argument (use currying for more), which is put into their environment upon invocation.

These are core instructions:

| instr | meaning | notes |
| --- | --- | --- |
| `access $n` | load the `n`th variable from environment | `n`: positive integer |
| `closure label` | create non-recursive closure, the code is at `label` | |
| `apply` | apply the non-recursive closure with the argument which are on top of the stack | |
| `return` | return from closure; the return value is at the top of the stack | |
| `halt` | we're done | |
| `closures l1 l2...` | create a group(>=1) of mutually recursive closures | created on environment |
| `focus n` | with a group of closures, focus on one (so it turns into 'one' closure ready for invocation) | `n`: positive integer |
| `applyn` | apply the (already focused) recursive closure with the argument. | |

These should be obvious

| instr | meaning | notes |
| --- | --- | --- |
| `label:` | label (as function or branch destination) | end with `:` |
| `add`, `sub` ... | arithmetic operations | |
| `br`, `brfl` ... | branching operations | |
| `const val` | push constant onto stack | `val` can be of any type |
