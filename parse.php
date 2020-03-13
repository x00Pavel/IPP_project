<?php

/**
 * \author Pavel Yadlouski (xyadlo00)
 * \project Interpret for IPPcode20 language 
 * \brief Script for parsing input code and representing it in XML format 
 * \file parse.php
 * \date 03.2020
 */

include 'functions.php';

$commands = array(
    "MOVE" => 2,
    "CREATEFRAME" => 0, "PUSHFRAME" => 0, "POPFRAME" => 0,
    "DEFVAR" => 1,
    "CALL" => 1,
    "RETURN" => 0,
    "PUSHS" => 1, "POPS" => 1,
    "ADD" => 3, "SUB" => 3, "MUL" => 3, "IDIV" => 3,
    "LT" => 3, "GT" => 3, "EQ" => 3,
    "AND" => 3, "OR" => 3, "NOT" => 2,
    "INT2CHAR" => 2, "STRI2INT" => 3,
    "READ"  => 2, "WRITE" => 1,
    "CONCAT" => 3, "STRLEN" => 2, "GETCHAR" => 3, "SETCHAR" => 3,
    "TYPE" => 2, "LABEL" => 1,
    "JUMP" => 1, "JUMPIFEQ" => 3, "JUMPIFNEQ" => 3,
    "EXIT" => 1,
    "DPRINT" => 1, "BREAK" => 0
);

$beginning = true;
$order = 1;
$stats = false;
$loc = -1;
$comments = -1;
$labels = -1;
$temp_arr = array();
$jumps = -1;

$longargs = array("help", "stats::", "loc", "comments", "label", "jumps",);
$args = getopt("h", $longargs);

if ($argc - 1 > count($longargs)) {
    fwrite(STDERR, "Wrong argument of parse.php\n");
    exit(10);
}

if (array_key_exists("help", $args)) {
    if (count($args) != 1) {
        fwrite(STDERR, "Parameter --help can't be combined with 
                        other parameters\n");
        exit(10);
    } else {
        fwrite(STDOUT, "Script 'parse.php' read from standard input code in 
                        IPPcode20 language,");
        fwrite(STDOUT, "held lexical and syntax control on input code.\n");
        fwrite(STDOUT, "Then write down processed code in XML format to 
                        standard output based on specifications\n");
        exit(0);
    }
}

if (array_key_exists("stats", $args)) {
    $stats = checkFile($args["stats"], 1);
    if ($stats == null) {
        exit(11);
    }
}
$loc = checkArgs("loc", $args, $stats);
if ($loc != 0) {
    exit($loc);
}
$comments = checkArgs("comments", $args, $stats);
if ($comments != 0) {
    exit($comments);
}
$labels = checkArgs("labels", $args, $stats);
if ($labels != 0) {
    exit($labels);
}

$jumps = checkArgs("jumps", $args, $stats);
if ($jumps != 0) {
    exit($jumps);
}

// Create XML instance and write down default info
$initial = new XMLWriter();
$xw = new Writer();
$xw->init();

$xw->addElement('program', array('language' => 'IPPcode20'));

// Reading code from standard input
while ($input_code = fgets(STDIN)) {
    $input_code = trim($input_code, " ");
    switch ($input_code[0]) {
        case "#":
            if ($comments != -1) {
                $comments++;
            }
            break;
        case "\n":
            break;
        case '.': // Initial string
            $rc = checkHeader($input_code, $beginning);
            if ($rc != 0) {
                exit($rc);
            }
            break;
        default:
            $rc = checkArgsCount($input_code, $comments, $commands);
            if ($rc != 0) {
                $xw->close();
                exit($rc);
            }
            $xw->addElement('instruction', array('order' => $order, 'opcode' => strtoupper($input_code[0])));
            // Check if it is valid operation code
            switch (strtoupper($input_code[0])) {
                case "BREAK":
                case "CREATEFRAME":
                case "PUSHFRAME":
                case "RETURN":
                    $jumps++;
                case "POPFRAME":
                    break;
                case "PUSHS":
                case "EXIT":
                case "POPS":
                case "DPRINT":
                case "WRITE":
                case "DEFVAR":
                    $rc = var_symb($input_code, 1, $xw);
                    if ($rc != 0) {
                        exit($rc);
                    }
                    break;
                case "ADD":
                case "SUB":
                case "MUL":
                case "IDIV":
                case "LT":
                case "GT":
                case "EQ":
                case "AND":
                case "OR":
                case "GETCHAR":
                case "SETCHAR":
                case "CONCAT":
                case "STRI2INT":
                    for ($i = 1; $i < 4; $i++) {
                        $rc = var_symb($input_code, $i, $xw);
                        if ($rc != 0) {
                            exit($rc);
                        }
                    }
                    break;
                case "READ":
                    $rc = var_symb($input_code, 1, $xw);
                    if ($rc != 0) {
                        exit($rc);
                    }
                    $rc = label_type(
                        $input_code,
                        2,
                        $xw,
                        $jumps,
                        $labels,
                        $temp_arr
                    );
                    if ($rc != 0) {
                        exit($rc);
                    }
                    break;
                case "TYPE":
                case "INT2CHAR":
                case "MOVE":
                case "STRLEN":
                case "NOT":
                    for ($i = 1; $i < 3; $i++) {
                        $rc = var_symb($input_code, $i, $xw);
                        if ($rc != 0) {
                            exit($rc);
                        }
                    }
                    break;
                case "LABEL":
                case "JUMP":
                case "CALL":
                    $rc = label_type(
                        $input_code,
                        1,
                        $xw,
                        $jumps,
                        $labels,
                        $temp_arr
                    );
                    if ($rc != 0) {
                        exit($rc);
                    }
                    break;
                case "JUMPIFEQ":
                case "JUMPIFNEQ":
                    $rc = label_type(
                        $input_code,
                        1,
                        $xw,
                        $jumps,
                        $labels,
                        $temp_arr
                    );
                    if ($rc != 0) {
                        exit($rc);
                    }
                    for ($i = 2; $i < 4; $i++) {
                        $rc = var_symb($input_code, $i, $xw);
                        if ($rc != 0) {
                            exit($rc);
                        }
                    }
                    break;
                default:
                    fwrite(STDERR, "Command not supported " .
                        $input_code[0] . "\n");
                    exit(23);
                    break;
            }
            // Increment order of command 
            $order++;
            // Close element 'instruction'
            $xw->closeElement();
    }
    continue;
}

if ($stats != false) {
    array_shift($argv);
    $file = fopen($stats, "w") or die("unable to open file\n");
    foreach ($argv as $arg) {
        if ($arg == '--comments') {
            fwrite($file, $comments . "\n");
        }
        if ($arg == '--loc') {
            if ($loc == 0) {
                $new_order = $order - 1;
                fwrite($file, $new_order . "\n");
            }
        }
        if ($arg == '--labels') {
            if ($labels == 0) {
                fwrite($file, count(array_unique($temp_arr)) . "\n");
            }
        }
        if ($arg == '--jumps') {
            if ($jumps != -1) {
                fwrite($file, $jumps . "\n");
            }
        }
    }
    fclose($file);
}

$xw->closeElement();
$xw->close();
$xw->show();
