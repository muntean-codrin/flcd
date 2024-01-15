%{
#include <stdio.h>
#include <stdlib.h>

#define YYDEBUG 1 
%}

%token CITESTE
%token PRINTEAZA
%token DACA
%token ALTFEL
%token PENTRU
%token PANACAND
%token NUMAR
%token STRING
%token SI
%token SAU
%token TRUE
%token FALSE

%token lessOrEqual
%token moreOrEqual
%token less
%token more
%token equal
%token different
%token eq



%token leftCurlyBracket
%token rightCurlyBracket
%token leftRoundBracket
%token rightRoundBracket
%token leftBracket
%token rightBracket
%token colon
%token semicolon
%token comma
%token quote

%token IDENTIFIER
%token NUMBER_CONST
%token STRING_CONST

%start program

%%

program : stmtlist

stmtlist : stmt stmtlist | 

stmt : simplstmt semicolon | composedsmt

composedsmt : leftCurlyBracket groupofstmts rightCurlyBracket | ifstmt | altfelstms

ifstmt : DACA leftRoundBracket boolexpression rightRoundBracket

altfelstms: ALTFEL

groupofstmts : stmt groupofstmts | 

simplstmt : assignstmt | iostmt | declarationstmt

assignstmt : variable eq varorexp 

iostmt : PRINTEAZA leftRoundBracket varorexp rightRoundBracket | CITESTE leftRoundBracket varorexp rightRoundBracket

declarationstmt : type variable 

type : NUMAR | STRING

variable : IDENTIFIER

expression : NUMBER_CONST | STRING_CONST

varorexp : variable | expression

boolexpression : TRUE | FALSE | varorexp comparesign varorexp | boolexpression boolexpressionconnector boolexpression

boolexpressionconnector : SI | SAU

comparesign : lessOrEqual | moreOrEqual | less | more | equal | different


%%

yyerror(char *s)
{	
	printf("%s\n",s);
}

extern FILE *yyin;

main(int argc, char **argv)
{
	if(argc>1) yyin :  fopen(argv[1],"r");
	if(argc>2 && !strcmp(argv[2],"-d")) yydebug: 1;
	if(!yyparse()) fprintf(stderr, "\tProgram is syntactically correct.\n");
}