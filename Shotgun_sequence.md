#### Launch an interactive session on ARC

    salloc --mem=20G -c 1 -N 1 -n 1  -t 04:00:00

<details>
<summary>
    
#### 1. Reads quality control report - FastQC </summary>
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
</details>

<details>
<summary>

#### 2. Raw reads filtration - [BBduk](https://jgi.doe.gov/data-and-tools/software-tools/bbtools/bb-tools-user-guide/bbduk-guide/) </summary>
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

    #!/bin/bash
    #SBATCH --job-name=BBduk_3low_clip      # Job name
    #SBATCH --output=%x.log  # Job's standard output and error log
    #SBATCH --nodes=1             # Run all processes on a single node
    #SBATCH --ntasks=1            # Run 1 tasks
    #SBATCH --cpus-per-task=32    # Number of CPU cores per task
    #SBATCH --mem=50G            # Job memory request
    #SBATCH --time=24:00:00       # processing 20 paired-end Illumina reads spends 20 min
    #SBATCH --mail-user=lianchun.yi1@ucalgary.ca  # Send the job information to this email
    #SBATCH --mail-type=ALL                       # Send the type: <BEGIN><FAIL><END>
    pwd; hostname; date

    cd /work/ebg_lab/eb/Lianchun/shotgun_2024Aug

    for sample in Li49157 Li49158 Li49159 Li49160 Li49161 Li49162 Li49163 Li49164 Li49165 Li49166; do
        bbduk.sh in=${sample}_unmached_R1.fastq.gz out=${sample}_clean_R1.fastq.gz qtrim=rl trimq=15 minlength=30 t=32
        bbduk.sh in=${sample}_unmached_R2.fastq.gz out=${sample}_clean_R2.fastq.gz qtrim=rl trimq=15 minlength=30 t=32
    done

The name of the output file is Li491xx_**clean**_Rx.fastq.gz.

</details>

<details>
<summary>
    
#### 3. Generating taxonomic results - [sourmash](https://github.com/sourmash-bio/sourmash) </summary>
##### 3.1 Installation

    mamba create -n sourmash_env -c conda-forge sourmash-minimal
    mamba activate sourmash_env
    sourmash --help

##### 3.2 Slurm - sourmash.slurm

    
</details>





<details>
<summary>

#### 3. Metagenomic assembly - MetaSPAdes or [Megahit](https://github.com/voutcn/megahit)</summary>
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

**megahit_separate.slurm**

    #!/bin/bash
    #SBATCH --job-name=megahit_sperate      # Job name
    #SBATCH --output=%x.log  # Job's standard output and error log
    #SBATCH --nodes=1             # Run all processes on a single node
    #SBATCH --ntasks=1            # Run 1 tasks
    #SBATCH --cpus-per-task=32    # Number of CPU cores per task
    #SBATCH --mem=50G            # Job memory request
    #SBATCH --time=100:00:00       # processing 20 paired-end Illumina reads spends 3 days
    #SBATCH --mail-user=lianchun.yi1@ucalgary.ca  # Send the job information to this email
    #SBATCH --mail-type=ALL                       # Send the type: <BEGIN><FAIL><END>
    pwd; hostname; date

    cd /work/ebg_lab/eb/Lianchun/shotgun_2024Aug
    module load megahit/1.2.9

    gunzip *_clean_R1.fastq.gz
    gunzip *_clean_R2.fastq.gz

    for i in {57..66}; do
        SAMPLE="Li491${i}"
        megahit -1 ${SAMPLE}_clean_R1.fastq -2 ${SAMPLE}_clean_R2.fastq -o ./megahit_assembly/separate/${SAMPLE}_output -t 32 --continue
    done

The output contig file *final.contigs.fa* is in ./megahit_assembly/separate/Li491xx_output. Metaerg prefer to accept one ".".
Change the name of the contigs accordingly (Li491xx.fa) and move them to ./shotgun_2024Aug.

**megahit_co-assemble.slurm**

    #!/bin/bash
    #SBATCH --job-name=megahit_co-assemble      # Job name
    #SBATCH --output=%x.log  # Job's standard output and error log
    #SBATCH --nodes=1             # Run all processes on a single node
    #SBATCH --ntasks=1            # Run 1 tasks
    #SBATCH --cpus-per-task=32    # Number of CPU cores per task
    #SBATCH --mem=300G            # Job memory request
    #SBATCH --time=168:00:00       # processing 20 paired-end Illumina reads spends 64 h
    #SBATCH --mail-user=lianchun.yi1@ucalgary.ca  # Send the job information to this email
    #SBATCH --mail-type=ALL                       # Send the type: <BEGIN><FAIL><END>
    pwd; hostname; date
    
    cd /work/ebg_lab/eb/Lianchun/shotgun_2024Aug
    module load megahit/1.2.9

    megahit -1  Li49157_clean_R1.fastq,Li49158_clean_R1.fastq,Li49159_clean_R1.fastq,Li49160_clean_R1.fastq,Li49161_clean_R1.fastq,Li49162_clean_R1.fastq,Li49163_clean_R1.fastq,Li49164_clean_R1.fastq,Li49165_clean_R1.fastq,Li49166_clean_R1.fastq \
            -2 Li49157_clean_R2.fastq,Li49158_clean_R2.fastq,Li49159_clean_R2.fastq,Li49160_clean_R2.fastq,Li49161_clean_R2.fastq,Li49162_clean_R2.fastq,Li49163_clean_R2.fastq,Li49164_clean_R2.fastq,Li49165_clean_R2.fastq,Li49166_clean_R2.fastq \
            -o ./megahit_assembly/co-assemble  -t 32


</details>

<details>
<summary>
    
