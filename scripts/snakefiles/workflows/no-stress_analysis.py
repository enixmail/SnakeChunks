"""Workflow for the analysis of transcriptomic RNA-seq data in
Desulfovibrio desulfuricans.

Reference genome: Desulfovibrio desulfuricans ATCC_27774 uid59213

Collaboration with Alain Dolla
Data from : Jeff Cole

"""

#================================================================#
#                        Imports/Configuration file              #
#================================================================#

import os
import subprocess
from snakemake.utils import R

configfile: "scripts/snakefiles/workflows/no-stress_analysis_config.json"
workdir: config["dir"]["base"] # Local Root directory for the project. Should be adapted for porting.
## A MODIFIER
#LIST_ALL_COUNTS = "data/1258-BRM/N1/N1_bowtie2_mm1_sorted_name_count.txt", "data/1258-BRM/N2/N2_bowtie2_mm1_sorted_name_count.txt", "data/1258-BRM/N4/N4_bowtie2_mm1_sorted_name_count.txt", "data/1258-BRM/NN2/NN2_bowtie2_mm1_sorted_name_count.txt", "data/1258-BRM/NN4/NN4_bowtie2_mm1_sorted_name_count.txt", "data/1258-BRM/NN5/NN5_bowtie2_mm1_sorted_name_count.txt"

path = "scripts/python-scripts/"
sys.path.append(path) # For find my module "read_analysis_table_lib"
import util # read_analysis_table_lib is a module where you can find two functions who give you several lists for peak-callers softwares



#================================================================#
#                         Includes                               #
#================================================================#

include: "../rules/flowcharts.rules"
# include: "../rules/gunzip.rules"
# include: "../rules/rsync.rules"
include: "../rules/fastqc.rules"
include: "../rules/sickle_paired_ends.rules"
include: "../rules/bowtie2_build.rules"
include: "../rules/bowtie2_paired_ends.rules"
include: "../rules/convert_sam_to_bam.rules"
include: "../rules/sorted_bam.rules"
include: "../rules/htseq.rules"
# include: "../rules/featurecounts.rules"
include: "../rules/index_bam.rules"

#================================================================#
#     Global variables                                           #
#================================================================#

# Usage: snakemake -c "qsub {params.qsub}" -j 25
# workdir:"/home/desulfo-no" # Root directory for the project. Should be adapted for porting.
# workdir: "/home/desulfo-no/no-stress_project/data/1258-BRM" # Root directory for the project. Should be adapted for porting.
# workdir:"/home/no-stress/Documents/no-stress_project/data/1258-BRM" # Local Root directory for the project. Should be adapted for porting.
# workdir: os.getcwd() # Local Root directory for the project. Should be adapted for porting.
SAMPLE_IDS=util.read_sample_ids(config["files"]["samples"], column=1, verbose=0)

#DATASETS_FWD = expand("{sample_id}" + config["suffix"]["reads_fwd"], sample_id=SAMPLE_IDS)
#DATASETS_REV = expand("{sample_id}" + config["suffix"]["reads_rev"], sample_id=SAMPLE_IDS)
#DATASETS = DATASETS_FWD + DATASETS_REV

DATASETS = "N1_1 N1_2 N2_1 N2_2 N4_1 N4_2 S1_1 S1_2 S4_1 S4_2 S5_1 S5_2 NN2_1 NN2_2 NN4_1 NN4_2 NN5_1 NN5_2 SN1_1 SN1_2 SN2_1 SN2_2 SN5_1 SN5_2".split() # list of files
DATA_DIRS = "N1 N1 N2 N2 N4 N4 S1 S1 S4 S4 S5 S5 NN2 NN2 NN4 NN4 NN5 NN5 SN1 SN1 SN2 SN2 SN5 SN5".split() # list all directories

