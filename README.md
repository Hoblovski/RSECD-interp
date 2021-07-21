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

The closures have a uniform representation, whether they are recursive: `(fn, fns, env)`.
The `fn` is the program counter of the closure; `fns` are the functions that may be mutually recursive to `fn`;
`env` is the environment saved when the closure was created (and will be restored upon closure invocation).
For example, a non-recursive closure would have `fns` empty. The `fn` may be empty, in case of mutually recursive closures not focused yet.

These are core instructions:

| instr | meaning | notes |
| --- | --- | --- |
| `access $n` | load the `n`th variable from environment | `n`: positive integer |
| `closure label` | create non-recursive closure **onto stack**, the code is at `label` | |
| `closures l1 l2...` | create a group(>=1) of mutually recursive closures **onto environment** | |
| `apply` | apply the closure with the argument which are on top of the stack | |
| `return` | return from closure; the return value is at the top of the stack | restores environment and pc |
| `halt` | we're done | usually the return value of the program is on top of the stack |
| `focus n` | with a group of closures on top of the stack, focus on one (so it turns into 'one' closure ready for invocation) | `n`: positive integer |

These should be obvious

| instr | meaning | notes |
| --- | --- | --- |
| `label:` | label (as function or branch destination) | end with `:` |
| `add`, `sub` ... | arithmetic operations | |
| `br`, `brfl` ... | branching operations | |
| `const val` | push constant onto stack | `val` can be of any type |
