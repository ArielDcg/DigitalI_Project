/**
 * Analizador de Expresiones Lógicas
 * Genera tablas de verdad para expresiones lógicas con operadores estándar
 *
 * Operadores soportados:
 * - ∧, &&, AND: Conjunción (AND)
 * - ∨, ||, OR: Disyunción (OR)
 * - ¬, !, NOT: Negación (NOT)
 * - →, =>, IMPLIES: Implicación
 * - ↔, <=>, IFF: Bicondicional (si y solo si)
 * - ⊕, XOR: Disyunción exclusiva
 *
 * Ejemplos de uso:
 * - "A ∧ B"
 * - "¬A ∨ B"
 * - "A → B"
 * - "(A ∨ B) ∧ ¬C"
 */

class LogicExpressionAnalyzer {
    constructor() {
        // Definir operadores y sus símbolos
        this.operators = {
            // NOT (negación)
            '¬': { precedence: 4, type: 'unary', eval: (a) => !a, symbol: '¬' },
            '!': { precedence: 4, type: 'unary', eval: (a) => !a, symbol: '¬' },
            'NOT': { precedence: 4, type: 'unary', eval: (a) => !a, symbol: '¬' },

            // AND (conjunción)
            '∧': { precedence: 3, type: 'binary', eval: (a, b) => a && b, symbol: '∧' },
            '&&': { precedence: 3, type: 'binary', eval: (a, b) => a && b, symbol: '∧' },
            'AND': { precedence: 3, type: 'binary', eval: (a, b) => a && b, symbol: '∧' },

            // OR (disyunción)
            '∨': { precedence: 2, type: 'binary', eval: (a, b) => a || b, symbol: '∨' },
            '||': { precedence: 2, type: 'binary', eval: (a, b) => a || b, symbol: '∨' },
            'OR': { precedence: 2, type: 'binary', eval: (a, b) => a || b, symbol: '∨' },

            // XOR (disyunción exclusiva)
            '⊕': { precedence: 2, type: 'binary', eval: (a, b) => a !== b, symbol: '⊕' },
            'XOR': { precedence: 2, type: 'binary', eval: (a, b) => a !== b, symbol: '⊕' },

            // IMPLIES (implicación)
            '→': { precedence: 1, type: 'binary', eval: (a, b) => !a || b, symbol: '→' },
            '=>': { precedence: 1, type: 'binary', eval: (a, b) => !a || b, symbol: '→' },
            'IMPLIES': { precedence: 1, type: 'binary', eval: (a, b) => !a || b, symbol: '→' },

            // IFF (bicondicional)
            '↔': { precedence: 1, type: 'binary', eval: (a, b) => a === b, symbol: '↔' },
            '<=>': { precedence: 1, type: 'binary', eval: (a, b) => a === b, symbol: '↔' },
            'IFF': { precedence: 1, type: 'binary', eval: (a, b) => a === b, symbol: '↔' },
        };

        // Constantes lógicas
        this.constants = {
            '⊤': { value: true, symbol: '⊤', name: 'Top (Verdad)' },
            'TOP': { value: true, symbol: '⊤', name: 'Top (Verdad)' },
            'T': { value: true, symbol: '⊤', name: 'Top (Verdad)' },
            '⊥': { value: false, symbol: '⊥', name: 'Bottom (Falsedad)' },
            'BOTTOM': { value: false, symbol: '⊥', name: 'Bottom (Falsedad)' },
            'BOT': { value: false, symbol: '⊥', name: 'Bottom (Falsedad)' },
        };
    }

