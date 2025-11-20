"""
Visualizador de arquitectura de redes neuronales en ASCII
Muestra la estructura de las redes usadas en los ejemplos
"""

from neural_network import NeuralNetwork


def draw_neuron(y: int, x: int) -> str:
    """Dibuja un neurona como un círculo"""
    return "●"


def draw_network_architecture(input_nodes: int, hidden_nodes: list, output_nodes: int, title: str = ""):
    """
    Dibuja la arquitectura de una red neuronal en ASCII art

    Args:
        input_nodes: Número de neuronas de entrada
        hidden_nodes: Lista con el número de neuronas en cada capa oculta
        output_nodes: Número de neuronas de salida
        title: Título de la red
    """
    print("\n" + "="*80)
    if title:
        print(f"{title:^80}")
    print("="*80)

    layers = [input_nodes] + hidden_nodes + [output_nodes]
    max_neurons = max(layers)

    # Determinar el ancho de cada columna
    col_width = 15
    total_width = len(layers) * col_width

    # Etiquetas de las capas
    print("\n")
    layer_labels = ["ENTRADA"] + [f"OCULTA {i+1}" for i in range(len(hidden_nodes))] + ["SALIDA"]

    # Imprimir etiquetas
    for i, label in enumerate(layer_labels):
        print(f"{label:^{col_width}}", end="")
    print()

    # Imprimir número de neuronas
    for i, num in enumerate(layers):
        print(f"({num} neuronas)".center(col_width), end="")
    print("\n")

    # Dibujar las neuronas capa por capa
    # Calcular espaciado vertical para centrar
    max_height = max_neurons * 2 + 1

    for row in range(max_height):
        line = ""
        for layer_idx, num_neurons in enumerate(layers):
            # Calcular si en esta fila debe haber una neurona
            start_row = (max_height - num_neurons * 2) // 2
            neuron_rows = [start_row + i * 2 for i in range(num_neurons)]

            col_content = " " * col_width

            if row in neuron_rows:
                # Hay una neurona en esta posición
                neuron_idx = neuron_rows.index(row)
                neuron_symbol = "●"

                # Centrar la neurona
                neuron_pos = col_width // 2
                col_content = " " * neuron_pos + neuron_symbol + " " * (col_width - neuron_pos - 1)

                # Dibujar conexiones a la siguiente capa
                if layer_idx < len(layers) - 1:
                    # Agregar líneas de conexión
                    next_num = layers[layer_idx + 1]
                    if next_num <= 4 or num_neurons <= 4:  # Solo si hay pocas neuronas
                        col_content = col_content[:-5] + "----"
                    else:
                        col_content = col_content[:-5] + " -- "

            line += col_content

        print(line)

    # Mostrar información adicional
    print("\n" + "-"*80)
    print(f"Total de capas: {len(layers)}")
    print(f"Total de parámetros (pesos + biases):")

    total_params = 0
    for i in range(len(layers) - 1):
        weights = layers[i] * layers[i + 1]
        biases = layers[i + 1]
        layer_params = weights + biases
        total_params += layer_params
        print(f"  Capa {i} → {i+1}: {weights:,} pesos + {biases:,} biases = {layer_params:,} parámetros")

    print(f"\nTOTAL DE PARÁMETROS: {total_params:,}")
    print("="*80)


def draw_simple_network(layers: list, title: str = ""):
    """
    Dibuja una red neuronal simple con todas las conexiones visibles

    Args:
        layers: Lista con el número de neuronas en cada capa
        title: Título de la red
    """
    print("\n" + "="*80)
    if title:
        print(f"{title:^80}")
    print("="*80 + "\n")

    max_neurons = max(layers)

    # Solo mostrar conexiones si la red es pequeña
    show_connections = max_neurons <= 5 and len(layers) <= 4

    if show_connections:
        print("Vista detallada con conexiones:\n")

        # Crear matriz para la visualización
        height = max_neurons * 3
        width = len(layers) * 20

        # Para cada capa
        for layer_idx, num_neurons in enumerate(layers):
            # Calcular posiciones verticales centradas
            spacing = height // (num_neurons + 1)

            for neuron_idx in range(num_neurons):
                y_pos = spacing * (neuron_idx + 1)

                # Dibujar neurona
                x_pos = layer_idx * 20 + 5
                print(" " * x_pos + "●", end="")

                # Dibujar conexiones a la siguiente capa
                if layer_idx < len(layers) - 1:
                    print(" ----", end="")

                print()

            print()

    # Mostrar representación compacta
    print("\nRepresentación compacta:\n")

    layer_labels = ["INPUT"] + [f"H{i+1}" for i in range(len(layers)-2)] + ["OUTPUT"]

    for i, (num, label) in enumerate(zip(layers, layer_labels)):
        if i > 0:
            print("    ║")
            print("    ║")
        print(f"  ┌─────────────┐")
        print(f"  │   {label:^7s}   │")
        print(f"  │ {num:^2d} neuronas │")
        print(f"  └─────────────┘")


