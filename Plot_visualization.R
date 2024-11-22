# Define variables
num <- "III"
mutations_file <- "desktop/VC20333.tsv"      # Define mutations file path
mutation_types_file <- "desktop/mutation_types.tsv"  # Define mutation types file path

# Load libraries
library(ggplot2)
library(dplyr)
library(stringr)

# Define the function first
select_priority_type <- function(types_string) {
  if (is.na(types_string)) return(NA)
  
  # Split the string on commas and trim whitespace
  types <- str_trim(str_split(types_string, ",")[[1]])
  
  # If only one type, return it
  if (length(types) == 1) return(types)
  
  # Check for ncRNA + deletion combination
  if (all(c("ncRNA", "deletion") %in% types)) {
    return("ncRNA_deletion")
  }
  
  # Check if deletion is present
  if ("deletion" %in% types) {
    return("deletion")
  }
  # RNA types to check
  rna_types <- c("miRNA", "piRNA", "scRNA", "snRNA", "snoRNA", "tRNA", "rRNA", "ncRNA")
  
  # If any of these types are present alone, return the type
  rna_matches <- types %in% rna_types
  if (any(rna_matches) && !all(rna_matches)) {
    return("mixed")  # RNA type mixed with other mutation type
  }
  
  # If multiple types exist (but not the special cases above), mark as mixed
  return("mixed")
}

# Define colors
mutation_colors <- c(
  "nonsense" = "red",
  "splicing" = "red",
  "deletion" = "red",
  "insertion" = "red",
  "start ATG" = "red",
  "missense" = "yellow",
  "synonymous" = "turquoise",
  "intron" = "purple",
  "3' UTR" = "purple",
  "5' UTR" = "purple",
  "intergenic" = "white",
  "no mutation" = "black",
  "mixed" = "orange",
  "ncRNA_deletion" = "pink",
  "miRNA" = "green",
  "piRNA" = "green",
  "scRNA" = "green",
  "snRNA" = "green",
  "snoRNA" = "green",
  "tRNA" = "green",
 "rRNA" = "green",
  "ncRNA" = "green"
)

# Read in the data
data <- read.delim(mutations_file, sep = "\t", header = TRUE)
mutation_types <- read.delim(mutation_types_file, sep = "\t", header = TRUE) %>%
  select(Position, Type)

# Filter data and process types
chromosome_data <- data %>%
  filter(chrom == num) %>%
  mutate(type = mutation_types$Type[match(position, mutation_types$Position)]) %>%
  mutate(type = sapply(type, select_priority_type))

# Create the plot
ggplot(chromosome_data, aes(x = position / 1e6, y = `Frequency.mutation` * 100)) +
  geom_point(aes(fill = type), color = "black", shape = 21, size = 4) +
  scale_fill_manual(values = mutation_colors) +
  geom_hline(yintercept = 50, linetype = "dashed", color = "red") +
  scale_y_continuous(limits = c(0, 100), labels = function(y) paste0(y, "%")) +
  scale_x_continuous(breaks = seq(0, max(chromosome_data$position) / 1e6, by = 5), 
                     labels = function(x) paste0(x, " Mb")) +
  labs(title = paste("Mutation Frequency for Chromosome", num),
       x = "Position (Mb)",
       y = "Mutation Frequency (%)") +
  theme_minimal()






