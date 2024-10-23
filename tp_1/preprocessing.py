# This is the preprocessing module for the TP1 of the NLP course. 
# It contains the following functions:
# 
# merge_files: merges the files in the given directory into a single file
# separate_words: separates the words in the given text by spaces
# remove_punctuation: removes punctuation from the given text
# lowercase: converts the given text to lowercase 

import os
import re
import random
from collections import Counter

def merge_files(input_dir, output_file):
    """
    Merges all text files in the given input directory into a single output file.

    Args:
        input_dir: the directory to merge
        output_file: the file to write the merged text to

    Returns:
        None
    """
    with open(output_file, 'w') as outfile:
        # check if the input directory exists
        if not os.path.exists(input_dir):
            print(f"Directory {input_dir} does not exist.")
            return
        for root, dirs, files in os.walk(input_dir):
            for file in files:
                if file.endswith('.txt'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', errors = 'ignore') as infile:
                        content = infile.read()
                        # print(f"Reading from {file_path}: {content[:100]}...")  # Debugging: Print the first 100 characters
                        outfile.write(content + '\n')
                        # print(f"Written to {output_file}: {content[:100]}...")  # Debugging: Print the first 100 characters

def separate_words(text):
    """
    Separates the words in the given text by spaces.
    """
    return ' '.join(re.findall(r'\w+', text))

def remove_punctuation(text):
    """
    Removes punctuation from the given text.
    """
    return re.sub(r'[^\w\s]', '', text)

def lowercase(text):
    """
    Converts the given text to lowercase.
    """
    return text.lower()

def preprocess_text(text):
    """
    Preprocesses the given text by separating words, removing punctuation and converting to lowercase.
    """
    text = separate_words(text)
    text = remove_punctuation(text)
    text = lowercase(text)
    return text

def preprocess_file(input_file, output_file):
    """
    Preprocesses the text in the given input file and writes the result to the given output file.
    """
    with open(input_file, 'r') as f:
        text = f.read()
    print("Original Text:", text[:100])  # Debugging: Print the original text

    text = preprocess_text(text)
    print("Processed Text:", text[:100])  # Debugging: Print the processed text

    with open(output_file, 'w') as out:
        out.write(text)
    print(f"Processed text written to {output_file}")  # Debugging: Confirm writing to the output file


def most_common_words(words):
    """
    Returns the most common words in the given list of words, after removing stopwords.

    Args:
        words: a list of words

    Returns:
        most_common_words: a list of tuples, where each tuple contains a word and its frequency in the given list of words
    """

    # Get word frequencies
    word_counts = Counter(words)

    # Define stopwords 
    with open('tp_1/stopwords.txt', 'r') as f:
        stop_words = f.read().split()

    # Filter out stop words from the word frequencies
    filtered_words = {word: count for word, count in word_counts.items() if word not in stop_words}

    # Sort the words by frequency (most common words first)
    most_common_words = sorted(filtered_words.items(), key=lambda item: item[1], reverse=True)

    return most_common_words




def create_basis_and_target_set(most_common_words, overlap=0.5, b_size=200, t_size=50):
    """
    Creates the basis and target sets from the most common words in the given list of words.
    It also saves the B and T words to text files.
    The target words set partially overlaps with the basis set, a parameter that can be adjusted.

    Args:
        most_common_words: a list of tuples, where each tuple contains a word and its frequency in the given list of words
        overlap: the percentage of overlap between the basis and target sets (default is 30%)

    Returns:
        B_words: a list of the b_size most common words
        T_words: a list of (t_size + int(overlap * t_size)) words 
    """

    B_words = [word for word, count in most_common_words[:b_size]]

    # Save B words to a text file (one word per line)
    with open('tp_1/B.txt', 'w') as f:
        for word in B_words:
            f.write(f"{word}\n")
    
    T_words = [word for word, count in most_common_words[b_size:b_size+t_size]]  # Select the next most common t_size words

    # add to T_words other overlap*t_size words randomly taken from the B_words
    random.shuffle(B_words)
    T_words += B_words[:int(overlap * t_size)]

    # Save T words to a text file (one word per line)
    with open('tp_1/T.txt', 'w') as f:
        for word in T_words:
            f.write(f"{word}\n")

    return B_words, T_words

def create_basis_and_target_set_from_file(input_file):
    """
    Creates the basis and target sets from a .txt separated file of words.
    The file does need to contain only word divided by whitespace.

    Args:
        input_file: the file to read the words from

    Returns:
        B_words: a list of the b_size most common words
        T_words: a list of (t_size + int(overlap * t_size)) words

    """

    with open(input_file, 'r') as f:
        words = f.read().split()

    return create_basis_and_target_set(most_common_words(words))


if __name__ == '__main__':
    data = 'tp_1/bbc-news-summary/BBC News Summary/BBC News Summary'
    merge_files(data, 'tp_1/data_merged.txt')
    preprocess_file('tp_1/data_merged.txt', 'tp_1/data_preprocessed.txt')

    data = 'tp_1/data_preprocessed.txt'

    create_basis_and_target_set_from_file(data)
    