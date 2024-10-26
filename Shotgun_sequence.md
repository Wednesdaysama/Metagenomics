#### 1. read quality control - FastQC
##### 1.1 FastQC Installation

    conda create --prefix ~/bio/bin/fastqc_env
    conda activate ~/bio/bin/fastqc_env
    conda install -c bioconda fastqc
    fastqc -h  
Check [here](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/Help/) for FastQC documentation.

##### 1.2 Slurm

    #!/bin/bash
    #SBATCH --job-name=fastqc      # Job name
    #SBATCH --output=%x.log  # Job's standard output and error log
    #SBATCH --nodes=1             # Run all processes on a single node
    #SBATCH --ntasks=1            # Run 1 tasks
    #SBATCH --cpus-per-task=16    # Number of CPU cores per task
    #SBATCH --mem=50G            # Job memory request
    #SBATCH --time=50:00:00       # processing 1500 genes spends 10 hours 
    #SBATCH --mail-user=lianchun.yi1@ucalgary.ca  # Send the job information to this email
    #SBATCH --mail-type=ALL                       # Send the type: <BEGIN><FAIL><END>
    pwd; hostname; date

    conda activate ~/bio/bin/fastqc_env
    cd /work/ebg_lab/eb/Lianchun/shotgun_2024Aug
    fastqc *.gz -o ./out_put --svg --noextract -t 16

Results will be saved in /work/ebg_lab/eb/Lianchun/shotgun_2024Aug/out_put

