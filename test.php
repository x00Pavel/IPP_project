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
if (shell_exec('pwd') == "/home/xyadlo00/studies/IPP/project\n") {
    $jexamxml = './JExamXML/jexamxml.jar';
} else {
    $jexamxml = '/pub/courses/ipp/jexamxml/jexamxml.jar';
}
$args = getopt("", $longarms);

// Check if all arguments are valid
if ($argc - 1 > count($args)) {
    fwrite(STDOUT, "Wrong parameter\n");
    exit(10);
}

if (array_key_exists("help", $args)) {
    if (count($args) != 1) {
        fwrite(STDERR, "Parameter --help can't be combined with other parameters\n");
        exit(10);
    } else {
        fwrite(STDOUT, "Skript (test.php v jazyce PHP 7.4) bude sloužit pro automatické testování postupné aplikace
        parse.php a interpret.py12. Skript projde zadaný adresář s testy a využije je pro automatické
        otestování správné funkčnosti obou předchozích programů včetně vygenerování přehledného souhrnu
        v HTML 5 do standardního výstupu. Pro hodnocení test.php budou dodány referenční implementace parse.php i interpret.py. Testovací skript nemusí u předchozích dvou skriptů testovat
        jejich dodatečnou funkčnost aktivovanou parametry příkazové řádky (s výjimkou potřeby parametru
        --source a/nebo --input u interpret.py).\n");
        exit(0);
    }
}

if (array_key_exists("directory", $args)) {
    $directory = checkFile($args["directory"], 2);
    if ($directory == null) {
        exit(11);
    }
}

if (array_key_exists("recursive", $args)) {
    $recursive = true;
}

if (array_key_exists("parse-only", $args)) {
    if (array_key_exists("int-script", $args) || array_key_exists("int-only", $args)) {
        fwrite(STDERR, "Parameter --parse-only can't be combined with parameters --int-script or/and --int-only\n");
        exit(10);
    } else {
        $parse_only = true;
    }
}

if (array_key_exists("int-only", $args)) {
    if (array_key_exists("parse-script", $args) || array_key_exists("parse-only", $args)) {
        fwrite(STDERR, "Parameter --parse-only can't be combined with parameters --parse-script or/and --parse-only\n");
        exit(10);
    } else {
        $int_only = true;
    }
}

if (array_key_exists("parse-script", $args)) {
    if ($args["parse-script"] != null && file_exists($args["parse-script"])) {
        $parse_script = checkFile($args["parse_script"]);
        if ($parse_script == null) {
            exit(11);
        }
    }
}
if (array_key_exists("int-script", $args)) {
    if ($args["int-script"] != null && file_exists($args["int-script"])) {
        $int_script = checkFile($args["int-script"]);
        if ($int_script == null) {
            exit(11);
        }
    }
}

if (array_key_exists("jexamxml", $args)) {
    if ($args["jexamxml"] != null && file_exists($args["jexamxml"])) {
        $jexamxml = checkFile($args["jexamxml"]);
        if ($jexamxml == null) {
            exit(11);
        }
    }
}

fwrite(STDOUT, '<html>');


fwrite(STDOUT, "<body>\n<h1>Output of testing</h1>\n
<p>Parameters</p>\n
<ol>\n");
for ($i = 1; $i < $argc; $i++) {
    fwrite(STDOUT, "<li>" . $argv[$i] . "</li>\n");
}
fwrite(STDOUT, "</ol>\n");

fwrite(STDOUT, "<hr size=5>\n");


if (!$int_only) {
    $passed = 0;
    $faled = 0;

    $srcs = array();
    $outs = array();
    $rcs  = array();
    if ($recursive) {
        $dir   = new RecursiveDirectoryIterator($directory, RecursiveDirectoryIterator::SKIP_DOTS);
        $files = new RecursiveIteratorIterator($dir, RecursiveIteratorIterator::SELF_FIRST);
        list($srcs, $outs, $rcs) = iterFiles($files);
    } else {
        $files = new DirectoryIterator($directory);
        list($srcs, $outs, $rcs) = iterFiles($files);
    }


    $out_str_passed = "";
    $out_str_fault = "";
    foreach ($srcs as $index => $file) {
        shell_exec("php7.3 $parse_script --stats=./tests/stats --comments --loc --labels --jumps <$file > $file.my");
        // shell_exec("php7.3 ~/Desktop/parse_al.php --stats=./tests/stats --comments --loc --labels --jumps <$file > $file.my");
        $return_code = shell_exec("echo $?");
        $refer_code = null;
        if ($index <= count($rcs)) {
            $refer_code = file_get_contents($rcs[$index], false, NULL, 0);
            if ($refer_code == "") {
                $refer_code == "0";
            }
        } else {
            $refer_code == "0";
        }


        if (strcmp("$return_code", $refer_code)){
            if ($index < count($outs)){
                $out_file = $outs[$index];
                if (file_get_contents($out_file)) {
                    $out = shell_exec("java -jar $jexamxml $file.my " . $outs[$index] . " $file.diff");
                    $xml_result = preg_match('/.*Two files are identical.*/', $out);
                    if($xml_result){
                        $out_str_passed = $out_str_passed . "<b>Source file:<b/>\n$file<br/>\n<b>Reference output file:<b/> " . $outs[$index];
                        $out_str_passed = $out_str_passed . "<br/>\n<b>Expecting return code:<b/> " . $refer_code."<br/>\n";
                        $out_str_passed = $out_str_passed . "<b>Result:</b><font color=\"green\">PASSED</font>\n";
                        $out_str_passed = $out_str_passed . "<hr size=5>\n";
                        $passed++;
                    }
                    else{
                        $out_str_fault = $out_str_fault . "<b>Source file:<b/>\n$file<br/>\n<b>Reference output file:<b/> " . $outs[$index];
                        $out_str_fault = $out_str_fault . "<br/>\n<b>Expecting return code:<b/> " . $refer_code."<br/>\n";
                        $out_str_fault = $out_str_fault . "<b>Return code: $return_code<b/><br/>";
                        $out_str_fault = $out_str_fault . "<b>Result:</b><font color=\"red\">FAULT</font>\n";
                        $out_str_fault = $out_str_fault . "<hr size=5>\n";
                        $faled++;                        
                    }
                }
                else{
                    $out_str_passed = $out_str_passed . "<b>Source file:<b/>\n$file<br/>\n<b>Reference output file:<b/> " . $outs[$index];
                    $out_str_passed = $out_str_passed . "<br/>\n<b>Expecting return code:<b/> " . $refer_code . "<br/>\n";
                    $out_str_passed = $out_str_passed . "<b>Result:</b><font color=\"green\">PASSED</font>\n";
                    $out_str_passed = $out_str_passed . "<hr size=5>\n";
                    $passed++;
                }                    
            } else {
                $out_str_fault = $out_str_fault . "<b>No reference file (.out) for : $file</b><br/>\n";
                $out_str_fault = $out_str_fault . "<hr size=5>\n";
                break;
            }
        }
        else{
            $out_str_fault = $out_str_fault . "<b>Source file:<b/>\n$file<br/>\n<b>Reference output file:<b/> " . $outs[$index];
            $out_str_fault = $out_str_fault . "<br/>\n<b>Expecting return code:<b/> " . $refer_code . "<br/>\n";
            $out_str_fault = $out_str_fault . "<b>Return code: $return_code<b/>";
            $out_str_fault = $out_str_fault . "<font color=\"red\">FAULT</font>\n";
            $out_str_fault = $out_str_fault . "<hr size=5>\n";
            $faled++;
        }
    }
}

$general = $passed + $faled;
$par_passed = 0;
if($passed != 0){
    $par_passed = (100 / $general) * $passed;
}
$par_faled = 0;
if($faled != 0){
    $par_faled  = (100 / $general) * $faled;
}
fwrite(STDOUT, "<b>Statistics<b/><br/>\n");
fwrite(STDOUT, "Test passed $passed/$general ($par_passed%)<br/><b>\n");
fwrite(STDOUT, "Test faled $faled/$general ($par_faled%)<br/>\n");
fwrite(STDOUT, "<hr color=yellow size=8>\n");
fwrite(STDOUT, $out_str_fault);
fwrite(STDOUT, $out_str_passed);

fwrite(STDOUT, "</body>\n</html>");