    /**
     * Tokeniza la expresión en tokens individuales
     */
    tokenize(expression) {
        const tokens = [];
        let i = 0;
        expression = expression.trim();

        while (i < expression.length) {
            const char = expression[i];

            // Ignorar espacios
            if (/\s/.test(char)) {
                i++;
                continue;
            }

            // Paréntesis
            if (char === '(' || char === ')') {
                tokens.push({ type: char, value: char });
                i++;
                continue;
            }

            // Operadores de múltiples caracteres
            let found = false;
            for (let len = 3; len >= 1; len--) {
                const substr = expression.substr(i, len);
                if (this.operators[substr]) {
                    tokens.push({
                        type: 'operator',
                        value: substr,
                        opInfo: this.operators[substr]
                    });
                    i += len;
                    found = true;
                    break;
                }
            }
            if (found) continue;

            // Constantes lógicas (⊤, ⊥)
            if (this.constants[char]) {
                tokens.push({
                    type: 'constant',
                    value: char,
                    constInfo: this.constants[char]
                });
                i++;
                continue;
            }

            // Variables (letras)
            if (/[A-Za-z]/.test(char)) {
                let varName = '';
                while (i < expression.length && /[A-Za-z0-9]/.test(expression[i])) {
                    varName += expression[i];
                    i++;
                }

                // Verificar si es un operador (AND, OR, NOT, etc.)
                if (this.operators[varName.toUpperCase()]) {
                    tokens.push({
                        type: 'operator',
                        value: varName.toUpperCase(),
                        opInfo: this.operators[varName.toUpperCase()]
                    });
                } else if (this.constants[varName.toUpperCase()]) {
                    // Verificar si es una constante (TOP, BOTTOM, T, BOT)
                    tokens.push({
                        type: 'constant',
                        value: varName.toUpperCase(),
                        constInfo: this.constants[varName.toUpperCase()]
                    });
                } else {
                    tokens.push({ type: 'variable', value: varName });
                }
                continue;
            }

            throw new Error(`Carácter no reconocido: '${char}' en posición ${i}`);
        }

        return tokens;
    }

    /**
     * Convierte la expresión infija a notación postfija (Shunting Yard Algorithm)
     */
    infixToPostfix(tokens) {
        const output = [];
        const operatorStack = [];

        for (const token of tokens) {
            if (token.type === 'variable' || token.type === 'constant') {
                output.push(token);
            } else if (token.type === 'operator') {
                while (
                    operatorStack.length > 0 &&
                    operatorStack[operatorStack.length - 1].type === 'operator' &&
                    operatorStack[operatorStack.length - 1].opInfo.precedence >= token.opInfo.precedence &&
                    token.opInfo.type !== 'unary'
                ) {
                    output.push(operatorStack.pop());
                }
                operatorStack.push(token);
            } else if (token.type === '(') {
                operatorStack.push(token);
            } else if (token.type === ')') {
                while (
                    operatorStack.length > 0 &&
                    operatorStack[operatorStack.length - 1].type !== '('
                ) {
                    output.push(operatorStack.pop());
                }
                if (operatorStack.length === 0) {
                    throw new Error('Paréntesis no balanceados');
                }
                operatorStack.pop(); // Remover '('
            }
        }

        while (operatorStack.length > 0) {
            const op = operatorStack.pop();
            if (op.type === '(') {
                throw new Error('Paréntesis no balanceados');
            }
            output.push(op);
        }

        return output;
    }

    /**
     * Evalúa una expresión en notación postfija con valores específicos
     */
    evaluatePostfix(postfix, values) {
        const stack = [];

        for (const token of postfix) {
            if (token.type === 'variable') {
                if (!(token.value in values)) {
                    throw new Error(`Variable '${token.value}' no definida`);
                }
                stack.push(values[token.value]);
            } else if (token.type === 'constant') {
                // Las constantes siempre tienen el mismo valor
                stack.push(token.constInfo.value);
            } else if (token.type === 'operator') {
                if (token.opInfo.type === 'unary') {
                    if (stack.length < 1) {
                        throw new Error('Expresión inválida: operador unario sin operando');
                    }
                    const a = stack.pop();
                    stack.push(token.opInfo.eval(a));
                } else { // binary
                    if (stack.length < 2) {
                        throw new Error('Expresión inválida: operador binario con menos de 2 operandos');
                    }
                    const b = stack.pop();
                    const a = stack.pop();
                    stack.push(token.opInfo.eval(a, b));
                }
            }
        }

        if (stack.length !== 1) {
            throw new Error('Expresión inválida');
        }

        return stack[0];
    }

