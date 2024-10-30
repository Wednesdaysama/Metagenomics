#### 1. Reads quality control report - FastQC
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

#### 2. Raw reads filtration - [BBduk](https://jgi.doe.gov/data-and-tools/software-tools/bbtools/bb-tools-user-guide/bbduk-guide/)
##### 2.1 Installation
**BBMap**
    
    wget https://sourceforge.net/projects/bbmap/files/BBMap_39.10.tar.gz/download -O BBMap.tar.gz
    tar -xvzf BBMap.tar.gz
    rm BBMap.tar.gz
    nano ~/.bashrc # export PATH=$PATH:/home/lianchun.yi1/software/bbmap
    source ~/.bashrc
    bbmap.sh --version

Once BBMap is installed, we can directly use **BBNorm** for read normalization, **BBMerge** for merging overlapping reads, or **BBduk** for raw reads filtration.

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

The output file name is Li491xx_**trimmed**_Rx.fastq.gz.

##### 2.2 Slurm - clip.slurm

    #!/bin/bash
    #SBATCH --job-name=BBduk_clip      # Job name
    #SBATCH --output=%x.log  # Job's standard output and error log
    #SBATCH --nodes=1             # Run all processes on a single node
    #SBATCH --ntasks=1            # Run 1 tasks
    #SBATCH --cpus-per-task=32    # Number of CPU cores per task
    #SBATCH --mem=50G            # Job memory request
    #SBATCH --time=24:00:00       # processing 20 paired-end Illumina reads spends 40 min
    #SBATCH --mail-user=lianchun.yi1@ucalgary.ca  # Send the job information to this email
    #SBATCH --mail-type=ALL                       # Send the type: <BEGIN><FAIL><END>
    pwd; hostname; date

    cd /work/ebg_lab/eb/Lianchun/shotgun_2024Aug

    for sample in Li49157 Li49158 Li49159 Li49160 Li49161 Li49162 Li49163 Li49164 Li49165 Li49166
    do
        bbduk.sh \
            in1=${sample}_trimmed_R1.fastq.gz \
            in2=${sample}_trimmed_R2.fastq.gz \
            out1=${sample}_clip_R1.fastq.gz \
            out2=${sample}_clip_R2.fastq.gz \
            tbo tpe k=23 mink=11 hdist=1 ktrim=r t=32
    done

The name of the output file is Li491xx_**clip**_Rx.fastq.gz.

##### 2.3 Slurm - phix.slurm

    #!/bin/bash
    #SBATCH --job-name=BBduk_phix      # Job name
    #SBATCH --output=%x.log  # Job's standard output and error log
    #SBATCH --nodes=1             # Run all processes on a single node
    #SBATCH --ntasks=1            # Run 1 tasks
    #SBATCH --cpus-per-task=32    # Number of CPU cores per task
    #SBATCH --mem=50G            # Job memory request
    #SBATCH --time=24:00:00       # processing 20 paired-end Illumina reads spends 1.5 hours
    #SBATCH --mail-user=lianchun.yi1@ucalgary.ca  # Send the job information to this email
    #SBATCH --mail-type=ALL                       # Send the type: <BEGIN><FAIL><END>
    pwd; hostname; date

    cd /work/ebg_lab/eb/Lianchun/shotgun_2024Aug

    for sample in Li49157 Li49158 Li49159 Li49160 Li49161 Li49162 Li49163 Li49164 Li49165 Li49166
    do
      bbduk.sh in1=${sample}_clip_R1.fastq.gz in2=${sample}_clip_R2.fastq.gz \
               out1=${sample}_unmached_R1.fastq.gz out2=${sample}_unmached_R2.fastq.gz \
               outm1=${sample}_matched_R1.fastq.gz outm2=${sample}_matched_R2.fastq.gz \
               ref=~/software/bbmap/resources/phix174_ill.ref.fa.gz k=31 hdist=1 t=32
    done

Keep the output files whose names are Li491xx_**unmached**_Rx.fastq.gz.

##### 2.4 Slurm - 3low_clip.slurm

#### 3. Metagenomic assembly - MetaSPAdes or [Megahit](https://github.com/voutcn/megahit)
##### 3.1 Installation
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

##### 3.2 Slurm
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

#### 4. Annotaion - Metaerg
##### 4.1 [Installation](https://github.com/Wednesdaysama/evolutionary_adaptation/blob/main/installation.md)
##### 4.2 Slurm - metaerg.slurm

#### 5. Per-contig sequencing coverage estimation - BBMap / MetaBat2
##### 5.1 Installation


**MetaBat2**


    

##### 5.2 Slurm


#### 6. Binning - MetaBat2 

#### 7. Contamination and completeness checking - CheckM2


