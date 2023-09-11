# -*- coding: utf-8 -*-
"""Retodomingo.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1p7_ATgp0Nyk00LntUWDT0zO6ElDsKXXz
"""

# muchas librerias para varias pruebas y variaciones
from sklearn.tree import DecisionTreeRegressor
import graphviz
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import export_graphviz
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import make_scorer

data=pd.read_csv('winequality-red.csv')

# Vamos a predecir el valor de volatile acidity
data.head()

# Desplegamos la info del data set
data.info

print(data.info())

# Sacamos la matriz de correlacion para poder ver que correlacion tienen las diferentes variables

# Calcula la matriz de correlación
correlation_matrix = data.corr()

# Configura el tamaño de la figura
plt.figure(figsize=(10, 8))

# Crea un mapa de calor (heatmap) de la matriz de correlación
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=.5)

# Añade etiquetas de los ejes
plt.title('Matriz de Correlación')
plt.show()

# Codigo de ML

# Verificar valores nulos en el DataFrame
valores_nulos = data.isnull().sum()

# Mostrar el recuento de valores nulos por columna
print(valores_nulos)
# Data.dropna(inplace=True)

# En esta ocasion no tenemos valores nulos

# No tenemos que comvertir datos en dummys, gracias a dios

# Seleccionamos nuestra variable target
# En nuestro caso sera quality
y=data[['quality']].values
data.drop(data[['quality']],axis=1,inplace=True)
X=data.values
X_train, X_test, y_train, y_test=train_test_split(X, y, test_size=0.2, random_state=7)

# Entrenamos nuestro modelo (la profundidad fue puesta de manera manual buscando
# el mejor valor)
model = DecisionTreeRegressor(max_depth=4)
model.fit(X_train, y_train)
y_pred=model.predict(X_test)
y_pred_train = model.predict(X_train)

# mostramos la profundidad actual del arbol
depth = model.tree_.max_depth
print("Profundidad máxima del árbol:", depth)

# Vamos a buscar medir la efectividad de nuestro metodo
# El mas importante para nosotros sera el MSE
mse = mean_squared_error(y_test,y_pred)
#mae = mean_absolute_error(y_test,y_pred)

print('MSE  (deseable 0): {}'.format(mse))
#print('MAE (deseable 0): {}'.format(mae))

# Crea listas para almacenar los valores de profundidad máxima y MSE
depth_values = []
mse_values = []
mse_train_values = []


max_depths=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]

# Realiza un bucle for para ajustar el modelo y calcular el MSE para cada profundidad máxima
for depth in max_depths:
    model = DecisionTreeRegressor(max_depth=depth)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_pred_train = model.predict(X_train)
    mse = mean_squared_error(y_test, y_pred)
    mse_train = mean_squared_error(y_train, y_pred_train)


    depth_values.append(depth)
    mse_values.append(mse)
    mse_train_values.append(mse_train)


# Crea la gráfica
plt.figure(figsize=(8, 6))
plt.plot(depth_values, mse_values, marker='o', label='MSE en Test')
plt.plot(depth_values, mse_train_values, marker='x', label='MSE en Train')
plt.title('MSE vs. Profundidad Máxima del Árbol')
plt.xlabel('Profundidad Máxima del Árbol')
plt.ylabel('MSE')
plt.grid(True)
plt.legend()
plt.show()





# Gracias a la siguiente grafica podemos ver la varianza y ver el fit del modelo

