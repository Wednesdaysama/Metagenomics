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

### 2. Reads coverage-normalization
##### installation
Check BBMap installation
##### Slurm - bbnorm.slurm

    #!/bin/bash
    #SBATCH --job-name=bbnorm      # Job name
    #SBATCH --output=%x.log  # Job's standard output and error log
    #SBATCH --nodes=1             # Run all processes on a single node
    #SBATCH --ntasks=1            # Run 1 tasks
    #SBATCH --cpus-per-task=16    # Number of CPU cores per task
    #SBATCH --mem=50G            # Job memory request
    #SBATCH --time=24:00:00       # processing 20 paired-end Illumina reads spends x min
    #SBATCH --mail-user=lianchun.yi1@ucalgary.ca  # Send the job information to this email
    #SBATCH --mail-type=ALL                       # Send the type: <BEGIN><FAIL><END>
    pwd; hostname; date

    cd /work/ebg_lab/eb/Lianchun/shotgun_2024Aug

    bbnorm.sh in1=Li49158-LY-2024Aug-SedTrip2_S7_R1_001.fastq.gz in2=Li49158-LY-2024Aug-SedTrip2_S7_R2_001.fastq.gz \ out1=norm_Li49158-LY-2024Aug-SedTrip2_S7_R1_001.fastq.gz out2=norm_Li49158-LY-2024Aug-SedTrip2_S7_R2_001.fastq.gz \ target=100 min=4



#### *. Per-contig sequencing coverage estimation - BBMap / MetaBat
##### Installation
    
    wget https://sourceforge.net/projects/bbmap/files/BBMap_39.10.tar.gz/download -O BBMap.tar.gz
    tar -xvzf BBMap.tar.gz
    rm BBMap.tar.gz
    nano ~/.bashrc # export PATH=$PATH:/home/lianchun.yi1/software/bbmap
    source ~/.bashrc
    bbmap.sh --version

Once BBMap is installed, we can directly use **BBNorm** for read normalization or **BBMerge** for merging overlapping reads. 

#### *. Metagenomic assembly - MetaSPAdes or Megahit

#### *. Binning - MetaBat 

## overview
1. read quality fastqc software to visualize the data?
2. BBmap, count K-mer count 30-70 long,  show reads for assembly
3. metahit for assembly, look at the N50 value, plot the distribution with contig length, remove < 1000 bp.
4. put 10 samples together and assemble them together, 0.1%. kit type? Next seq 2000
5. BBmap again, give a file that each the contig what is their depth
6. metabat2/3 to bin the data into mags
7. checkm2 to get the quality of the bins
