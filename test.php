<?php

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
$parse_script = './parse.php';
$int_script = './interpret.py';
$jexamxml = '/pub/courses/ipp/jexamxml/jexamxml.jar';

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

if(array_key_exists("recursive", $args)){
    $recursive = true;
}

if(array_key_exists("parse-script", $args)){
    if($args["parse-script"] == null){
        fwrite(STDERR, "You didn't specified any file\n");
        exit (10);
    }
    $parse_script = $args["parse-script"];
}

if(array_key_exists("int-script", $args)){
    $int_script = $args["int-script"];
}

if(array_key_exists("jexamxml", $args)){
    $jexamxml = $args["jexamxml"];
}


?>