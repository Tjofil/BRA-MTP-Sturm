from numpy.polynomial import Polynomial
from math import pi
from decimal import Decimal, ROUND_DOWN, ROUND_UP
import numpy as np
import argh

Pi = Decimal(str(pi))


def d_pow(x: Decimal, deg: int) -> Decimal:
    return x**deg


def d(x: float) -> Decimal:
    return Decimal(str(x))


def gcd_euclid(a: Polynomial, b: Polynomial) -> Polynomial:
    if b.trim(1e-6) == Polynomial([0]):
        return a

    q, r = divmod(a, b)
    # print(f"A: {a}\nB: {b}\nQ: {a // b}\nR: {a % b}\n\n")
    return gcd_euclid(b, r)


def custom_trim(P: Polynomial) -> Polynomial:
    P = P.trim()
    return Polynomial([c if abs(c) > 1e-4 else 0 for c in P.coef])


def V(P_series: list[Polynomial], value: Decimal):
    v: int = 0
    for i in range(0, len(P_series) - 1):
        left, right = P_series[i], P_series[i + 1]
        if left(value) * right(value) < 0:
            v += 1
    return v


def sturm(P: Polynomial, interval: tuple[Decimal, Decimal]) -> int:
    print(f"P: {P}")
    P_prim = P.deriv()
    print(f"Deriv(P): {P_prim}")
    G = gcd_euclid(P, P_prim)
    G = G // G.coef[-1]
    print(f"G: {G}")

    # print(f"P_init: {P_init}\ngcd(P_init, P_deriv): {G}\n")
    P: Polynomial = P // G
    P = custom_trim(P)
    # print(f"P INIT: {(P_init)}")
    P_prim: Polynomial = P.deriv()
    P_series: list[Polynomial] = [P, P_prim]
    while P_series[-2].degree() != 1:
        R: Polynomial = P_series[-2] % P_series[-1]
        P_series.append(-R)

    for i, pol in enumerate(P_series):
        print(f"P[{i}]: {pol}")

    print(f"V(a): {V(P_series, interval[0])}, V(b): {V(P_series, interval[1])}")
    return V(P_series, interval[0]) - V(P_series, interval[1])


def quantize_coef(x: Decimal, k: int) -> Decimal:
    return x.quantize(
        1 * d(10.0) ** d(x.adjusted() - 2),
        rounding=ROUND_DOWN if x > d(0.0) else ROUND_UP,
    )


def prepare_coefs(P: Polynomial, k: int) -> Polynomial:
    coefs: list[Decimal] = [quantize_coef(c, k) for c in P.coef]
    max_pow = max([abs(c.adjusted()) for c in P.coef]) + k
    coefs: list[Decimal] = [float(c * d(10) ** max_pow) for c in coefs]
    return Polynomial(coefs)


@argh.arg("--lower_bound", "-a", help="Lower bound.", type=float)
@argh.arg("--higher_bound", "-b", help="Higher bound.", type=float)
def main(a: float = -0.5, b: float = 0.75):
    P_init = Polynomial(
        [
            2 * Pi,
            d(-5),
            2 * Pi,
            d(-1),
            -4 * Pi,
            d(0.0),
            Pi,
        ]
    )
    # P_init = Polynomial([1, -1, 2, -1, -3, 0, 1])
    print(f"P before coeff aprox: {P_init}")
    # print("\n")
    # print()
    P_init = prepare_coefs(P_init, 2)
    print(f"P after coeff aprox: {P_init}")

    print(type(P_init.roots()[0]))
    print(f"P has zeroes in {P_init.roots()}")

    print(f"P(a) = {P_init(a)}, P(b) = {P_init(b)}")
    print(f"Number of zeroes on ({a}, {b}): {sturm(P_init, (a, b))}")

    # print(10 ** -x.adjusted() * x)
    # P_init = Polynomial([1, 0, -3, -1, 3, 3, -1, -3, 0, 1])

    # for p in P_series:
    #     print(p)
    # print(quantize_coefs(P_init))
    # print(type(P_init.coef[-1]))


if __name__ == "__main__":
    main()
