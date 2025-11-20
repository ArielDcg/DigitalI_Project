"""
Red Neuronal desde cero - Implementación completa sin librerías externas
Autor: Claude
Fecha: 2025-11-20
"""

import random
import math
import json
from typing import List, Callable, Tuple


class Matrix:
    """Clase para operaciones matriciales básicas"""

    def __init__(self, rows: int, cols: int, data: List[List[float]] = None):
        self.rows = rows
        self.cols = cols
        if data is None:
            self.data = [[0.0 for _ in range(cols)] for _ in range(rows)]
        else:
            self.data = data

    @staticmethod
    def from_array(arr: List[float]) -> 'Matrix':
        """Crea una matriz columna desde un array"""
        m = Matrix(len(arr), 1)
        for i in range(len(arr)):
            m.data[i][0] = arr[i]
        return m

    def to_array(self) -> List[float]:
        """Convierte matriz a array"""
        arr = []
        for i in range(self.rows):
            for j in range(self.cols):
                arr.append(self.data[i][j])
        return arr

    def randomize(self, low: float = -1.0, high: float = 1.0):
        """Inicializa con valores aleatorios"""
        for i in range(self.rows):
            for j in range(self.cols):
                self.data[i][j] = random.uniform(low, high)

    def add(self, other: 'Matrix') -> 'Matrix':
        """Suma de matrices"""
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Las dimensiones de las matrices no coinciden")

        result = Matrix(self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                result.data[i][j] = self.data[i][j] + other.data[i][j]
        return result

    def subtract(self, other: 'Matrix') -> 'Matrix':
        """Resta de matrices"""
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Las dimensiones de las matrices no coinciden")

        result = Matrix(self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                result.data[i][j] = self.data[i][j] - other.data[i][j]
        return result

    def multiply(self, other: 'Matrix') -> 'Matrix':
        """Multiplicación de matrices"""
        if self.cols != other.rows:
            raise ValueError(f"No se pueden multiplicar matrices de dimensiones {self.rows}x{self.cols} y {other.rows}x{other.cols}")

        result = Matrix(self.rows, other.cols)
        for i in range(result.rows):
            for j in range(result.cols):
                sum_val = 0
                for k in range(self.cols):
                    sum_val += self.data[i][k] * other.data[k][j]
                result.data[i][j] = sum_val
        return result

    def hadamard(self, other: 'Matrix') -> 'Matrix':
        """Producto de Hadamard (elemento por elemento)"""
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Las dimensiones de las matrices no coinciden")

        result = Matrix(self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                result.data[i][j] = self.data[i][j] * other.data[i][j]
        return result

    def scalar_multiply(self, scalar: float) -> 'Matrix':
        """Multiplicación por escalar"""
        result = Matrix(self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                result.data[i][j] = self.data[i][j] * scalar
        return result

    def transpose(self) -> 'Matrix':
        """Transpuesta de la matriz"""
        result = Matrix(self.cols, self.rows)
        for i in range(self.rows):
            for j in range(self.cols):
                result.data[j][i] = self.data[i][j]
        return result

    def map(self, func: Callable[[float], float]) -> 'Matrix':
        """Aplica una función a cada elemento"""
        result = Matrix(self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                result.data[i][j] = func(self.data[i][j])
        return result

    def copy(self) -> 'Matrix':
        """Crea una copia de la matriz"""
        return Matrix(self.rows, self.cols, [row[:] for row in self.data])

    def __str__(self):
        return '\n'.join(['\t'.join([f'{val:.4f}' for val in row]) for row in self.data])


class ActivationFunction:
    """Funciones de activación y sus derivadas"""

    @staticmethod
    def sigmoid(x: float) -> float:
        """Función sigmoide"""
        try:
            return 1 / (1 + math.exp(-x))
        except OverflowError:
            return 0.0 if x < 0 else 1.0

    @staticmethod
    def sigmoid_derivative(y: float) -> float:
        """Derivada de la sigmoide (y es la salida de sigmoid)"""
        return y * (1 - y)

    @staticmethod
    def tanh(x: float) -> float:
        """Función tangente hiperbólica"""
        return math.tanh(x)

    @staticmethod
    def tanh_derivative(y: float) -> float:
        """Derivada de tanh (y es la salida de tanh)"""
        return 1 - y * y

    @staticmethod
    def relu(x: float) -> float:
        """Rectified Linear Unit"""
        return max(0, x)

    @staticmethod
    def relu_derivative(y: float) -> float:
        """Derivada de ReLU (y es la salida de relu)"""
        return 1.0 if y > 0 else 0.0

    @staticmethod
    def leaky_relu(x: float, alpha: float = 0.01) -> float:
        """Leaky ReLU"""
        return x if x > 0 else alpha * x

    @staticmethod
    def leaky_relu_derivative(y: float, alpha: float = 0.01) -> float:
        """Derivada de Leaky ReLU"""
        return 1.0 if y > 0 else alpha


class NeuralNetwork:
    """
    Red Neuronal Feedforward completamente conectada
    Implementa backpropagation y descenso de gradiente
    """

    def __init__(self, input_nodes: int, hidden_nodes: List[int], output_nodes: int):
        """
        Inicializa la red neuronal

        Args:
            input_nodes: Número de neuronas de entrada
            hidden_nodes: Lista con el número de neuronas en cada capa oculta
            output_nodes: Número de neuronas de salida
        """
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes

        # Lista de capas (número de neuronas en cada capa)
        self.layers = [input_nodes] + hidden_nodes + [output_nodes]

        # Inicializar pesos y biases
        self.weights = []
        self.biases = []

        for i in range(len(self.layers) - 1):
            # Inicialización Xavier/Glorot
            limit = math.sqrt(6 / (self.layers[i] + self.layers[i + 1]))

            weight_matrix = Matrix(self.layers[i + 1], self.layers[i])
            weight_matrix.randomize(-limit, limit)
            self.weights.append(weight_matrix)

            bias_matrix = Matrix(self.layers[i + 1], 1)
            bias_matrix.randomize(-limit, limit)
            self.biases.append(bias_matrix)

        # Configuración de entrenamiento
        self.learning_rate = 0.1
        self.activation_function = ActivationFunction.sigmoid
        self.activation_derivative = ActivationFunction.sigmoid_derivative

    def set_learning_rate(self, lr: float):
        """Establece la tasa de aprendizaje"""
        self.learning_rate = lr

    def set_activation_function(self, activation: str):
        """
        Establece la función de activación

        Args:
            activation: 'sigmoid', 'tanh', 'relu', o 'leaky_relu'
        """
        if activation == 'sigmoid':
            self.activation_function = ActivationFunction.sigmoid
            self.activation_derivative = ActivationFunction.sigmoid_derivative
        elif activation == 'tanh':
            self.activation_function = ActivationFunction.tanh
            self.activation_derivative = ActivationFunction.tanh_derivative
        elif activation == 'relu':
            self.activation_function = ActivationFunction.relu
            self.activation_derivative = ActivationFunction.relu_derivative
        elif activation == 'leaky_relu':
            self.activation_function = ActivationFunction.leaky_relu
            self.activation_derivative = ActivationFunction.leaky_relu_derivative
        else:
            raise ValueError(f"Función de activación desconocida: {activation}")

    def feedforward(self, input_array: List[float]) -> List[float]:
        """
        Propagación hacia adelante

        Args:
            input_array: Array de entrada

        Returns:
            Array de salida
        """
        # Convertir entrada a matriz
        outputs = Matrix.from_array(input_array)

        # Propagar a través de cada capa
        for i in range(len(self.weights)):
            outputs = self.weights[i].multiply(outputs)
            outputs = outputs.add(self.biases[i])
            outputs = outputs.map(self.activation_function)

        return outputs.to_array()

    def train(self, input_array: List[float], target_array: List[float]):
        """
        Entrena la red con un ejemplo

        Args:
            input_array: Array de entrada
            target_array: Array de salida esperada
        """
        # === FORWARD PASS ===
        # Guardar todas las activaciones
        activations = [Matrix.from_array(input_array)]

        # Propagar a través de cada capa
        for i in range(len(self.weights)):
            outputs = self.weights[i].multiply(activations[-1])
            outputs = outputs.add(self.biases[i])
            outputs = outputs.map(self.activation_function)
            activations.append(outputs)

        # === BACKWARD PASS ===
        # Convertir target a matriz
        targets = Matrix.from_array(target_array)

        # Calcular error de salida
        errors = [targets.subtract(activations[-1])]

        # Backpropagation para calcular errores de cada capa
        for i in range(len(self.weights) - 1, 0, -1):
            error = self.weights[i].transpose().multiply(errors[0])
            errors.insert(0, error)

        # Actualizar pesos y biases
        for i in range(len(self.weights)):
            # Calcular gradiente
            gradients = activations[i + 1].map(self.activation_derivative)
            gradients = gradients.hadamard(errors[i])
            gradients = gradients.scalar_multiply(self.learning_rate)

            # Calcular deltas
            activations_t = activations[i].transpose()
            weight_deltas = gradients.multiply(activations_t)

            # Actualizar pesos y biases
            self.weights[i] = self.weights[i].add(weight_deltas)
            self.biases[i] = self.biases[i].add(gradients)

    def predict(self, input_array: List[float]) -> List[float]:
        """Alias para feedforward"""
        return self.feedforward(input_array)

    def calculate_loss(self, predictions: List[float], targets: List[float]) -> float:
        """
        Calcula el error cuadrático medio (MSE)

        Args:
            predictions: Predicciones de la red
            targets: Valores objetivo

        Returns:
            Error MSE
        """
        mse = 0.0
        for i in range(len(predictions)):
            error = targets[i] - predictions[i]
            mse += error * error
        return mse / len(predictions)

    def save_model(self, filename: str):
        """Guarda el modelo en un archivo JSON"""
        model_data = {
            'input_nodes': self.input_nodes,
            'hidden_nodes': self.hidden_nodes,
            'output_nodes': self.output_nodes,
            'learning_rate': self.learning_rate,
            'weights': [[row for row in w.data] for w in self.weights],
            'biases': [[row for row in b.data] for b in self.biases]
        }

        with open(filename, 'w') as f:
            json.dump(model_data, f, indent=2)

        print(f"Modelo guardado en {filename}")

    def load_model(self, filename: str):
        """Carga el modelo desde un archivo JSON"""
        with open(filename, 'r') as f:
            model_data = json.load(f)

        self.input_nodes = model_data['input_nodes']
        self.hidden_nodes = model_data['hidden_nodes']
        self.output_nodes = model_data['output_nodes']
        self.learning_rate = model_data['learning_rate']

        # Reconstruir capas
        self.layers = [self.input_nodes] + self.hidden_nodes + [self.output_nodes]

        # Cargar pesos y biases
        self.weights = []
        self.biases = []

        for w_data in model_data['weights']:
            rows = len(w_data)
            cols = len(w_data[0]) if rows > 0 else 0
            self.weights.append(Matrix(rows, cols, w_data))

        for b_data in model_data['biases']:
            rows = len(b_data)
            cols = len(b_data[0]) if rows > 0 else 0
            self.biases.append(Matrix(rows, cols, b_data))

        print(f"Modelo cargado desde {filename}")


def print_progress_bar(iteration: int, total: int, prefix: str = '', suffix: str = '',
                       length: int = 50, fill: str = '█'):
    """Imprime una barra de progreso en consola"""
    percent = 100 * (iteration / float(total))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent:.1f}% {suffix}', end='')
    if iteration == total:
        print()


if __name__ == "__main__":
    print("=== Red Neuronal desde Cero ===")
    print("Módulo de implementación básica")
    print("Importa este módulo para usar la red neuronal\n")

    # Ejemplo simple de uso
    print("Ejemplo: Red neuronal para XOR")
    nn = NeuralNetwork(2, [4], 1)
    nn.set_learning_rate(0.5)

    # Dataset XOR
    training_data = [
        ([0, 0], [0]),
        ([0, 1], [1]),
        ([1, 0], [1]),
        ([1, 1], [0])
    ]

    print("Entrenando...")
    epochs = 10000
    for epoch in range(epochs):
        if (epoch + 1) % 1000 == 0:
            print_progress_bar(epoch + 1, epochs, prefix='Progreso:', suffix='Completo')

        for inputs, targets in training_data:
            nn.train(inputs, targets)

    print("\nResultados después del entrenamiento:")
    for inputs, targets in training_data:
        prediction = nn.predict(inputs)
        print(f"Entrada: {inputs} -> Predicción: {prediction[0]:.4f} (Esperado: {targets[0]})")
