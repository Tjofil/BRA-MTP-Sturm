from sympy import symbols, sin, cos, Function, series, sympify, Poly
from sympy.core.add import Add
from sympy.core.mul import Mul
from sympy.core.power import Pow
from sympy.core.numbers import Float, Integer
from sympy.functions.elementary.trigonometric import TrigonometricFunction
from sympy.core import Expr
from math import pi
from numpy.polynomial import Polynomial
from sturm import prepare_coefs, sturm, d
from decimal import Decimal


def transform_factor(expr: Expr, neg: bool) -> Expr:
    deg: int = 0
    # Prvo proveravamo da li je u pitanju factor koji je stepenovan
    if isinstance(expr, Pow):
        deg = expr.args[1]  # Pamtimo stepen
        expr: Expr = expr.args[0]  # Oslobadjamo se stepena

    if isinstance(expr, cos) and not neg:
        expr = series(cos(x), x, 0, 4 * S + 2 + 1, "+").removeO()

    if isinstance(expr, cos) and neg:
        expr = series(cos(x), x, 0, 4 * S + 1, "+").removeO()

    if isinstance(expr, sin) and not neg:
        expr = series(sin(x), x, 0, 4 * R + 3 + 1, "+").removeO()

    if isinstance(expr, sin) and neg:
        expr = series(sin(x), x, 0, 4 * R + 1 + 1, "+").removeO()

    # Ukoliko je faktor bio stepenovan na transformisani faktor ga ponovo vracamo
    return Pow(expr, deg) if deg != 0 else expr


# Funkcija za obradu jednog sabirka
def transform_term(expr: Mul) -> Mul:
    factors: list[Expr] = Mul.make_args(expr)
    negative: bool = False
    # Ako je prvi faktor u sabirku broj proveravamo mu znak
    if isinstance(factors[0], Float) or isinstance(factors[0], Integer):
        negative = factors[0] < sympify(0.0)
    # Analogno rastavljamo sabirak na faktore i prosledjujemo ih funkciji za obradu faktora
    return Mul(*map(transform_factor, factors, [negative for _ in range(len(factors))]))
    # Zatim ih ponovo mnozimo


def direct_comparison(func: Add) -> Expr:
    # Rastavljamo polinom na sabirke i nad svakim sabirkom pozivamo funkciju za obradu
    return Add(*map(transform_term, Add.make_args(func)))
    # Sve transformisane sabirke spajamo nazad u zbir


x = symbols("x")  # jedina promenljiva koju koristimo
# R i S definisemo kao globalne hiperaparametre kako bi izbegli
# preveliku propagaciju
R = 1  # k1
S = 1  # k2


def main() -> None:
    a, b = -2, -1.25
    # print(f_expanded)
    f: Function = 2*x**2 - 4*x*cos(x) + 2*sin(x)**2 - 6
    print(f"Original f: {f}")
    poly = Poly(direct_comparison(f).expand(), x)
    P_init = Polynomial([d(float(coef)) for coef in poly.all_coeffs()[::-1]])
    print(f"P before coeff aprox: {P_init}")
    P_init = prepare_coefs(P_init, 2)
    print(f"P after coeff aprox: {P_init}")
    print(type(P_init.roots()[0]))
    print(f"P has zeroes in {P_init.roots()}")
    print(f"P({a}) = {P_init(a)}, P({b}) = {P_init(b)}")
    print(f"Number of zeroes on ({a}, {b}): {sturm(P_init, (a, b))}")


if __name__ == "__main__":
    main()
