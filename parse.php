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
$stats = false;
$loc = -1;
$comments = -1;
$labels = -1;
$temp_arr = array();
$jumps = -1;

$longargs = array("help", "stats::", "loc", "comments", "label", "jumps",);
// Handling about number of arguments and printing out help massage
$args = getopt("h", $longargs);

if($argc - 1 > count($longargs)){
    fwrite(STDERR, "Wrong argument of parse.php\n");
    exit (10);
}

if(array_key_exists("help",$args)){
    if(count($args) != 1){
        fwrite(STDERR, "Parameter --help can't be combined with other parameters\n");
        exit (10);
    }
    else{
        fwrite(STDOUT, "Script 'parse.php' read from standard input code in IPPcode20 language,");
        fwrite(STDOUT, "held lexical and syntax control on input code.\n");
        fwrite(STDOUT, "Then write down processed code in XML format to standard output based on specifications\n");
        exit (0);
    }
}




if(array_key_exists("stats", $args)){
    $stats = checkFile($args["stats"], 1);
    if($stats == null){
        exit (11);
    }
}

$loc = checkArgs("loc",$args,$stats);
if($loc != 0){
    exit($loc);
}
$comments = checkArgs("comments",$args,$stats);
if($comments != 0){
    exit($comments);
}
$labels = checkArgs("labels",$args,$stats);
if($labels != 0){
    exit($labels);
}

$jumps = checkArgs("jumps",$args,$stats);
if($jumps != 0){
    exit($jumps);
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
            if($comments != -1){
                $comments++;
            }
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
            $rc = checkArgsCount($input_code, $comments);
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
                $xw->addElement('instruction', array('order'=>$order, 'opcode'=>strtoupper($input_code[0])));
                $arg_num = $commands[strtoupper($input_code[0])];
                if($arg_num != 0){
                    for ($i = 1; $i <= $arg_num; $i++){
                        // Is it a variable or constant?
                        if(preg_match('/\s*\S*@\S*/',$input_code[$i])){
                            $rc = var_const($input_code, $i, $xw);
                            if($rc != 0){
                                exit ($rc);
                            }
                        }
                        // Is it a label?
                        else{
                            label_type($input_code, $i, $xw, $jumps, $labels, $temp_arr);
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

if ($stats != false){
    $file = fopen($stats, "w") or die("unable to open file\n");
    if($comments){
        fwrite($file,$comments."\n");
    }
    if($loc == 0){
        $order = $order -1;
        fwrite($file,$order."\n");
    }
    if($labels == 0){
        fwrite($file,count(array_unique($temp_arr))."\n");
    }
    if($jumps != -1){        
        fwrite($file,count(array_unique($temp_arr))."\n");
    }
    fclose($file);
}

$xw->closeElement();
$xw->close();
$xw->show();

?>