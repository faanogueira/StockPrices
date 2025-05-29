# 🧹 Data Cleaning and Preprocessing

## 📌 Description

This task is part of the data preparation pipeline for data science projects. The main goal was to apply essential data cleaning and preprocessing techniques to a stock prices dataset, making it ready for advanced analysis and predictive modeling.

---

## 🎯 Task Objectives

- ✅ Handle missing data (imputation using the mean)
- ✅ Detect and remove outliers (IQR method)
- ✅ Convert categorical variables into numerical (One-Hot Encoding)
- ✅ Standardize numerical features (StandardScaler)
- ✅ Save the cleaned dataset for further use

---

## 🧰 Tools & Libraries

- Language: **Python 3**
- Libraries:
  - `pandas` for data manipulation
  - `numpy` for numerical operations
  - `scikit-learn` for data transformation (scaling)
  - `matplotlib` and `seaborn` (recommended for visualization)

---

## 📁 Project Files

| File Name                              | Description                                                |
|----------------------------------------|------------------------------------------------------------|
| `stock_prices.csv`                 | Original stock prices dataset                              |
| `StockPrices.ipynb.ipynb`              | Notebook with all processing steps               |
| `stock_prices_clean.csv` (generated)   | Final dataset, ready for analysis or modeling              |
| `README.md`                            | This documentation file                                    |

---

## 🧪 Processing Steps

1. **Loading and inspecting the dataset**
2. **Handling missing values**: filled missing numerical values with column means.
3. **Outlier removal**: used the Interquartile Range (IQR) method to filter out outliers.
4. **Categorical encoding**: applied one-hot encoding using `pd.get_dummies()`.
5. **Standardization**: scaled numeric features using `StandardScaler`.
6. **Exported the cleaned dataset** to a new CSV file for later use.

---

## 📌 Final Notes

- All transformations ensure the dataset is clean and well-structured for machine learning or statistical modeling.
- Cleaning data is a critical step to avoid bias, overfitting, or poor model performance.

---

## 🚀 Next Steps

- Perform exploratory data analysis (EDA)
- Build predictive models (e.g., regression, classification)
- Optimize model performance (hyperparameter tuning)

---

## 📬 Contact

For questions or suggestions, feel free to get in touch!

Activity carried out by **Fábio Nogueira**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-1B1C1E?style=for-the-badge&logo=linkedin&logoColor=0077B5&border_color=fcf901)](https://www.linkedin.com/in/faanogueira/)
[![GitHub](https://img.shields.io/badge/GitHub-1B1C1E?style=for-the-badge&logo=linkedin&logoColor=0077B5&border_color=fcf901)](https://github.com/faanogueira)
[![Gmail](https://img.shields.io/badge/Gmail-1B1C1E?style=for-the-badge&logo=gmail&logoColor=C71610)](mailto:faanogueira@gmail.com)
[![WhatsApp](https://img.shields.io/badge/WhatsApp-1B1C1E?style=for-the-badge&logo=whatsapp&logoColor=green)](https://api.whatsapp.com/send?phone=5571983937557)

---
