# istanbul-rent-prediction
### Istanbul Real Estate Pricing Prediction Project

This project focuses on building a predictive model to estimate real estate prices using linear regression. Below is a summary of the tasks completed:

1. **Data Preparation and Feature Engineering**: The dataset was refined by one-hot encoding categorical variables such as district, neighborhood, usage status, heating type, and building condition. Missing values were addressed, and irrelevant or redundant features, such as deposit, dues, and building type, were removed.

2. **Normalization and Polynomial Features**: Data normalization was performed to ensure all features contributed equally to the model. Polynomial features were added to capture non-linear relationships between the features and the target variable.

3. **Model Training and Evaluation**: The dataset was divided into training and testing sets. The linear regression model was trained using gradient descent, experimenting with various learning rates and iteration numbers to find the optimal values. Model performance was evaluated using metrics like Mean Squared Error (MSE) and R-squared.

4. **Implementation and Testing**: The model was implemented in a Flask application, enabling real-time predictions. The application featured a web interface where users could input property details or provide a URL for scraping property information. The predicted price and its comparison to the actual price were displayed on the interface.

5. **Result Visualization and Deployment**: Predictions were visualized using Matplotlib, and functionality was included to convert normalized predictions back to Turkish Lira. The Flask application was modularized into separate components for web scraping, data processing, and prediction, ensuring a clean and maintainable codebase.