#### 4. K-mer coverage - BBMap </summary>
##### 4.1 Installation
Please refer to BBMap
##### 4.2 Slurm
**kmercoverage.slurm**

    #!/bin/bash
    #SBATCH --job-name=kmercoverage     # Job name
    #SBATCH --output=%x.log  # Job's standard output and error log
    #SBATCH --nodes=1             # Run all processes on a single node
    #SBATCH --ntasks=1            # Run 1 tasks
    #SBATCH --cpus-per-task=32    # Number of CPU cores per task
    #SBATCH --mem=50G            # Job memory request
    #SBATCH --time=24:00:00       # processing 20 paired-end Illumina reads spends 13 h
    #SBATCH --mail-user=lianchun.yi1@ucalgary.ca  # Send the job information to this email
    #SBATCH --mail-type=ALL                       # Send the type: <BEGIN><FAIL><END>
    pwd; hostname; date

    cd /work/ebg_lab/eb/Lianchun/shotgun_2024Aug

    for r1_file in *R1.fastq; do
        r2_file="${r1_file/_R1/_R2}"
        paired_output_r1="${r1_file/_R1.fastq/_paired_R1.fastq}"
        paired_output_r2="${r1_file/_R1.fastq/_paired_R2.fastq}"
        repair.sh in1="${r1_file}" in2="${r2_file}" out1="${paired_output_r1}" out2="${paired_output_r2}"
    done

    for i in {49157..49166}; do
        kmercoverage.sh in=Li${i}_clean_paired_R1.fastq in2=Li${i}_clean_paired_R2.fastq \
        out=Li${i}_kmer.fastq hist=Li${i}_hist.txt
    done

Check the Li491xx_hist.txt files for Raw_Count and Unique_Kmers.

##### 4.3 Plot
change the Li491xx_hist.txt files accordingly, download to local and run K-mer_coverage.py.

</details>

<details>
<summary>

#### 5. Remove contigs that less than 500bp - remove_short_contigs.py </summary>

    source ~/bio/bin/3.10_python-env/bin/activate
    python remove_short_contigs.py
    rm Li*.fa

Keep the filtered_Li491*.fa files for further analysis.

</details>

<details>
<summary>

#### 6. Per contig sequencing depth - BBMap / MetaBat2  </summary>
**MetaBat2** Installation

    mamba create --name metabat2
    mamba activate metabat2
    mamba install metabat2
    mamba update metabat2
    
**bbmap.slurm**

    #!/bin/bash
    #SBATCH --job-name=bbmap     # Job name
    #SBATCH --output=%x.log  # Job's standard output and error log
    #SBATCH --nodes=1             # Run all processes on a single node
    #SBATCH --ntasks=1            # Run 1 tasks
    #SBATCH --cpus-per-task=32    # Number of CPU cores per task
    #SBATCH --mem=150G            # Job memory request
    #SBATCH --time=24:00:00       # processing 20 paired-end Illumina reads spends 17 h
    #SBATCH --mail-user=lianchun.yi1@ucalgary.ca  # Send the job information to this email
    #SBATCH --mail-type=ALL                       # Send the type: <BEGIN><FAIL><END>
    pwd; hostname; date

    cd /work/ebg_lab/eb/Lianchun/shotgun_2024Aug

    references=("filtered_Li49157.fa" "filtered_Li49158.fa" "filtered_Li49159.fa" "filtered_Li49160.fa" "filtered_Li49161.fa" "filtered_Li49162.fa" "filtered_Li49163.fa" "filtered_Li49164.fa" "filtered_Li49165.fa" "filtered_Li49166.fa")
    reads_R1=("Li49158_clean_R1.fastq" "Li49159_clean_R1.fastq" "Li49160_clean_R1.fastq" "Li49161_clean_R1.fastq" "Li49162_clean_R1.fastq" "Li49163_clean_R1.fastq" "Li49164_clean_R1.fastq" "Li49165_clean_R1.fastq" "Li49166_clean_R1.fastq" "Li49157_clean_R1.fastq")
    reads_R2=("Li49158_clean_R2.fastq" "Li49159_clean_R2.fastq" "Li49160_clean_R2.fastq" "Li49161_clean_R2.fastq" "Li49162_clean_R2.fastq" "Li49163_clean_R2.fastq" "Li49164_clean_R2.fastq" "Li49165_clean_R2.fastq" "Li49166_clean_R2.fastq" "Li49157_clean_R2.fastq")

    for i in ${!references[@]}; do
        ref=${references[$i]}
        r1=${reads_R1[$i]}
        r2=${reads_R2[$i]}

        out_file="mapped_${ref%.fa}.sam"
    
        bbmap.sh ref="$ref" in1="$r1" in2="$r2" out="$out_file" minid=0.99 nodisk=f threads=32
    
        coverage_file="coverage_${ref%.fa}.txt"
        pileup.sh in="$out_file" out="$coverage_file"
    done


The name of the output files are **mapped_filtered_Li491xx.sam** and **coverage_filtered_Li491xx.txt** for contig sequencing depth.
Change the coverage_filtered_Li491xx.txt files accordingly, run plot_contig_sequencing_depth.py.

</details>


<details>
<summary>
    


#### 7. Binning - MetaBat2 </summary>


<details>
<summary>

#### 5. Annotaion - Metaerg </summary>
##### 5.1 [Installation](https://github.com/Wednesdaysama/evolutionary_adaptation/blob/main/installation.md)
##### 5.2 Slurm - metaerg.slurm
Make a metaerg directory under shotgun_2024Aug. Replace all ./megahit_assembly/separate/Li491xx_output/*final.contigs.fa* names with *Li491xx.fa*. And move them to ./metaerg. 


</details>

#### 8. Contamination and completeness checking - CheckM2


