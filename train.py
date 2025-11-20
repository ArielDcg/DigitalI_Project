"""
Script de entrenamiento de Red Neuronal
Incluye varios ejemplos de datasets y problemas
"""

from neural_network import NeuralNetwork, print_progress_bar
import random
import math


def train_xor():
    """
    Entrena una red neuronal para aprender la función XOR
    Este es un problema clásico no linealmente separable
    """
    print("\n" + "="*60)
    print("PROBLEMA 1: Compuerta XOR")
    print("="*60)

    # Crear red neuronal
    nn = NeuralNetwork(input_nodes=2, hidden_nodes=[4], output_nodes=1)
    nn.set_learning_rate(0.5)
    nn.set_activation_function('sigmoid')

    # Dataset XOR
    training_data = [
        ([0, 0], [0]),
        ([0, 1], [1]),
        ([1, 0], [1]),
        ([1, 1], [0])
    ]

    print("\nDataset de entrenamiento:")
    for inputs, targets in training_data:
        print(f"  {inputs} -> {targets}")

    # Entrenamiento
    print("\nEntrenando red neuronal...")
    epochs = 20000
    loss_history = []

    for epoch in range(epochs):
        # Mezclar datos
        random.shuffle(training_data)

        # Entrenar con cada ejemplo
        epoch_loss = 0
        for inputs, targets in training_data:
            nn.train(inputs, targets)
            predictions = nn.predict(inputs)
            epoch_loss += nn.calculate_loss(predictions, targets)

        epoch_loss /= len(training_data)
        loss_history.append(epoch_loss)

        # Mostrar progreso
        if (epoch + 1) % 2000 == 0:
            print(f"Época {epoch + 1}/{epochs} - Loss: {epoch_loss:.6f}")

    # Evaluación
    print("\n" + "-"*60)
    print("RESULTADOS:")
    print("-"*60)
    total_error = 0
    for inputs, targets in training_data:
        prediction = nn.predict(inputs)
        error = abs(prediction[0] - targets[0])
        total_error += error
        resultado = "✓ CORRECTO" if error < 0.5 else "✗ INCORRECTO"
        print(f"Entrada: {inputs} -> Predicción: {prediction[0]:.4f} | Esperado: {targets[0]} | {resultado}")

    accuracy = (1 - total_error / len(training_data)) * 100
    print(f"\nPrecisión: {accuracy:.2f}%")
    print(f"Error promedio final: {loss_history[-1]:.6f}")

    # Guardar modelo
    nn.save_model('xor_model.json')

    return nn


def train_logic_gates():
    """
    Entrena una red neuronal para aprender múltiples compuertas lógicas
    AND, OR, NAND, NOR
    """
    print("\n" + "="*60)
    print("PROBLEMA 2: Múltiples Compuertas Lógicas")
    print("="*60)

    # Crear red neuronal con 4 salidas (una por cada compuerta)
    nn = NeuralNetwork(input_nodes=2, hidden_nodes=[8], output_nodes=4)
    nn.set_learning_rate(0.3)
    nn.set_activation_function('sigmoid')

    # Dataset: [A, B] -> [AND, OR, NAND, NOR]
    training_data = [
        ([0, 0], [0, 0, 1, 1]),
        ([0, 1], [0, 1, 1, 0]),
        ([1, 0], [0, 1, 1, 0]),
        ([1, 1], [1, 1, 0, 0])
    ]

    print("\nDataset de entrenamiento:")
    print("Entrada -> [AND, OR, NAND, NOR]")
    for inputs, targets in training_data:
        print(f"  {inputs} -> {targets}")

    # Entrenamiento
    print("\nEntrenando red neuronal...")
    epochs = 30000

    for epoch in range(epochs):
        random.shuffle(training_data)

        for inputs, targets in training_data:
            nn.train(inputs, targets)

        if (epoch + 1) % 5000 == 0:
            # Calcular loss
            total_loss = 0
            for inputs, targets in training_data:
                predictions = nn.predict(inputs)
                total_loss += nn.calculate_loss(predictions, targets)
            total_loss /= len(training_data)
            print(f"Época {epoch + 1}/{epochs} - Loss: {total_loss:.6f}")

    # Evaluación
    print("\n" + "-"*60)
    print("RESULTADOS:")
    print("-"*60)
    print("Entrada | AND  | OR   | NAND | NOR  |")
    print("-"*60)

    gate_names = ['AND', 'OR', 'NAND', 'NOR']
    correct_predictions = 0
    total_predictions = len(training_data) * 4

    for inputs, targets in training_data:
        prediction = nn.predict(inputs)
        print(f"{inputs} | ", end="")

        for i, (pred, target) in enumerate(zip(prediction, targets)):
            rounded = round(pred)
            is_correct = rounded == target
            if is_correct:
                correct_predictions += 1
            symbol = "✓" if is_correct else "✗"
            print(f"{pred:.2f}{symbol} | ", end="")
        print()

    accuracy = (correct_predictions / total_predictions) * 100
    print(f"\nPrecisión: {accuracy:.2f}%")

    # Guardar modelo
    nn.save_model('logic_gates_model.json')

    return nn


