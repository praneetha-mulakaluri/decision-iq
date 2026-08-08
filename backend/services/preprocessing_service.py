
from sklearn.preprocessing import LabelEncoder, StandardScaler

def fill_missing_values(df):
    missing_values_filled = dict()
    for column in df.select_dtypes(include=['number']).columns:
        if(df[column].isna().sum() > 0):
            df[column] = df[column].fillna(df[column].mean())
            missing_values_filled[column] = "Mean Imputation"
    for column in df.select_dtypes(include=['object']).columns:
        if(df[column].isna().sum() > 0):
            mode = df[column].mode()
            if (not mode.empty):
                df[column] = df[column].fillna(mode.iloc[0])
                missing_values_filled[column] = "Mode Imputation"
    return df, missing_values_filled;

def drop_duplicates(df):
    initial_row_count = df.shape[0]
    df.drop_duplicates()
    duplicates_removed = initial_row_count - df.shape[0]
    return df, duplicates_removed

def encode_categorical_columns(df):
    encoder = LabelEncoder()
    categorical_columns = df.select_dtypes(include=["object", "category"]).columns
    for column in categorical_columns:
        df[column] = encoder.fit_transform(df[column])
    return df, categorical_columns.tolist()

def scale_numeric_columns(df):
    scaler = StandardScaler()
    numeric_columns = df.select_dtypes(include=["number"]).columns
    df[numeric_columns] = scaler.fit_transform(df[numeric_columns])
    return df, numeric_columns.tolist()