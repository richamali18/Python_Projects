# Iris Flower Classification

A beginner machine-learning project that trains a Decision Tree model to classify Iris flowers using the dataset bundled with scikit-learn.

## What it demonstrates

- Loading a built-in dataset.
- Separating features (`X`) from labels (`y`).
- Splitting data into training and testing sets.
- Training a `DecisionTreeClassifier`.
- Evaluating predictions with accuracy and a classification report.

## Run

Install dependencies from the parent folder:

```bash
pip install -r ../requirements.txt
```

Then run:

```bash
python iris_classifier.py
```

The printed accuracy is the result for this particular train/test split, not a guarantee that the model will achieve the same score on every dataset.
