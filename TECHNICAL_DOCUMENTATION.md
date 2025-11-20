# Documentación Técnica - Analizador de Expresiones Lógicas

## 📚 Índice

1. [Visión General](#visión-general)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Flujo de Ejecución](#flujo-de-ejecución)
4. [Algoritmos Implementados](#algoritmos-implementados)
5. [Estructuras de Datos](#estructuras-de-datos)
6. [Funciones Principales](#funciones-principales)
7. [Validación de FBF](#validación-de-fbf)
8. [Interfaz Web](#interfaz-web)

---

## Visión General

El **Analizador de Expresiones Lógicas** es un sistema que evalúa expresiones de lógica proposicional, genera tablas de verdad completas, y valida fórmulas bien formadas (FBF). El sistema utiliza algoritmos clásicos de compiladores como tokenización, Shunting Yard, y evaluación postfija.

### Componentes Principales

```
DigitalI_Project/
├── logic-expression-analyzer.js   # Motor de análisis (backend)
├── index.html                      # Interfaz web (frontend)
├── styles.css                      # Estilos visuales
└── TECHNICAL_DOCUMENTATION.md      # Este archivo
```

---

## Arquitectura del Sistema

### Clase Principal: `LogicExpressionAnalyzer`

Esta clase encapsula toda la lógica del analizador:

```javascript
class LogicExpressionAnalyzer {
    constructor() {
        this.operators = { ... };  // Definición de operadores
        this.constants = { ... };  // Definición de constantes (⊤, ⊥)
    }
}
```

#### Propiedades

1. **`operators`**: Objeto que define todos los operadores lógicos
   - Tipo: unario (¬) o binario (∧, ∨, →, ↔, ⊕)
   - Precedencia: 1 (menor) a 3 (mayor)
   - Función de evaluación
   - Símbolo Unicode estándar

2. **`constants`**: Objeto que define constantes lógicas
   - Top (⊤): Valor verdadero constante
   - Bottom (⊥): Valor falso constante

---

## Flujo de Ejecución

### Paso 1: Entrada del Usuario

```
Expresión: "(A ∧ B) → C"
         ↓
```

### Paso 2: Tokenización

Convierte la cadena de texto en tokens individuales:

```javascript
tokenize(expression) → [
    { type: '(', value: '(' },
    { type: 'variable', value: 'A' },
    { type: 'operator', value: '∧', opInfo: {...} },
    { type: 'variable', value: 'B' },
    { type: ')', value: ')' },
    { type: 'operator', value: '→', opInfo: {...} },
    { type: 'variable', value: 'C' }
]
```

**Algoritmo de Tokenización:**

1. Recorre la expresión carácter por carácter
2. Ignora espacios en blanco
3. Identifica:
   - **Paréntesis**: `(` y `)`
   - **Operadores**: Busca coincidencias en `this.operators`
   - **Constantes**: Busca en `this.constants` (⊤, ⊥)
   - **Variables**: Letras (A-Z, a-z)
4. Maneja operadores multi-carácter (AND, OR, IMPLIES, etc.)

### Paso 3: Validación FBF

Verifica que la expresión sea una Fórmula Bien Formada:

```javascript
validateWellFormedFormula(tokens) → {
    isWellFormed: boolean,
    issues: string[],
    warnings: string[]
}
```

**Reglas Verificadas:**

1. ✅ Paréntesis balanceados
2. ✅ No paréntesis innecesarios: `(A)`, `(¬p)` son inválidos
3. ✅ Operadores binarios con ambos operandos
4. ✅ Operadores unarios con operando siguiente
5. ✅ No dos variables/constantes consecutivas
6. ✅ No dos operadores binarios consecutivos
7. ✅ No paréntesis vacíos

### Paso 4: Extracción de Variables

```javascript
extractVariables(tokens) → ['A', 'B', 'C']
```

Obtiene todas las variables únicas de la expresión.

### Paso 5: Conversión a Notación Postfija (RPN)

Utiliza el **Algoritmo Shunting Yard** de Dijkstra:

```
Infija:   (A ∧ B) → C
Postfija: A B ∧ C →
```

**Algoritmo Shunting Yard:**

```javascript
infixToPostfix(tokens) {
    output = []
    operatorStack = []

    para cada token:
        si es variable/constante:
            output.push(token)

        si es '(':
            operatorStack.push(token)

        si es ')':
            mientras operatorStack.top ≠ '(':
                output.push(operatorStack.pop())
            operatorStack.pop()  // quitar '('

        si es operador:
            mientras haya operador en stack con mayor precedencia:
                output.push(operatorStack.pop())
            operatorStack.push(token)

    mientras operatorStack no esté vacía:
        output.push(operatorStack.pop())

    retornar output
}
```

**Tabla de Precedencia:**

| Operador | Precedencia | Tipo    |
|----------|-------------|---------|
| ¬        | 3           | Unario  |
| ∧        | 2           | Binario |
| ∨, ⊕     | 1           | Binario |
| →, ↔     | 1           | Binario |

### Paso 6: Generación de Combinaciones

Genera todas las combinaciones posibles de valores verdad (2^n):

```javascript
generateTruthCombinations(['A', 'B', 'C']) → [
    { A: false, B: false, C: false },
    { A: false, B: false, C: true  },
    { A: false, B: true,  C: false },
    { A: false, B: true,  C: true  },
    { A: true,  B: false, C: false },
    { A: true,  B: false, C: true  },
    { A: true,  B: true,  C: false },
    { A: true,  B: true,  C: true  }
]
```

**Algoritmo:**

1. Calcula 2^n donde n = número de variables
2. Para cada número i de 0 a 2^n - 1:
   - Convierte i a binario
   - Cada bit representa el valor de una variable
   - `0` = false, `1` = true

### Paso 7: Evaluación Postfija

Evalúa la expresión usando una **pila (stack)**:

```javascript
evaluatePostfix(postfix, values) {
    stack = []

    para cada token en postfix:
        si es variable:
            stack.push(values[token.value])

        si es constante:
            stack.push(token.constInfo.value)

        si es operador unario:
            operando = stack.pop()
            resultado = operador.eval(operando)
            stack.push(resultado)

        si es operador binario:
            derecha = stack.pop()
            izquierda = stack.pop()
            resultado = operador.eval(izquierda, derecha)
            stack.push(resultado)

    retornar stack.pop()  // resultado final
}
```

**Ejemplo: Evaluación de `A B ∧ C →` con A=true, B=true, C=false**

```
Token | Stack antes   | Operación            | Stack después
------|---------------|----------------------|---------------
A     | []            | push(true)           | [true]
B     | [true]        | push(true)           | [true, true]
∧     | [true, true]  | pop(), pop(), AND    | [true]
C     | [true]        | push(false)          | [true, false]
→     | [true, false] | pop(), pop(), IMPL   | [false]
```

### Paso 8: Evaluación Paso a Paso

Genera subexpresiones progresivas:

```javascript
evaluateStepByStep(postfix, combinations) {
    steps = []

    para i = 0 hasta postfix.length:
        si postfix[i] es operador:
            subPostfix = postfix[0...i+1]
            expresion = reconstruir(subPostfix)

            resultados = evaluar subPostfix para todas las combinaciones

            steps.push({
                stepNumber: steps.length + 1,
                expression: expresion,
                operator: operador,
                operands: [operandos],
                results: resultados
            })

    retornar steps
}
```

**Ejemplo para `(A ∧ B) → C`:**

```
Paso 1: A ∧ B
Paso 2: (A ∧ B) → C
```

### Paso 9: Clasificación

Clasifica la expresión según los resultados:

```javascript
classifyExpression(results) {
    allTrue = todos los resultados son true
    allFalse = todos los resultados son false

    si allTrue:
        retornar "TAUTOLOGÍA"
    si allFalse:
        retornar "CONTRADICCIÓN"
    sino:
        retornar "CONTINGENCIA"
}
```

---

## Algoritmos Implementados

### 1. Tokenización (Lexer)

**Complejidad**: O(n) donde n = longitud de la expresión

**Propósito**: Analizar léxico de la entrada

```javascript
tokenize(expression) {
    tokens = []
    i = 0

    mientras i < expression.length:
        char = expression[i]

        // Ignorar espacios
        si char es espacio:
            i++
            continuar

        // Paréntesis
        si char es '(' o ')':
            tokens.push({ type: char, value: char })
            i++
            continuar

        // Operadores multi-carácter
        para cada longitud en [3, 2, 1]:
            substr = expression.substring(i, i + longitud)
            si substr existe en operators:
                tokens.push({
                    type: 'operator',
                    value: substr,
                    opInfo: operators[substr]
                })
                i += longitud
                encontrado = true
                break

        si encontrado: continuar

        // Constantes
        si char existe en constants:
            tokens.push({
                type: 'constant',
                value: char,
                constInfo: constants[char]
            })
            i++
            continuar

        // Variables (letras)
        si char es letra:
            varName = ''
            mientras char es alfanumérico:
                varName += char
                i++
                char = expression[i]

            // Verificar si es palabra clave (AND, OR, NOT, etc.)
            si varName.toUpperCase() en operators:
                tokens.push({
                    type: 'operator',
                    value: varName.toUpperCase(),
                    opInfo: operators[varName.toUpperCase()]
                })
            sino si varName.toUpperCase() en constants:
                tokens.push({
                    type: 'constant',
                    value: varName.toUpperCase(),
                    constInfo: constants[varName.toUpperCase()]
                })
            sino:
                tokens.push({
                    type: 'variable',
                    value: varName
                })
            continuar

        // Carácter no reconocido
        lanzar Error("Carácter no reconocido: " + char)

    retornar tokens
}
```

### 2. Shunting Yard Algorithm

**Complejidad**: O(n) donde n = número de tokens

**Inventor**: Edsger Dijkstra (1961)

**Propósito**: Convertir notación infija a postfija (RPN)

**Por qué RPN?**
- Más fácil de evaluar (sin paréntesis)
- No requiere considerar precedencia durante evaluación
- Uso eficiente de pila

**Pseudocódigo detallado:**

```
ALGORITMO: Shunting Yard

ENTRADA: tokens[] (expresión en notación infija)
SALIDA: output[] (expresión en notación postfija)

output ← cola vacía
operatorStack ← pila vacía

PARA CADA token EN tokens:
    CASO token.type:
        'variable' O 'constant':
            output.encolar(token)

        '(':
            operatorStack.apilar(token)

        ')':
            MIENTRAS operatorStack.cima() ≠ '(':
                output.encolar(operatorStack.desapilar())
            operatorStack.desapilar()  // quitar '('

        'operator':
            // Manejar precedencia
            MIENTRAS operatorStack NO VACÍA Y
                     operatorStack.cima().type = 'operator' Y
                     operatorStack.cima().precedencia ≥ token.precedencia Y
                     token.type ≠ 'unary':
                output.encolar(operatorStack.desapilar())

            operatorStack.apilar(token)

// Vaciar stack
MIENTRAS operatorStack NO VACÍA:
    output.encolar(operatorStack.desapilar())

RETORNAR output
```

**Ejemplo paso a paso: `(A ∧ B) → C`**

| Token | Output        | Operator Stack | Acción                           |
|-------|---------------|----------------|----------------------------------|
| (     | []            | [(]            | Apilar paréntesis                |
| A     | [A]           | [(]            | Variable → output                |
| ∧     | [A]           | [(, ∧]         | Apilar operador                  |
| B     | [A, B]        | [(, ∧]         | Variable → output                |
| )     | [A, B, ∧]     | []             | Desapilar hasta '(', ∧ → output  |
| →     | [A, B, ∧]     | [→]            | Apilar operador                  |
| C     | [A, B, ∧, C]  | [→]            | Variable → output                |
| FIN   | [A, B, ∧, C, →] | []          | Vaciar stack, → → output         |

### 3. Evaluación de Expresiones Postfijas

**Complejidad**: O(n) donde n = número de tokens

**Propósito**: Calcular el valor de verdad de la expresión

```
ALGORITMO: Evaluación Postfija

ENTRADA: postfix[] (expresión en RPN), values{} (valores de variables)
SALIDA: boolean (resultado de la evaluación)

stack ← pila vacía

PARA CADA token EN postfix:
    CASO token.type:
        'variable':
            SI values[token.value] NO EXISTE:
                ERROR "Variable no definida"
            stack.apilar(values[token.value])

        'constant':
            stack.apilar(token.constInfo.value)

        'operator':
            SI token.opInfo.type = 'unary':
                SI stack.tamaño < 1:
                    ERROR "Operador unario sin operando"
                a ← stack.desapilar()
                resultado ← token.opInfo.eval(a)
                stack.apilar(resultado)

            SI token.opInfo.type = 'binary':
                SI stack.tamaño < 2:
                    ERROR "Operador binario sin operandos"
                b ← stack.desapilar()  // derecha
                a ← stack.desapilar()  // izquierda
                resultado ← token.opInfo.eval(a, b)
                stack.apilar(resultado)

SI stack.tamaño ≠ 1:
    ERROR "Expresión mal formada"

RETORNAR stack.desapilar()
```

### 4. Generación de Combinaciones de Valores

**Complejidad**: O(2^n) donde n = número de variables

**Propósito**: Generar todas las filas de la tabla de verdad

```
ALGORITMO: Generación de Combinaciones

ENTRADA: variables[] (lista de nombres de variables)
SALIDA: combinations[] (array de objetos con todas las combinaciones)

n ← variables.length
totalCombinations ← 2^n
combinations ← []

PARA i ← 0 HASTA totalCombinations - 1:
    combination ← {}

    PARA j ← 0 HASTA n - 1:
        variable ← variables[j]
        // Bit j del número i determina el valor de la variable j
        valor ← (i >> j) & 1  // Extrae bit j
        combination[variable] ← (valor = 1) ? true : false

    combinations.agregar(combination)

RETORNAR combinations
```

**Ejemplo: variables = ['A', 'B']**

```
i   | Binario | A (bit 0) | B (bit 1) | Combination
----|---------|-----------|-----------|------------------
0   | 00      | 0 (false) | 0 (false) | {A:F, B:F}
1   | 01      | 1 (true)  | 0 (false) | {A:T, B:F}
2   | 10      | 0 (false) | 1 (true)  | {A:F, B:T}
3   | 11      | 1 (true)  | 1 (true)  | {A:T, B:T}
```

---

## Estructuras de Datos

### 1. Token

Representa un elemento de la expresión:

```javascript
{
    type: 'variable' | 'constant' | 'operator' | '(' | ')',
    value: string,
    opInfo?: {           // Solo para operators
        precedence: number,
        type: 'unary' | 'binary',
        eval: Function,
        symbol: string
    },
    constInfo?: {        // Solo para constants
        value: boolean,
        symbol: string,
        name: string
    }
}
```

### 2. Resultado de Tabla de Verdad

```javascript
{
    success: boolean,
    expression: string,
    variables: string[],
    table: [
        {
            A: boolean,
            B: boolean,
            ...
            result: boolean
        }
    ],
    tokens: Token[],
    postfix: Token[],
    steps: [
        {
            stepNumber: number,
            expression: string,
            operator: string,
            operands: string[],
            results: [
                {
                    A: boolean,
                    B: boolean,
                    ...
                    result: boolean
                }
            ]
        }
    ],
    classification: {
        type: 'TAUTOLOGÍA' | 'CONTRADICCIÓN' | 'CONTINGENCIA',
        description: string
    },
    fbfValidation: {
        isWellFormed: boolean,
        issues: string[],
        warnings: string[],
        message: string
    },
    autoComplete: {
        original: string,
        corrected: string | null,
        suggestions: string[]
    }
}
```

---

## Validación de FBF

### Reglas de Fórmulas Bien Formadas

Una **Fórmula Bien Formada (FBF)** en lógica proposicional debe cumplir:

1. **Átomos**: Una variable sola (p, q, A, B) es una FBF
2. **Constantes**: ⊤ y ⊥ son FBF
3. **Negación**: Si φ es FBF, entonces ¬φ es FBF
4. **Conectivos Binarios**: Si φ y ψ son FBF, entonces:
   - (φ ∧ ψ) es FBF
   - (φ ∨ ψ) es FBF
   - (φ → ψ) es FBF
   - (φ ↔ ψ) es FBF
   - (φ ⊕ ψ) es FBF

### Paréntesis Innecesarios

El validador detecta y rechaza:

❌ `(A)` - Variable entre paréntesis
❌ `(⊤)` - Constante entre paréntesis
❌ `(¬A)` - Negación simple entre paréntesis
❌ `()` - Paréntesis vacío

✅ `A` - Variable sola
✅ `¬A` - Negación sin paréntesis
✅ `(A ∧ B)` - Operador binario CON paréntesis
✅ `¬(A ∧ B)` - Negación de expresión compuesta

### Implementación de la Validación

```javascript
validateWellFormedFormula(tokens) {
    issues = []
    parenthesesCount = 0
    lastToken = null

    PARA CADA token EN tokens:
        // Verificar paréntesis balanceados
        SI token.type = '(':
            parenthesesCount++

            // Detectar paréntesis innecesarios
            SI siguiente token es variable Y token i+2 es ')':
                issues.agregar("Paréntesis innecesarios: (variable)")

            SI siguiente token es constante Y token i+2 es ')':
                issues.agregar("Paréntesis innecesarios: (constante)")

            SI siguiente token es ¬ Y token i+2 es variable/constante Y token i+3 es ')':
                issues.agregar("Paréntesis innecesarios: (¬átomo)")

        SI token.type = ')':
            parenthesesCount--
            SI parenthesesCount < 0:
                issues.agregar("Paréntesis de cierre sin apertura")

        // Verificar operadores binarios
        SI token.type = 'operator' Y token.opInfo.type = 'binary':
            SI es primer token:
                issues.agregar("Operador binario al inicio")
            SI es último token:
                issues.agregar("Operador binario al final")

        // Verificar operadores unarios
        SI token.type = 'operator' Y token.opInfo.type = 'unary':
            SI es último token:
                issues.agregar("Operador unario sin operando")
            SI siguiente token NO es variable/constante/paréntesis:
                issues.agregar("Operador unario debe ser seguido por átomo o expresión")

        // Verificar símbolos consecutivos
        SI lastToken es variable/constante Y token es variable/constante:
            issues.agregar("Símbolos consecutivos sin operador")

        SI lastToken es operador binario Y token es operador binario:
            issues.agregar("Operadores binarios consecutivos")

        // Verificar paréntesis vacío
        SI lastToken es '(' Y token es ')':
            issues.agregar("Paréntesis vacío")

        lastToken = token

    SI parenthesesCount > 0:
        issues.agregar(parenthesesCount + " paréntesis sin cerrar")

    RETORNAR {
        isWellFormed: issues.length = 0,
        issues: issues,
        message: mensaje de validación
    }
}
```

---

## Interfaz Web

### Componentes HTML

1. **Encabezado**: Título y descripción
2. **Área de Entrada**: Input para expresión + botones de operadores
3. **Área de Resultado**: Muestra análisis completo
4. **Biblioteca de Leyes**: Ejemplos de leyes lógicas

### Funcionalidad de Pestañas Colapsables

**Objetivo**: Permitir ocultar/mostrar pasos individuales

#### HTML Generado Dinámicamente

```html
<div class="step-card" data-step="0">
    <div class="step-header" onclick="toggleStep(0)">
        <div class="step-header-left">
            <span class="step-toggle">▼</span>
            <span class="step-number">Paso 1</span>
            <span class="step-expression">A ∧ B</span>
        </div>
    </div>
    <div class="step-body step-expanded">
        <!-- Contenido del paso -->
    </div>
</div>
```

#### JavaScript - Toggle Individual

```javascript
function toggleStep(stepIndex) {
    // Encontrar la tarjeta del paso
    stepCard = document.querySelector(`.step-card[data-step="${stepIndex}"]`)
    stepBody = stepCard.querySelector('.step-body')
    stepToggle = stepCard.querySelector('.step-toggle')

    // Alternar estado
    SI stepBody tiene clase 'step-expanded':
        stepBody.removeClass('step-expanded')
        stepBody.addClass('step-collapsed')
        stepToggle.text = '▶'
    SINO:
        stepBody.removeClass('step-collapsed')
        stepBody.addClass('step-expanded')
        stepToggle.text = '▼'
}
```

#### JavaScript - Toggle Todos

```javascript
allStepsExpanded = true  // Variable global

function toggleAllSteps() {
    allStepBodies = document.querySelectorAll('.step-body')
    allToggles = document.querySelectorAll('.step-toggle')
    toggleBtn = document.querySelector('.toggle-all-btn')

    SI allStepsExpanded:
        // Colapsar todos
        PARA CADA body EN allStepBodies:
            body.removeClass('step-expanded')
            body.addClass('step-collapsed')

        PARA CADA toggle EN allToggles:
            toggle.text = '▶'

        toggleBtn.text = '⬆️ Expandir Todos'
        allStepsExpanded = false
    SINO:
        // Expandir todos
        PARA CADA body EN allStepBodies:
            body.removeClass('step-collapsed')
            body.addClass('step-expanded')

        PARA CADA toggle EN allToggles:
            toggle.text = '▼'

        toggleBtn.text = '⬇️ Contraer Todos'
        allStepsExpanded = true
}
```

#### CSS - Animaciones

```css
.step-body {
    overflow: hidden;
    transition: max-height 0.4s ease,
                padding 0.4s ease,
                opacity 0.4s ease;
}

.step-expanded {
    max-height: 2000px;
    opacity: 1;
    padding: 20px;
}

.step-collapsed {
    max-height: 0;
    opacity: 0;
    padding: 0 20px;
}

.step-header {
    cursor: pointer;
    user-select: none;
    transition: background 0.3s ease;
}

.step-header:hover {
    background: linear-gradient(135deg, #7688f0 0%, #8559b0 100%);
}
```

### Flujo de Interacción Usuario

```
1. Usuario ingresa expresión: "(A ∧ B) → C"
         ↓
2. Click en botón "Analizar"
         ↓
3. analyzeExpression() se ejecuta
         ↓
4. Llama al analizador: analyzer.generateTruthTable(expression)
         ↓
5. Recibe resultado con:
   - Validación FBF
   - Pasos intermedios
   - Tabla final
   - Clasificación
         ↓
6. Genera HTML dinámicamente
         ↓
7. Renderiza en resultDiv
         ↓
8. Usuario puede:
   - Colapsar/expandir pasos
   - Probar leyes predefinidas
   - Ver estadísticas
```

---

## Operadores Lógicos - Definición Formal

### Operador NOT (Negación) - ¬

**Símbolo**: ¬, !, NOT

**Tipo**: Unario

**Precedencia**: 3 (máxima)

**Tabla de Verdad**:

| p | ¬p |
|---|----|
| F | V  |
| V | F  |

**Función**:
```javascript
eval: (a) => !a
```

### Operador AND (Conjunción) - ∧

**Símbolo**: ∧, &&, AND

**Tipo**: Binario

**Precedencia**: 2

**Tabla de Verdad**:

| p | q | p ∧ q |
|---|---|-------|
| F | F | F     |
| F | V | F     |
| V | F | F     |
| V | V | V     |

**Función**:
```javascript
eval: (a, b) => a && b
```

### Operador OR (Disyunción) - ∨

**Símbolo**: ∨, ||, OR

**Tipo**: Binario

**Precedencia**: 1

**Tabla de Verdad**:

| p | q | p ∨ q |
|---|---|-------|
| F | F | F     |
| F | V | V     |
| V | F | V     |
| V | V | V     |

**Función**:
```javascript
eval: (a, b) => a || b
```

### Operador XOR (Disyunción Exclusiva) - ⊕

**Símbolo**: ⊕, XOR

**Tipo**: Binario

**Precedencia**: 1

**Tabla de Verdad**:

| p | q | p ⊕ q |
|---|---|-------|
| F | F | F     |
| F | V | V     |
| V | F | V     |
| V | V | F     |

**Función**:
```javascript
eval: (a, b) => a !== b
```

### Operador IMPLIES (Implicación) - →

**Símbolo**: →, =>, IMPLIES

**Tipo**: Binario

**Precedencia**: 1

**Tabla de Verdad**:

| p | q | p → q |
|---|---|-------|
| F | F | V     |
| F | V | V     |
| V | F | F     |
| V | V | V     |

**Equivalencia**: p → q ≡ ¬p ∨ q

**Función**:
```javascript
eval: (a, b) => !a || b
```

### Operador IFF (Bicondicional) - ↔

**Símbolo**: ↔, <=>, IFF

**Tipo**: Binario

**Precedencia**: 1

**Tabla de Verdad**:

| p | q | p ↔ q |
|---|---|-------|
| F | F | V     |
| F | V | F     |
| V | F | F     |
| V | V | V     |

**Equivalencia**: p ↔ q ≡ (p → q) ∧ (q → p)

**Función**:
```javascript
eval: (a, b) => a === b
```

### Constante TOP - ⊤

**Símbolo**: ⊤, TOP, T

**Tipo**: Constante

**Valor**: Siempre `true`

**Propiedades**:
- A ∧ ⊤ ≡ A (Identidad para AND)
- A ∨ ⊤ ≡ ⊤ (Dominancia para OR)

### Constante BOTTOM - ⊥

**Símbolo**: ⊥, BOTTOM, BOT

**Tipo**: Constante

**Valor**: Siempre `false`

**Propiedades**:
- A ∨ ⊥ ≡ A (Identidad para OR)
- A ∧ ⊥ ≡ ⊥ (Dominancia para AND)

---

## Complejidad Computacional

### Análisis de Complejidad

| Operación                  | Complejidad    | Explicación                        |
|----------------------------|----------------|------------------------------------|
| Tokenización               | O(n)           | n = longitud expresión             |
| Validación FBF             | O(t)           | t = número de tokens               |
| Extracción de variables    | O(t)           | Recorre tokens una vez             |
| Shunting Yard              | O(t)           | Cada token procesado una vez       |
| Generación combinaciones   | O(2^v)         | v = número de variables            |
| Evaluación postfija        | O(t)           | Por cada combinación               |
| **Total tabla de verdad**  | **O(t × 2^v)** | t tokens × 2^v combinaciones       |
| Evaluación paso a paso     | O(t² × 2^v)    | t pasos × t tokens × 2^v combos    |

### Limitaciones Prácticas

- **Variables**: Máximo recomendado ~ 10 variables
  - 10 variables = 1,024 filas
  - 15 variables = 32,768 filas
  - 20 variables = 1,048,576 filas (¡poco práctico!)

- **Expresiones**: Sin límite teórico, pero la UI puede volverse lenta con expresiones muy largas

---

## Casos de Uso y Ejemplos

### Caso 1: Verificar Ley de De Morgan

**Expresión**: `¬(A ∨ B) ↔ (¬A ∧ ¬B)`

**Proceso**:
1. Tokenización → 13 tokens
2. Validación FBF → ✓ Válida
3. Variables → ['A', 'B']
4. Combinaciones → 4 filas (2² = 4)
5. Evaluación → Todos resultados = true
6. **Clasificación → TAUTOLOGÍA** ✅

### Caso 2: Expresión Inválida

**Expresión**: `(¬A)`

**Proceso**:
1. Tokenización → 4 tokens: [(, ¬, A, )]
2. Validación FBF → ✗ **Error detectado**
   - Issue: "Paréntesis innecesarios: (¬A). La negación no requiere paréntesis"
3. **NO se procesa más**

### Caso 3: Contradicción

**Expresión**: `A ∧ ¬A`

**Proceso**:
1. Tokenización → 3 tokens
2. Validación FBF → ✓ Válida
3. Variables → ['A']
4. Combinaciones → 2 filas
5. Evaluación → Todos resultados = false
6. **Clasificación → CONTRADICCIÓN** ❌

---

## Diagrama de Flujo General

```
┌─────────────────┐
│ Entrada Usuario │
│  "(A ∧ B) → C"  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Tokenización   │
│   ┌───┬───┬───┐ │
│   │(│A│∧│B│)│...│
│   └───┴───┴───┘ │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Validación FBF  │
│   ¿Válida?      │
└────┬────────────┘
     │
     ├─NO─→ [Mostrar Errores] → FIN
     │
     YES
     ▼
┌─────────────────┐
│ Extracción Vars │
│   [A, B, C]     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Shunting Yard   │
│ Infix → Postfix │
│  A B ∧ C →      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Combinaciones   │
│    2^3 = 8      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Evaluación     │
│  Para cada      │
│  combinación    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Pasos           │
│ Intermedios     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Clasificación   │
│ Tautología?     │
│ Contradicción?  │
│ Contingencia?   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Renderizar UI   │
│ - FBF Badge     │
│ - Pasos         │
│ - Tabla Final   │
│ - Estadísticas  │
└─────────────────┘
```

---

## Conclusión

Este analizador implementa algoritmos fundamentales de:
- **Compiladores**: Tokenización, parsing
- **Estructuras de Datos**: Pilas, colas
- **Algoritmos Clásicos**: Shunting Yard
- **Lógica Matemática**: Tablas de verdad, FBF

Es una herramienta educativa completa para aprender lógica proposicional y algoritmos de compiladores.

---

**Autor**: Proyecto DigitalI
**Fecha**: 2025
**Licencia**: MIT