RAWR_FILES_FWD, RAWR_DIRS_FWD, RAWR_BASENAMES_FWD = util.glob_multi_dir(SAMPLE_IDS, "*" + config["suffix"]["reads_fwd"] + ".fastq.gz", config["dir"]["data_root"], config["suffix"]["reads_fwd"] + ".fastq.gz")

RAWR_FILES, RAWR_DIRS, RAWR_BASENAMES = util.glob_multi_dir(SAMPLE_IDS, "*_?" + ".fastq.gz", config["dir"]["data_root"], ".fastq.gz")

# Variables for EdgeR (Differential expression) 
COND_1 = config["Diff_Exp"]["cond1"]
COND_2 = config["Diff_Exp"]["cond2"]

COUNT_FILES = expand(config["dir"]["results"] + "{sample_id}/{sample_id}_sickle_pe_q" + config["sickle"]["threshold"] + "_bowtie2_pe_sorted_" + config["htseq"]["order"] + "_HTSeqcount.tab", sample_id = SAMPLE_IDS)

# Results with Htseq
RESULTS_EDGER = expand(config["dir"]["results"] + "DEG/{cond_1}_vs_{cond_2}/{cond_1}_VS_{cond_2}_sickle_pe_q" + config["sickle"]["threshold"] + "_bowtie2_pe_sorted_" + config["htseq"]["order"] + config["edgeR"]["software"] +".tab", zip, cond_1=COND_1, cond_2=COND_2)
# Results with subreads
# RESULTS_EDGER = expand(config["dir"]["results"] + "DEG/{cond_1}_vs_{cond_2}/{cond_1}_VS_{cond_2}_sickle_pe_q" + config["sickle"]["threshold"] + "_bowtie2_pe__featurecounts" + config["edgeR"]["software"] +".tab", zip, cond_1=COND_1, cond_2=COND_2)


LOGS_DESEQ2 = expand(config["dir"]["results"] + "DEG/{cond_1}_VS_{cond_2}_sickle_pe_q" + config["sickle"]["threshold"] + "_bowtie2_pe_sorted_" + config["htseq"]["order"] + config["DESeq2"]["software"] + ".log", zip, cond_1=COND_1, cond_2=COND_2)

# Results with Htseq
# RESULTS_DESEQ2 = expand(config["dir"]["results"] + "DEG/{cond_1}_vs_{cond_2}/{cond_1}_VS_{cond_2}_sickle_pe_q" + config["sickle"]["threshold"] + "_bowtie2_pe_sorted_" + config["htseq"]["order"] + config["DESeq2"]["software"] + ".tab", zip, cond_1=COND_1, cond_2=COND_2)
RESULTS_DESEQ2 = expand(config["dir"]["results"] + "DEG/{cond_1}_vs_{cond_2}/{cond_1}_VS_{cond_2}_{trimmed}_{alignment}_sorted_" + config["htseq"]["order"] + config["DESeq2"]["software"] + ".tab", zip, cond_1=COND_1, cond_2=COND_2, trimmed = "sickle_pe_q" + config["sickle"]["threshold"], alignment = "bowtie2_pe")
# Results with subreads
# RESULTS_DESEQ2 = expand(config["dir"]["results"] + "DEG/{cond_1}_vs_{cond_2}/{cond_1}_VS_{cond_2}_sickle_pe_q" + config["sickle"]["threshold"] + "_bowtie2_pe_featurecounts" + config["DESeq2"]["software"] + ".tab", zip, cond_1=COND_1, cond_2=COND_2)
# RESULTS_DESEQ2 = expand(config["dir"]["results"] + "DEG/{cond_1}_vs_{cond_2}/{cond_1}_VS_{cond_2}_{trimmed}_{alignment}_featurecounts" + config["DESeq2"]["software"] + ".tab", zip, cond_1=COND_1, cond_2=COND_2, trimmed = "sickle_pe_q" + config["sickle"]["threshold"], alignment = "bowtie2_pe")


