# MiSeq 
## 1. Original data acquisition
Preparing three documents to get PI's support for MiSeq data. Login ARC and go to the EBG space:

    cd /work/ebg_lab/Instrument_data/Sequences/Amplicon/run
Download the target files to your own directory. Unzip all the .gz files in Linux by the command below.

    gzip -d *.gz
Save all the .fastq files, which are the input files of [Metaamp](http://ebg.ucalgary.ca/metaamp/index.asc.html).
## 2. Preparation of Metaamp
There are 3 files need to be prepared before running Metaamp online. 
1. a mapping text file.
2. a compressed .fastq file (.zip)
3. primers information

Then, run Metaamp online. It may take a few minutes.
## 3. Taxonomy
3.1 Click "Download a packaged file containing all results in this page" in the Metaamp Results Page.

3.2 Open the results package and Upload the ".asv.fasta" file from the "asv_and_taxonomy" directory to the Cloud. 
Attention: the uploaded file should be downloaded in a directory **without any Chinese characters or Onedrive**.

3.3 Activated python-env and source. 
      
    source /bio/bin/profile
    echo $PATH
    source /bio/bin/python-env/bin/activate
3.4 Run the command below under a directory, which contains the ".asv.fasta" file.

    blastn -db /bio/databases/metaerg/db_rna.fna -query .asv.fasta -max_target_seqs 1 -outfmt 6 
This process may take a while.

3.5 Copy the blastn results to a file named taxonomy.csv. There are 12 columns in this sheet.
The name of each column:

 | Column names     | Description                                                     |
 |------------------|-----------------------------------------------------------------| 
 | query_id         | identifier of the query sequence                                | 
 | subject_id       | identifier of the matching subject sequence                     | 
 | %_identity       | percentage identity between the query and subject sequences     | 
 | alignment_length | length of the alignment between the query and subject sequences | 
 | mismatches      | number of mismatches in the alignment                           | 
 | gap_opens      | number of gaps (insertions or deletions) in the alignment       |
 | q_start       | the starting position of the alignment in the query sequence      |
 | q_end      | the ending position of the alignment in the query sequence         |
 | s_start    | the starting position of the alignment in the subject sequence   |
 | s_end    | the ending position of the alignment in the subject sequence  |
 | evalue    |representing the expected number of matches by chance        |
 | bit_score| representing the strength of the match         |

3.6 The first number of subject ID is the identify number of the taxonomy (taxonomy id). 
According to the taxonomy id, 
the real taxonomy can be found in */bio/databases/metaerg/db_taxonomy.txt* on the cloud.
Should transform the db_taxonomy.txt file to db_taxonomy.csv file.
Life would become difficult, if you look up thousands of asvs manually. 
Here, Ms.Solanki provided a [python script](https://github.com/Ruchita-0310/MiSeq/blob/main/taxonomy_lookup.py) to generate taxonomy automatically.
Note: 
1. Input two .csv files: *taxonomy.csv* and *db_taxonomy.csv*.
2. This script will generate a file named *blastn_taxonomy.csv*, which would be the final taxonomy result.



