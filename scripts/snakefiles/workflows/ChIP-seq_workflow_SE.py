"""Generic workflow for the analysis of ChIP-seq data for the binding
of transcription factors.


This workflow performs the following treatments: 

 - quality check
 - read mapping
 - peak-calling with alternate peak-calling programs
 - motif discovery

The details are specified in a yaml-formatted configuration file.

Usage:

1. Run in command line mode

    snakemake -p -s gene-regulation/scripts/snakefiles/workflows/chip-seq_workflow_SE.py 
        --configfile path/to/specific/config_file.yml \
        [targets]

2. Send tasks to qsub job scheduler

    snakemake -p -c "qsub {params.qsub}" -j 12 \
        -s gene-regulation/scripts/snakefiles/workflows/chip-seq_workflow_SE.py \
        --configfile path/to/specific/config_file.yml \
        [targets]

3. Generate flowcharts:

    snakemake -p -s gene-regulation/scripts/snakefiles/workflows/chip-seq_workflow_SE.py \
        --configfile path/to/specific/config_file.yml \
        --force flowcharts

Sequencing type: 	single end

Author: 		Claire Rioualen, Jacques van Helden
Contact: 		claire.rioualen@inserm.fr

"""



#================================================================#
#                       Python Imports 
#================================================================#

from snakemake.utils import R
import os
import sys
import datetime
import re
import pandas as pd

GENEREG_LIB = os.path.join(config["dir"]["base"], config["dir"]["gene_regulation"])

include: os.path.join(GENEREG_LIB, "scripts/python_lib/util.py")


#================================================================#
#                      Variables
#================================================================#

# Genome & annotations
GENOME_DIR = os.path.join(config["dir"]["base"], config["dir"]["genome"])
GENOME_FASTA = os.path.join(GENOME_DIR, config["genome"]["fasta_file"])
GENOME_GFF3 = os.path.join(GENOME_DIR, config["genome"]["gff3_file"])
GENOME_GTF = os.path.join(GENOME_DIR, config["genome"]["gtf_file"])

# Samples
SAMPLE_IDS = read_table(os.path.join(config["dir"]["base"], config["metadata"]["samples"]))['ID']

# Design
DESIGN = read_table(os.path.join(config["dir"]["base"],config["metadata"]["design"]))
TREATMENT = DESIGN['treatment']
CONTROL = DESIGN['control']

## Data & results dir
if not (("dir" in config.keys()) and ("reads_source" in config["dir"].keys())):
    sys.exit("The parameter config['dir']['reads_source'] should be specified in the config file.")
else:
    READS = os.path.join(config["dir"]["base"], config["dir"]["reads_source"])

if not ("fastq" in config["dir"].keys()):
    sys.exit("The parameter config['dir']['fastq'] should be specified in the config file.")
else:
    FASTQ_DIR = os.path.join(config["dir"]["base"], config["dir"]["fastq"])

if not ("results" in config["dir"].keys()):
    sys.exit("The parameter config['dir']['results'] should be specified in the config file.")
else:
    RESULTS_DIR = os.path.join(config["dir"]["base"],config["dir"]["results"])

if not ("samples" in config["dir"].keys()):
    SAMPLE_DIR = os.path.join(config["dir"]["base"],config["dir"]["results"])
else:
    SAMPLE_DIR = os.path.join(config["dir"]["base"],config["dir"]["samples"])

if not ("reports" in config["dir"].keys()):
    REPORTS_DIR = os.path.join(config["dir"]["base"],config["dir"]["results"])
else:
    REPORTS_DIR = os.path.join(config["dir"]["base"],config["dir"]["reports"])

if not ("peaks" in config["dir"].keys()):
    PEAKS_DIR = os.path.join(config["dir"]["base"],config["dir"]["results"])
else:
    PEAKS_DIR = os.path.join(config["dir"]["base"],config["dir"]["peaks"])


#================================================================#
#               Snakemake includes
#================================================================#

RULES = os.path.join(GENEREG_LIB, "scripts/snakefiles/rules")

