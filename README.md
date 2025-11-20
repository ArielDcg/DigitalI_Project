# Analizador de Expresiones Lógicas

Un analizador de expresiones lógicas que genera tablas de verdad utilizando símbolos lógicos estándar.

## Características

- ✅ Soporta múltiples símbolos para cada operador lógico
- ✅ Genera tablas de verdad completas
- ✅ Manejo de paréntesis para precedencia
- ✅ Interfaz de línea de comandos
- ✅ Interfaz web interactiva

## Operadores Soportados

| Operador | Símbolos | Descripción |
|----------|----------|-------------|
| **NOT** | `¬`, `!`, `NOT` | Negación |
| **AND** | `∧`, `&&`, `AND` | Conjunción |
| **OR** | `∨`, `\|\|`, `OR` | Disyunción |
| **XOR** | `⊕`, `XOR` | Disyunción exclusiva |
| **IMPLIES** | `→`, `=>`, `IMPLIES` | Implicación |
| **IFF** | `↔`, `<=>`, `IFF` | Bicondicional (si y solo si) |

## Instalación

No requiere instalación de dependencias. Solo necesitas Node.js instalado.

```bash
# Clonar o descargar el proyecto
git clone <repository-url>
cd DigitalI_Project
```

## Uso

### Desde la línea de comandos

```bash
# Ejecutar con los ejemplos predefinidos
node logic-expression-analyzer.js

# Analizar una expresión personalizada
node logic-expression-analyzer.js "A ∧ B"
node logic-expression-analyzer.js "(A ∨ B) → C"
node logic-expression-analyzer.js "¬(A ∧ B) ↔ (¬A ∨ ¬B)"
```

### Desde el navegador

Abre el archivo `index.html` en tu navegador web para usar la interfaz interactiva.

### Como módulo en tu código

```javascript
const LogicExpressionAnalyzer = require('./logic-expression-analyzer');

const analyzer = new LogicExpressionAnalyzer();

// Generar tabla de verdad
const result = analyzer.generateTruthTable('A ∧ B');

if (result.success) {
    console.log(analyzer.formatTruthTable(result));

    // Acceder a los datos
    console.log('Variables:', result.variables);
    console.log('Tabla:', result.table);
} else {
    console.error('Error:', result.error);
}
```

## Ejemplos de Expresiones

### Operaciones básicas

```
A ∧ B          # A AND B
A ∨ B          # A OR B
¬A             # NOT A
A → B          # A implica B
A ↔ B          # A si y solo si B
A ⊕ B          # A XOR B
```

### Expresiones complejas

```
(A ∨ B) ∧ C
¬(A ∧ B)
(A → B) ∧ (B → C)
¬A ∨ B ∨ C
```

### Leyes lógicas

```
¬(A ∨ B) ↔ (¬A ∧ ¬B)     # Ley de De Morgan
¬(A ∧ B) ↔ (¬A ∨ ¬B)     # Ley de De Morgan
A ∨ ¬A                     # Ley del tercero excluido
A ∧ ¬A                     # Contradicción
```

## Ejemplo de Salida

```
════════════════════════════════════════════════════════════
Expresión: (A ∧ B)
════════════════════════════════════════════════════════════

Tabla de Verdad:
────────────────────────────────────────────────────────────
A           │B           │Resultado
────────────────────────────────────────────────────────────
F           │F           │F
F           │V           │F
V           │F           │F
V           │V           │V
════════════════════════════════════════════════════════════
```

## Estructura del Proyecto

```
DigitalI_Project/
├── logic-expression-analyzer.js   # Analizador principal
├── index.html                      # Interfaz web interactiva
└── README.md                       # Documentación
```

## Algoritmos Utilizados

1. **Tokenización**: Convierte la expresión en tokens (variables, operadores, paréntesis)
2. **Shunting Yard Algorithm**: Convierte notación infija a postfija (RPN)
3. **Evaluación Postfija**: Evalúa la expresión usando una pila
4. **Generación de combinaciones**: Genera todas las combinaciones posibles de valores de verdad (2^n)

## Características Técnicas

- Manejo robusto de errores
- Validación de sintaxis
- Soporte para paréntesis anidados
- Precedencia de operadores correcta
- Símbolos Unicode y ASCII

## Precedencia de Operadores

1. `¬` (NOT) - Mayor precedencia
2. `∧` (AND)
3. `∨` (OR), `⊕` (XOR)
4. `→` (IMPLIES), `↔` (IFF) - Menor precedencia

## Limitaciones

- Las variables deben ser letras (A-Z, a-z)
- No soporta constantes verdaderas/falsas (0/1, true/false)
- Los operadores deben estar separados de los operandos

## Licencia

MIT

## Autor

Proyecto creado para análisis de expresiones lógicas y generación de tablas de verdad.
