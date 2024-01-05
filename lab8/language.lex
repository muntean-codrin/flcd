
%{ 	 
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int line = 1;
%} 

%option noyywrap

IDENTIFIER		[a-zA-Z_][a-zA-Z0-9_]*
NUMBER_CONST	0|[+|-]?[1-9][0-9]*([.][0-9]*)?|[+|-]?0[.][0-9]*
STRING_CONST	[\"][a-zA-Z0-9 ]+[\"]

%%

{STRING_CONST}		{printf("String: %s\n", yytext);}
"citeste"|"printeaza"|"daca"|"altfel"|"pentru"|"panacand"|"numar"|"string"|"si"|"sau"		{printf("Reserved word: %s\n", yytext);}
"+"|"-"|"*"|"/"|"%"|"<="|">="|"=="|"!="|"<"|">"|"="		{printf("Operator: %s\n", yytext);}
":("|":)"|"{"|"}"|"("|")"|"["|"]"|":"|";"|","|"'"|"\""		{printf("Separator: %s\n", yytext);}
{IDENTIFIER}		{printf("Identifier: %s\n", yytext);}
{NUMBER_CONST}		{printf("Number: %s\n", yytext);}

[ ]+ 		{}
[\t]+		{}
[\n]+		{line++;}

[0-9][a-zA-Z0-9_]*				{printf("Illegal identifier at line %d : %s\n", line, yytext);}
[+|-]?[0][0-9]*([.][0-9]*)?		{printf("Illegal numeric constant at line %d\n", line);}

%%

void main(argc, argv)
int argc;
char** argv;
{ 
    FILE *file;
    file = fopen(argv[1], "r");
    yyin = file;
	yylex();
}