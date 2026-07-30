import argparse
import json
import os

from fission1d.paths import DATA_DIR


def readInputFile(inputFile):
    inputData = {}
    currentSection = None

    with open(inputFile, 'r') as file:
        for line in file:
            line = line.strip() # Remove whitespace from the line 

            if len(line) ==0: # Skip empty lines
                continue

            if line.startswith('#'): # Skip comments
                continue
            
            if line == "XSData": # Check if were entering the XSData section
                currentSection = "XSData"
                inputData["XSData"] = {}
                continue

            if line == "ConfigSets": # Check if were entering the ConfigSets section
                currentSection = "ConfigSets"
                inputData["ConfigSets"] = {}
                continue

            if line == "END": # Check if were exiting the current section
                currentSection = None
                continue

            if currentSection is None: # Check if we're not in a section
                if '=' in line: # Check if the line contains an equal sign
                    key, value = line.split('=')
                    key = key.strip()
                    value = value.strip()

                    # List of keys that should be integers
                    integerKeys = ['Solution', 'TestCase', 'Config', 'Analk', 'Cases', 'Configs', 
                                'MatTypes', 'EnergyGroups', 'solver', 'Generations', 'Histories', 
                                'Skip', 'NumAss', 'NumRods', 'MPFR', 'MPWR',]

                    if ' ' in value: # Check if the value contains a space
                        value = value.split()
                        # Check if this key should have integer values
                        if key in ['BoundL', 'BoundR']:
                            # These are float arrays
                            value = [float(v) for v in value]
                        else:
                            # Try to convert to integers if possible
                            try:
                                value = [int(v) for v in value]
                            except ValueError:
                                value = [float(v) for v in value]
                        inputData[key] = value
                    else:
                        # Check if this key should be an integer
                        if key in integerKeys:
                            inputData[key] = int(float(value))
                        else:
                            inputData[key] = float(value)
            else: # Currently inside a section

                if currentSection == "XSData": # Checking if we're inside the XSData section
                    if '=' in line:
                        key, value = line.split('=')
                        key = key.strip()
                        value = value.strip()
                        if key == "case":
                            currentCase = int(float(value))
                            inputData["XSData"][currentCase] = {}
                        else:
                            # Get EnergyGroups and MatTypes from inputData
                            energyGroups = int(inputData.get("EnergyGroups", 1))
                            matTypes = int(inputData.get("MatTypes", 1))
                            
                            # Parse the values
                            value = value.split()
                            value = [float(x) for x in value]
                            
                            # Organize values by material type first, then energy group
                            # Each energy group has MatTypes values: first value = UO2 (0), second = MOX (1), etc.
                            materialData = {}
                            for matIdx in range(matTypes):
                                materialData[matIdx] = {}
                                for eg in range(energyGroups):
                                    # Calculate index: energy group * matTypes + material index
                                    valueIdx = eg * matTypes + matIdx
                                    materialData[matIdx][eg] = value[valueIdx]
                            
                            inputData["XSData"][currentCase][key] = materialData

                if currentSection == "ConfigSets": # Checking if we're currently inside the ConfigSets section
                    if '=' in line:
                        key, value = line.split('=')
                        key = key.strip()
                        value = value.strip()
                        if key == "Set": # Checking if we're entering a new set
                            currentSet = int(float(value))
                            inputData["ConfigSets"][currentSet] = {}
                            matIDCounter = 0
                        elif key == "MatID":
                            # Multiple MatID lines = one row per assembly (see NumAss)
                            value = value.split()
                            value = [int(x) for x in value]
                            cfg = inputData["ConfigSets"][currentSet]
                            if "MatID" not in cfg:
                                cfg["MatID"] = []
                            cfg["MatID"].append(value)
                        else:
                            value = value.split()
                            value = [int(x) for x in value]
                            inputData["ConfigSets"][currentSet][key] = value
    return inputData


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Parse ENU6106 project .txt input into JSON."
    )
    parser.add_argument(
        "--energy-groups",
        "-g",
        type=int,
        default=2,
        metavar="N",
        help="Selects data/project{N}groupData.txt and writes data/parsed_output_{N}_group.json.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output JSON path (default: data/parsed_output_{N}_group.json).",
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    energy_groups = args.energy_groups
    if energy_groups < 1:
        raise SystemExit("--energy-groups must be >= 1")

    input_txt = f"project{energy_groups}groupData.txt"
    output_file_name = (
        args.output
        if args.output is not None
        else f"parsed_output_{energy_groups}_group.json"
    )
    input_file = os.path.join(str(DATA_DIR), input_txt)

    input_data = readInputFile(input_file)

    out_path = (
        output_file_name
        if os.path.isabs(output_file_name)
        else os.path.join(str(DATA_DIR), output_file_name)
    )
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(input_data, f, indent=2, sort_keys=False)


if __name__ == "__main__":
    main()
