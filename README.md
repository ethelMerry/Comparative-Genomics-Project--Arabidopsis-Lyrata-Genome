# Analysis of Gene Duplication in Arabidopsis lyrata
Identification of Duplicated Genes and TAGs  in the Arabidopsis Lyrata Genome: Estimation of their proportion and evolutionary analysis based on Ks Values

**Description:**

This project investigates the distribution and evolutionary dynamics of duplicated genes, particularly tandemly arrayed genes (TAGs), in the Arabidopsis lyrata genome. 

**Key Analyses:**

* **Detection of Duplicated Genes:** Identified homologous gene pairs using BLASTP and clustered them into gene families using MCL.
* **Identification of TAGs:** Defined and identified TAGs based on chromosomal location, gene family assignment, and stringent criteria.
* **Calculation of Ks Values:** Estimated synonymous substitution rates (Ks values) for duplicated gene pairs using a robust pipeline involving ClustalW, PAL2NAL, and PAML's yn00.
* **Statistical Analysis:** Compared the distributions of Ks values for TAGs and non-TAGs using Mann-Whitney U test, Levene's test, and Kolmogorov-Smirnov test.

**Results:**

* The analysis revealed a multimodal distribution of Ks values, indicating multiple rounds of gene duplication events.
* TAGs exhibited a distinct pattern with a higher proportion of recent duplications compared to non-TAGs.
* Statistical tests confirmed significant differences in the distribution of Ks values between TAGs and non-TAGs.

**Findings:**

* Tandem duplication is an active and ongoing process in A. lyrata, contributing significantly to recent gene expansions.

**Files:**

* `scripts/`: Contains scripts for data processing, analysis, and visualization (e.g., BLASTP, MCL, Ks calculation, plotting scripts).
* `results/`: Contains processed data, figures, and statistical results.

