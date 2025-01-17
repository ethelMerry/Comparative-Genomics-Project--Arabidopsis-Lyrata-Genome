import sys

def extract_ks_values(YN_dS, output_file):
    """
    Extracts Ks values from a PAML 2YN.dS file and appends them to the output file.

    Args:
        YN_dS (str): Path to the PAML output file (2YN.dS).
        output_file (str): Path to the output file to append the results.
    """
    try:
        with open(YN_dS, "r") as file:
            lines = file.readlines()  # Read all lines at once
        
        # Ensure there are enough lines for valid extraction
        if len(lines) < 3:
            raise ValueError(f"File '{YN_dS}' does not have the expected format.")

        seq1, seq2, dS_value = lines[1].strip(), *lines[2].split()[:2]

        # Append the extracted values to the output file
        with open(output_file, "a") as outfile:
            outfile.write(f"{seq1}\t{seq2}\t{dS_value}\n")

    except FileNotFoundError:
        print(f"Error: File '{YN_dS}' not found.", file=sys.stderr)
        sys.exit(1)
    except (IndexError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 extract_ks.py <2YN.dS_file> <output_file>")
        sys.exit(1)

    extract_ks_values(sys.argv[1], sys.argv[2])
