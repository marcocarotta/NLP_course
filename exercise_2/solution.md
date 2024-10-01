## Exercise 1: Text Parsing

| ID | Word           | Lemma         | UPOS  | Features                                            | Dep. link | Dep. label  |
|----|----------------|---------------|-------|-----------------------------------------------------|-----------|-------------|
| 1  | J'             | je            | PRON  | Number=Sing&Person=1&PronType=Prs                   | 2         | nsubj       |
| 2  | espère         | espérer       | VERB  | Mood=Ind&Number=Sing&Person=1&Tense=Pres            | 0         | root        |
| 3  | que            | que           | SCONJ |                                                     | 7         | mark        |
| 4  | ma             | mon           | DET   | Gender=Fem&Number=Sing&PronType=Prs                 | 5         | det         |
| 5  | proposition    | proposition   | NOUN  | Gender=Fem&Number=Sing                              | 7         | nsubj       |
| 6  | sera           | être          | AUX   | Mood=Ind&Number=Sing&Person=3&Tense=Fut             | 7         | aux         |
| 7  | prise          | prendre       | VERB  | Gender=Fem& Number=Sing&Tense=Past&VerbForm=Part    | 2         | ccomp       |
| 8  | en             | en            | ADP   |                                                     | 9         | case        |
| 9  | considération  | considération | NOUN  | Gender=Fem&Number=Sing                              | 7         | obl         |


## Exercise 2: End-User Tasks

| Sentence 1                                    | Sentence 2                                              | Score | Syntactic Difference |
|-----------------------------------------------|---------------------------------------------------------|-------|----------------------|
| A parrot is talking.                          | A parrot is talking into a microphone.                  | 3.000 | YES                  |
| A man is singing into a microphone.           | A man is dancing in the rain.                           | 0.400 | NO                   |
| A woman is exercising.                        | A woman lifts weights.                                  | 3.400 | YES                  |
| A child runs into and out of the ocean waves. | A young boy is running toward and from the ocean waves. | 3.800 | YES                  |
| A man is playing the piano.                   | A man is playing a wooden flute.                        | 1.400 | YES                  |

### Answers:

**2.1** The NLP task is **Semantic Textual Similarity (STS)**, which measures how similar two sentences are.

**2.3** The biggest difference is in the second row, in fact the phrases are sintactically identical but they have complete different meaning.
