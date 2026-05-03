from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
import joblib

def train_model(df):
    """
    Trains a linear regression model on the marketing dataset.

    Parameters:
        df : marketing dataframe

    Returns:
        model    : trained LinearRegression object
        features : list of feature column names
        metrics  : dict with r2 and mae
        test_data: tuple of (y_test, y_pred) for plotting
    """
    features = [col for col in df.columns if col.endswith('_spend')]
    X = df[features]
    y = df['revenue']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    metrics = {
        'r2':  r2_score(y_test, y_pred),
        'mae': mean_absolute_error(y_test, y_pred),
        'coefficients': dict(zip(features, model.coef_))
    }

    return model, features, metrics, (y_test, y_pred)

def save_model(model, path='data/model.joblib'):
    """Saves the trained model to disk."""
    joblib.dump(model, path)


def load_model(path='data/model.joblib'):
    """Loads a saved model from disk."""
    return joblib.load(path)