    /**
     * Extrae todas las variables únicas de la expresión
     */
    extractVariables(tokens) {
        const variables = new Set();
        for (const token of tokens) {
            if (token.type === 'variable') {
                variables.add(token.value);
            }
        }
        return Array.from(variables).sort();
    }

    /**
     * Genera todas las combinaciones posibles de valores de verdad
     */
    generateTruthCombinations(variables) {
        const n = variables.length;
        const combinations = [];

        for (let i = 0; i < Math.pow(2, n); i++) {
            const combination = {};
            for (let j = 0; j < n; j++) {
                combination[variables[j]] = Boolean((i >> (n - 1 - j)) & 1);
            }
            combinations.push(combination);
        }

        return combinations;
    }

    /**
     * Convierte la expresión postfija a formato legible con símbolos estándar
     */
    postfixToString(postfix) {
        const stack = [];

        for (const token of postfix) {
            if (token.type === 'variable') {
                stack.push(token.value);
            } else if (token.type === 'constant') {
                stack.push(token.constInfo.symbol);
            } else if (token.type === 'operator') {
                if (token.opInfo.type === 'unary') {
                    const a = stack.pop();
                    stack.push(`${token.opInfo.symbol}${a}`);
                } else {
                    const b = stack.pop();
                    const a = stack.pop();
                    stack.push(`(${a} ${token.opInfo.symbol} ${b})`);
                }
            }
        }

        return stack[0] || '';
    }

    /**
     * Evalúa paso a paso mostrando cada subexpresión
     */
    evaluateStepByStep(postfix, combinations) {
        const steps = [];
        const subexpressionStack = [];

        // Evaluar cada token en la expresión postfija
        for (let stepIndex = 0; stepIndex < postfix.length; stepIndex++) {
            const token = postfix[stepIndex];

            if (token.type === 'variable') {
                subexpressionStack.push(token.value);
            } else if (token.type === 'constant') {
                subexpressionStack.push(token.constInfo.symbol);
            } else if (token.type === 'operator') {
                let expr, operands;

                if (token.opInfo.type === 'unary') {
                    const a = subexpressionStack.pop();
                    expr = `${token.opInfo.symbol}${a}`;
                    operands = [a];
                    subexpressionStack.push(expr);
                } else { // binary
                    const b = subexpressionStack.pop();
                    const a = subexpressionStack.pop();
                    expr = `(${a} ${token.opInfo.symbol} ${b})`;
                    operands = [a, b];
                    subexpressionStack.push(expr);
                }

                // Crear paso con evaluación
                const stepData = {
                    stepNumber: steps.length + 1,
                    expression: expr,
                    operator: token.opInfo.symbol,
                    operands: operands,
                    results: []
                };

                // Evaluar esta subexpresión para cada combinación
                const subPostfix = postfix.slice(0, stepIndex + 1);
                for (const combination of combinations) {
                    try {
                        const result = this.evaluatePostfix(subPostfix, combination);
                        stepData.results.push({
                            ...combination,
                            result
                        });
                    } catch (error) {
                        // Si hay error, simplemente saltamos este paso
                        continue;
                    }
                }

                steps.push(stepData);
            }
        }

        return steps;
    }

    /**
     * Clasifica la expresión como tautología, contingencia o contradicción
     */
    classifyExpression(results) {
        const allTrue = results.every(row => row.result === true);
        const allFalse = results.every(row => row.result === false);

        if (allTrue) {
            return {
                type: 'TAUTOLOGÍA',
                description: 'La expresión es siempre verdadera para cualquier combinación de valores'
            };
        } else if (allFalse) {
            return {
                type: 'CONTRADICCIÓN',
                description: 'La expresión es siempre falsa para cualquier combinación de valores'
            };
        } else {
            return {
                type: 'CONTINGENCIA',
                description: 'La expresión es verdadera en algunos casos y falsa en otros'
            };
        }
    }

