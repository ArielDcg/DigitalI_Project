# Analizador de Expresiones Lógicas

Un analizador completo de expresiones lógicas que genera tablas de verdad utilizando símbolos lógicos estándar y verifica todas las leyes fundamentales del álgebra booleana.

## Características

- ✅ Soporta múltiples símbolos para cada operador lógico
- ✅ Genera tablas de verdad completas
- ✅ Manejo de paréntesis para precedencia
- ✅ Interfaz de línea de comandos
- ✅ **Interfaz web moderna e interactiva**
- ✅ **Incluye todas las leyes lógicas fundamentales**
- ✅ **Detecta tautologías y contradicciones automáticamente**
- ✅ **Estadísticas detalladas de cada análisis**
- ✅ **Diseño responsive y profesional**
- ✅ **CSS separado para fácil personalización**

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

## Leyes Lógicas Incluidas

La interfaz web incluye ejemplos interactivos de todas las leyes fundamentales:

### Leyes de De Morgan
- `¬(A ∨ B) ↔ (¬A ∧ ¬B)`
- `¬(A ∧ B) ↔ (¬A ∨ ¬B)`

### Leyes de Identidad
- `A ∧ A ↔ A`
- `A ∨ A ↔ A`

### Ley de Doble Negación
- `¬¬A ↔ A`

### Leyes Conmutativas
- `A ∧ B ↔ B ∧ A`
- `A ∨ B ↔ B ∨ A`

### Leyes Asociativas
- `(A ∧ B) ∧ C ↔ A ∧ (B ∧ C)`
- `(A ∨ B) ∨ C ↔ A ∨ (B ∨ C)`

### Leyes Distributivas
- `A ∧ (B ∨ C) ↔ (A ∧ B) ∨ (A ∧ C)`
- `A ∨ (B ∧ C) ↔ (A ∨ B) ∧ (A ∨ C)`

### Leyes de Absorción
- `A ∧ (A ∨ B) ↔ A`
- `A ∨ (A ∧ B) ↔ A`

### Leyes de Implicación
- `A → B ↔ ¬A ∨ B`
- `A → B ↔ ¬B → ¬A` (Contraposición)

### Leyes del Bicondicional
- `A ↔ B ↔ (A → B) ∧ (B → A)`
- `A ↔ B ↔ (A ∧ B) ∨ (¬A ∧ ¬B)`

### Leyes XOR
- `A ⊕ B ↔ (A ∨ B) ∧ ¬(A ∧ B)`
- `A ⊕ B ↔ (A ∧ ¬B) ∨ (¬A ∧ B)`

### Tautología y Contradicción
- `A ∨ ¬A` (Tercero Excluido - Tautología)
- `A ∧ ¬A` (Contradicción)

## Estructura del Proyecto

```
DigitalI_Project/
├── logic-expression-analyzer.js   # Analizador principal (motor del análisis)
├── index.html                      # Interfaz web interactiva con leyes lógicas
├── styles.css                      # Estilos CSS separados y modernos
└── README.md                       # Documentación completa
```

## Algoritmos Utilizados

1. **Tokenización**: Convierte la expresión en tokens (variables, operadores, paréntesis)
2. **Shunting Yard Algorithm**: Convierte notación infija a postfija (RPN)
3. **Evaluación Postfija**: Evalúa la expresión usando una pila
4. **Generación de combinaciones**: Genera todas las combinaciones posibles de valores de verdad (2^n)

## Interfaz Web Mejorada

La nueva interfaz incluye:

- **Layout de dos columnas**: Entrada a la izquierda, leyes lógicas a la derecha
- **Panel de operadores**: Botones para insertar símbolos lógicos fácilmente
- **Biblioteca de leyes**: Más de 20 leyes lógicas organizadas por categorías
- **Detección automática**: Identifica tautologías y contradicciones
- **Estadísticas en tiempo real**: Muestra porcentajes y análisis detallado
- **Diseño responsive**: Se adapta a dispositivos móviles y tablets
- **Animaciones suaves**: Transiciones y efectos visuales modernos
- **Scroll suave**: Navegación fluida entre secciones

## Características Técnicas

- Manejo robusto de errores
- Validación de sintaxis
- Soporte para paréntesis anidados
- Precedencia de operadores correcta
- Símbolos Unicode y ASCII
- CSS modular y separado
- JavaScript vanilla (sin dependencias)
- Código limpio y bien documentado

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