PARAMS_R = config["dir"]["results"] + "DEG/sickle_pe_q" + config["sickle"]["threshold"] + "_bowtie2_pe_sorted_" + config["htseq"]["order"] + "_params.R"
ALL_COUNTS = config["dir"]["results"] + "DEG/sickle_pe_q" + config["sickle"]["threshold"] + "_bowtie2_pe_sorted_" + config["htseq"]["order"] + "_allcounts.tab"

include: "../rules/HTseq_allcount_params.rules"
include: "../rules/edgeR.rules"
include: "../rules/DESeq2.rules"

#================================================================#
#                         Workflow                               #
#================================================================#

################################################################
## Define the lists of requested files
################################################################


TRIMMED = "sickle_pe_q" + config["sickle"]["threshold"]
ALIGNMENT = "bowtie2_pe"
SORTING = "sorted_" + config["htseq"]["order"]

GUNZIP_FASTQ=expand(config["dir"]["reads_source"] + "{data_dir}/{dataset}.fastq", zip, dataset=DATASETS, data_dir=DATA_DIRS)
RSYNC_FASTQ=expand(config["dir"]["results"] + "{data_dir}/{dataset}.fastq", zip, dataset=DATASETS, data_dir=DATA_DIRS)

RAW_FASTQC=expand(config["dir"]["results"] + "{data_dir}/{dataset}_fastqc/", zip, dataset=DATASETS, data_dir=DATA_DIRS)
TRIMMED_FASTQC=expand(config["dir"]["results"] + "{data_dir}/{dataset}_" + TRIMMED + "_fastqc/", zip, dataset=DATASETS, data_dir=DATA_DIRS)

TRIMMED_FASTQ=expand(config["dir"]["results"] + "{sample_ids}/{sample_ids}_{single_trimmed}.fastq", sample_ids=SAMPLE_IDS, single_trimmed= "single_sickle_pe_q" + config["sickle"]["threshold"])
TRIMMED_SUMMARY=expand(config["dir"]["results"] + "{sample_ids}/{sample_ids}_{trimmed}_summary.txt", sample_ids=SAMPLE_IDS, trimmed=TRIMMED)
TRIMMED_FW=expand(config["dir"]["results"] + "{sample_ids}/{sample_ids}" + config["suffix"]["reads_fwd"] + "_{trimmed}.fastq", sample_ids=SAMPLE_IDS, trimmed=TRIMMED)
TRIMMED_REV=expand(config["dir"]["results"] + "{sample_ids}/{sample_ids}" + config["suffix"]["reads_rev"] + "_{trimmed}.fastq", sample_ids=SAMPLE_IDS, trimmed= TRIMMED)
TRIMMED_ALL=TRIMMED_FW, TRIMMED_REV

BOWTIE2_INDEX = config["dir"]["genome"] + config["genome"]["organism"] + ".1.bt2"
BOWTIE2 = expand(config["dir"]["results"] + "{sample_ids}/{sample_ids}_{trimmed}_{alignment}.sam", sample_ids=SAMPLE_IDS, trimmed=TRIMMED, alignment=ALIGNMENT)

SAM_BAM = expand(config["dir"]["results"] + "{sample_ids}/{sample_ids}_{trimmed}_{alignment}.bam", sample_ids=SAMPLE_IDS, trimmed=TRIMMED, alignment=ALIGNMENT)
BAM_SORTED = expand(config["dir"]["results"] + "{sample_ids}/{sample_ids}_{trimmed}_{alignment}_{sorting}.bam", sample_ids=SAMPLE_IDS, trimmed=TRIMMED, alignment=ALIGNMENT, sorting=SORTING)
BAM_INDEX = expand(config["dir"]["results"] + "{sample_ids}/{sample_ids}_{trimmed}_{alignment}_{sorting}.bam.bai", sample_ids=SAMPLE_IDS, trimmed=TRIMMED, alignment=ALIGNMENT, sorting=SORTING)

