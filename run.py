import os
import json
import time
import argparse
from mendelianPea.simulate.simulate import Simulate
from mendelianPea.pea.pea import Pea, ColorGene, ShapeGene


def parse_args():
    parser = argparse.ArgumentParser(description='Meandeian Pea Simulator.')
    parser.add_argument('--version', action='version', version='Mendelian Simulator 1.0')
    parser.add_argument('-i', '--input', type=str, required=True, dest='input_file',
                        help='Input json file with config params')
    return parser.parse_args()


NO_EXTERNAL_FACTORS = {ColorGene.YELLOW.value: 0.1, ColorGene.GREEN.value: 0.1, ShapeGene.WRINKLED.value: 0.1,
                       ShapeGene.ROUND.value: 0.1}

if __name__ == "__main__":
    args = parse_args()

    with open(args.input_file) as json_file:
        data = json.load(json_file)

    iterations = data.get("no-of-iterations", 30)
    no_of_generations = data.get("no-of-generations-per-iteration", 30)
    advantage = data.get("advantage", NO_EXTERNAL_FACTORS)
    base_survival = data.get("base-survival", 0.4)
    no_of_children = data.get("no-of-children", 4)

    output_location = data.get("output-location")
    output_file = data.get("output-file")
    op_file_path = os.path.join(output_location, output_file)

    raw_generation0 = data.get("generation0", {"hetrogygote": 20})
    peas = []
    if raw_generation0.get("hetrogygote"):
        peas += [Pea.get_hetrozygote()] * raw_generation0.get("hetrogygote")
    if raw_generation0.get("homozygote-recessive"):
        peas += [Pea.get_recessive_homozygote()] * raw_generation0.get("homozygote-recessive")
    if raw_generation0.get("homozygote-dominant"):
        peas += [Pea.get_dominant_homozygote()] * raw_generation0.get("homozygote-dominant")

    t1 = time.time()
    sim = Simulate(generation0=peas, no_of_generations=no_of_generations, advantage=advantage,
                  base_survival=base_survival, no_of_children=no_of_children)
    sim.run_iterations(iterations=iterations)

    sim.save_xls(op_file_path)
    t2 =time.time()
    print("Simulation took : {}secs".format(t2-t1))
