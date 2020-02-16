<?php

/**
 * \brief Function for checking header in file
 * Also set flag 'beginning' to false
 * 
 * \param[in] header - string which should contain header
 * \param[in] beginning - boolean variable which shows if it is first valid line in input file
 * 
 * \return 0 if header is correct
 * \return 21 if header is incorrect
 * \return 23 if line that seams to be a header, but it somewhere in the code
 */ 
function checkHeader (string $header,bool $beginning){
    global $beginning;
    if ($beginning){
        if (preg_match('/^\s*.ippcode20\s*/i',$header)){ // regex take strings like "    .IPpcode20     \n". Spaces are not mandatory
            $beginning = false;
            return 0;
        }
        else{
            fwrite(STDERR, "Wrong header of code\n");
            return 21;                 
        }
    }
    else{
        fwrite(STDERR, "Header is not in the beginning of the code\n");
        return 23;
    }
}

/**
 * \brief Function checks number of arguments in given lune
 * Also convert this line to array
 * 
 * \param[in] input_code given line of code
 * 
 * \return 0 in success
 * \return 23 in case of count of arguments
 */
function checkArgsCount(string $input_code, $comments){
    global $input_code;
    global $comments;
    // Check for comments on line with code
    if(strpos($input_code, '#')){
        $input_code = substr($input_code, 0, strpos($input_code, '#'));
        if ($comments != -1){
            $comments++;
        }
    }
    
    $input_code = array_values(array_filter(preg_split('/\s+/', $input_code)));
    $size = count($input_code);
    if ($size <= 4){
        return 0;
    }
    else{
        fwrite(STDERR,"Wrong number of arguments for '".$input_code[0]."' command.\n");
        fwrite(STDERR, "You have following arguments: \n");
        for ($i = 1; $i < $size; $i++){
            fwrite(STDERR, $i.")".$input_code[$i]."   "); 
        }
        fwrite(STDERR, "\n");
        return (23); 
    }
}

function checkArgs(string $param, $args, $stats){
    if(array_key_exists($param,$args)){
        if($stats != null){
            return 0;
        }
        else{
            fwrite(STDERR, "Parameter file for statistics is not set(no --stats=file parameter), but used other parameter for collecting them (--".$param.")\n");
            return 10;
        }
    }
    return false;
}

function var_const($input_code, $i, $xw){
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

function label_type($input_code, $i, $xw, $jumps, $label, $temp_arr){
    global $jumps;
    global $labels;
    global $temp_arr;
    switch ($input_code[0]){
        case 'LABEL':
            if($label != -1){
                array_push($temp_arr, $input_code[$i]);
            }
            $xw->addElement('arg'.$i, array('type'=>'label'));
            $xw->text($input_code[$i]);
            $xw->closeElement();
            return;
        case 'JUMP':
        case 'JUMPIFEQ':
        case 'JUMPIFNEQ':
        case 'CALL':
            if($jumps != -1){
                $jumps++;
            }
            $xw->addElement('arg'.$i, array('type'=>'label'));
            $xw->text($input_code[$i]);
            $xw->closeElement();
            return;
        default:
            $xw->addElement('arg'.$i, array('type'=>'type'));
            $xw->text($input_code[$i]);
            $xw->closeElement();
            return;
    }
}

class Writer extends XMLWriter{
    public function init(){
        // $this = new XMLWriter();
        $this->openMemory();
        $this->startDocument('1.0', 'UTF-8');
        $this->setIndent(true);
        $this->setIndentString('    ');
    }
    
    public function addElement(string $element, array $attributes){
        $this->startElement($element);
        foreach ($attributes as $name=>$text){
            $this->startAttribute($name);
            $this->text($text);
            $this->endAttribute();
        }
    }

    public function closeElement(){
        $this->endElement();
    }

    public function close(){
        $this->endDocument();
    }
    
    public function show(){
        echo $this->outputMemory(); 
    }
}

?>