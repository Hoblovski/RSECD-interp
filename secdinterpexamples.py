##############################################################################
# (\f. f 22 10) (\x -> \y -> x-y)

#code = """
#main:
#    closure p1
#    closure p2
#    apply
#    halt
#
#p1:
#    access $1
#    const 22
#    apply
#    const 10
#    apply
#    return
#
#p2:
#    closure p3
#    return
#
#p3:
#    access $2
#    access $1
#    sub
#    return
#"""


##############################################################################
# (\x. x + 1) 5

#code = """
#main:
#    closure p1
#    const 5
#    apply
#    halt
#
#p1:
#    access $1
#    const 1
#    add
#    return
#"""


##############################################################################
# (\f. f 0) (\x. x+1)

#code = """
#main:
#    closure p1
#    closure p2
#    apply
#    halt
#
#p1:
#    access $1
#    const 12
#    apply
#    return
#
#p2:
#    access $1
#    const 1
#    add
#    return
#"""


##############################################################################
# ((\g -> ((\f -> g f) (\x -> \y -> x-y))) (\x -> x 22)) 10

#code = """
#main:
#    closure p1
#    closure p2
#    apply
#    const 10
#    apply
#    halt
#
#p1:
#    closure p3
#    closure p4
#    apply
#    return
#
#p2:
#    access $1
#    const 22
#    apply
#    return
#
#p3:
#    access $2
#    access $1
#    apply
#    return
#
#p4:
#    closure p5
#    return
#
#p5:
#    access $2
#    access $1
#    sub
#    return
#"""


##############################################################################
# letrec f x = f x in f 0

#code = """
#main:
#    closures p1
#    access $1
#    focus 1
#    const 0
#    applyn
#    return
#
#p1:
#    access $2
#    focus 1
#    access $1
#    applyn
#    return
#"""


##############################################################################
# (\x -> if x==0 then 1 else x-1) 5

#code = """
#main:
#    closure p1
#    const 5
#    apply
#    halt
#
#p1:
#    access $1
#    const 0
#    eq
#    brfl fl
#  tr:
#    const 1
#    br end
#  fl:
#    access $1
#    const 1
#    sub
#  end:
#    return
#"""


##############################################################################
# letrec fact n =
#    if n==0 then 1 else n * (fact (n-1))
# in fact 6 * fact 8

#code = """
#main:
#    closures p1
#    access $1
#    focus 1
#    const 6
#    applyn
#    access $1
#    focus 1
#    const 8
#    applyn
#    mul
#    halt
#
#p1:
#    access $1
#    const 0 ; eq
#    brfl fl
#  tr:
#    const 1
#    br end
#  fl:
#    access $1
#    access $2
#    focus 1
#    access $1
#    const 1
#    sub
#    applyn
#    mul
#  end:
#    return
#"""


##############################################################################
# letrec even n = if n == 0 then True else odd (n-1)
#    and odd  n = if n == 0 then False else even (n-1)
# in
#     _inspect (even 5) (even 6) (odd 4) (odd 5)

#code = """
#main:
#    closures p1 p2
#    access $1 ; focus 1
#    const 5
#    applyn
#    access $1 ; focus 1
#    const 6
#    applyn
#    access $1 ; focus 2
#    const 4
#    applyn
#    access $1 ; focus 2
#    const 5
#    applyn
#    _inspect
#    return
#
#p1:
#    access $1 ; const 0 ; eq
#    brfl fl1
#  tr1:
#    const True
#    br end1
#  fl1:
#    access $2 ; focus 2
#    access $1 ; const 1 ; sub
#    applyn
#  end1:
#    return
#
#p2:
#    access $1 ; const 0 ; eq
#    brfl fl2
#  tr2:
#    const False
#    br end2
#  fl2:
#    access $2 ; focus 1
#    access $1 ; const 1 ; sub
#    applyn
#  end2:
#    return
#"""


##############################################################################
# letrec add x =
#     \y -> if x == 0 then y else 1 + add (x-1) y
# in
#     add 11 23

code = """
main:
    closures p1
    access $1 ; focus 1
    const 11 ; applyn
    const 23 ; apply
    halt

p1:
    closure p2
    return

p2:
    access $2 ; const 0 ; eq
    brfl fl
  tr:
    access $1
    br end
  fl:
    const 1
    access $3 ; focus 1
    access $2 ; const 1 ; sub
    applyn
    access $1 ; apply
    add
  end:
    return
"""