HTSEQ_COUNT = expand(config["dir"]["results"] + "{sample_ids}/{sample_ids}_{trimmed}_{alignment}_{sorting}_HTSeqcount.tab", sample_ids=SAMPLE_IDS, trimmed=TRIMMED, alignment=ALIGNMENT, sorting=SORTING)
OUT_HTSEQ = PARAMS_R, ALL_COUNTS

rule all:
    """Run workflow for each replica of each experience"""
    input:
        # GUNZIP_FASTQ, \
        #;RSYNC_FASTQ, \
        RAW_FASTQC, \
        # TRIMMED_ALL
        # TRIMMED_FASTQ, \
        #TRIMMED_fatal
        TRIMMED_FASTQC, \
        # BOWTIE2_INDEX, \
        # BOWTIE2
        # SAM_BAM
        # BAM_SORTED, \
        BAM_INDEX, \
        # HTSEQ_COUNT, \
        # OUT_HTSEQ
        RESULTS_EDGER, \
        RESULTS_DESEQ2
        # expand(config["dir"]["results"] + "{data_dir}/{dataset}_sickle_pe_q" + config["sickle"]["threshold"] + "_fastqc/", zip, dataset=DATASETS, data_dir=DATA_DIRS), \
        # expand(config["dir"]["results"] + "{data_dir}/{data_dir}" + config["sickle"]["threshold"] + ".fastq", zip, dataset=DATASETS, data_dir=DATA_DIRS), \
        # expand(config["data_root_dir"] + "{data_dir}/{data_dir}_trimmed_thr" + THRESHOLD + ".fastq.gz", data_dir=DATA_DIRS), \
        # expand(config["data_root_dir"] + "{data_dir}/{data_dir}_bowtie2_mm" + config["bowtie2"]["max_mismatches"] + ".sam", data_dir=DATA_DIRS), \
        # expand(config["data_root_dir"] + "{data_dir}/{data_dir}_bowtie2_mm" + config["bowtie2"]["max_mismatches"] + ".bam", data_dir=DATA_DIRS), \
        # expand(config["data_root_dir"] + "{data_dir}/{data_dir}_bowtie2_mm" + config["bowtie2"]["max_mismatches"] + "_sorted_" + config["htseq"]["order"] + ".bam", data_dir=DATA_DIRS), \
        # expand(config["dir"]["results"] + "{data_dir}/{data_dir}_sickle_pe_q" + config["sickle"]["threshold"] + "_bowtie2_sorted_pos.bam.bai", data_dir=DATA_DIRS), \
        # expand(config["dir"]["results"] + "{sample_ids}/{sample_ids}_{trimmed}_{alignment}.sam", sample_ids=SAMPLE_IDS), \
        # expand(config["dir"]["results"] + "{sample_ids}/{sample_ids}_{trimmed}_{alignment}_featurecounts.tab", sample_ids=SAMPLE_IDS, trimmed = "sickle_pe_q" + config["sickle"]["threshold"], alignment = "bowtie2_pe"), \
        # PARAMS_R, \
        # ALL_COUNTS, \


    shell: "echo 'job done'"


# ruleorder: bowtie2_paired_end > sorted_bam
# ruleorder: sorted_bam > index_bam





################################################################
## Build the report (including DAG and rulegraph flowcharts).
from snakemake.utils import report

