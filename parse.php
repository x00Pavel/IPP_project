<?php

include './functions.php';

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

// Reading code from standard input
while ($input_code = fgets(STDIN)){
    switch ($input_code[0]){
        case "#":
            continue;
        case "\n":
            continue;
        default:
            echo $input_code;

    }
} 

?>