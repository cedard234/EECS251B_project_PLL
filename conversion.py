import argparse
import os
import re
import shutil

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    args = parser.parse_args()

    # First, find all words with prefix sky130_fd_sc_hd__ in therm_to_bin.spice
    sky130_fd_sc_hd_files = set()
    with open(args.filename, "r", encoding="utf-8") as f:
        for line in f.readlines():
            matches = re.findall(r"sky130_fd_sc_hd__(\S+)", line)
            for match in matches:
                sky130_fd_sc_hd_files.add(match)

    # Then, find corresponding files in ../skywater-pdk-libs-sky130_fd_sc_hd/cells/ directory
    pdk_directory = "../skywater-pdk-libs-sky130_fd_sc_hd/cells/"
    for file_name in sky130_fd_sc_hd_files:
        cell_name, cell_number = file_name.split("_")
        cell_directory = os.path.join(pdk_directory, cell_name)
        file_to_clone = os.path.join(cell_directory, file_name + ".spice")
        if os.path.exists(file_to_clone):
            shutil.copy(file_to_clone, "/scratch/eecs251b-abe/virtuoso_workdir")

    # Modify the original file (therm_to_bin.spice) replacing sky130_fd_sc_hd__ with just __
    new_spice = []
    with open(args.filename, "r", encoding="utf-8") as f:
        for line in f.readlines():
            new_line = re.sub(r"sky130_fd_sc_hd__(\S+)", r"\1", line)
            new_spice.append(new_line)

    # Write the modified content back to the original file
    with open(args.filename, "w", encoding="utf-8") as f:
        f.writelines(new_spice)

    # Finally, run the code provided on the new files
    for file_name in sky130_fd_sc_hd_files:
        new_file_name = "/scratch/eecs251-abe/virtuoso_workdir/" + file_name + ".spice"
        modify_spice_file(new_file_name)


def modify_spice_file(file_name: str) -> None:
    new_spice = []
    with open(file_name, "r", encoding="utf-8") as f:
        for line in f.readlines():
            new_line = re.sub(r"sky130_fd_pr__", "", line)
            new_line = re.sub(r"=([1-9]+)0+", r"=0.\1", new_line)
            new_line = re.sub(r"=(\d+)e\+06", r"=\1", new_line)
            new_line = re.sub(r"X(\d+)", r"M\1", new_line)
            new_spice.append(new_line)
    with open(file_name, "w", encoding="utf-8") as f:
        f.writelines(new_spice)


if __name__ == "__main__":
    main()

