################################################################
## This makefile downloads data for tutorials based on dataset GSE41195
## 
## Ref:     Myers KS, Yan H, Ong IM, Chung D et al. Genome-scale analysis of escherichia coli FNR reveals complex features of transcription factor binding. 
## 			PLoS Genet 2013 Jun;9(6):e1003565. PMID: 23818864
##
## Author: Claire Rioualen
## Date: 2017-11-24
##
## Usage: make -f tutorial_material.mk all ANALYSIS_DIR=/my/dir
##
export LC_ALL=C
export LANG=C

#export ANALYSIS_DIR=$(ANALYSIS)

.PHONY: \
	init\
#	create_dir\
	download_genome_data\
	download_raw_data



#create_dir:
#	@echo "Creating $(ANALYSIS_DIR) directory" && \
#	mkdir -p $(ANALYSIS_DIR) && \
#	mv $(HOME)/SnakeChunks $(ANALYSIS_DIR)/SnakeChunks # to be changed when v4.1 is available


### Download genome & annotations 
download_genome_data:
	mkdir -p $(ANALYSIS_DIR)/genome && \
	wget -nc ftp://ftp.ensemblgenomes.org/pub/bacteria/release-37/fasta/bacteria_0_collection/escherichia_coli_str_k_12_substr_mg1655/dna/Escherichia_coli_str_k_12_substr_mg1655.ASM584v2.dna.chromosome.Chromosome.fa.gz -P $(ANALYSIS_DIR)/genome && \
	wget -nc ftp://ftp.ensemblgenomes.org/pub/bacteria/release-37/gff3/bacteria_0_collection/escherichia_coli_str_k_12_substr_mg1655/Escherichia_coli_str_k_12_substr_mg1655.ASM584v2.37.chromosome.Chromosome.gff3.gz -P $(ANALYSIS_DIR)/genome && \
	wget -nc ftp://ftp.ensemblgenomes.org/pub/release-37/bacteria/gtf/bacteria_0_collection/escherichia_coli_str_k_12_substr_mg1655/Escherichia_coli_str_k_12_substr_mg1655.ASM584v2.37.gtf.gz -P $(ANALYSIS_DIR)/genome
	gunzip -f $(ANALYSIS_DIR)/genome/*.gz

### Download raw data 
download_chipseq_data:
	cd $(ANALYSIS_DIR)
	mkdir -p $(ANALYSIS_DIR)/ChIP-seq/fastq/input1 $(ANALYSIS_DIR)/ChIP-seq/fastq/FNR1
	curl --create-dirs ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR576/SRR576934/SRR576934.fastq.gz -o $(ANALYSIS_DIR)/ChIP-seq/fastq/FNR1/FNR1.fastq.gz
	curl --create-dirs ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR576/SRR576938/SRR576938.fastq.gz -o $(ANALYSIS_DIR)/ChIP-seq/fastq/input1/input1.fastq.gz

download_rnaseq_data:
	cd $(ANALYSIS_DIR) && \
	mkdir -p $(ANALYSIS_DIR)/RNA-seq/fastq/WT1 $(ANALYSIS_DIR)/RNA-seq/fastq/WT2 $(ANALYSIS_DIR)/RNA-seq/fastq/dFNR1 $(ANALYSIS_DIR)/RNA-seq/fastq/dFNR2 && \
	curl --create-dirs  ftp.sra.ebi.ac.uk/vol1/fastq/SRR534/001/SRR5344681/SRR5344681_1.fastq.gz -o $(ANALYSIS_DIR)/RNA-seq/fastq/WT1/WT1_1.fastq.gz && \
	curl --create-dirs  ftp.sra.ebi.ac.uk/vol1/fastq/SRR534/001/SRR5344681/SRR5344681_2.fastq.gz -o $(ANALYSIS_DIR)/RNA-seq/fastq/WT1/WT1_2.fastq.gz && \
	curl --create-dirs  ftp.sra.ebi.ac.uk/vol1/fastq/SRR534/002/SRR5344682/SRR5344682_1.fastq.gz -o $(ANALYSIS_DIR)/RNA-seq/fastq/WT2/WT2_1.fastq.gz && \
	curl --create-dirs  ftp.sra.ebi.ac.uk/vol1/fastq/SRR534/002/SRR5344682/SRR5344682_2.fastq.gz -o $(ANALYSIS_DIR)/RNA-seq/fastq/WT2/WT2_2.fastq.gz && \
	curl --create-dirs  ftp.sra.ebi.ac.uk/vol1/fastq/SRR534/003/SRR5344683/SRR5344683_1.fastq.gz -o $(ANALYSIS_DIR)/RNA-seq/fastq/dFNR1/dFNR1_1.fastq.gz && \
	curl --create-dirs  ftp.sra.ebi.ac.uk/vol1/fastq/SRR534/003/SRR5344683/SRR5344683_2.fastq.gz -o $(ANALYSIS_DIR)/RNA-seq/fastq/dFNR1/dFNR1_2.fastq.gz && \
	curl --create-dirs  ftp.sra.ebi.ac.uk/vol1/fastq/SRR534/004/SRR5344684/SRR5344684_1.fastq.gz -o $(ANALYSIS_DIR)/RNA-seq/fastq/dFNR2/dFNR2_1.fastq.gz && \
	curl --create-dirs  ftp.sra.ebi.ac.uk/vol1/fastq/SRR534/004/SRR5344684/SRR5344684_2.fastq.gz -o $(ANALYSIS_DIR)/RNA-seq/fastq/dFNR2/dFNR2_2.fastq.gz


download_rnaseq_data_prev:
	cd $(ANALYSIS_DIR) && \
	mkdir -p $(ANALYSIS_DIR)/RNA-seq/fastq/WT1 $(ANALYSIS_DIR)/RNA-seq/fastq/WT2 $(ANALYSIS_DIR)/RNA-seq/fastq/dFNR1 $(ANALYSIS_DIR)/RNA-seq/fastq/dFNR2 && \
	wget -nc ftp.sra.ebi.ac.uk/vol1/fastq/SRR534/001/SRR5344681/SRR5344681_1.fastq.gz ftp.sra.ebi.ac.uk/vol1/fastq/SRR534/001/SRR5344681/SRR5344681_2.fastq.gz -P $(ANALYSIS_DIR)/RNA-seq/fastq/WT1 && \
	wget -nc ftp.sra.ebi.ac.uk/vol1/fastq/SRR534/002/SRR5344682/SRR5344682_1.fastq.gz ftp.sra.ebi.ac.uk/vol1/fastq/SRR534/002/SRR5344682/SRR5344682_2.fastq.gz -P $(ANALYSIS_DIR)/RNA-seq/fastq/WT2 && \
	wget -nc ftp.sra.ebi.ac.uk/vol1/fastq/SRR534/003/SRR5344683/SRR5344683_1.fastq.gz ftp.sra.ebi.ac.uk/vol1/fastq/SRR534/003/SRR5344683/SRR5344683_2.fastq.gz -P $(ANALYSIS_DIR)/RNA-seq/fastq/dFNR1 && \
	wget -nc ftp.sra.ebi.ac.uk/vol1/fastq/SRR534/004/SRR5344684/SRR5344684_1.fastq.gz ftp.sra.ebi.ac.uk/vol1/fastq/SRR534/004/SRR5344684/SRR5344684_2.fastq.gz -P $(ANALYSIS_DIR)/RNA-seq/fastq/dFNR2

mv_previous:
	mv $(ANALYSIS_DIR)/RNA-seq/fastq/WT1/SRR5344681_1.fastq.gz $(ANALYSIS_DIR)/RNA-seq/fastq/WT1/WT1_1.fastq.gz && \
	mv $(ANALYSIS_DIR)/RNA-seq/fastq/WT1/SRR5344681_2.fastq.gz $(ANALYSIS_DIR)/RNA-seq/fastq/WT1/WT1_2.fastq.gz && \
	mv $(ANALYSIS_DIR)/RNA-seq/fastq/WT2/SRR5344682_1.fastq.gz $(ANALYSIS_DIR)/RNA-seq/fastq/WT2/WT2_1.fastq.gz && \
	mv $(ANALYSIS_DIR)/RNA-seq/fastq/WT2/SRR5344682_2.fastq.gz $(ANALYSIS_DIR)/RNA-seq/fastq/WT2/WT2_2.fastq.gz && \
	mv $(ANALYSIS_DIR)/RNA-seq/fastq/dFNR1/SRR5344683_1.fastq.gz $(ANALYSIS_DIR)/RNA-seq/fastq/dFNR1/dFNR1_1.fastq.gz && \
	mv $(ANALYSIS_DIR)/RNA-seq/fastq/dFNR1/SRR5344683_2.fastq.gz $(ANALYSIS_DIR)/RNA-seq/fastq/dFNR1/dFNR1_2.fastq.gz && \
	mv $(ANALYSIS_DIR)/RNA-seq/fastq/dFNR2/SRR5344684_1.fastq.gz $(ANALYSIS_DIR)/RNA-seq/fastq/dFNR2/dFNR2_1.fastq.gz && \
	mv $(ANALYSIS_DIR)/RNA-seq/fastq/dFNR2/SRR5344684_2.fastq.gz $(ANALYSIS_DIR)/RNA-seq/fastq/dFNR2/dFNR2_2.fastq.gz
#	gunzip -f -c $(ANALYSIS_DIR)/RNA-seq/fastq/WT1/SRR5344681_1.fastq.gz > $(ANALYSIS_DIR)/RNA-seq/fastq/WT1/WT1_1.fastq; rm -f $(ANALYSIS_DIR)/RNA-seq/fastq/WT1/SRR5344681_1.fastq.gz && \
#	gunzip -f -c $(ANALYSIS_DIR)/RNA-seq/fastq/WT1/SRR5344681_2.fastq.gz > $(ANALYSIS_DIR)/RNA-seq/fastq/WT1/WT1_2.fastq; rm -f $(ANALYSIS_DIR)/RNA-seq/fastq/WT1/SRR5344681_2.fastq.gz && \
#	gunzip -f -c $(ANALYSIS_DIR)/RNA-seq/fastq/WT2/SRR5344682_1.fastq.gz > $(ANALYSIS_DIR)/RNA-seq/fastq/WT2/WT2_1.fastq; rm -f $(ANALYSIS_DIR)/RNA-seq/fastq/WT2/SRR5344682_1.fastq.gz && \
#	gunzip -f -c $(ANALYSIS_DIR)/RNA-seq/fastq/WT2/SRR5344682_2.fastq.gz > $(ANALYSIS_DIR)/RNA-seq/fastq/WT2/WT2_2.fastq; rm -f $(ANALYSIS_DIR)/RNA-seq/fastq/WT2/SRR5344682_2.fastq.gz && \
#	gunzip -f -c $(ANALYSIS_DIR)/RNA-seq/fastq/dFNR1/SRR5344683_1.fastq.gz > $(ANALYSIS_DIR)/RNA-seq/fastq/dFNR1/dFNR1_1.fastq; rm -f $(ANALYSIS_DIR)/RNA-seq/fastq/dFNR1/SRR5344683_1.fastq.gz && \
#	gunzip -f -c $(ANALYSIS_DIR)/RNA-seq/fastq/dFNR1/SRR5344683_2.fastq.gz > $(ANALYSIS_DIR)/RNA-seq/fastq/dFNR1/dFNR1_2.fastq; rm -f $(ANALYSIS_DIR)/RNA-seq/fastq/dFNR1/SRR5344683_2.fastq.gz && \
#	gunzip -f -c $(ANALYSIS_DIR)/RNA-seq/fastq/dFNR2/SRR5344684_1.fastq.gz > $(ANALYSIS_DIR)/RNA-seq/fastq/dFNR2/dFNR2_1.fastq; rm -f $(ANALYSIS_DIR)/RNA-seq/fastq/dFNR2/SRR5344684_1.fastq.gz && \
#	gunzip -f -c $(ANALYSIS_DIR)/RNA-seq/fastq/dFNR2/SRR5344684_2.fastq.gz > $(ANALYSIS_DIR)/RNA-seq/fastq/dFNR2/dFNR2_2.fastq; rm -f $(ANALYSIS_DIR)/RNA-seq/fastq/dFNR2/SRR5344684_2.fastq.gz


### Copy metadata from SnakeChunks library to analysis directory

copy_metadata:
	mkdir -p metadata ; rsync -ruptvl SnakeChunks/examples/GSE41195/* metadata

### all

all: \
	init\
#	create_dir\
	copy_metadata\
	download_genome_data\
	download_raw_data

