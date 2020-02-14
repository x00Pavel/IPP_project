<?php


/*
21 - chybná nebo chybějící hlavička ve zdrojovém kódu zapsaném v IPPcode20;
22 - neznámý nebo chybný operační kód ve zdrojovém kódu zapsaném v IPPcode20;
23 - jiná lexikální nebo syntaktická chyba zdrojového kódu zapsaného v IPPcode20.
*/
include 'functions.php';

$commands = array(
    "MOVE" => 2, 
    "CREATEFRAME" => 0, "PUSHFRAME" => 0, "POPFRAME" => 0, 
    "DEFVAR" => 1,
    "CALL" => 1, 
    "RETURN" => 0, 
    "PUSHS" => 1, "POPS" => 1, 
    "ADD" => 3,"SUB" => 3, "MUL" => 3, "IDIV" => 3, 
    "LT" => 3, "GT" => 3, "EQ" => 3, 
    "AND" => 3, "OR" => 3, "NOT" => 3, 
    "INT2CHAR" => 2, "STRI2INT" => 3, 
    "READ"  => 2, "WRITE" => 1, 
    "CONCAT" => 3, "STRLEN" => 2, "GETCHAR" => 3,"SETCHAR" => 3, 
    "TYPE" => 2, "LABEL" => 1, 
    "JUMP" => 1, "JUMPIFEQ" => 3, "JUMPIFNEQ" => 3, 
    "EXIT" => 1, 
    "DPRINT" => 1, "BREAK" => 0); 


$beginning = true;

// Handling about number of arguments and printing out help massage
if ($argc >= 2){
    if ($argc > 2){
        fwrite(STDERR, "Wrong number of parameters\n");
        exit (10);
    }
    else{
        if($argv[1] == "--help"){
            fwrite(STDOUT, "Script 'parse.php' read from standard input code in IPPcode20 language,");
            fwrite(STDOUT, "held lexical and syntax control on input code.\n");
            fwrite(STDOUT, "Then write down processed code in XML format to standard output based on specifications\n");
            exit (0);
        }
        else{
            fwrite(STDERR, "Wrong argument '".$argv[1]."', here can be only argument '--help'\n");
            exit (10);
        }
    }    
}

// Create XML instance and write down default info
$xw = xmlwriter_open_memory();
xmlwriter_set_indent($xw, true);
$res = xmlwriter_set_indent_string($xw, '  ');
xmlwriter_start_document($xw, '1.0', 'UTF-8');
xmlwriter_start_element($xw, 'program');
xmlwriter_start_attribute($xw, 'language');
xmlwriter_text($xw, 'IPPcode20');
xmlwriter_end_attribute($xw);

// Reading code from standard input
while ($input_code = fgets(STDIN)){
    switch ($input_code[0]){
        case "#":
            continue;
        case "\n":
            continue;
        case ".": // Initial string
            $rc = checkHeader($input_code, $beginning);
            if($rc != 0){
                exit ($rc);
            }
            
            continue;
        default:
            $rc = checkArgsCount($input_code);
            if($rc != 0){
                exit ($rc);
            }
            // Check if it is valid operation code
            if (!array_key_exists(strtoupper($input_code[0]), $commands)){
                fwrite(STDERR, "Wrong command '".$input_code[0]."'\n");
                xmlwriter_end_document($xw);
                exit (22);
            }
            else{
                // TODO 
                // write down arguments to xml file (read specifications)
            }
            
            continue;

        
    }
} 
xmlwriter_end_element($xw);
xmlwriter_end_document($xw);

echo xmlwriter_output_memory($xw);
?>