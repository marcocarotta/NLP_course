import numpy as np
from scipy.special import softmax

# Given inputs x1, x2, x3 and weight matrices W_Q, W_K, W_V
x1 = np.array([1, 2, 1, 2])
x2 = np.array([0, 1, 3, 0])
x3 = np.array([2, 2, 1, 2])

W_Q = np.array([[2, 2, 1],
                [3, 0, 2],
                [1, 4, 2],
                [0, 1, 2]])

W_K = np.array([[1, 3, 2],
                [2, 1, 1],
                [2, 0, 1],
                [1, 1, 3]])

W_V = np.array([[3, 1, 0],
                [0, 2, 1],
                [2, 1, 2],
                [2, 3, 0]])

# Step 1: Calculate Q, K, V for each x
Q1, Q2, Q3 = x1 @ W_Q, x2 @ W_Q, x3 @ W_Q
K1, K2, K3 = x1 @ W_K, x2 @ W_K, x3 @ W_K
V1, V2, V3 = x1 @ W_V, x2 @ W_V, x3 @ W_V

# Step 2: Calculate scores
scores = np.array([
    [np.dot(Q1, K1), np.dot(Q1, K2), np.dot(Q1, K3)],
    [np.dot(Q2, K1), np.dot(Q2, K2), np.dot(Q2, K3)],
    [np.dot(Q3, K1), np.dot(Q3, K2), np.dot(Q3, K3)]
])

# Step 3: Apply softmax to obtain α values (attention weights)
alpha = np.apply_along_axis(softmax, 1, scores)

# Step 4: Calculate α * V for each position
V = np.array([V1, V2, V3])
alpha_V = np.dot(alpha, V)

# Output results for each input token
a_x1, a_x2, a_x3 = alpha_V[0], alpha_V[1], alpha_V[2]

print("Output for x1:", a_x1)
print("Output for x2:", a_x2)
print("Output for x3:", a_x3)
