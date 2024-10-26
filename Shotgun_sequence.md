#### 1. read quality control - FastQC
##### 1.1 FastQC Installation

    conda create --prefix ~/bio/bin/fastqc_env
    conda activate ~/bio/bin/fastqc_env
    conda install -c bioconda fastqc
    fastqc -h  
Check [here](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/Help/) for FastQC documentation.

##### 1.2 Command line

    cd /work/ebg_lab/eb/Lianchun/shotgun_2024Aug/
    conda activate ~/bio/bin/fastqc_env
    fastqc *.gz -o ./out_put --svg

