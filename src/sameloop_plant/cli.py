# SPDX-License-Identifier: MIT
import argparse
import json
import sys
from .model import Plant


def main():
    p = argparse.ArgumentParser(description='Simulation déterministe, sans temps réel ni réseau')
    p.add_argument('--seconds', type=float, default=10)
    p.add_argument('--step', type=float, default=0.1)
    p.add_argument('--demand', type=float, default=50)
    p.add_argument('--heat', type=float, default=0.18)
    p.add_argument('--jsonl', action='store_true', help='Lire {dt,demand,heat} sur stdin ; une réponse par ligne')
    a = p.parse_args()
    plant = Plant()
    try:
        if a.jsonl:
            for line in sys.stdin:
                try:
                    obj = json.loads(line)
                    if not isinstance(obj, dict) or set(obj)-{'dt','demand','heat'}:
                        raise ValueError('Objet {dt,demand,heat} attendu')
                    result = plant.step(**obj)
                    print(json.dumps({'ok': True, 'state': result}, allow_nan=False), flush=True)
                except (ValueError, TypeError) as e:
                    print(json.dumps({'ok': False, 'error': str(e)}), flush=True)
        else:
            from .model import finite
            finite(a.seconds, 0, 86400, 'seconds'); finite(a.step, 0.001, 60, 'step')
            remaining = a.seconds
            while remaining > 1e-10:
                dt = min(a.step, remaining)
                print(json.dumps(plant.step(dt, a.demand, a.heat), allow_nan=False))
                remaining -= dt
    except ValueError as e:
        p.error(str(e))
