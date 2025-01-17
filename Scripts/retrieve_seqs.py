import sys
from Bio import SeqIO

def retrieve_single_pair(genepair, protein_fasta, cds_fasta):
    """
    Retrieve protein and CDS sequences for a single gene pair.
    Write the sequences to the specified output files.
    """
    # Split and clean gene pair input
    try:
        gene1, gene2 = [gene.strip() for gene in genepair.split(" ")]
    except ValueError:
        print(f"Error: Invalid gene pair format: '{genepair}'", file=sys.stderr)
        return

    # Parse FASTA files
    protein_seqs = SeqIO.to_dict(SeqIO.parse(protein_fasta, "fasta"))
    cds_seqs = SeqIO.to_dict(SeqIO.parse(cds_fasta, "fasta"))

    # Extract sequences for the gene pair
    gene_protein_seqs = []
    gene_cds_seqs = []

    # Append sequences if they exist
    if gene1 in protein_seqs and gene2 in protein_seqs:
        gene_protein_seqs.extend([protein_seqs[gene1], protein_seqs[gene2]])
    else:
        print(f"Warning: Missing protein sequence for one or both genes: {gene1}, {gene2}", file=sys.stderr)

    if gene1 in cds_seqs and gene2 in cds_seqs:
        gene_cds_seqs.extend([cds_seqs[gene1], cds_seqs[gene2]])
    else:
        print(f"Warning: Missing CDS sequence for one or both genes: {gene1}, {gene2}", file=sys.stderr)

    # Write sequences to output files
    if gene_protein_seqs:
        SeqIO.write(gene_protein_seqs, "prot.fst", "fasta")
    if gene_cds_seqs:
        SeqIO.write(gene_cds_seqs, "cds.fst", "fasta")

    print(f"Sequences for gene pair {gene1}, {gene2} written to output files.")

if __name__ == "__main__":
    # Read command-line arguments
    genepair = sys.argv[1]
    protein_fasta = sys.argv[2]
    cds_fasta = sys.argv[3]

    # Run sequence retrieval for the gene pair
    retrieve_single_pair(genepair, protein_fasta, cds_fasta)
