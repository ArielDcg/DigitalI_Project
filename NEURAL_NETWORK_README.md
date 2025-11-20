# Red Neuronal desde Cero - Sin Librerías Externas

## 🧠 Descripción

Implementación completa de una red neuronal artificial desde cero usando **únicamente Python puro**, sin dependencias externas como NumPy, TensorFlow o PyTorch.

Este proyecto demuestra los conceptos fundamentales del aprendizaje profundo implementando:
- Operaciones matriciales básicas
- Propagación hacia adelante (forward propagation)
- Propagación hacia atrás (backpropagation)
- Descenso de gradiente
- Múltiples funciones de activación
- Arquitecturas de redes profundas

## 📁 Estructura del Proyecto

```
.
├── neural_network.py      # Implementación de la red neuronal
├── train.py              # Script de entrenamiento con ejemplos
├── visualize_network.py  # Visualizador de arquitecturas
└── NEURAL_NETWORK_README.md  # Este archivo
```

## 🚀 Uso Rápido

### 1. Ejecutar Ejemplos de Entrenamiento

```bash
python3 train.py
```

Este comando abrirá un menú interactivo con 4 ejemplos:

1. **Compuerta XOR** - Problema clásico no linealmente separable
2. **Múltiples Compuertas Lógicas** - AND, OR, NAND, NOR simultáneamente
3. **Aproximación de Función Seno** - Regresión de funciones continuas
4. **Reconocimiento de Patrones 3×3** - Clasificación de patrones visuales

### 2. Visualizar Arquitecturas

```bash
python3 visualize_network.py
```

Muestra diagramas ASCII de todas las arquitecturas de ejemplo y permite diseñar redes personalizadas.

### 3. Uso Programático

```python
from neural_network import NeuralNetwork

# Crear una red neuronal
# 2 entradas, 1 capa oculta con 4 neuronas, 1 salida
nn = NeuralNetwork(input_nodes=2, hidden_nodes=[4], output_nodes=1)

# Configurar parámetros
nn.set_learning_rate(0.5)
nn.set_activation_function('sigmoid')

# Datos de entrenamiento (XOR)
training_data = [
    ([0, 0], [0]),
    ([0, 1], [1]),
    ([1, 0], [1]),
    ([1, 1], [0])
]

# Entrenar
for epoch in range(10000):
    for inputs, targets in training_data:
        nn.train(inputs, targets)

# Predecir
prediction = nn.predict([1, 0])
print(f"Predicción: {prediction[0]:.4f}")

# Guardar/Cargar modelo
nn.save_model('mi_modelo.json')
nn.load_model('mi_modelo.json')
```

## 🏗️ Arquitecturas de Ejemplo

### Ejemplo 1: XOR (17 parámetros)
```
ENTRADA (2) → OCULTA (4) → SALIDA (1)
```
- **Problema**: Función XOR no linealmente separable
- **Precisión**: >95% después de 20,000 épocas

### Ejemplo 2: Compuertas Lógicas (60 parámetros)
```
ENTRADA (2) → OCULTA (8) → SALIDA (4)
```
- **Problema**: AND, OR, NAND, NOR simultáneamente
- **Precisión**: >99% después de 30,000 épocas

### Ejemplo 3: Función Seno (321 parámetros)
```
ENTRADA (1) → OCULTA (16) → OCULTA (16) → SALIDA (1)
```
- **Problema**: Aproximar sen(x) en [0, 2π]
- **Error**: <0.05 después de 10,000 épocas

### Ejemplo 4: Patrones 3×3 (260 parámetros)
```
ENTRADA (9) → OCULTA (12) → OCULTA (8) → SALIDA (4)
```
- **Problema**: Clasificar patrones visuales (Cruz, Líneas, Diagonal)
- **Precisión**: >90% con ruido después de 5,000 épocas

## 🔧 Características Técnicas

### Operaciones Matriciales
Implementación completa sin NumPy:
- Multiplicación de matrices
- Transposición
- Producto de Hadamard (elemento por elemento)
- Operaciones escalares

