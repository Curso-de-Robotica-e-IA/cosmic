import argparse
import os

def get_input_file() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='path to the input XML file.')
    args = parser.parse_args()
    
    if not os.path.exists(args.input_file):
        print(f"input file '{args.input_file}' does not exist.")
        exit(1)
    return args