import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

def check_enough_words(input_file, min_words=100000):
    """
    Checks if the given input file contains at least the minimum number of words.

    Args:
        input_file: the file to check
        min_words: the minimum number of words required (default is 100,000)

    Returns:
        words: a list of words in the file
        enough_words: True if the file contains at least the minimum number of words, False otherwise
    """
    
    with open(input_file, 'r') as f:
        words = f.read().split()

    enough_words = len(words) >= min_words
    print("Reading ",input_file,f". Found {len(words)} words. {'Enough words for the assignment\n' if enough_words else 'Not enough words for the assignment\n'}")

    return words, enough_words

def make_cooccurence_matrix(words, basis_word, target_word, window_size=5): #TODO fix it, it's broken, the results is always zero
    """
    Creates a co-occurrence matrix where the rows are the target words and the columns are the context words (basis words) and in each cell there is how many times the target word appears in the context of the basis word

    Args:
        words: a list of words
        basis_word: the basis word to use
        target_word: the target word to use
        window_size: the size of the context window to consider (default is 5)

    Returns:
        cooccurrence_matrix: a numpy matrix of size len(target_word)*len(basis_word) 
    """
    half_window = window_size // 2
    # Get the indices of the basis word
    basis_indices = [(i, word) for i, word in enumerate(words) if word == basis_word]

    # Create a boolean dictionary for the target word
    target_boolean_dict = {word: True for word in target_word}

    # Create the co-occurrence dictionary
    cooccurrence_dict = {}

    # Fill the co-occurrence dictionary
    for k, context_word in basis_indices:
        window = words[max(0, k-half_window):k] + words[k+1:min(len(words), k+half_window+1)]
        for word in window:
            if word in target_boolean_dict:
                cooccurrence_dict[(word, context_word)] = cooccurrence_dict.get((word, context_word), 0) + 1
                
    # Create the co-occurrence matrix
    cooccurrence_matrix = np.zeros((len(target_word), len(basis_word)))

    for i, target in enumerate(target_word):
        for j, basis in enumerate(basis_word):
            cooccurrence_matrix[i, j] = cooccurrence_dict.get((target, basis), 0)

    return cooccurrence_matrix

def make_positive_pointwise_mutual_information(cooccurrence_matrix):
    """
    Creates a positive pointwise mutual information matrix from the given co-occurrence matrix.

    Args:
        cooccurrence_matrix: the co-occurrence matrix

    Returns:
        ppmi_matrix: the positive pointwise mutual information matrix
    """
    # Calculate the row and column sums
    row_sums = np.sum(cooccurrence_matrix, axis=1)
    column_sums = np.sum(cooccurrence_matrix, axis=0)
    total_sum = np.sum(cooccurrence_matrix)

    # Calculate the probability of each row and column
    row_probabilities = row_sums / total_sum
    column_probabilities = column_sums / total_sum

    # Calculate the pointwise mutual information
    ppmi_matrix = np.log(cooccurrence_matrix * total_sum / (row_sums[:, None] * column_sums[None, :]))

    # Replace negative values with zeros
    ppmi_matrix[ppmi_matrix < 0] = 0

    # Check size of the matrix
    print("Co-occurrence matrix size: ",cooccurrence_matrix.shape)
    print("PPMI matrix size: ",ppmi_matrix.shape)
    if cooccurrence_matrix.shape != ppmi_matrix.shape:
        raise ValueError("Error: The PPMI matrix has a different size than the co-occurrence matrix")

    return ppmi_matrix

def make_pca(ppmi_matrix, n_components=2):
    """
    Creates a PCA matrix from the given positive pointwise mutual information matrix.

    Args:
        ppmi_matrix: the positive pointwise mutual information matrix
        n_components: the number of components to keep (default is 2)

    Returns:
        pca_matrix: the PCA matrix
    """
    # Perform PCA
    pca = PCA(n_components=n_components)
    pca_matrix = pca.fit_transform(ppmi_matrix)

    return pca_matrix

def plot_pca(pca_matrix, target_word):
    """
    Plots the PCA matrix.

    Args:
        pca_matrix: the PCA matrix
        target_word: the target words
    """
    # Plot the PCA matrix
    plt.figure(figsize=(10, 10))
    plt.scatter(pca_matrix[:, 0], pca_matrix[:, 1])
    for i, word in enumerate(target_word):
        plt.annotate(word, (pca_matrix[i, 0], pca_matrix[i, 1]))
    plt.xlabel('PC1')
    plt.ylabel('PC2')
    plt.title('PCA')
    plt.show()

if __name__ == '__main__':
    data = 'tp_1/data_preprocessed.txt'
    words, _ = check_enough_words(data)
    basis_word, _ = check_enough_words('tp_1/B.txt', min_words=200)
    target_word, _ = check_enough_words('tp_1/T.txt', min_words=50)

    input("Do you want to continue? Press Enter to continue...")

    cooccurrence_matrix = make_cooccurence_matrix(words, basis_word, target_word)
    print("Co-occurrence matrix:")
    print(cooccurrence_matrix)

    ppmi_matrix = make_positive_pointwise_mutual_information(cooccurrence_matrix)

    # check for NaNs
    if np.isnan(ppmi_matrix).sum():
        print(np.isnan(ppmi_matrix).sum())
    else:
        print("There are no NaNs in the PPMI matrix")

    # substitute NaNs with 0
    ppmi_matrix = np.nan_to_num(ppmi_matrix)

    pca_matrix = make_pca(ppmi_matrix)
    plot_pca(pca_matrix, target_word)