include: os.path.join(RULES, "annotate_peaks.rules")
include: os.path.join(RULES, "bam_by_pos.rules")
include: os.path.join(RULES, "bam_to_bed.rules")
include: os.path.join(RULES, "bam_stats.rules")
include: os.path.join(RULES, "bedgraph_to_tdf.rules")
include: os.path.join(RULES, "bedtools_closest.rules")
include: os.path.join(RULES, "bedtools_intersect.rules")
include: os.path.join(RULES, "bedtools_window.rules")
include: os.path.join(RULES, "bowtie_index.rules")
include: os.path.join(RULES, "bowtie.rules")
include: os.path.join(RULES, "bowtie2_index.rules")
include: os.path.join(RULES, "bowtie2.rules")
include: os.path.join(RULES, "bPeaks.rules")
include: os.path.join(RULES, "bwa_index.rules")
include: os.path.join(RULES, "bwa.rules")
include: os.path.join(RULES, "count_reads.rules")
include: os.path.join(RULES, "dot_graph.rules")
include: os.path.join(RULES, "dot_to_image.rules")
include: os.path.join(RULES, "fastqc.rules")
include: os.path.join(RULES, "genome_coverage_bedgraph.rules")
include: os.path.join(RULES, "genome_coverage_bigwig.rules")
include: os.path.join(RULES, "getfasta.rules")
include: os.path.join(RULES, "get_chrom_sizes.rules")
include: os.path.join(RULES, "gzip.rules")
include: os.path.join(RULES, "homer.rules")
include: os.path.join(RULES, "igv_session.rules")
include: os.path.join(RULES, "index_bam.rules")
include: os.path.join(RULES, "index_fasta.rules")
include: os.path.join(RULES, "macs2.rules")
include: os.path.join(RULES, "macs14.rules")
include: os.path.join(RULES, "peak_motifs.rules")
include: os.path.join(RULES, "sickle.rules")
include: os.path.join(RULES, "spp.rules")
include: os.path.join(RULES, "sra_to_fastq.rules")
include: os.path.join(RULES, "subread_index.rules")
include: os.path.join(RULES, "subread_align.rules")
include: os.path.join(RULES, "swembl.rules")


#================================================================#
#                         Workflow                               #
#================================================================#

## Data import 
IMPORT = expand(FASTQ_DIR + "/{samples}/{samples}.fastq", samples=SAMPLE_IDS)

## Graphics & reports
GRAPHICS = expand(REPORTS_DIR + "/{graph}.png", graph=["dag", "rulegraph"])

## Quality report
RAW_QC = expand(FASTQ_DIR + "/{samples}/{samples}_fastqc/{samples}_fastqc.html", samples=SAMPLE_IDS)
QC = RAW_QC

#----------------------------------------------------------------#
# Trimming
#----------------------------------------------------------------#

if not (("tools" in config.keys()) and ("trimming" in config["tools"].keys())):
    sys.exit("The parameter config['tools']['trimming'] should be specified in the config file. Empty quotes equal to no trimming.")

TRIMMING_TOOLS = config["tools"]["trimming"].split()

TRIMMING = expand(FASTQ_DIR + "/{samples}/{samples}_{trimmer}.fastq", samples=SAMPLE_IDS, trimmer=TRIMMING_TOOLS)

TRIM_QC = expand(FASTQ_DIR + "/{samples}/{samples}_{trimmer}_fastqc/{samples}_{trimmer}_fastqc.html", samples=SAMPLE_IDS, trimmer=TRIMMING_TOOLS)
QC = RAW_QC + TRIM_QC

#----------------------------------------------------------------#
# Alignment
#----------------------------------------------------------------#

if not (("tools" in config.keys()) and ("mapping" in config["tools"].keys())):
    sys.exit("The parameter config['tools']['mapping'] should be specified in the config file.")

MAPPING_TOOLS = config["tools"]["mapping"].split()

INDEX = expand(GENOME_DIR + "/{aligner}/" + config["genome"]["fasta_file"], aligner=MAPPING_TOOLS)

if TRIMMING_TOOLS:
    PREFIX = expand("{trimmer}_{aligner}", aligner=MAPPING_TOOLS, trimmer=TRIMMING_TOOLS)
else:
    PREFIX = expand("{aligner}", aligner=MAPPING_TOOLS)

MAPPING         = expand(SAMPLE_DIR + "/{samples}/{samples}_{prefix}.bam", samples=SAMPLE_IDS, prefix=PREFIX)

SORTED_BAM      = expand(SAMPLE_DIR + "/{samples}/{samples}_{prefix}_sorted_pos.bam", samples=SAMPLE_IDS, prefix=PREFIX)
SORTED_BAM_BAI  = expand(SAMPLE_DIR + "/{samples}/{samples}_{prefix}_sorted_pos.bam.bai", samples=SAMPLE_IDS, prefix=PREFIX)
BAM_STATS       = expand(SAMPLE_DIR + "/{samples}/{samples}_{prefix}_bam_stats.txt", samples=SAMPLE_IDS, prefix=PREFIX)
SORTED_BED      = expand(SAMPLE_DIR + "/{samples}/{samples}_{prefix}_sorted_pos.bed", samples=SAMPLE_IDS, prefix=PREFIX)

