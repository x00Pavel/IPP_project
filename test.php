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
$directory = './';
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
    $directory = checkFile($args["directory"], 2);
    if($directory == null){
        exit (11);
    }
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

// $html = fopen('output.html', 'w');
fwrite(STDOUT,'<html>');


fwrite(STDOUT, "<body>\n<h1>Output of testing</h1>\n
<p>Parameters</p>\n
<ol>\n");
for ($i = 1; $i < $argc; $i++){
    fwrite(STDOUT,"<li>".$argv[$i]."</li>\n");
}
fwrite(STDOUT, "</ol>\n");

fwrite(STDOUT,"</body>\n</html>");


if(!$int_only){
    $srcs = array();
    $outs = array();
    $rcs  = array();
    if($recursive){
        $dir   = new RecursiveDirectoryIterator($directory, RecursiveDirectoryIterator::SKIP_DOTS);
        $files = new RecursiveIteratorIterator($dir, RecursiveIteratorIterator::SELF_FIRST);
        list ($srcs, $outs, $rcs) = iterFiles($files);

    }
    else{
        $dir = new DirectoryIterator($directory);
        foreach ($dir as $file) {
            $name = $file->getFilename();
            if(preg_match('/\w*\.src/', $name)){
                array_push($srcs,$name);
            }
            if(preg_match('/\w*\.out/', $name)){
                array_push($outs,$name);
            }
            if(preg_match('/\w*\.rc/', $name)){
                array_push($rcs,$name);
            }
        }
        
    }
    // print_r(array($srcs, $outs, $rcs));
    foreach($srcs as $src=>$file){
        shell_exec("php $parse_script --stats=tests/stats --comments --loc --labels --jumps <$file > $file.my");
        $out = shell_exec("java -jar $jexamxml $file.my ".$outs[$src]." $file.diff");
        echo $out;

    }
}




?>