import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import model_from_json
from joblib import load
from pathlib import Path


def batch_preprocess(df):
    print("Starting preprocessing")
    """
        This function is to cover all the preprocessing steps on the churn dataframe. It involves selecting important features,
        encoding categorical data, handling missing values,feature scaling and splitting the data
        """
    # remove rows with no TotalCharges
    df = df[df.TotalCharges != " "]
    df.TotalCharges = df.TotalCharges.astype(float)
    # replace values
    df.replace("No internet service", "No", inplace=True)
    df.replace("No phone service", "No", inplace=True)

    # # Encode categorical features
    binary_columns = ['Partner', 'Dependents', 'PhoneService', 'MultipleLines', 'OnlineSecurity', 'OnlineBackup',
                      'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 'PaperlessBilling']

    for col in binary_columns:
        df[col].replace({"Yes": 1, "No": 0}, inplace=True)

    df["gender"].replace({"Female": 1, "Male": 0}, inplace=True)
    # The customerID column is not useful as the feature is used for identification of customers.
    # df.drop(["Churn"], axis=1, inplace=True)
    # df.drop(["Unnamed: 0"], axis=1, inplace=True)
    cols_to_scale = ["tenure", "MonthlyCharges", "TotalCharges"]
    scaler = MinMaxScaler()
    df[cols_to_scale] = scaler.fit_transform(df[cols_to_scale])
    # Get dummy data for some of the categorical data
    df = pd.get_dummies(data=df, columns=['InternetService', 'Contract', 'PaymentMethod'])
    print("Finished preprocessing")
    print(type(df))
    return df


def preprocess(df):
    print(df.head())
    print("Starting preprocessing")
    """
        This function is to cover all the preprocessing steps on the churn dataframe. It involves selecting important features,
        encoding categorical data, handling missing values,feature scaling and splitting the data
        """
    # remove rows with no TotalCharges
    df = df[df.TotalCharges != " "]
    df.TotalCharges = df.TotalCharges.astype(float)
    # replace values
    df.replace("No internet service", "No", inplace=True)
    df.replace("No phone service", "No", inplace=True)

    # # Encode categorical features
    binary_columns = ['SeniorCitizen', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines', 'OnlineSecurity', 'OnlineBackup',
                      'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 'PaperlessBilling']

    for col in binary_columns:
        df[col].replace({"Yes": 1, "No": 0}, inplace=True)

    df["gender"].replace({"Female": 1, "Male": 0}, inplace=True)
    # The customerID column is not useful as the feature is used for identification of customers.
    # df.drop(["Churn"], axis=1, inplace=True)
    # df.drop(["Unnamed: 0"], axis=1, inplace=True)
    cols_to_scale = ["tenure", "MonthlyCharges", "TotalCharges"]
    scaler = MinMaxScaler()
    df[cols_to_scale] = scaler.fit_transform(df[cols_to_scale])
    # Get dummy data for some of the categorical data

    internetService_types = ['DSL', 'Fiber optic', 'No']
    for internetService_type in internetService_types:
        df['InternetService_'+internetService_type] = 0
        df.loc[df.InternetService == internetService_type, 'InternetService_'+internetService_type] = 1

    contract_types = ['Month-to-month', 'One year', 'Two year']
    for contract_type in contract_types:
        df['Contract_'+contract_type] = 0
        df.loc[df.Contract == contract_type, 'Contract_'+contract_type] = 1

    payment_types = ['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)']
    for payment_type in payment_types:
        df['PaymentMethod_'+payment_type] = 0
        df.loc[df.PaymentMethod == payment_type, 'PaymentMethod_'+payment_type] = 1

    df.drop(["InternetService"], axis=1, inplace=True)
    df.drop(["Contract"], axis=1, inplace=True)
    df.drop(["PaymentMethod"], axis=1, inplace=True)

    print("Finished preprocessing")
    print(type(df))
    return df

def load_models():
    print("Loading saved artifacts....")
    global __models
    global __cnn_model
    global __rfc_clf
    global __knn_clf
    global __svm_clf
    global __xgb_clf
    global __lr_clf
    global __meta_model
    __models = []

    print("Loading cnn model....")
    # Load the json file that contains the model's structure
    f = Path("artifacts/models/cnn_model/cnn_model_structure.json")
    model_structure = f.read_text()
    # Recreate the Keras model object from the json data
    __cnn_model = model_from_json(model_structure)
    # Re-load the model's trained weights
    __cnn_model.load_weights("artifacts/models/cnn_model/cnn_model_weights.h5")
    __models.append(__cnn_model)
    print("Loading RF model....")
    __rfc_clf = load('artifacts/models/rfc_model.joblib')
    __models.append(__rfc_clf)
    print("Loading knn model....")
    __knn_clf = load('artifacts/models/knn_model.joblib')
    __models.append(__knn_clf)
    print("Loading svm model....")
    __svm_clf = load('artifacts/models/svm_model.joblib')
    __models.append(__svm_clf)
    print("Loading xgb model....")
    __xgb_clf = load('artifacts/models/xgb_model.joblib')
    __models.append(__xgb_clf)
    print("Loading lr model....")
    __lr_clf = load('artifacts/models/lr_model.joblib')
    __models.append(__lr_clf)
    print("Loading meta model....")
    __meta_model = load('artifacts/models/stacked_ensemble_model.joblib')
    __models.append(__meta_model)
    print("successfully loaded saved artifacts!")
    return


def get_predictions(df):
    print("Predicting")
    preprocessed_df = preprocess(df)
    print("single prediction")

    X_test = preprocessed_df.drop("customerID", axis=1)
    identifier = preprocessed_df["customerID"]
    X_test = X_test.astype(float)

    print(type(X_test))
    print(X_test.head())
    print("identifier")
    print(identifier.head())
    cnn_predictions = __cnn_model.predict(X_test)

    cnn_predictions = [round(x[0]) for x in cnn_predictions]
    print("CNN:")
    print(cnn_predictions)
    rf_predictions = __rfc_clf.predict(X_test)
    print()
    knn_predictions = __knn_clf.predict(X_test)
    svm_predictions = __svm_clf.predict(X_test)
    xgb_predictions = __xgb_clf.predict(X_test)
    lr_predictions = __lr_clf.predict(X_test)

    # Combine the predictions into a new dataframe
    predictions = np.column_stack(
        (cnn_predictions, knn_predictions, rf_predictions, svm_predictions, xgb_predictions, lr_predictions)
    )

    # Get the final predictions from the meta model
    final_predictions = __meta_model.predict(predictions)
    print(final_predictions)
    print("final identifier type: ")
    print(type(identifier))
    print(identifier.head())
    print("Concatinating final predictions")
    testDf = pd.DataFrame({'Prediction': final_predictions})
    print(testDf.head())
    identifier = identifier.to_frame()
    print(identifier.head())
    # identifier = pd.concat([identifier, testDf], axis=1)
    identifier = pd.concat([identifier.reset_index(drop=True), testDf], axis=1)
    print(identifier.head())
    print("Returning prediction")
    return identifier


if __name__ == '__main__':
    load_models()
    print("Starting process")
    df = get_predictions(pd.read_csv('customer_churn.csv'))
    print(df.head())
    print("Finished")

    # row_data = {
    #     'customerID': "9237-HQITU",
    #     'gender': 'Female',
    #     'SeniorCitizen': '0',
    #     'Partner': 'No',
    #     'Dependents': 'No',
    #     'tenure': '2',
    #     'PhoneService': 'Yes',
    #     'MultipleLines': 'No',
    #     'InternetService': 'Fiber optic',
    #     'OnlineSecurity': 'No',
    #     'OnlineBackup': 'No',
    #     'DeviceProtection': 'No',
    #     'TechSupport': 'No',
    #     'StreamingTV': 'No',
    #     'StreamingMovies': 'No',
    #     'Contract': 'Month-to-month',
    #     'PaperlessBilling': 'Yes',
    #     'PaymentMethod': 'Electronic check',
    #     'MonthlyCharges': 70.7,
    #     'TotalCharges': 151.65
    # }
    #
    # df2 = get_predictions(pd.DataFrame([row_data]), 'single')
    # print(df2.head())
    # print("Finished")
