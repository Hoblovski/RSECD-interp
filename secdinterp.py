from collections import namedtuple
from secdinterpexamples import code
import argparse
import sys
from copy import deepcopy
from ast import literal_eval

SECDDump = namedtuple('SECDDump', ('pc', 'stk', 'env'))

def clrscr():
    print("\033[H\033[J")

def step(dmp):
    com = coms[dmp.pc]
    pc, stk, env = dmp
    op, *args = com.split()

    if com.endswith(':'):
        pc += 1
        return SECDDump(pc, stk, env)

    if op == 'access':
        pc += 1
        sel = args[0][1:]
        envIdx = int(sel)
        stk += [env[-envIdx]]
        return SECDDump(pc, stk, env)

    if op == 'closure':
        pc += 1
        stk += [(labelToPc[args[0]], env)]
        return SECDDump(pc, stk, env)

    if op == 'apply':
        v, (pc1, env1), stk = stk[-1], stk[-2], stk[:-2]
        stk = stk + [env, pc+1]
        env = env1 + [v]
        pc = pc1
        return SECDDump(pc, stk, env)

    if op == 'return':
        v, pc1, env1, stk = stk[-1], stk[-2], stk[-3], stk[:-3]
        env = env1
        pc = pc1
        stk = stk + [v]
        return SECDDump(pc, stk, env)

    if op == 'halt':
        print(f'HALTED, return value = {stk[-1]}')
        return 'halted'

    if op == 'closures':
        pc += 1
        env = env + [(None, tuple(labelToPc[arg] for arg in args), env)]
        return SECDDump(pc, stk, env)

    if op == 'focus':
        pc += 1
        (_, fns, env1), stk = stk[-1], stk[:-1]
        stk = stk + [(int(args[0]), fns, env1)]
        return SECDDump(pc, stk, env)

    if op == 'applyn':
        v, (idx, fns, env1), stk = stk[-1], stk[-2], stk[:-2]
        stk = stk + [env, pc+1]
        env = env1 + [(None, fns, env1), v]
        pc = fns[idx-1]
        return SECDDump(pc, stk, env)

    return trivialStep(op, args, pc, stk, env)

arithOps = {
    'sub': (2, lambda args: args[0] - args[1]),
    'add': (2, lambda args: args[0] + args[1]),
    'mul': (2, lambda args: args[0] * args[1]),
    'eq': (2, lambda args: args[0] == args[1]),
}

branchOps = {
    'brfl': (1, lambda args: not args[0]),
    'br': (0, lambda args: True),

}

def trivialStep(op, args, pc, stk, env):
    if op == 'const':
        pc += 1
        arg = literal_eval(args[0])
        stk += [arg]
        return SECDDump(pc, stk, env)

    if op in arithOps:
        pc += 1
        arity, fn = arithOps[op]
        fargs, stk = stk[-arity:], stk[:-arity]
        stk = stk + [fn(fargs)]
        return SECDDump(pc, stk, env)

    if op in branchOps:
        arity, fn = branchOps[op]
        if op != 'br':
            fargs, stk = stk[-arity:], stk[:-arity]
            taken = fn(fargs)
        else:
            taken = True
        if taken:
            pc = labelToPc[args[0]]
        else:
            pc += 1
        return SECDDump(pc, stk, env)

    # in case of inspection, just raise an exception to print stk
    raise Exception(f'bad op {op}, args={args}, stk={stk}')

def printDmp(dmp):
    if dmp == 'halted':
        print('HALTED!')
        return

    print('--- pc')
    progStr = '\n'.join(code[:dmp.pc] + ['> ' + code[dmp.pc][2:]] + code[dmp.pc+1:])
    print(f'{progStr}')

    print('--- stk (from bottom to top)')
    stkStr = '\n'.join(str(x) for x in dmp.stk)
    print(f'{stkStr}')

    print('--- env (from bottom to top)')
    envStr = '\n'.join(str(x) for x in dmp.env)
    print(f'{envStr}')


def parseArgs(argv):
    parser = argparse.ArgumentParser(description='SECD interpreter')
    parser.add_argument('-i', '--interactive', action='store_true', help='interactive mode')
    return parser.parse_args()


if __name__ == "__main__":
    args = parseArgs(sys.argv)

    coms = [l.strip() for l in code.replace('##', '\n#').replace(';', '\n').split('\n')]
    coms = [l for l in coms if len(l) != 0 and not l.startswith('#')]
    code = [f'  {i}: {com}' for i, com in enumerate(coms)]
    labelToPc = { com[:-1]: pc for pc, com in enumerate(coms) if com.endswith(':') }

    pc = labelToPc['main']
    env, stk = [], []
    dmp = SECDDump(pc, stk, env)

    i = 0
    MAXSTEP = 1000
    dmps = [dmp]
    while i < MAXSTEP:
        if args.interactive:
            clrscr()

        print(f'\n{i}================================\n')
        printDmp(dmps[i])

        if args.interactive:
            cmd = None
            while cmd not in {'n', 'p', '', 'q'}:
                cmd = input()
            if cmd == 'p':
                i -= 1
            elif cmd in {'', 'n'}:
                if dmps[i] != 'halted':
                    i += 1
                    if i == len(dmps):
                        dmps += [step(deepcopy(dmps[-1]))]
            elif cmd == 'q':
                break

        else:
            dmps += [step(deepcopy(dmps[-1]))]
            if dmps[-1] == 'halted':
                break
            i += 1

    if dmps[-1] != 'halted':
        print('Abort.')

