#!/usr/bin/python3

#Generate dependencies with pipreqs ./

#Python script to generate .dot graph files of variants encoded in several vcfs.

#IMPORTANT: THE ASSUMPTION IS THAT THE VCFs CONTAIN ONLY HIGH CONFIDENCE VARIANTS.
#CURRENTLY ONLY TESTED ON SMALL (SNP AND INDEL) VARIANTS

#Viewing options for very large/wide graphs
#http://www.webgraphviz.com/
#http://viz-js.com/
#VIEW LOCALLY WITH KGraphViewer - install both kgraphviewer and kgraphviewer-dev
#ONLY USE WEB-BASED TOOLS FOR SMALL OR LOW COMLEXITY DOT FILES.

#KgraphViewer displays .dot files up to 300kb within workable wall time.
#This is a relative estimate as the rendering time depends on the number of nodes
#Large SVs will generate large files (due to sequence representation) but will have fewer nodes. Essentially using SNP data represents the
#worst case scenario

#SUGGESTED IMRPOVEMENTS
#HAVE TO SPECIFY A RANGE TO VIEW. HUGH SUGGESTED WE DRAW BARCODE PLOTS FROM VCF. INDICATE VARIANT DENSITY BY INCREMENTING RGB VALUES
#BASED ON OVERLAP BETWEEN VCFs. THEN BASED ON THIS, DYNAMICALLY DETERMINE REGIONS AND PLOT VARIATION BUBBLES BASED ON THIS SCRIPT.
#BONUS POINTS FOR SLAMMING IT INTO A GUI OR GENOME BROWSER OF SOME SORT

#DYNAMICALLY DETERMINE RANGE BASED ON NUMBER OF NODES
#MERGING OF DOT GRAPHs WITH ADDITIONAL VCFs AND MERGING OF DOTs

#NB! HUMAN VCFs WILL BE MASSIVE (A FEW GB). PREFILTER VCF INPUT ACCORDING TO RANGE SPECIFIED.
#COULD USE PYTHON PACKAGE FOR VCFs OR SUPER FAST AWK - HOWEVER THE LATTER LIMITS TO POSIX SYSTEMS.

#ONLY WORKS ON SINGLE SAMPLE VCFs
#CONVERT MULTISAMPLE WITH: for sample in `bcftools query -l multi.vcf`; do vcf-subset --exclude-ref -c $sample multi.vcf > ${sample}.vcf; done

###############################################
#DEPENDENCIES:
#GRAPHVIZ $ pip3 install graphviz
#SEABORN $ pip3 install seaborn
###############################################

###############################################
#USAGE
#python3 DRIVER_dyedot -h
#EXAMPLE
#python3 Driver_dyedot.py -p /home/rndw/PycharmProjects/graph_dag/Yeast_data/Full_vcfs -o output -c chrVII -b 6000 -e 100000
###############################################

from os import name
from time import time
import argparse
from class_vcf_parser import ReadVcfs, VarGraphCons, RegionOfInterestGraph
from class_Grapher import RefGraphBuilder



#PARSER FOR CMD ARGUMENTS
parser = argparse.ArgumentParser(description='Read in vcf files and constructs a variations graph', prog='DyeDot')
parser.add_argument('-p', metavar='<path>', type=str, help="Path to vcf files")
parser.add_argument('-o', type=str, metavar='<filename>', help="Output filename")
parser.add_argument('-c', type=str, metavar='chromosome', nargs='?', default='DEFAULT', const='DEFAULT', help='Chromosome to investigate (default: First element in graph dictionary)')
parser.add_argument('-b', type=int, metavar='integer', nargs='?', default=0, const=0, help='Start location of region to investigate (default: 0 bp)')
parser.add_argument('-e', type=int, metavar='integer', nargs='?', default=20000, const=20000, help='End location of region to investigate (default: 20 000 bp)')
args = parser.parse_args()

#FRIENDLY CMD ARGUMENT CORRECTION/WARNING/NOTIFICATIONS
print(f"Output will be written to {args.o}.dot: ")
print(f"The region of interest is: {args.c}:{args.b}-{args.e}")
path = args.p
#CHECK OS AND CORRECT PATH IF REQUIRED
if name == 'posix' and path.endswith('/'):
    print(f'Path is: {args.p}')
if name != 'posix' and path.endswith('\\'):
    print(f'Path is: {args.p}')
if name == 'posix' and not path.endswith('/'):
    path = path + '/'
    print(f'Path set to: {path}')
if name != 'posix' and not path.endswith('\\'):
    path = path + '\\'
    print(f'Path set to: {path}')
#CONSTRUCT RANGE OBJECT
#Default: loci = ['chrI',0,50000]
loci = [args.c, args.b, args.e]
#CREATE A DICTIONARY OBJECT LINKING EACH KEY TO A VCF
dat = ReadVcfs(path).variant_builder()
#EXIT IF THE DIR CONTAINS NO VCFs
if not dat:
    print(f"No vcf files in directory. Please check path: {path}")
    exit(1)

#UTILITY - WALL TIME. IF SSD OR FAST RAID SETUP, THREADING IMPROVES SPEED BY A FEW SECONDS. SLOWS DOWN WHEN ON MECHANICAL DSK
start = time()

#READ IN VCF FILES AS A DICT - EACH VARIANT IS A TUPLE(CHR, POS, ALT, REF) PER VCF/KEY
## -- Saving intermediate files in same dir as vcfs
#Manual run : output = VarGraphCons().anchor_builder(dat)
output = VarGraphCons().anchor_builder(dat)
#LIMIT DATA TO SPECIFIED REGION
#IMPROVEMENT: OUTPUT MULTIPLE RANGES OR BLOCKS
RegionOfInterestGraph(output, loci).region()
#CONSTRUCT A REFERENCE PATH OBJECT. THIS COULD BE ANYTHING REALLY (HAPLOTYPES) - AS LONG AS IT CONTAINS OVERLAPPING NODES
refpath = RegionOfInterestGraph(output, loci).referencegr()

#CONSTRUCT THE REFERENCE PATH
graph = RefGraphBuilder().referencepath(refpath)
#CONSTRUCT THE VARAINT PATHS: BUILT ON TOP OF THE REFERENCE PATH
xgraph = RefGraphBuilder().variantpath(output, graph, loci, refpath)

#ANOTHER FRIENDLY MESSAGE - OUTPUT FILE
print(f'Writing output to: {str(args.o+".dot")}')
#SAVE THE GRAPH IN DOT FORMAT
#IMPROVEMENT: LOOK AT ALTERNATIVE ALGORITHMS/ENGINES - MAYBE NEATO?
graph.save(filename=str(args.o+'.dot'))

#PRINT TIME TAKEN ~ 80s FOR TEST DATA
end = time()
print(end - start)
