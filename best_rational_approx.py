import argh
from decimal import Decimal, getcontext
from math import floor
from pprint import pprint
from fractions import Fraction

DE_FACTO_ZERO: Decimal = Decimal("1e-4")


class Approx:
    def __init__(self, nomin: int, denom: int, target: Decimal, cls: int = None) -> None:
        self.nomin = nomin
        self.denom = denom
        self.target = target
        self.cls = cls
        self.cont_frac = get_cont_frac(self.decimal_value())

    def decimal_value(self) -> Decimal:
        return Decimal(str(self.nomin)) / Decimal(str(self.denom))

    def abs_approx_quality(self) -> Decimal:
        return abs(self.approx_quality())

    def approx_quality(self) -> Decimal:
        return self.target - (Decimal(str(self.nomin)) / Decimal(str(self.denom)))

    def __str__(self) -> str:
        return f"{{approx= {self.nomin}/{self.denom} deviation= {self.approx_quality().quantize(Decimal('1e-6'))} class= {"I" if self.cls == 1 else "II" if self.cls == 2 else "N"} cont_frac= {self.cont_frac}}}"

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, __value: object) -> bool:
        return self.nomin == __value.nomin and self.denom == __value.denom

    def __hash__(self) -> int:
        return hash((self.nomin, self.denom))


def get_cont_frac(target: Decimal) -> list[int]:
    x: list[Decimal] = [target]
    alpha: list[int] = [floor(target)]
    diff = x[0] - Decimal(str(alpha[0]))
    d = list[Decimal]()

    while abs(diff) > DE_FACTO_ZERO:
        d.append(diff)
        x.append(Decimal("1") / d[-1])
        alpha.append(floor(x[-1]))
        diff = x[-1] - alpha[-1]


    if alpha[-1] == 1:
        alpha[-2] = alpha[-2] + 1
        alpha.pop(-1)
    return alpha


def divide(frac: tuple[int, int]) -> Decimal:
    return Decimal(str(frac[0]))


def get_convergents(cont_frac=list[int]) -> set[tuple[int, int]]:
    p: list[int] = [cont_frac[0], cont_frac[0] * cont_frac[1] + 1]
    q: list[int] = [1, cont_frac[1]]

    cont_frac = cont_frac[2:]
    for decim in cont_frac:
        p.append(p[-1] * decim + p[-2])
        q.append(q[-1] * decim + q[-2])

    return [(nom, denom) for nom, denom in zip(p, q)]


@argh.arg("--target", "-t", help="Finite digit rational number.", type=float)
@argh.arg("--lower_bound", "-l", help="Lower bound.", type=int)
@argh.arg("--higher_bound", "-h", help="Higher bound.", type=int)
def main(target: float = 0.5794415416798357, lower_bound: int = 3, higher_bound: int = 15):
    target = Decimal(str(target))
    pprint(getcontext())
    cont_frac: list[int] = get_cont_frac(target)
    print(cont_frac)
    convergents: list[tuple[int, int]] = get_convergents(cont_frac)
    # print(convergents)
    approxs = set[Approx]()
    for denom in range(lower_bound, higher_bound + 1):
        nomin: int = round(Decimal(str(denom)) * target)
        approx_frac: tuple[int, int] = (nomin, denom)
        approx_reduced = Fraction(nomin, denom).as_integer_ratio()
        if approx_reduced[1] < lower_bound:
            continue
        approx = Approx(approx_reduced[0], approx_reduced[1], target)
        if len(approxs) > 0 and approx.abs_approx_quality() >= min([appr.abs_approx_quality() for appr in approxs]):
            approx.cls = 3
        else:
            approx.cls = 2 if approx_reduced in convergents else 1
        
        approxs.add(
           approx 
        )

    ans = sorted([approx for approx in approxs], key=lambda x : x.abs_approx_quality())

    for approx in ans:
        print(approx)


if __name__ == "__main__":
    main()