def show_all_examples():
    """Muestra las arquitecturas de todos los ejemplos"""

    print("\n" + "█"*80)
    print("VISUALIZACIÓN DE ARQUITECTURAS DE REDES NEURONALES")
    print("█"*80)

    # Ejemplo 1: XOR
    draw_network_architecture(
        input_nodes=2,
        hidden_nodes=[4],
        output_nodes=1,
        title="EJEMPLO 1: COMPUERTA XOR"
    )

    print("\n📊 Descripción:")
    print("  • Problema: Aprender la función XOR (no linealmente separable)")
    print("  • Entrada: 2 valores binarios")
    print("  • Salida: 1 valor (resultado XOR)")
    print("  • Función de activación: Sigmoid")
    print("  • Tasa de aprendizaje: 0.5")

    # Ejemplo 2: Compuertas lógicas
    draw_network_architecture(
        input_nodes=2,
        hidden_nodes=[8],
        output_nodes=4,
        title="EJEMPLO 2: MÚLTIPLES COMPUERTAS LÓGICAS"
    )

    print("\n📊 Descripción:")
    print("  • Problema: Aprender AND, OR, NAND, NOR simultáneamente")
    print("  • Entrada: 2 valores binarios")
    print("  • Salida: 4 valores (una por cada compuerta)")
    print("  • Función de activación: Sigmoid")
    print("  • Tasa de aprendizaje: 0.3")

    # Ejemplo 3: Función seno
    draw_network_architecture(
        input_nodes=1,
        hidden_nodes=[16, 16],
        output_nodes=1,
        title="EJEMPLO 3: APROXIMACIÓN DE FUNCIÓN SENO"
    )

    print("\n📊 Descripción:")
    print("  • Problema: Aproximar la función sen(x) en [0, 2π]")
    print("  • Entrada: 1 valor (ángulo normalizado)")
    print("  • Salida: 1 valor (seno del ángulo)")
    print("  • Función de activación: Tanh")
    print("  • Tasa de aprendizaje: 0.01")
    print("  • Arquitectura más profunda para funciones no lineales complejas")

    # Ejemplo 4: Patrones
    draw_network_architecture(
        input_nodes=9,
        hidden_nodes=[12, 8],
        output_nodes=4,
        title="EJEMPLO 4: RECONOCIMIENTO DE PATRONES 3×3"
    )

    print("\n📊 Descripción:")
    print("  • Problema: Clasificar patrones visuales de 3×3 píxeles")
    print("  • Entrada: 9 valores (grid de 3×3)")
    print("  • Salida: 4 valores (Cruz, Horizontal, Vertical, Diagonal)")
    print("  • Función de activación: Sigmoid")
    print("  • Tasa de aprendizaje: 0.1")
    print("  • Incluye entrenamiento con variaciones y ruido")

    # Mostrar comparación
    print("\n" + "█"*80)
    print("COMPARACIÓN DE COMPLEJIDAD")
    print("█"*80 + "\n")

    examples = [
        ("XOR", [2, 4, 1]),
        ("Compuertas", [2, 8, 4]),
        ("Seno", [1, 16, 16, 1]),
        ("Patrones", [9, 12, 8, 4])
    ]

    print(f"{'Ejemplo':<20} {'Capas':<15} {'Parámetros':<15} {'Complejidad'}")
    print("-"*80)

    for name, layers in examples:
        total_params = 0
        for i in range(len(layers) - 1):
            total_params += layers[i] * layers[i + 1] + layers[i + 1]

        num_layers = len(layers)
        complexity = "Baja" if total_params < 100 else "Media" if total_params < 500 else "Alta"

        print(f"{name:<20} {num_layers:<15} {total_params:<15,} {complexity}")

    print("\n" + "█"*80)


def interactive_visualizer():
    """Visualizador interactivo"""
    print("\n" + "="*80)
    print("VISUALIZADOR INTERACTIVO DE REDES NEURONALES")
    print("="*80)

    while True:
        print("\nOpciones:")
        print("  1. Ver todas las arquitecturas de ejemplo")
        print("  2. Diseñar una red personalizada")
        print("  3. Comparar arquitecturas")
        print("  0. Salir")

        choice = input("\nSeleccione una opción: ").strip()

        if choice == '0':
            print("\n¡Hasta luego!")
            break
        elif choice == '1':
            show_all_examples()
        elif choice == '2':
            try:
                print("\n--- Diseño de Red Personalizada ---")
                input_nodes = int(input("Número de neuronas de entrada: "))
                num_hidden = int(input("Número de capas ocultas: "))
                hidden_nodes = []
                for i in range(num_hidden):
                    n = int(input(f"Neuronas en capa oculta {i+1}: "))
                    hidden_nodes.append(n)
                output_nodes = int(input("Número de neuronas de salida: "))

                draw_network_architecture(
                    input_nodes=input_nodes,
                    hidden_nodes=hidden_nodes,
                    output_nodes=output_nodes,
                    title="RED PERSONALIZADA"
                )
            except ValueError:
                print("Error: Por favor ingrese números válidos")
        elif choice == '3':
            show_all_examples()
        else:
            print("Opción inválida")


if __name__ == "__main__":
    # Mostrar ejemplos directamente
    show_all_examples()

    print("\n")
    response = input("¿Desea entrar al modo interactivo? (s/n): ").strip().lower()
    if response in ['s', 'si', 'sí', 'y', 'yes']:
        interactive_visualizer()