def train_sine_wave():
    """
    Entrena una red neuronal para aproximar la función seno
    Ejemplo de regresión no lineal
    """
    print("\n" + "="*60)
    print("PROBLEMA 3: Aproximación de la función SENO")
    print("="*60)

    # Crear red neuronal
    nn = NeuralNetwork(input_nodes=1, hidden_nodes=[16, 16], output_nodes=1)
    nn.set_learning_rate(0.01)
    nn.set_activation_function('tanh')

    # Generar dataset
    print("\nGenerando dataset de entrenamiento...")
    training_data = []
    test_data = []

    # Datos de entrenamiento: 0 a 2π
    for i in range(100):
        x = (i / 100) * 2 * math.pi
        y = math.sin(x)
        # Normalizar entrada a [-1, 1]
        x_norm = (x / (2 * math.pi)) * 2 - 1
        training_data.append(([x_norm], [y]))

    # Datos de prueba
    for i in range(50):
        x = (i / 50) * 2 * math.pi
        y = math.sin(x)
        x_norm = (x / (2 * math.pi)) * 2 - 1
        test_data.append(([x_norm], [y]))

    print(f"Ejemplos de entrenamiento: {len(training_data)}")
    print(f"Ejemplos de prueba: {len(test_data)}")

    # Entrenamiento
    print("\nEntrenando red neuronal...")
    epochs = 10000
    batch_size = 10

    for epoch in range(epochs):
        random.shuffle(training_data)

        # Mini-batch training
        for i in range(0, len(training_data), batch_size):
            batch = training_data[i:i+batch_size]
            for inputs, targets in batch:
                nn.train(inputs, targets)

        if (epoch + 1) % 1000 == 0:
            # Calcular loss en conjunto de prueba
            test_loss = 0
            for inputs, targets in test_data:
                predictions = nn.predict(inputs)
                test_loss += nn.calculate_loss(predictions, targets)
            test_loss /= len(test_data)
            print(f"Época {epoch + 1}/{epochs} - Test Loss: {test_loss:.6f}")

    # Evaluación
    print("\n" + "-"*60)
    print("RESULTADOS EN PUNTOS DE PRUEBA:")
    print("-"*60)
    print("X (rad) | Predicción | Esperado | Error")
    print("-"*60)

    total_error = 0
    for i in range(0, len(test_data), 10):  # Mostrar cada 10 puntos
        inputs, targets = test_data[i]
        prediction = nn.predict(inputs)
        x_original = ((inputs[0] + 1) / 2) * 2 * math.pi
        error = abs(prediction[0] - targets[0])
        total_error += error
        print(f"{x_original:.4f} | {prediction[0]:>10.4f} | {targets[0]:>8.4f} | {error:.4f}")

    # Calcular error promedio en todo el conjunto de prueba
    total_test_error = 0
    for inputs, targets in test_data:
        prediction = nn.predict(inputs)
        total_test_error += abs(prediction[0] - targets[0])

    avg_error = total_test_error / len(test_data)
    print(f"\nError absoluto promedio: {avg_error:.6f}")

    # Guardar modelo
    nn.save_model('sine_model.json')

    return nn