    /**
     * Valida si la expresión es una Fórmula Bien Formada (FBF)
     *
     * IMPORTANTE: Separa ERRORES (que invalidan la FBF) de ADVERTENCIAS (sintaxis redundante pero válida)
     *
     * Reglas de FBF:
     * 1. Una variable sola es una FBF
     * 2. Una constante sola (⊤, ⊥) es una FBF
     * 3. Si φ es una FBF, entonces ¬φ es una FBF
     * 4. Si φ y ψ son FBF, entonces (φ ∧ ψ), (φ ∨ ψ), (φ → ψ), (φ ↔ ψ), (φ ⊕ ψ) son FBF
     *
     * Paréntesis redundantes: Son FBF VÁLIDAS pero con sintaxis innecesaria
     * Ejemplos: (A), (⊤), (¬p) son válidas pero redundantes
     */
    validateWellFormedFormula(tokens) {
        const issues = [];      // Errores críticos que invalidan la FBF
        const warnings = [];    // Advertencias: sintaxis redundante pero válida
        let parenthesesCount = 0;
        let lastToken = null;

        for (let i = 0; i < tokens.length; i++) {
            const token = tokens[i];

            // Verificar paréntesis balanceados
            if (token.type === '(') {
                parenthesesCount++;

                // Detectar paréntesis redundantes (NO son errores, solo advertencias)
                if (i + 1 < tokens.length) {
                    const nextToken = tokens[i + 1];

                    // Caso 1: (variable) - redundante pero válido
                    if (nextToken.type === 'variable' && i + 2 < tokens.length && tokens[i + 2].type === ')') {
                        warnings.push(`Paréntesis redundantes alrededor de '${nextToken.value}' (sintaxis válida pero innecesaria)`);
                    }

                    // Caso 2: (constante) - redundante pero válido
                    if (nextToken.type === 'constant' && i + 2 < tokens.length && tokens[i + 2].type === ')') {
                        warnings.push(`Paréntesis redundantes alrededor de '${nextToken.constInfo.symbol}' (sintaxis válida pero innecesaria)`);
                    }

                    // Caso 3: (¬átomo) - redundante pero válido
                    if (nextToken.type === 'operator' && nextToken.opInfo.type === 'unary' &&
                        i + 2 < tokens.length && (tokens[i + 2].type === 'variable' || tokens[i + 2].type === 'constant') &&
                        i + 3 < tokens.length && tokens[i + 3].type === ')') {
                        const operandSymbol = tokens[i + 2].type === 'variable' ? tokens[i + 2].value : tokens[i + 2].constInfo.symbol;
                        warnings.push(`Paréntesis redundantes en '(${nextToken.opInfo.symbol}${operandSymbol})' (sintaxis válida pero innecesaria)`);
                    }
                }
            } else if (token.type === ')') {
                parenthesesCount--;
                if (parenthesesCount < 0) {
                    issues.push('Paréntesis de cierre sin apertura correspondiente');
                }
            }

            // Verificar que operadores binarios tengan operandos
            if (token.type === 'operator' && token.opInfo.type === 'binary') {
                if (i === 0) {
                    issues.push(`Operador binario '${token.opInfo.symbol}' al inicio sin operando izquierdo`);
                }
                if (i === tokens.length - 1) {
                    issues.push(`Operador binario '${token.opInfo.symbol}' al final sin operando derecho`);
                }

                // Verificar que el operador binario esté dentro de paréntesis (excepto si es la expresión completa)
                if (tokens.length > 3) {
                    // Buscar si este operador binario tiene paréntesis que lo rodean
                    let hasParentheses = false;
                    let parenDepth = 0;
                    let foundOperator = false;

                    for (let j = 0; j < tokens.length; j++) {
                        if (tokens[j].type === '(') parenDepth++;
                        if (tokens[j].type === ')') parenDepth--;
                        if (j === i) foundOperator = true;
                        if (foundOperator && parenDepth === 0) break;
                    }

                    // Si hay múltiples operadores binarios al mismo nivel, deben estar parentizados
                    let binaryOpsAtSameLevel = 0;
                    let depth = 0;
                    for (let j = 0; j < tokens.length; j++) {
                        if (tokens[j].type === '(') depth++;
                        if (tokens[j].type === ')') depth--;
                        if (depth === 0 && tokens[j].type === 'operator' && tokens[j].opInfo.type === 'binary') {
                            binaryOpsAtSameLevel++;
                        }
                    }
                }
            }

            // Verificar que operadores unarios tengan operando
            if (token.type === 'operator' && token.opInfo.type === 'unary') {
                if (i === tokens.length - 1) {
                    issues.push(`Operador unario '${token.opInfo.symbol}' sin operando`);
                }

                // El operando de un unario debe ser variable, constante, u otra expresión entre paréntesis
                if (i + 1 < tokens.length) {
                    const nextToken = tokens[i + 1];
                    if (nextToken.type !== 'variable' && nextToken.type !== 'constant' && nextToken.type !== '(') {
                        issues.push(`Operador unario '${token.opInfo.symbol}' debe ser seguido por variable, constante o expresión entre paréntesis`);
                    }
                }
            }

            // Verificar que no haya dos variables/constantes seguidas
            if (lastToken && (lastToken.type === 'variable' || lastToken.type === 'constant') &&
                (token.type === 'variable' || token.type === 'constant')) {
                const last = lastToken.type === 'variable' ? lastToken.value : lastToken.constInfo.symbol;
                const curr = token.type === 'variable' ? token.value : token.constInfo.symbol;
                issues.push(`Símbolos consecutivos sin operador: '${last}' y '${curr}'`);
            }

            // Verificar que no haya dos operadores binarios seguidos
            if (lastToken && lastToken.type === 'operator' && lastToken.opInfo.type === 'binary' &&
                token.type === 'operator' && token.opInfo.type === 'binary') {
                issues.push(`Operadores binarios consecutivos: '${lastToken.opInfo.symbol}' y '${token.opInfo.symbol}'`);
            }

            // Verificar paréntesis vacío
            if (lastToken && lastToken.type === '(' && token.type === ')') {
                issues.push('Paréntesis vacío: ()');
            }

            lastToken = token;
        }

        if (parenthesesCount > 0) {
            issues.push(`${parenthesesCount} paréntesis de apertura sin cierre`);
        }

        const isWellFormed = issues.length === 0;
        const hasWarnings = warnings.length > 0;

        // Mensaje detallado
        let message = '';
        if (isWellFormed && !hasWarnings) {
            message = '✓ La expresión es una Fórmula Bien Formada (FBF)';
        } else if (isWellFormed && hasWarnings) {
            message = '✓ La expresión es una Fórmula Bien Formada (FBF) - Con advertencias de sintaxis redundante';
        } else {
            message = '✗ La expresión NO es una Fórmula Bien Formada (FBF) - Contiene errores';
        }

        return {
            isWellFormed,
            issues,
            warnings,
            message
        };
    }