### Funciones de Activación
- **Sigmoid**: σ(x) = 1 / (1 + e^(-x))
- **Tanh**: tanh(x)
- **ReLU**: max(0, x)
- **Leaky ReLU**: max(αx, x)

### Algoritmo de Entrenamiento
1. **Forward Propagation**: Calcular salidas de cada capa
2. **Cálculo de Error**: Diferencia entre predicción y objetivo
3. **Backpropagation**: Propagar error hacia atrás
4. **Actualización de Pesos**: Descenso de gradiente

### Inicialización de Pesos
- Inicialización Xavier/Glorot para mejor convergencia
- Límite: √(6 / (n_in + n_out))

## 📊 Ejemplos de Salida

### Entrenamiento XOR
```
=============================================================
PROBLEMA 1: Compuerta XOR
=============================================================

Dataset de entrenamiento:
  [0, 0] -> [0]
  [0, 1] -> [1]
  [1, 0] -> [1]
  [1, 1] -> [0]

Entrenando red neuronal...
Época 2000/20000 - Loss: 0.152341
Época 4000/20000 - Loss: 0.062847
...
Época 20000/20000 - Loss: 0.001523

-------------------------------------------------------------
RESULTADOS:
-------------------------------------------------------------
Entrada: [0, 0] -> Predicción: 0.0234 | Esperado: 0 | ✓ CORRECTO
Entrada: [0, 1] -> Predicción: 0.9812 | Esperado: 1 | ✓ CORRECTO
Entrada: [1, 0] -> Predicción: 0.9823 | Esperado: 1 | ✓ CORRECTO
Entrada: [1, 1] -> Predicción: 0.0187 | Esperado: 0 | ✓ CORRECTO

Precisión: 98.12%
```

### Visualización de Arquitectura
```
================================================================================
                            EJEMPLO 1: COMPUERTA XOR
================================================================================

    ENTRADA       OCULTA 1        SALIDA
  (2 neuronas)   (4 neuronas)   (1 neuronas)

                      ●  ----
       ●  ----       ●  ----
                                     ●
       ●  ----       ●  ----
                      ●  ----

Total de capas: 3
TOTAL DE PARÁMETROS: 17
```

## 🎓 Conceptos Implementados

### 1. Red Neuronal Feedforward
Arquitectura donde la información fluye solo hacia adelante, desde la entrada hasta la salida.

### 2. Backpropagation
Algoritmo para calcular gradientes eficientemente:
- Calcula derivadas parciales usando la regla de la cadena
- Propaga errores desde la salida hacia la entrada
- Permite entrenar redes profundas

### 3. Descenso de Gradiente
Método de optimización:
- Ajusta pesos en dirección opuesta al gradiente
- Tasa de aprendizaje controla el tamaño del paso
- Minimiza la función de pérdida

### 4. Función de Pérdida MSE
Error Cuadrático Medio:
```
MSE = (1/n) Σ(y_pred - y_true)²
```

## 🛠️ API de la Clase NeuralNetwork

### Constructor
```python
nn = NeuralNetwork(
    input_nodes=2,      # Número de entradas
    hidden_nodes=[4],   # Lista de capas ocultas
    output_nodes=1      # Número de salidas
)
```

### Métodos Principales

#### Configuración
```python
nn.set_learning_rate(0.1)           # Establece tasa de aprendizaje
nn.set_activation_function('relu')  # sigmoid, tanh, relu, leaky_relu
```

#### Entrenamiento
```python
nn.train(input_array, target_array)  # Entrena con un ejemplo
```

#### Predicción
```python
predictions = nn.predict(input_array)  # Obtiene predicciones
predictions = nn.feedforward(input_array)  # Alias
```

#### Evaluación
```python
loss = nn.calculate_loss(predictions, targets)  # Calcula MSE
```

#### Persistencia
```python
nn.save_model('modelo.json')   # Guarda pesos y arquitectura
nn.load_model('modelo.json')   # Carga modelo guardado
```

## 📈 Consejos de Entrenamiento