def train_pattern_recognition():
    """
    Entrena una red neuronal para reconocer patrones simples de 3x3
    Problema de clasificación de patrones
    """
    print("\n" + "="*60)
    print("PROBLEMA 4: Reconocimiento de Patrones 3x3")
    print("="*60)

    # Crear red neuronal
    # Entrada: 9 píxeles (3x3), Salida: 4 clases (cruz, línea horizontal, línea vertical, diagonal)
    nn = NeuralNetwork(input_nodes=9, hidden_nodes=[12, 8], output_nodes=4)
    nn.set_learning_rate(0.1)
    nn.set_activation_function('sigmoid')

    # Definir patrones (1 = negro, 0 = blanco)
    patterns = {
        'Cruz': [
            0, 1, 0,
            1, 1, 1,
            0, 1, 0
        ],
        'Horizontal': [
            0, 0, 0,
            1, 1, 1,
            0, 0, 0
        ],
        'Vertical': [
            0, 1, 0,
            0, 1, 0,
            0, 1, 0
        ],
        'Diagonal': [
            1, 0, 0,
            0, 1, 0,
            0, 0, 1
        ]
    }

    # Crear dataset de entrenamiento con variaciones
    training_data = []

    # Agregar patrones originales
    target_vectors = {
        'Cruz': [1, 0, 0, 0],
        'Horizontal': [0, 1, 0, 0],
        'Vertical': [0, 0, 1, 0],
        'Diagonal': [0, 0, 0, 1]
    }

    for name, pattern in patterns.items():
        training_data.append((pattern, target_vectors[name]))

    # Agregar versiones con ruido
    for _ in range(20):
        for name, pattern in patterns.items():
            noisy_pattern = pattern.copy()
            # Cambiar aleatoriamente 1-2 píxeles
            for _ in range(random.randint(1, 2)):
                idx = random.randint(0, 8)
                noisy_pattern[idx] = 1 - noisy_pattern[idx]
            training_data.append((noisy_pattern, target_vectors[name]))

    print(f"\nPatrones definidos: {len(patterns)}")
    print(f"Ejemplos de entrenamiento (con variaciones): {len(training_data)}")

    print("\nPatrones originales:")
    for name, pattern in patterns.items():
        print(f"\n{name}:")
        for i in range(0, 9, 3):
            print("  " + " ".join(["█" if p else "·" for p in pattern[i:i+3]]))

    # Entrenamiento
    print("\nEntrenando red neuronal...")
    epochs = 5000

    for epoch in range(epochs):
        random.shuffle(training_data)

        for inputs, targets in training_data:
            nn.train(inputs, targets)

        if (epoch + 1) % 1000 == 0:
            # Calcular precisión en patrones originales
            correct = 0
            for name, pattern in patterns.items():
                prediction = nn.predict(pattern)
                predicted_class = prediction.index(max(prediction))
                expected_class = list(patterns.keys()).index(name)
                if predicted_class == expected_class:
                    correct += 1

            accuracy = (correct / len(patterns)) * 100
            print(f"Época {epoch + 1}/{epochs} - Precisión: {accuracy:.1f}%")

    # Evaluación
    print("\n" + "-"*60)
    print("RESULTADOS EN PATRONES ORIGINALES:")
    print("-"*60)

    class_names = list(patterns.keys())
    correct = 0

    for name, pattern in patterns.items():
        prediction = nn.predict(pattern)
        predicted_class = prediction.index(max(prediction))
        predicted_name = class_names[predicted_class]
        confidence = max(prediction) * 100

        is_correct = predicted_name == name
        if is_correct:
            correct += 1

        print(f"\nPatrón: {name}")
        for i in range(0, 9, 3):
            print("  " + " ".join(["█" if p else "·" for p in pattern[i:i+3]]))
        print(f"Predicción: {predicted_name} (confianza: {confidence:.1f}%)")
        print(f"Estado: {'✓ CORRECTO' if is_correct else '✗ INCORRECTO'}")

    accuracy = (correct / len(patterns)) * 100
    print(f"\nPrecisión final: {accuracy:.1f}%")

    # Guardar modelo
    nn.save_model('pattern_model.json')

    return nn


def main_menu():
    """Menú principal para seleccionar ejemplos"""
    print("\n" + "="*60)
    print("ENTRENAMIENTO DE RED NEURONAL - SIN LIBRERÍAS EXTERNAS")
    print("="*60)
    print("\nImplementación completamente desde cero usando solo Python")
    print("\nEjemplos disponibles:")
    print("  1. Compuerta XOR (problema clásico no lineal)")
    print("  2. Múltiples Compuertas Lógicas (AND, OR, NAND, NOR)")
    print("  3. Aproximación de función Seno (regresión)")
    print("  4. Reconocimiento de Patrones 3x3 (clasificación)")
    print("  5. Ejecutar todos los ejemplos")
    print("  0. Salir")

    while True:
        try:
            print("\n" + "-"*60)
            choice = input("\nSeleccione una opción (0-5): ").strip()

            if choice == '0':
                print("\n¡Hasta luego!")
                break
            elif choice == '1':
                train_xor()
            elif choice == '2':
                train_logic_gates()
            elif choice == '3':
                train_sine_wave()
            elif choice == '4':
                train_pattern_recognition()
            elif choice == '5':
                train_xor()
                train_logic_gates()
                train_sine_wave()
                train_pattern_recognition()
                print("\n" + "="*60)
                print("TODOS LOS EJEMPLOS COMPLETADOS")
                print("="*60)
            else:
                print("Opción inválida. Por favor seleccione 0-5.")

        except KeyboardInterrupt:
            print("\n\nInterrumpido por el usuario.")
            break
        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    main_menu()