    /**
     * Intenta completar o corregir una expresión
     */
    autoComplete(expression) {
        const suggestions = [];
        let corrected = expression.trim();

        // Contar paréntesis
        const openParens = (corrected.match(/\(/g) || []).length;
        const closeParens = (corrected.match(/\)/g) || []).length;

        if (openParens > closeParens) {
            const missing = openParens - closeParens;
            corrected += ')'.repeat(missing);
            suggestions.push(`Se agregaron ${missing} paréntesis de cierre`);
        } else if (closeParens > openParens) {
            const missing = closeParens - openParens;
            corrected = '('.repeat(missing) + corrected;
            suggestions.push(`Se agregaron ${missing} paréntesis de apertura al inicio`);
        }

        // Detectar operadores al final sin operando
        const endsWithBinaryOp = /[∧∨⊕→↔]$/.test(corrected.trim());
        if (endsWithBinaryOp) {
            corrected += ' ?';
            suggestions.push('Falta operando derecho (indicado con ?)');
        }

        // Detectar operadores al inicio sin operando
        const startsWithBinaryOp = /^[∧∨⊕→↔]/.test(corrected.trim());
        if (startsWithBinaryOp) {
            corrected = '? ' + corrected;
            suggestions.push('Falta operando izquierdo (indicado con ?)');
        }

        return {
            original: expression,
            corrected: corrected !== expression ? corrected : null,
            suggestions
        };
    }

