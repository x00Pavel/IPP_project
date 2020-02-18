<?php

include 'functions.php';

$longarms = array(
    "help",
    "directory:",
    "recursive",
    "parse-script:",
    "int-script:",
    "parse-only",
    "int-only",
    "jexamxml:",
    " "
);

$parse_only = false;
$int_only = false;
$recursive = false;
$directory = '.';
$parse_script = './parse.php';
$int_script = './interpret.py';
$jexamxml = null;
if (shell_exec('pwd') == "/home/xyadlo00/studies/IPP/IPP_project\n"){
    $jexamxml = './JExamXML/jexamxml.jar';
}
else {
    $jexamxml = '/pub/courses/ipp/jexamxml/jexamxml.jar';
}
$args = getopt("",$longarms);

// Check if all arguments are valid
if ($argc -1 > count($args)){
    fwrite(STDOUT, "Wrong parameter\n");
    exit (10);
}

if (array_key_exists("help", $args)){
    if(count($args) != 1){
        fwrite(STDERR, "Parameter --help can't be combined with other parameters\n");
        exit (10);
    }
    else{
        fwrite(STDOUT, "Skript (test.php v jazyce PHP 7.4) bude sloužit pro automatické testování postupné aplikace
        parse.php a interpret.py12. Skript projde zadaný adresář s testy a využije je pro automatické
        otestování správné funkčnosti obou předchozích programů včetně vygenerování přehledného souhrnu
        v HTML 5 do standardního výstupu. Pro hodnocení test.php budou dodány referenční implementace parse.php i interpret.py. Testovací skript nemusí u předchozích dvou skriptů testovat
        jejich dodatečnou funkčnost aktivovanou parametry příkazové řádky (s výjimkou potřeby parametru
        --source a/nebo --input u interpret.py).\n");
        exit (0);
    }
}
// $dir   = new RecursiveDirectoryIterator($directory, RecursiveDirectoryIterator::SKIP_DOTS);

if(array_key_exists("directory", $args)){   
    $directory = checkFile($args["directory"], $dir, 2);
    if($directory == null){
        exit (11);
    }
    echo " HERE\n";
}

if(array_key_exists("recursive", $args)){
    $recursive = true;
}

if(array_key_exists("parse-only", $args)){
    if(array_key_exists("int-script", $args) || array_key_exists("int-only", $args)){
        fwrite(STDERR, "Parameter --parse-only can't be combined with parameters --int-script or/and --int-only\n");
        exit (10);
    }
    else{
        $parse_only = true;
    }
}

if(array_key_exists("int-only", $args)){
    if(array_key_exists("parse-script", $args) || array_key_exists("parse-only", $args)){
        fwrite(STDERR, "Parameter --parse-only can't be combined with parameters --parse-script or/and --parse-only\n");
        exit (10);
    }
    else{
        $int_only = true;
    }
}

if(array_key_exists("parse-script", $args)){
    if($args["parse-script"] != null && file_exists($args["parse-script"])){
        $parse_script = checkFile($args["parse_script"]);
        if($parse_script == null){
            exit (11);
        }
    }
}
if(array_key_exists("int-script", $args)){
    if($args["int-script"] != null && file_exists($args["int-script"])){
        $int_script = checkFile($args["int-script"]);
        if($int_script == null){
            exit (11);
        }
    }
}

if(array_key_exists("jexamxml", $args)){
    if($args["jexamxml"] != null && file_exists($args["jexamxml"])){
        $jexamxml = checkFile($args["jexamxml"]);
        if($jexamxml == null){
            exit (11);
        }
    }
}
// if(!$int_only){
//     shell_exec('php '.$parse_script.' --stats=stats --comments --loc --labels --jumps <./tests/for_test >> read_test.my');
//     $out = shell_exec('java -jar '.$jexamxml.' read_test.my '.$directory.'/read_test.out read_test_diff.my');
//     echo $out;
// }




?>