## Bulleted list of samples for the report
RAWR_FILES_OL = util.report_numbered_list(RAWR_FILES)
SAMPLE_IDS_OL=util.report_numbered_list(SAMPLE_IDS)
RAW_FASTQC_OL=util.report_numbered_list(RAW_FASTQC)
TRIMMED_FASTQC_OL = util.report_numbered_list(TRIMMED_FASTQC)
TRIMMED_FW_OL = util.report_numbered_list(TRIMMED_FW)
TRIMMED_REV_OL = util.report_numbered_list(TRIMMED_REV)
BOWTIE2_OL = util.report_numbered_list(BOWTIE2)
SAM_BAM_OL = util.report_numbered_list(SAM_BAM)
BAM_SORTED_OL = util.report_numbered_list(BAM_SORTED)
BAM_INDEX_OL = util.report_numbered_list(BAM_INDEX)
HTSEQ_COUNT_OL = util.report_numbered_list(HTSEQ_COUNT)
PARAMS_R_OL = PARAMS_R
ALL_COUNTS_OL = ALL_COUNTS
RESULTS_EDGER_OL = util.report_numbered_list(RESULTS_EDGER)
RESULTS_DESEQ2_OL = util.report_numbered_list(RESULTS_DESEQ2)


rule report:
    """
    Generate a report with the list of datasets + summary of the results.
    """
    input:  dag_pdf=config["reports"]["dag"] + ".pdf", \
            dag_png=config["reports"]["dag"] + ".png", \
            rulegraph_pdf=config["reports"]["rulegraph"] + ".pdf", \
            rulegraph_png=config["reports"]["rulegraph"] + ".png"
    output: html=config["dir"]["reports"] + "/report.html"
    run:
        report("""
        ============================
        RNA-seq analysis - Jeff Cole
        ============================
        
        :Project:              Jeff Cole
        :Collaboration:        Alain Dolla
        :Analysis workflow:    Justine Long, Jeanne Chèneby & Jacques van Helden
        
        Contents
        ========
        
        - `Flowcharts`_
        - `Datasets`_
            - `Sample identifiers`_
            - `Raw reads`_
        - `Result files`_
            - `Quality control (raw reads)`_
            - `Quality control (trimmed reads)`_
            - `Trimming (reads forward, with Sickle)`_
            - `Trimming (reads reverse, with Sickle)`_
            - `Alignment (Bowtie2)`_
            - `Alignment in BAM (Samtools)`_
            - `Sorting by names or positions (Samtools)`_
            - `Index of the mapping results`_
            - `Count (HTSeq)`_
            - `Parameters file for DE`_
            - `All count in one file`_
            - `Differential Expression (edgeR)`_
            - `Differential Expression (DESeq2)`_


        -----------------------------------------------------

        Flowcharts
        ==========

        - Sample treatment: dag_pdf_
        - Workflow: rulegraph_pdf_

        .. image:: rulegraph.png

        -----------------------------------------------------

        Datasets
        ========
        
        Sample identifiers
        ------------------

        {SAMPLE_IDS_OL} 


        Raw reads
        ----------
        {RAWR_FILES_OL}



        Result files
        ============

        Quality control (raw reads)
        ---------------------------

        {RAW_FASTQC_OL}
        
        
        Trimming (reads forward, with Sickle)
        -------------------------------------

        {TRIMMED_FW_OL}

        Trimming (reads reverse, with Sickle)
        -------------------------------------

        {TRIMMED_REV_OL}

        Quality control (trimmed reads)
        -------------------------------

        {TRIMMED_FASTQC_OL}
        
        Alignment (Bowtie2)
        -------------------

        {BOWTIE2_OL}


        Alignment in BAM (Samtools)
        ----------------------------

        {SAM_BAM_OL}


        Sorting by names or positions (Samtools)
        ----------------------------------------

        {BAM_SORTED_OL}


        Index of the mapping results 
        -----------------------------

        {BAM_INDEX_OL}


        Count (HTSeq)
        -------------

        {HTSEQ_COUNT_OL}


        Parameters file for DE
        ----------------------

            {PARAMS_R_OL}


        All count in one file
        ----------------------

            {ALL_COUNTS_OL}


        Differential Expression (edgeR)
        -------------------------------

        {RESULTS_EDGER_OL}


        Differential Expression (DESeq2)
        --------------------------------

        {RESULTS_DESEQ2_OL}







        """, output.html, metadata="Jacques van Helden (Jacques.van-Helden@univ-amu.fr)", **input)