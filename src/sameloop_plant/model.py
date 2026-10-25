# SPDX-License-Identifier: MIT
from dataclasses import dataclass, asdict
import math


def finite(value, lower, upper, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name}: nombre requis")
    if not math.isfinite(value) or not lower <= value <= upper:
        raise ValueError(f"{name}: valeur finie dans [{lower}, {upper}] requise")
    return float(value)


@dataclass
class Plant:
    """RK4 reference model, internal steps <= 10 ms; no controller embedded."""
    temperature: float = 32.4
    applied: float = 0.0
    rpm: float = 0.0
    elapsed: float = 0.0

    def __post_init__(self):
        self.temperature = finite(self.temperature, -40, 150, 'temperature')
        self.applied = finite(self.applied, 0, 100, 'applied')
        self.rpm = finite(self.rpm, 0, 10000, 'rpm')
        self.elapsed = finite(self.elapsed, 0, 1e12, 'elapsed')

    def step(self, dt, demand=0.0, heat=0.18):
        dt = finite(dt, 0, 60, 'dt')
        demand = finite(demand, 0, 100, 'demand')
        heat = finite(heat, 0, 2, 'heat')
        if dt == 0:
            return self.snapshot()
        n = max(1, math.ceil(dt / 0.01))
        h = dt / n
        def derivative(y):
            t, a, rpm = y
            return (heat - (0.015 + 0.12*a/100)*(t-20),
                    (demand-a)/0.6, (40*a-rpm)/0.8)
        y = (self.temperature, self.applied, self.rpm)
        for _ in range(n):
            k1 = derivative(y)
            k2 = derivative(tuple(v+h*k/2 for v,k in zip(y,k1)))
            k3 = derivative(tuple(v+h*k/2 for v,k in zip(y,k2)))
            k4 = derivative(tuple(v+h*k for v,k in zip(y,k3)))
            y = tuple(v+h*(a+2*b+2*c+d)/6 for v,a,b,c,d in zip(y,k1,k2,k3,k4))
        self.temperature, self.applied, self.rpm = y
        self.elapsed += dt
        return self.snapshot()

    def snapshot(self):
        return asdict(self)
