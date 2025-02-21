import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

class LinearRegressor:
    #Prueba de cambio
    """
    Linear Regression model that can perform both simple and multiple linear regression.

    Attributes:
        coefficients (np.ndarray or float): Coefficients of the independent variables in the regression model.
        intercept (float): Intercept of the regression model.
    """

    def __init__(self):
        """Initializes the LinearRegressor model with default coefficient and intercept values."""
        self.coefficients = None
        self.intercept = None

    def fit_simple(self, X, y):
        """
        Fit the model using simple linear regression (one independent variable).

        This method calculates the coefficients for a linear relationship between
        a single predictor variable X and a response variable y.

        Args:
            X (np.ndarray): Independent variable data (1D array).
            y (np.ndarray): Dependent variable data (1D array).

        Returns:
            None: Modifies the model's coefficients and intercept in-place.
        """
        X = np.array(X).flatten()
        y = np.array(y)
        numerator = np.sum((X - np.mean(X)) * (y - np.mean(y)))
        denominator = np.sum((X - np.mean(X)) ** 2)
        self.coefficients = numerator / denominator
        self.intercept = np.mean(y) - self.coefficients * np.mean(X)

    def fit_multiple(self, X, y):
        """
        Fit the model using multiple linear regression (more than one independent variable).

        This method applies the matrix approach to calculate the coefficients for
        multiple linear regression.

        Args:
            X (np.ndarray): Independent variable data (2D array where each column is a variable).
            y (np.ndarray): Dependent variable data (1D array).

        Returns:
            None: Modifies the model's coefficients and intercept in-place.
        """
        X = np.array(X)
        y = np.array(y)
        ones = np.ones((X.shape[0], 1))
        X_b = np.hstack([ones, X])
        beta = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(y)
        self.intercept = beta[0]
        self.coefficients = beta[1:]

    def predict(self, X):
        """
        Predict the dependent variable values using the fitted model.

        Args:
            X (np.ndarray): Independent variable data (1D or 2D array).

        Returns:
            np.ndarray: Predicted values of the dependent variable.

        Raises:
            ValueError: If the model is not yet fitted.
        """
        if self.coefficients is None or self.intercept is None:
            raise ValueError("Model is not yet fitted")
        
        X = np.array(X)
        if np.ndim(X) == 1:
            predictions = self.intercept + self.coefficients * X
        else:
            predictions = self.intercept + np.dot(X, self.coefficients)
        return predictions


def evaluate_regression(y_true, y_pred):
    """
    Evaluates the performance of a regression model by calculating R^2, RMSE, and MAE.

    Args:
        y_true (np.ndarray): True values of the dependent variable.
        y_pred (np.ndarray): Predicted values by the regression model.

    Returns:
        dict: A dictionary containing the R^2, RMSE, and MAE values.
    """
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    # Calcular R^2
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    r_squared = 1 - ss_res / ss_tot

    # Calcular RMSE
    rmse = np.sqrt(np.mean((y_true - y_pred) ** 2))

    # Calcular MAE
    mae = np.mean(np.abs(y_true - y_pred))

    return {"R2": r_squared, "RMSE": rmse, "MAE": mae}


def sklearn_comparison(x, y, linreg):
    """Compares a custom linear regression model with scikit-learn's LinearRegression.

    Args:
        x (numpy.ndarray): The input feature data (1D array).
        y (numpy.ndarray): The target values (1D array).
        linreg (object): An instance of a custom linear regression model. Must have
            attributes `coefficients` and `intercept`.

    Returns:
        dict: A dictionary containing the coefficients and intercepts of both the
            custom model and the scikit-learn model. Keys are:
            - "custom_coefficient": Coefficient of the custom model.
            - "custom_intercept": Intercept of the custom model.
            - "sklearn_coefficient": Coefficient of the scikit-learn model.
            - "sklearn_intercept": Intercept of the scikit-learn model.
    """
    from sklearn.linear_model import LinearRegression

    x = np.array(x)
    x_reshaped = x.reshape(-1, 1)

    sklearn_model = LinearRegression()
    sklearn_model.fit(x_reshaped, y)

    print("Custom Model Coefficient:", linreg.coefficients)
    print("Custom Model Intercept:", linreg.intercept)
    print("Scikit-Learn Coefficient:", sklearn_model.coef_[0])
    print("Scikit-Learn Intercept:", sklearn_model.intercept_)
    return {
        "custom_coefficient": linreg.coefficients,
        "custom_intercept": linreg.intercept,
        "sklearn_coefficient": sklearn_model.coef_[0],
        "sklearn_intercept": sklearn_model.intercept_,
    }


def anscombe_quartet():
    """Loads Anscombe's quartet, fits custom linear regression models, and evaluates performance.

    Returns:
        tuple: A tuple containing:
            - anscombe (pandas.DataFrame): The Anscombe's quartet dataset.
            - datasets (list): A list of unique dataset identifiers in Anscombe's quartet.
            - models (dict): A dictionary where keys are dataset identifiers and values
              are the fitted custom linear regression models.
            - results (dict): A dictionary containing evaluation metrics (R2, RMSE, MAE)
              for each dataset.
    """
    anscombe = sns.load_dataset("anscombe")

    datasets = anscombe['dataset'].unique()

    models = {}
    results = {"R2": [], "RMSE": [], "MAE": []}
    for dataset in datasets:
        data = anscombe[anscombe['dataset'] == dataset]

        model = LinearRegressor()

        X = data['x'].values
        y = data['y'].values
        model.fit_simple(X, y)

        y_pred = model.predict(X)

        models[dataset] = model

        print(
            f"Dataset {dataset}: Coefficient: {model.coefficients}, Intercept: {model.intercept}"
        )

        evaluation_metrics = evaluate_regression(y, y_pred)

        print(
            f"R2: {evaluation_metrics['R2']}, RMSE: {evaluation_metrics['RMSE']}, MAE: {evaluation_metrics['MAE']}"
        )
        results["R2"].append(evaluation_metrics["R2"])
        results["RMSE"].append(evaluation_metrics["RMSE"])
        results["MAE"].append(evaluation_metrics["MAE"])
    return anscombe, datasets, models, results
