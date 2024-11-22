import pandas as pd

# Function to generate regions.txt from a TSV file
def generate_regions_from_tsv(file_name):
    try:
        # Read the TSV file into a pandas DataFrame
        df = pd.read_csv(file_name, sep='\t')

        # Ensure the DataFrame has the correct columns
        df_selected = df[['Chr', 'Position']].copy()  # Create a copy to avoid SettingWithCopyWarning

        # Rename the columns for clarity
        df_selected.columns = ['chromosome', 'position']

        # Duplicate the 'position' column for start and end using .loc
        df_selected.loc[:, 'start'] = df_selected['position']
        df_selected.loc[:, 'end'] = df_selected['position']

        # Select the final columns: chromosome, start, and end
        df_final = df_selected[['chromosome', 'start', 'end']]

        # Write the DataFrame to regions.txt as a tab-separated file
        df_final.to_csv('regions.txt', sep='\t', header=False, index=False)

        print("regions.txt file has been generated successfully!")
    except FileNotFoundError:
        print(f"Error: The file {file_name} was not found.")
    except KeyError as e:
        print(f"Error: The expected column {e} was not found in the file.")

# Example usage
if __name__ == "__main__":
    file_name = input("Enter the name of the TSV file (including extension, e.g., file.tsv): ").strip()
    generate_regions_from_tsv(file_name)
