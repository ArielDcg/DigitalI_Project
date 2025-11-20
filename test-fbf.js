const LogicExpressionAnalyzer = require('./logic-expression-analyzer');

const analyzer = new LogicExpressionAnalyzer();

console.log('\n========================================');
console.log('PRUEBA 1: (¬p) - Paréntesis innecesarios');
console.log('========================================');
const test1 = analyzer.generateTruthTable('(¬p)');
console.log('FBF Válida:', test1.fbfValidation.isWellFormed);
console.log('Mensaje:', test1.fbfValidation.message);
if (test1.fbfValidation.issues.length > 0) {
    console.log('Issues:');
    test1.fbfValidation.issues.forEach((issue, i) => {
        console.log(`  ${i + 1}. ${issue}`);
    });
}

console.log('\n========================================');
console.log('PRUEBA 2: (A) - Variable con paréntesis');
console.log('========================================');
const test2 = analyzer.generateTruthTable('(A)');
console.log('FBF Válida:', test2.fbfValidation.isWellFormed);
console.log('Mensaje:', test2.fbfValidation.message);
if (test2.fbfValidation.issues.length > 0) {
    console.log('Issues:');
    test2.fbfValidation.issues.forEach((issue, i) => {
        console.log(`  ${i + 1}. ${issue}`);
    });
}

console.log('\n========================================');
console.log('PRUEBA 3: (⊤) - Constante con paréntesis');
console.log('========================================');
const test3 = analyzer.generateTruthTable('A ∧ (⊤)');
console.log('FBF Válida:', test3.fbfValidation.isWellFormed);
console.log('Mensaje:', test3.fbfValidation.message);
if (test3.fbfValidation.issues.length > 0) {
    console.log('Issues:');
    test3.fbfValidation.issues.forEach((issue, i) => {
        console.log(`  ${i + 1}. ${issue}`);
    });
}

console.log('\n========================================');
console.log('PRUEBA 4: A ∧ B - Expresión válida');
console.log('========================================');
const test4 = analyzer.generateTruthTable('A ∧ B');
console.log('FBF Válida:', test4.fbfValidation.isWellFormed);
console.log('Mensaje:', test4.fbfValidation.message);
if (test4.fbfValidation.issues.length > 0) {
    console.log('Issues:');
    test4.fbfValidation.issues.forEach((issue, i) => {
        console.log(`  ${i + 1}. ${issue}`);
    });
}

console.log('\n========================================');
console.log('PRUEBA 5: ¬A - Expresión válida');
console.log('========================================');
const test5 = analyzer.generateTruthTable('¬A');
console.log('FBF Válida:', test5.fbfValidation.isWellFormed);
console.log('Mensaje:', test5.fbfValidation.message);
if (test5.fbfValidation.issues.length > 0) {
    console.log('Issues:');
    test5.fbfValidation.issues.forEach((issue, i) => {
        console.log(`  ${i + 1}. ${issue}`);
    });
}

console.log('\n========================================');
console.log('PRUEBA 6: () - Paréntesis vacío');
console.log('========================================');
const test6 = analyzer.generateTruthTable('A ∧ ()');
console.log('Success:', test6.success);
console.log('Error:', test6.error || 'N/A');
if (test6.fbfValidation) {
    console.log('FBF Válida:', test6.fbfValidation.isWellFormed);
    console.log('Mensaje:', test6.fbfValidation.message);
    if (test6.fbfValidation.issues.length > 0) {
        console.log('Issues:');
        test6.fbfValidation.issues.forEach((issue, i) => {
            console.log(`  ${i + 1}. ${issue}`);
        });
    }
}
