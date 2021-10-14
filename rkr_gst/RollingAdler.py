from __future__ import annotations

class RollingAdler(object):
    BASE = 65521 # largest prime smaller than 65536
    NMAX = 5552 # NMAX is the largest n such that 255n(n+1)/2 + (n+1)(BASE-1) <= 2^32-1
    def __init__(self, a: int, b: int) -> None:
        self.a = a
        self.b = b

    @staticmethod
    def new() -> RollingAdler:
        return RollingAdler.from_value(1)

    @staticmethod
    def from_value(value: int) -> RollingAdler:
        a = value & 0xFFFF
        b = value >> 16
        return RollingAdler(a, b)

    def hash(self) -> int:
        return (self.b << 16) | self.a

    def remove(self, size: int, byte: int) -> None:
        self.a = (self.a + RollingAdler.BASE - byte) % RollingAdler.BASE
        self.b = ((self.b + RollingAdler.BASE - 1) + (RollingAdler.BASE - size * byte)) % RollingAdler.BASE

    def update(self, byte: int) -> None:
        self.a = (self.a + byte) % RollingAdler.BASE
        self.b = (self.b + self.a) % RollingAdler.BASE