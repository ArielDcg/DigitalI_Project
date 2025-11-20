"""
Demostración rápida de la Red Neuronal
Ejecuta un ejemplo simple en menos de 10 segundos
"""

from neural_network import NeuralNetwork
import random


def quick_demo():
    """Demo rápida: XOR en 5000 épocas"""

    print("\n" + "="*70)
    print("DEMOSTRACIÓN RÁPIDA - RED NEURONAL DESDE CERO")
    print("="*70)
    print("\nProblema: Aprender la función XOR")
    print("Arquitectura: 2 → 4 → 1 (17 parámetros totales)")
    print("-"*70)

    # Crear red
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

    print("\nDataset:")
    print("  A   B  │  XOR")
    print("─────────┼─────")
    for inputs, targets in training_data:
        print(f"  {inputs[0]}   {inputs[1]}  │   {targets[0]}")

    # Entrenar
    print("\nEntrenando 5,000 épocas... ", end="", flush=True)

    epochs = 5000
    for epoch in range(epochs):
        random.shuffle(training_data)
        for inputs, targets in training_data:
            nn.train(inputs, targets)

    print("✓ Completado")

    # Evaluar
    print("\n" + "-"*70)
    print("RESULTADOS:")
    print("-"*70)
    print("  A   B  │  Predicción  │  Esperado  │  Estado")
    print("─────────┼──────────────┼────────────┼──────────")

    total_error = 0
    for inputs, targets in training_data:
        prediction = nn.predict(inputs)
        error = abs(prediction[0] - targets[0])
        total_error += error

        status = "✓ PASS" if error < 0.5 else "✗ FAIL"
        print(f"  {inputs[0]}   {inputs[1]}  │    {prediction[0]:.4f}    │     {targets[0]}      │  {status}")

    accuracy = (1 - total_error / len(training_data)) * 100

    print("-"*70)
    print(f"Precisión: {accuracy:.2f}%")
    print("="*70)

    # Calcular error final
    final_loss = 0
    for inputs, targets in training_data:
        predictions = nn.predict(inputs)
        final_loss += nn.calculate_loss(predictions, targets)
    final_loss /= len(training_data)

    print(f"\nError (MSE): {final_loss:.6f}")

    # Mostrar algunos pesos (para verificar que aprendió)
    print(f"\nAlgunos pesos aprendidos:")
    print(f"  Capa 1 (primeros 4 pesos): {nn.weights[0].data[0][:4]}")

    print("\n" + "="*70)
    print("Para más ejemplos, ejecuta: python3 train.py")
    print("="*70 + "\n")


if __name__ == "__main__":
    quick_demo()
