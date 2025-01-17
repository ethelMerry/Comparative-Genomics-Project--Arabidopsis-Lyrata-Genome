#!/bin/bash
# Paths to necessary files and directories
prot_fasta="/mnt/c/Users/ethel/Downloads/ProjectCompGen/Arabidopsis_lyrata.v.1.0.pep.all.fa"
cds_fasta="/mnt/c/Users/ethel/Downloads/ProjectCompGen/Arabidopsis_lyrata.v.1.0.cds.all.fa"
pal2nal_script="/mnt/c/Users/ethel/Downloads/ProjectCompGen/KAKS/pal2nal.pl"
control_file_template="/mnt/c/Users/ethel/Downloads/ProjectCompGen/KAKS/yn00.ctl_master.txt"
control_file="yn00.ctl"
yn00_executable="/mnt/c/Users/ethel/Downloads/ProjectCompGen/paml/bin/yn00"
seq_retrieve_script="/mnt/c/Users/ethel/Downloads/ProjectCompGen/KAKS/retrieve_seqs.py"
ks_extract_script="/mnt/c/Users/ethel/Downloads/ProjectCompGen/KAKS/extractks.py"
pairs_file="/mnt/c/Users/ethel/Downloads/ProjectCompGen/KAKS/test_20_pairs.txt" #I divided the data into different parts, so this is the first part
output_file="/mnt/c/Users/ethel/Downloads/ProjectCompGen/KAKS/calculatedKSTEST.txt"

# Process each line in the pair file
while IFS= read -r pair || [ -n "$pair" ]; do
    echo "Processing pair: $pair"
    
    # Step 1: Retrieve the protein and CDS sequences
    python3 "$seq_retrieve_script" "$pair" "$prot_fasta" "$cds_fasta"
    
    # Step 2: Align the protein sequences
    clustalw -quiet -align -infile=prot.fst -outfile=prot.ali.aln
    
    # Step 3: Align CDS sequences based on protein alignment
    "$pal2nal_script" prot.ali.aln cds.fst -output paml > cds.ali.phy
    
    # Step 4: Modify the control file with the current alignment file
    awk -v file=cds.ali.phy '{gsub("XXXXX",file); print $0}' "$control_file_template" > "$control_file"
    
    # Step 5: Run yn00
    "$yn00_executable"
    
    # Step 6: Extract calculated values and append to the final output file
    python3 "$ks_extract_script" "2YN.dS" "$output_file"

    
    echo "Finished processing pair: $pair"
done < "$pairs_file"

#echo "Pipeline completed. Results are in $output_file"