### Tasa de Aprendizaje
- **Muy alta** (>1.0): Entrenamiento inestable, no converge
- **Alta** (0.5-1.0): Convergencia rápida, puede oscilar
- **Media** (0.1-0.5): Balance entre velocidad y estabilidad
- **Baja** (0.01-0.1): Convergencia lenta pero estable
- **Muy baja** (<0.01): Muy lento, puede quedarse atascado

### Funciones de Activación
- **Sigmoid**: Buena para salidas binarias (0-1)
- **Tanh**: Centrada en 0, mejor gradiente que sigmoid
- **ReLU**: Rápida, evita vanishing gradient, buena para redes profundas
- **Leaky ReLU**: Evita "neuronas muertas" de ReLU

### Número de Neuronas Ocultas
- Muy pocas: Subajuste (underfitting)
- Muchas: Sobreajuste (overfitting)
- Regla general: Entre el tamaño de entrada y salida

### Número de Épocas
- Monitorear la pérdida
- Detener cuando deje de mejorar (early stopping)
- Para los ejemplos: 5,000-30,000 épocas

## 🔬 Experimentación

### Crear tu Propia Red

```python
from neural_network import NeuralNetwork

# Red profunda personalizada
nn = NeuralNetwork(
    input_nodes=10,
    hidden_nodes=[20, 15, 10],  # 3 capas ocultas
    output_nodes=5
)

# Tu dataset personalizado
training_data = [
    ([...], [...]),  # (entradas, salidas esperadas)
    # ... más ejemplos
]

# Entrenar
for epoch in range(epochs):
    for inputs, targets in training_data:
        nn.train(inputs, targets)
```

## 📚 Teoría Matemática

### Forward Propagation
Para cada capa l:
```
z^l = W^l * a^(l-1) + b^l
a^l = σ(z^l)
```

### Backpropagation
Calcular gradientes:
```
δ^L = (a^L - y) ⊙ σ'(z^L)
δ^l = (W^(l+1))^T * δ^(l+1) ⊙ σ'(z^l)
```

Actualizar pesos:
```
W^l = W^l - η * δ^l * (a^(l-1))^T
b^l = b^l - η * δ^l
```

Donde:
- W: Matriz de pesos
- b: Vector de biases
- a: Activaciones
- σ: Función de activación
- η: Tasa de aprendizaje
- ⊙: Producto de Hadamard

## 🎯 Casos de Uso

### 1. Aprendizaje y Educación
- Entender cómo funcionan las redes neuronales
- Implementar algoritmos desde cero
- Depurar paso a paso

### 2. Prototipado Rápido
- Probar conceptos sin dependencias
- Entornos con restricciones de librerías
- Demostraciónes y tutoriales

### 3. Problemas Pequeños
- Datasets pequeños (<1000 ejemplos)
- Arquitecturas simples (2-3 capas)
- Cuando NumPy/TensorFlow son excesivos

## ⚠️ Limitaciones

- **Rendimiento**: Más lento que NumPy (operaciones no vectorizadas)
- **Escalabilidad**: No adecuado para datasets grandes (>10,000 ejemplos)
- **Funcionalidades**: No incluye regularización, dropout, batch normalization
- **GPU**: No aprovecha aceleración por hardware

## 🚀 Mejoras Futuras

Posibles extensiones:
- [ ] Regularización L1/L2
- [ ] Dropout para prevenir overfitting
- [ ] Batch Normalization
- [ ] Momentum y Adam optimizer
- [ ] Convolutional layers
- [ ] Recurrent layers (LSTM/GRU)
- [ ] Validación cruzada
- [ ] Gráficas de entrenamiento

## 📖 Referencias

- [Deep Learning Book - Ian Goodfellow](http://www.deeplearningbook.org/)
- [Neural Networks and Deep Learning - Michael Nielsen](http://neuralnetworksanddeeplearning.com/)
- [3Blue1Brown - Neural Networks Series](https://www.youtube.com/watch?v=aircAruvnKk)

## 📝 Licencia

Este proyecto es de código abierto y está disponible para uso educativo.

## 👤 Autor

Implementado por Claude - Red Neuronal desde Cero (2025)

---

**¡Disfruta aprendiendo sobre redes neuronales! 🧠🔥**
