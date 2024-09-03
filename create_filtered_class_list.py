import argparse

def filter_words(main_file_path, filter_file_path, output_file_path):
    # Load filter words into a set for quick lookup
    with open(filter_file_path, 'r', encoding='utf-8') as filter_file:
        filter_words = set(line.strip() for line in filter_file)

    # Open the main file and the output file
    with open(main_file_path, 'r', encoding='utf-8') as main_file, \
         open(output_file_path, 'w', encoding='utf-8') as output_file:

        # Process each line in the main file
        for line in main_file:
            id_value, word = line.strip().split('\t')
            if word not in filter_words:
                word = 'нет жеста'
            output_file.write(f'{id_value}\t{word}\n')

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Filter words from the main file using a filter file.")
    parser.add_argument("main_file", help="Path to the main file with IDs and words.")
    parser.add_argument("filter_file", help="Path to the filter file containing words to keep.")
    parser.add_argument("output_file", help="Path to the output file where the results will be saved.")

    # Parse the arguments
    args = parser.parse_args()

    # Call the filter_words function with the provided arguments
    filter_words(args.main_file, args.filter_file, args.output_file)