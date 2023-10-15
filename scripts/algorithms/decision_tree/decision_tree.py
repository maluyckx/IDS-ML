from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


### TODO take combined_df from parser.py
# Assuming you already have the 'combined_df' DataFrame with features and labels

# Define the feature columns (you may select the relevant features)
feature_columns = ['Timestamp', 'Source IP', 'Destination IP', 'Query Type', 'Query Details']

# Encode categorical features (e.g., one-hot encoding for 'Query Type')
combined_df_encoded = pd.get_dummies(combined_df, columns=['Query Type'])

# Split the data into features and labels
X = combined_df_encoded.drop(columns=['Label'])
y = combined_df_encoded['Label']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train a Decision Tree classifier
clf = DecisionTreeClassifier()
clf.fit(X_train, y_train)

# Make predictions on the test set
y_pred = clf.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
classification_report_str = classification_report(y_test, y_pred)

# Display the results
print("Accuracy:", accuracy)
print("\nClassification Report:\n", classification_report_str)
