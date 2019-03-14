# Yeast data in vcf
### Download from: http://www.moseslab.csb.utoronto.ca/sgrp/data/SGRP2-cerevisiae-freebayes-snps-Q30-GQ30.vcf.gz
#### DyeDot.py only works on single sample vcfs. Convert the multi-sample vcf with:
for sample in `bcftools query -l INPUT.vcf`; do vcf-subset --exclude-ref -c $sample INPUT.vcf > ${sample}.vcf; done
### A subset of vcfs included for testing
