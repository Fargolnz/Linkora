grammar Linkora;

// A Linkora document is a single Page block containing zero or more blocks.
document
    : PAGE LCURLY block* RCURLY EOF
    ;

// A block is a PascalCase name followed by a brace-delimited body of
// properties and/or nested blocks.
block
    : BLOCK_NAME LCURLY blockContent* RCURLY
    ;

blockContent
    : property
    | block
    ;

// Properties are written as `name: value`. An optional trailing comma
// supports both the expanded and compact formatting styles.
property
    : IDENTIFIER COLON value COMMA?
    ;

value
    : STRING
    | NUMBER
    | booleanLiteral
    | IDENTIFIER
    ;

booleanLiteral
    : TRUE
    | FALSE
    ;

// --- Lexer rules -----------------------------------------------------------

// Keywords must be declared before the generic identifier rules so they win
// on equal-length matches.
PAGE: 'Page';

TRUE: 'true';
FALSE: 'false';

// Structural punctuation.
LCURLY: '{';
RCURLY: '}';
COLON: ':';
COMMA: ',';

// Block names follow PascalCase.
BLOCK_NAME: [A-Z][A-Za-z0-9]*;

// Property names and enum values follow camelCase.
IDENTIFIER: [a-z][A-Za-z0-9]*;

// Double-quoted string literal supporting the escape sequences
// \" \\ \n \t \r. Any other escape sequence is a lexical error.
STRING
    : '"' ( ~["\\\r\n] | ESCAPE )* '"'
    ;

fragment ESCAPE
    : '\\' [tnr"\\]
    ;

// Signed integer or decimal number.
NUMBER
    : '-'? DIGIT+ ( '.' DIGIT+ )?
    ;

fragment DIGIT: [0-9];

// Single-line comments.
LINE_COMMENT: '//' ~[\r\n]* -> channel(HIDDEN);

// Whitespace is insignificant.
WS: [ \t\r\n]+ -> channel(HIDDEN);
