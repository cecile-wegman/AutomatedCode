
# Step 1: Generate regions.txt file from the TSV file 
python generate_positions.py "$TSV_FILE"

# Ask for user input
$WORKDIR = Read-Host "Enter the path to your working folder (e.g., C:\Users\username\Desktop\folder_of_working_strain)"
$STRAIN = Read-Host "Enter the strain name"
$REF_GENOME = Read-Host "Enter the reference genome file name (e.g., ce11.fa)"
$BAM_FILE = Read-Host "Enter the BAM file name (e.g., strain.aln.bam)"

# Step 2: Create temporary folder for sorting
Write-Host "Creating temporary folder for sorting..."
$TEMP_DIR = "${WORKDIR}\temp"
New-Item -Path $TEMP_DIR -ItemType Directory -Force

# Step 3: Sort the BAM file
Write-Host "Sorting the BAM file..."
docker run --rm -v "${WORKDIR}:/workdir" -w /workdir seqfu/alpine-samtools-1.10 samtools sort -T "/workdir/temp/$($STRAIN).temp" -o "$($STRAIN).sorted.bam" "$BAM_FILE"

# Step 4: Index the sorted BAM file
Write-Host "Indexing the sorted BAM file..."
docker run --rm -v "${WORKDIR}:/workdir" -w /workdir seqfu/alpine-samtools-1.10 samtools index "$($STRAIN).sorted.bam"

# Step 5: Generate the bam-readcount TSV file
Write-Host "Generating bam-readcount TSV file..."
docker run --rm -v "${WORKDIR}:/workdir" -w /workdir mgibio/bam-readcount -w1 -f "$REF_GENOME" -l regions.txt "$($STRAIN).sorted.bam" > "$($STRAIN).brc.tsv"

# Step 6: Parse the bam-readcount TSV file
Write-Host "Parsing bam-readcount TSV file..."
docker run --rm -v "${WORKDIR}:/workdir" -w /workdir python:3.8.2-alpine python parse_brc.py "$($STRAIN).brc.tsv" --encoding utf-16-le

# Step 7: Clean up temporary files
Write-Host "Cleaning up temporary files..."
Remove-Item -Path $TEMP_DIR -Recurse -Force

Write-Host "Process complete! Results can be found in $WORKDIR"