    /**
     * Genera la tabla de verdad completa con pasos
     */
    generateTruthTable(expression) {
        try {
            // Autocompletar expresión si es necesario
            const autoComplete = this.autoComplete(expression);

            // Tokenizar
            const tokens = this.tokenize(expression);

            // Validar si es FBF
            const fbfValidation = this.validateWellFormedFormula(tokens);

            // Extraer variables
            const variables = this.extractVariables(tokens);

            if (variables.length === 0) {
                throw new Error('No se encontraron variables en la expresión');
            }

            // Convertir a postfija
            const postfix = this.infixToPostfix(tokens);

            // Obtener expresión normalizada
            const normalizedExpression = this.postfixToString(postfix);

            // Generar combinaciones
            const combinations = this.generateTruthCombinations(variables);

            // Evaluar cada combinación
            const results = combinations.map(combination => {
                const result = this.evaluatePostfix(postfix, combination);
                return { ...combination, result };
            });

            // Generar evaluación paso a paso
            const steps = this.evaluateStepByStep(postfix, combinations);

            // Clasificar la expresión
            const classification = this.classifyExpression(results);

            return {
                success: true,
                expression: normalizedExpression,
                variables,
                table: results,
                tokens,
                postfix,
                steps,
                classification,
                fbfValidation,
                autoComplete
            };

        } catch (error) {
            // Intentar autocompletar incluso si hay error
            const autoComplete = this.autoComplete(expression);

            return {
                success: false,
                error: error.message,
                autoComplete
            };
        }
    }

    /**
     * Formatea la tabla de verdad para impresión
     */
    formatTruthTable(truthTable) {
        if (!truthTable.success) {
            return `Error: ${truthTable.error}`;
        }

        const { expression, variables, table } = truthTable;

        let output = '\n';
        output += '═'.repeat(60) + '\n';
        output += `Expresión: ${expression}\n`;
        output += '═'.repeat(60) + '\n\n';
        output += 'Tabla de Verdad:\n';
        output += '─'.repeat(60) + '\n';

        // Encabezados
        const headers = [...variables, 'Resultado'];
        const colWidth = 12;
        output += headers.map(h => h.padEnd(colWidth)).join('│') + '\n';
        output += '─'.repeat(60) + '\n';

        // Filas
        for (const row of table) {
            const values = variables.map(v => {
                const val = row[v] ? 'V' : 'F';
                return val.padEnd(colWidth);
            });
            const result = (row.result ? 'V' : 'F').padEnd(colWidth);
            output += [...values, result].join('│') + '\n';
        }

        output += '═'.repeat(60) + '\n';

        return output;
    }
}

// Exportar para uso en Node.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = LogicExpressionAnalyzer;
}

// Ejemplos de uso
if (require.main === module) {
    const analyzer = new LogicExpressionAnalyzer();

    console.log('╔════════════════════════════════════════════════════════════╗');
    console.log('║   ANALIZADOR DE EXPRESIONES LÓGICAS - TABLAS DE VERDAD    ║');
    console.log('╚════════════════════════════════════════════════════════════╝');

    // Ejemplos de expresiones
    const examples = [
        'A ∧ B',
        '¬A ∨ B',
        'A → B',
        '(A ∨ B) ∧ ¬C',
        'A ↔ B',
        'A ⊕ B',
        '(A ∧ B) → C',
        '¬(A ∨ B) ↔ (¬A ∧ ¬B)',  // Ley de De Morgan
    ];

    examples.forEach((expr, index) => {
        console.log(`\n\n${index + 1}. Analizando: "${expr}"`);
        const result = analyzer.generateTruthTable(expr);
        console.log(analyzer.formatTruthTable(result));
    });

    // Ejemplo interactivo (si se pasa argumento)
    if (process.argv.length > 2) {
        const customExpr = process.argv.slice(2).join(' ');
        console.log(`\n\nExpresión personalizada: "${customExpr}"`);
        const result = analyzer.generateTruthTable(customExpr);
        console.log(analyzer.formatTruthTable(result));
    }
}
