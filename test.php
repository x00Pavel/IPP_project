<?php

/**
 * \author Pavel Yadlouski (xyadlo00)
 * \project Interpret for IPPcode20 language 
 * \brief Script for auto testing of parser and interpret 
 * \file test.php
 * \date 03.2020
 */


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
$int_script = 'interpret.py';
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

// Header of HTML file
fwrite(STDOUT, '<!DOCTYPE html>
<html>
<head>
<style>
table, th, td {
  border: 1px solid black;
  border-collapse: collapse;
}
th {
    text-align: center;
}
body, h1 {
  background-color: grey;
  color: black;
}

</style>
</head>
<body>');

fwrite(STDOUT, "<h2>Output of testing</h2>\n<p>Parameters</p>\n<ol>\n");
for ($i = 1; $i < $argc; $i++) {
    fwrite(STDOUT, "<li>" . $argv[$i] . "</li>\n");
}
fwrite(STDOUT, "</ol>\n");

fwrite(STDOUT, "<hr size=5>\n");

$ok = "<span style=\"color:chartreuse\">&#10004</span>";
$not_ok = "<span style=\"color:red\">&#10008</span>";
$passed = 0;
$faled = 0;

$array = array();
$files = null;
if ($recursive) {
    $dir   = new RecursiveDirectoryIterator($directory, RecursiveDirectoryIterator::SKIP_DOTS);
    $files = new RecursiveIteratorIterator($dir, RecursiveIteratorIterator::SELF_FIRST);
} else {
    $files = new DirectoryIterator($directory);
}

foreach ($files as $file) {
    $name = $file->getPathname();
    preg_match('/(.*\/(.*))\.(src|out|rc|in)/', $name, $matches);
    if (is_dir($name)) {
        continue;
    }
    if (count($matches) != 4){
        continue;
    }
    else{
        $array[$matches[1]][$matches[3]] = $name;
    }
}
$out_str_passed = "";
$out_str_fault = "";

if ($parse_only & !$int_only) {
    foreach ($array as $path => $files) {
        shell_exec("php7.4 $parse_script  <" . $files['src'] . " > tmp.my");
        $return_code = shell_exec("echo $?");
        $refer_code = file_get_contents($files['rc'], false, NULL, 0);
        if ($refer_code == "") {
            $refer_code == "0";
        }

        if (strcmp("$return_code", $refer_code)) {
            $out_file = $files['out'];
            if (file_get_contents($out_file)) {
                $out = shell_exec("java -jar $jexamxml tmp.my " . $out_file . " tmp.diff");
                $xml_result = preg_match('/.*Two files are identical.*/', $out);
                if ($xml_result) {
                    $out_str_passed = $out_str_passed . "<tr>
                        <td>" . $files['src'] . "<td/>
                        <td>" . $out_file . "<td/>
                        <td>" . $refer_code . "<td/>
                        <td align=\"center\">$ok<td/>
                        <td align=\"center\" >$ok<td/>
                    <tr/>";
                    $passed++;
                } else {
                    $out_str_fault = $out_str_fault . "<tr>
                        <td>" . $files['src'] . "<td/>
                        <td>" . $out_file . "<td/>
                        <td>" . $refer_code . "<td/>
                        <td align=\"center\">$ok<td/>
                        <td align=\"center\" >$not_ok<td/>
                    <tr/>";
                    $faled++;
                }
            } else {
                $out_str_fault = $out_str_fault . "<b>No reference file (.out) for file " . $files['src'] . "</b><br/>\n";
                $out_str_fault = $out_str_fault . "<hr size=5>\n";
            }
        } else {
            $out_str_fault = $out_str_fault . "<tr>
                <td>" . $files['src'] . "<td/>
                <td>" . $out_file . "<td/>
                <td>" . $refer_code . "<td/>
                <td align=\"center\" >$not_ok<td/>
                <td align=\"center\" >$not_ok<td/>
            <tr/>";
            $faled++;
        }
    }
    shell_exec("rm tmp.my tmp.diff");
} else if ($int_only & !$parse_only) {
    foreach ($array as $path => $files) {
        $cmd = "python3.8 $int_script --source=" . $files['src'];
        if (array_key_exists("in", $file)) {
            $cmd = $cmd . " --input=" . $files['in'];
        }
        $cmd_out = shell_exec($cmd." > tmp.txt");
        $return_code = shell_exec("echo $?");
        if (array_key_exists('rc', $files)) {
            $refer_code = file_get_contents($files['rc'], false, NULL, 0);
            if ($refer_code == '') {
                $refer_code = 0;
            }
        } else {
            $refer_code = 0;
        }
        if (intval($return_code) == $refer_code) {
            if (array_key_exists('out', $files)) {
                $out_file = $files['out'];
                if (file_get_contents($out_file)) {
                    $out = shell_exec("diff $out_file tmp.txt");
                    $cmp_result = strcmp("", $out);
                    if ($cmp_result == 0) {
                        $out_str_passed = $out_str_passed . "<tr>
                            <td>" . $files['src'] . "<td/>
                            <td>" . $out_file . "<td/>
                            <td>" . $refer_code . "<td/>
                            <td align=\"center\" align=\"center\">$ok<td/>
                            <td align=\"center\">$ok<td/>
                        <tr/>";
                        $passed++;
                    } else {
                        $out_str_fault = $out_str_fault . "<tr>
                            <td>" . $files['src'] . "<td/>
                            <td>" . $out_file . "<td/>
                            <td>" . $refer_code . "<td/>
                            <td align=\"center\">$ok<td/>
                            <td align=\"center\" >$not_ok<td/>
                        <tr/>";
                        $faled++;
                    }
                }
            } else {
                $out_str_passed = $out_str_passed . "<tr>
                            <td>" . $files['src'] . "<td/>
                            <td> No reference output <td/>
                            <td>" . $refer_code . "<td/>
                            <td align=\"center\">$ok<td/>
                            <td align=\"center\">$ok<td/>
                        <tr/>";
                $passed++;
            }
        } else {
            $out_str_fault = $out_str_fault . "<tr>
            <td>" . $files['src'] . "<td/>
            <td>" . $out_file . "<td/>
            <td>" . $refer_code . "<td/>
            <td align=\"center\" >$not_ok<td/>
            <td align=\"center\" >$not_ok<td/>
            <tr/>";
            $faled++;
        }
    }
    shell_exec("rm tmp.txt");
}
else if (!$int_only & !$parse_only){
    foreach ($array as $path => $files) {
        $cmd = "php7.4 $parse_script  <" . $files['src'] ." | python3.8 $int_script";

        if (array_key_exists("in", $files)) {
            $cmd = $cmd . " --input=" . $files['in'];
        }
        $cmd_out = exec($cmd."> tmp.txt", $o, $return_code );

        if (array_key_exists('rc', $files)) {
            $refer_code = file_get_contents($files['rc'], false, NULL, 0);
            if ($refer_code == '') {
                $refer_code = 0;
            }
        } else {
            $refer_code = 0;
        }
        if (intval($return_code) == intval($refer_code)) {
            if (array_key_exists('out', $files)) {
                $out_file = $files['out'];
                if (file_get_contents($out_file)) {
                    $out = shell_exec("diff $out_file tmp.txt");
                    $cmp_result = strcmp("", $out);
                    if ($cmp_result == 0) {
                        $out_str_passed = $out_str_passed . "<tr>
                            <td>" . $files['src'] . "<td/>
                            <td>" . $out_file . "<td/>
                            <td>" . $refer_code . "<td/>
                            <td align=\"center\">$ok<td/>
                            <td align=\"center\">$ok<td/>
                        <tr/>";
                        $passed++;
                    } else {
                        $out_str_fault = $out_str_fault . "<tr>
                        <td>" . $files['src'] . "<td/>
                            <td>" . $out_file . "<td/>
                            <td>" . $refer_code . "<td/>
                            <td align=\"center\">$ok<td/>
                            <td align=\"center\" >$not_ok<td/>
                        <tr/>";
                        $faled++;
                    }
                }
            } else {
                $out_str_passed = $out_str_passed . "<tr>
                            <td>" . $files['src'] . "<td/>
                            <td> No reference output <td/>
                            <td>" . $refer_code . "<td/>
                            <td align=\"center\">$ok<td/>
                            <td align=\"center\">$ok<td/>
                        <tr/>";
                $passed++;
            }
        } else {
            $out_str_fault = $out_str_fault . "<tr>
            <td>" . $files['src'] . "<td/>
            <td>--<td/>
            <td>" . $refer_code . "<td/>
            <td align=\"center\" >$not_ok<td/>
            <td align=\"center\" >$not_ok<td/>
            <tr/>";
            $faled++;
        }
    }
    shell_exec("rm tmp.txt");
}

// Counting statistics
$general = $passed + $faled;
$par_passed = 0;
if ($passed != 0) {
    $par_passed = (100 / $general) * $passed;
}
$par_faled = 0;
if ($faled != 0) {
    $par_faled  = (100 / $general) * $faled;
}

// Generating HTML body
fwrite(STDOUT, "<b>Statistics<b/><br/>\n");
fwrite(STDOUT, "Test passed $passed/$general ($par_passed%)<br/><b>\n");
fwrite(STDOUT, "Test faled $faled/$general ($par_faled%)<br/>\n");
fwrite(STDOUT, "<table style=\"width:100%\">");
fwrite(STDOUT, "<tr>
        <th>Source file<th/>
        <th>Reference file<th/>
        <th>Reference return code<th/>
        <th>Return code result<th/>
        <th>Comparing result<th/>
    <tr/>");
fwrite(STDOUT, $out_str_fault);
fwrite(STDOUT, $out_str_passed);
fwrite(STDOUT, "<table/>");

fwrite(STDOUT, "</body>\n</html>");