"""# Diagnóstico y explicación el nivel de ajuste del modelo: underfitt fitt overfitt

Podemos ver en la grafica como se desepeña el modelo en los datos de train y test (menor error es mejor) curiosamente el modelo de prueba da un mejor rendimiento al principio, pero si no entrenamos el modelo hasta que tenga una profundidad de 4 no alcansamos a reducir de mejor manera el error, si solo usamos una profundidad de 3 o menor el modelo sigue teniendo un nivel alto de error lo que nos indicaria que tiene underfitting o le falta entrenamiento

pero si seguimos entrenando el modelo podemos ver como reducimos el error de set de prueba hasta 0 pero el error de el set prueba aumenta, lo cual nos indica que nuestro modelo se esta sobre entrenando y no funcionada en el mundo real, solo funciona con los datos que ya conoce
# Diagnóstico y explicación el grado de varianza: bajo medio alto
cabe recalcar que sabemos que la grafica tambien nos indica la varianza, al principio la varianza es baja por que el mode esta en underfitting, pero conforme aumenta la complejidad observamos que aumenta la varianza entre el set de entrenamiento y de prueba
#Diagnóstico y explicación el grado de bias o sesgo: bajo medio alto
y por ultimo el Bias aumenta conforme el modelo entiende mejor el data set, por eso al principio es bajo e ira aumentando, el problema principal es que el modelo se sobre entrenara lo cual hace el error de bias baje pero aumentando la varianza

# resumen

podemos revisar que se cumple lo visto en clase, al principio la varianza es bajar y el sesgo es alto mientras el modelo esta en underfitting pero conforme avanza revisamos que la varianza aumenta, el sesgo disminuye hasta que estan en equilibrio cuando esta el modelo correctamente entrenado y si lo sobre entrenamos vemos que la varianza se dispara y el sesgo se reduce

Hora haremos un Grid search para encontrar los mejores parametros de nuestro modelo, usaremos un grid search en lugar de una random search por que el poder computacional no es un problema
"""

#Grid search


model1 = DecisionTreeRegressor()

# Define el espacio de búsqueda de hiperparámetros
param_grid = {
    'max_depth':[None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15],
    'criterion' : ['squared_error', 'friedman_mse', 'absolute_error','poisson'],
    'min_samples_leaf': [1, 2,3, 4,5,6,7,8]
}

# Crea un objeto GridSearchCV
grid_search = GridSearchCV(estimator=model1, param_grid=param_grid, cv=5, scoring='neg_mean_squared_error')

# Se usa el grid search

grid_search.fit(X, y)

# Imprime los mejores hiperparámetros encontrados
print("Mejores hiperparámetros encontrados: ", grid_search.best_params_)

# Imprime la mejor puntuación de validación cruzada
print("Mejor puntuación de validación cruzada: ", grid_search.best_score_)



model = DecisionTreeRegressor(criterion= 'poisson', max_depth= 5, min_samples_leaf= 8)
model.fit(X_train, y_train)
y_pred=model.predict(X_test)
y_pred_train = model.predict(X_train)

depth = model.tree_.max_depth
print("Profundidad máxima del árbol:", depth)


# Vamos a buscar medir la efectividad de nuestro metodo
# El mas importante para nosotros sera el MSE
mse = mean_squared_error(y_test,y_pred)


print('MSE  (deseable 0): {}'.format(mse))

# Crea listas para almacenar los valores de profundidad máxima y MSE
depth_values = []
mse_values = []
mse_train_values = []


max_depths=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]

# Realiza un bucle for para ajustar el modelo y calcular el MSE para cada profundidad máxima
for depth in max_depths:
    model = DecisionTreeRegressor(criterion= 'poisson', max_depth= depth, min_samples_leaf= 8)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_pred_train = model.predict(X_train)
    mse = mean_squared_error(y_test, y_pred)
    mse_train = mean_squared_error(y_train, y_pred_train)


    depth_values.append(depth)
    mse_values.append(mse)
    mse_train_values.append(mse_train)


# Crea la gráfica
plt.figure(figsize=(8, 6))
plt.plot(depth_values, mse_values, marker='o', label='MSE en Test')
plt.plot(depth_values, mse_train_values, marker='x', label='MSE en Train')
plt.title('MSE vs. Profundidad Máxima del Árbol')
plt.xlabel('Profundidad Máxima del Árbol')
plt.ylabel('MSE')
plt.grid(True)
plt.legend()
plt.show()





# Gracias a la siguiente grafica podemos ver la varianza y ver el fit del modelo

#Impresionantemente el grid no logro encontrar mejores parametros que los bases,
#probe otros parametros de scoring, sospecho que puede ser que no use el
#ramdon state, y puede que el data set sea el problema de esa variacion minima
#en resumen sea cualquiera de las 2 maneras se puede