GENOME_COV      = expand(SAMPLE_DIR + "/{samples}/{samples}_{prefix}.bedgraph", samples=SAMPLE_IDS, prefix=PREFIX)
GENOME_COV_GZ   = expand(SAMPLE_DIR + "/{samples}/{samples}_{prefix}.bedgraph.gz", samples=SAMPLE_IDS, prefix=PREFIX)
GENOME_COV_TDF  = expand(SAMPLE_DIR + "/{samples}/{samples}_{prefix}.tdf", samples=SAMPLE_IDS, prefix=PREFIX)
GENOME_COV_BW   = expand(SAMPLE_DIR + "/{samples}/{samples}_{prefix}.bw", samples=SAMPLE_IDS, prefix=PREFIX)

# ----------------------------------------------------------------
# Peak-calling
# ----------------------------------------------------------------

if not (("tools" in config.keys()) and ("peakcalling" in config["tools"].keys())):
    sys.exit("The parameter config['tools']['peakcalling'] should be specified in the config file.")

PEAKCALLING_TOOLS = config["tools"]["peakcalling"].split()
PEAKS       = expand(expand(PEAKS_DIR + "/{treat}_vs_{control}/{{peakcaller}}/{treat}_vs_{control}_{{trimmer}}_{{aligner}}_{{peakcaller}}.bed", zip, treat=TREATMENT, control=CONTROL), peakcaller=PEAKCALLING_TOOLS, aligner=MAPPING_TOOLS, trimmer=TRIMMING_TOOLS)
GET_FASTA   = expand(expand(PEAKS_DIR + "/{treat}_vs_{control}/{{peakcaller}}/{treat}_vs_{control}_{{trimmer}}_{{aligner}}_{{peakcaller}}.fasta", zip, treat=TREATMENT, control=CONTROL), peakcaller=PEAKCALLING_TOOLS, aligner=MAPPING_TOOLS, trimmer=TRIMMING_TOOLS)

# ----------------------------------------------------------------
# Peak annotation
# ----------------------------------------------------------------

if not (("tools" in config.keys()) and ("annotation" in config["tools"].keys())):
    sys.exit("The parameter config['tools']['annotation'] should be specified in the config file.")

DISTANCE = config["tools"]["annotation"].split()
GENOMIC_FEAT    = expand(expand(PEAKS_DIR + "/{treat}_vs_{control}/{{peakcaller}}/{treat}_vs_{control}_{{trimmer}}_{{aligner}}_{{peakcaller}}_{{distance}}_annot.bed", zip, treat=TREATMENT, control=CONTROL), peakcaller=PEAKCALLING_TOOLS, distance=DISTANCE, aligner=MAPPING_TOOLS, trimmer=TRIMMING_TOOLS)

print(GENOMIC_FEAT)

GENE_LIST       = expand(expand(PEAKS_DIR + "/{treat}_vs_{control}/{{peakcaller}}/{treat}_vs_{control}_{{trimmer}}_{{aligner}}_{{peakcaller}}_{{distance}}_annot_gene_list.tab", zip, treat=TREATMENT, control=CONTROL), peakcaller=PEAKCALLING_TOOLS, distance=DISTANCE,aligner=MAPPING_TOOLS, trimmer=TRIMMING_TOOLS)

PEAK_MOTIFS     = expand(expand(PEAKS_DIR + "/{treat}_vs_{control}/{{peakcaller}}/peak-motifs/{treat}_vs_{control}_{{trimmer}}_{{aligner}}_{{peakcaller}}_peak-motifs_synthesis.html", zip, treat=TREATMENT, control=CONTROL), peakcaller=PEAKCALLING_TOOLS, aligner=MAPPING_TOOLS, trimmer=TRIMMING_TOOLS)

# ----------------------------------------------------------------
# Visualization & reports
# ----------------------------------------------------------------

## Following not yet properly implemented
IGV = expand(REPORTS_DIR + "/igv_session.xml")

#================================================================#
#                        Rule all                                #
#================================================================#

rule all: 
	"""
	Run all the required analyses.
	"""
	input: \
#            IMPORT, \
            QC, \
#            TRIMMING, \
#            INDEX, \
#            MAPPING, \
#            SORTED_BAM, \
            BAM_STATS, \
#            SORTED_BAM_BAI, \
#            GENOME_INDEX, \
            GENOME_COV_GZ, \
            GENOME_COV_BW, \
#            SORTED_BED, \
#            PEAKS, \
#            GENOMIC_FEAT, \
            GENE_LIST, \
#            PEAK_MOTIFS, \
            IGV, \
            GRAPHICS
	params: qsub=config["qsub"]
	shell: "echo Job done    `date '+%Y-%m-%d %H:%M'`"
