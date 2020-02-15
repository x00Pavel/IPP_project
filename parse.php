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
    "AND" => 3, "OR" => 3, "NOT" => 2, 
    "INT2CHAR" => 2, "STRI2INT" => 3, 
    "READ"  => 2, "WRITE" => 1, 
    "CONCAT" => 3, "STRLEN" => 2, "GETCHAR" => 3,"SETCHAR" => 3, 
    "TYPE" => 2, "LABEL" => 1, 
    "JUMP" => 1, "JUMPIFEQ" => 3, "JUMPIFNEQ" => 3, 
    "EXIT" => 1, 
    "DPRINT" => 1, "BREAK" => 0); 


$beginning = true;
$order = 1;

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

$initial = new XMLWriter();
$xw = new Writer();
$xw->init();

$xw->addElement('program', array('language'=>'IPPcode20'));

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
                $xw->close();
                exit (22);
            }
            else{
                // TODO 
                $xw->addElement('instruction', array('order'=>$order, 'opcode'=>strtoupper($input_code[0])));
                // $arg_num = $commands[$input_code[0]];
                $arg_num = $commands[strtoupper($input_code[0])];
                if($arg_num != 0){
                    for ($i = 1; $i <= $arg_num; $i++){
                        // Is it a variable or constant?
                        if(preg_match('/\s*\S*@\S*/',$input_code[$i])){
                            $parts = explode("@",$input_code[$i],2);

                            switch (strtolower($parts[0])){
                                case "gf":case "tf":case "lf":
                                    $xw->addElement('arg'.$i, array('type'=>'var'));
                                    $xw->text(strtoupper($parts[0])."@".$parts[1]);
                                    $xw->closeElement();
                                    continue;
                                case "int":
                                case "bool":
                                    $parts[1] = strtolower($parts[1]);
                                case "string": // For string converting of '<','>' and '&' is automatically
                                case "nil":
                                case "type":
                                    $xw->addElement('arg'.$i, array('type'=>$parts[0]));
                                    $xw->text($parts[1]);
                                    $xw->closeElement();                               
                                }
                        }
                        // Is it a label?
                        else{
                            if( strtolower($input_code[0]) == 'label'    || 
                                strtolower($input_code[0]) == 'jump'     ||
                                strtolower($input_code[0]) == 'jumpifeq' ||
                                strtolower($input_code[0]) == 'jumpifneq'||
                                strtolower($input_code[0]) == 'call'){
                                    $xw->addElement('arg'.$i, array('type'=>'label'));
                            }
                            else{
                                $xw->addElement('arg'.$i, array('type'=>'type'));
                            }
                            $xw->text($input_code[$i]);
                            $xw->closeElement();
                        }
                    }
                }
            }
        // Increment order of command 
        $order++;
        // Close element 'instruction'
        $xw->closeElement();
    }
            
    continue;
} 

$xw->closeElement();
$xw->close();
$xw->show();

?>