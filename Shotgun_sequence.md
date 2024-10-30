#### 1. read quality control - FastQC
##### 1.1 FastQC Installation

    conda create --prefix ~/bio/bin/fastqc_env
    conda activate ~/bio/bin/fastqc_env
    conda install -c bioconda fastqc
    fastqc -h  
Check [here](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/Help/) for FastQC documentation.

##### 1.2 Slurm - fastqc.slurm

    #!/bin/bash
    #SBATCH --job-name=fastqc      # Job name
    #SBATCH --output=%x.log  # Job's standard output and error log
    #SBATCH --nodes=1             # Run all processes on a single node
    #SBATCH --ntasks=1            # Run 1 tasks
    #SBATCH --cpus-per-task=16    # Number of CPU cores per task
    #SBATCH --mem=50G            # Job memory request
    #SBATCH --time=50:00:00       # processing 20 paired-end Illumina reads spends 30 min
    #SBATCH --mail-user=lianchun.yi1@ucalgary.ca  # Send the job information to this email
    #SBATCH --mail-type=ALL                       # Send the type: <BEGIN><FAIL><END>
    pwd; hostname; date

    conda activate ~/bio/bin/fastqc_env
    cd /work/ebg_lab/eb/Lianchun/shotgun_2024Aug
    fastqc *.gz -o ./out_put --svg --noextract -t 16 -k

Results will be saved in /work/ebg_lab/eb/Lianchun/shotgun_2024Aug/out_put

#### 2. Raw reads filtration - BBduk
##### 2.1 Installation
Check BBMap installation
##### 2.1 Slurm - ftm.slurm

    #!/bin/bash
    #SBATCH --job-name=BBduk_ftm      # Job name
    #SBATCH --output=%x.log  # Job's standard output and error log
    #SBATCH --nodes=1             # Run all processes on a single node
    #SBATCH --ntasks=1            # Run 1 tasks
    #SBATCH --cpus-per-task=32    # Number of CPU cores per task
    #SBATCH --mem=50G            # Job memory request
    #SBATCH --time=24:00:00       # processing 20 paired-end Illumina reads spends 21 min
    #SBATCH --mail-user=lianchun.yi1@ucalgary.ca  # Send the job information to this email
    #SBATCH --mail-type=ALL                       # Send the type: <BEGIN><FAIL><END>
    pwd; hostname; date

    cd /work/ebg_lab/eb/Lianchun/shotgun_2024Aug

    bbduk.sh in1=Li49157-LY-2024Aug-SedTrip1_S6_R1_001.fastq.gz in2=Li49157-LY-2024Aug-SedTrip1_S6_R2_001.fastq.gz out1=Li49157_trimmed_R1.fastq.gz out2=Li49157_trimmed_R2.fastq.gz ftm=5 t=32


#### 4. Metagenomic assembly - MetaSPAdes or Megahit
##### 4.1 Installation
**MetaSPAdes** is a module in SPAde. The steps for installing the SPAde are shown here.

    wget https://github.com/ablab/spades/releases/download/v4.0.0/SPAdes-4.0.0-Linux.tar.gz
    tar -xzf SPAdes-4.0.0-Linux.tar.gz
    rm SPAdes-4.0.0-Linux.tar.gz
    nano ~/.bashrc # export PATH=$PATH:/home/lianchun.yi1/software/SPAdes-4.0.0-Linux/bin
    source ~/bio/bin/3.10_python-env/bin/activate # minimal supported python version is 3.8
    spades.py --test

**Megahit**

    conda install -c bioconda megahit
    megahit --version

##### 4.4 Slurm
**metaSPAdes.slurm**

    #!/bin/bash
    #SBATCH --job-name=metaspades_separate_unmerged      # Job name
    #SBATCH --output=%x.log  # Job's standard output and error log
    #SBATCH --nodes=1             # Run all processes on a single node
    #SBATCH --ntasks=1            # Run 1 tasks
    #SBATCH --cpus-per-task=32    # Number of CPU cores per task
    #SBATCH --mem=100G            # Job memory request
    #SBATCH --time=24:00:00       # processing 20 paired-end Illumina reads spends x hours
    #SBATCH --mail-user=lianchun.yi1@ucalgary.ca  # Send the job information to this email
    #SBATCH --mail-type=ALL                       # Send the type: <BEGIN><FAIL><END>
    pwd; hostname; date

    source ~/bio/bin/3.10_python-env/bin/activate
    cd /work/ebg_lab/eb/Lianchun/shotgun_2024Aug

    samples=("Li49157-LY-2024Aug-SedTrip1_S6" "Li49158-LY-2024Aug-SedTrip2_S7" "Li49159-LY-2024Aug-SedTrip3_S8"
         "Li49160-LY-2024Aug-MatSite1_S9" "Li49161-LY-2024Aug-MatSite3_S10" "Li49162-LY-2024Aug-MatSite4_S11"
         "Li49163-LY-2024Aug-MatSite5_S12" "Li49164-LY-2024Aug-MatSite6_S13" "Li49165-LY-2024Aug-MatSite7_S14"
         "Li49166-LY-2024Aug-MatSite8_S15")


    main_output_dir="./metaspades_assembly"


    for sample in "${samples[@]}"; do
        R1="unmerged_norm_${sample}_R1.fastq.gz"
        R2="unmerged_norm_${sample}_R2.fastq.gz"
        output_dir="$main_output_dir/${sample}_separate_unmerged"
        mkdir -p "$output_dir"
        spades.py --meta -1 $R1 -2 $R2 -o $output_dir --threads 32
    done

**megahit.slurm**

#### 5. Annotaion - Metaerg
##### 5.1 [Installation](https://github.com/Wednesdaysama/evolutionary_adaptation/blob/main/installation.md)
##### 5.2 Slurm - metaerg.slurm

#### 6. Per-contig sequencing coverage estimation - BBMap / MetaBat2
##### 6.1 Installation
**BBMap**
    
    wget https://sourceforge.net/projects/bbmap/files/BBMap_39.10.tar.gz/download -O BBMap.tar.gz
    tar -xvzf BBMap.tar.gz
    rm BBMap.tar.gz
    nano ~/.bashrc # export PATH=$PATH:/home/lianchun.yi1/software/bbmap
    source ~/.bashrc
    bbmap.sh --version

Once BBMap is installed, we can directly use **BBNorm** for read normalization or **BBMerge** for merging overlapping reads. 

**MetaBat2**


    

##### 6.2 Slurm


#### 7. Binning - MetaBat2 

#### 8. Contamination and completeness checking - CheckM2


## overview
1. read quality fastqc software to visualize the data?
2. BBmap, count K-mer count 30-70 long,  show reads for assembly
3. metahit for assembly, look at the N50 value, plot the distribution with contig length, remove < 1000 bp.
4. put 10 samples together and assemble them together, 0.1%. kit type? Nextseq 2000
5. BBmap again, give a file that each the contig what is their depth
6. metabat2/3 to bin the data into mags
7. checkm2 to get the quality of the bins
