import subprocess

Pcs = [
    "usuariouc@172.31.232.60",
    "usuariouc@172.31.232.68",
    "usuariouc@172.31.232.66",
    "usuariouc@172.31.232.69",
    "usuariouc@172.31.232.61",
]

def split_cars(n_cars, n_pcs):
    cars = [f"{i:03d}" for i in range(1, n_cars + 1)]
    return [cars[i::n_pcs] for i in range(n_pcs)]

def run_experiment(n_cars):
    groups = split_cars(n_cars, len(Pcs))

    for pc, group in zip(Pcs, groups):
        for car in group:
            cmd = f'ssh {pc} "cd /home/usuariouc/Escritorio/ServidorFINAL/Servidor/orion-ld/scripts && ./venv/bin/python scriptSimuladorGrande.py {car}"'
            subprocess.Popen(cmd, shell=True)

run_experiment(10)
