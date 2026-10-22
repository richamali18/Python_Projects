"""Train and evaluate a Decision Tree classifier on the Iris dataset."""
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier


def main() -> None:
    iris = load_iris()
    features = iris.data
    labels = iris.target

    X_train, X_test, y_train, y_test = train_test_split(
        features,
        labels,
        test_size=0.2,
        random_state=42,
        stratify=labels,
    )

    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    print("Iris Flower Classification")
    print("--------------------------")
    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples:  {len(X_test)}")
    print(f"Accuracy: {accuracy:.2%}")
    print("\nClassification report:")
    print(
        classification_report(
            y_test,
            predictions,
            target_names=iris.target_names,
            zero_division=0,
        )
    )

    print("Example prediction:")
    sample = [features[0]]
    predicted_class = model.predict(sample)[0]
    print(f"Predicted flower: {iris.target_names[predicted_class]}")


if __name__ == "__main__":
    main()
