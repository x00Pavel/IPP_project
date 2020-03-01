<?php
/**
 * \author Pavel Yadlouski (xyadlo00)
 * \brief File with definition of all functions and classes used in this project
 * 
 */


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
        if (preg_match('/^\s*.ippcode20\s*/i',strtolower($header))){ // regex take strings like "    .IPpcode20     \n". Spaces are not mandatory
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
function checkArgsCount(string $input_code, $comments, $commands){
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
    $size = count($input_code) - 1;
    if (!array_key_exists(strtoupper($input_code[0]), $commands)) {
        fwrite(STDERR, "Wrong command '" . $input_code[0] . "'\n");
        return 22;
    }
    if($commands[strtoupper($input_code[0])] !=  $size){
        fwrite(STDERR, "You have wrong number of parameters for command ". $input_code[0]."\n");
        fwrite(STDERR, "You have ".$size.", but command requires ". $commands[$input_code[0]]."\n");
        fwrite(STDERR, "Following arguments are inserted: \n");
        for ($i = 1; $i < $size; $i++){
            fwrite(STDERR, $i.")".$input_code[$i]."  |  "); 
        }
        fwrite(STDERR, "\n");
        return 23;
    }
    return 0;
}

/**
 * \brief Function that check if given parameter is valid (presents in given array) 
 * It is used only for check parameters if user want to take statistics. If statistics is not set,
 * then function return false 
 * 
 * \param[in] param Parameter to check
 * \param[in] args Array of given parameters
 * \param[in] stats Flag for statistics 
 * 
 * \return 0 if statistics is set and given array contain given parameter
 * \return 10 if array have some parameters for statistics, but file for writing them is not set
 * \return false if there isn't given parameter for collecting statistics
 */
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

/**
 * \brief Function for handling variables and constants
 * Also function writes down to XML corresponding text 
 * 
 * \param[in] input_code Code of operation
 * \param[in] i position of current argument
 * \param[in] xw XML writer
 *
 */
function var_symb($input_code, $i, $xw){
    $parts = explode("@",$input_code[$i],2);    
 
    switch ($parts[0]){
        case "GF":case "TF":case "LF":
            $xw->addElement('arg'.$i, array('type'=>'var'));
            $xw->text(strtoupper($parts[0])."@".$parts[1]);
            $xw->closeElement();
            break;
        case "bool":
            $parts[1] = strtolower($parts[1]);
            $xw->addElement('arg' . $i, array('type' => $parts[0]));
            $xw->text($parts[1]);
            $xw->closeElement();                               
            break;
        case "int":
        case "string": // For string converting of '<','>' and '&' is automatically
        case "nil":
        // case "type":
            $xw->addElement('arg'.$i, array('type'=>$parts[0]));
            $xw->text($parts[1]);
            $xw->closeElement();                               
            break;
        default:
            fwrite(STDERR, "Wrong type or bad parameter " . $input_code[$i] . "\n");
            return 23;
        }
        
    return 0;
}

/**
 * \brief Function for handling labels and types
 * Also function writes down to XML corresponding text 
 * 
 * \param[in] input_code Code of operation
 * \param[in] i position of current argument
 * \param[in] xw XML writer
 * \param[in] jumps Variable for parameter --jumps
 * \param[in] label Variable for parameter --labels
 * \param     temp_arr Array for writing down all labels
 * 
 */
function label_type($input_code, $i, $xw, $jumps, $label, $temp_arr){
    global $jumps;
    global $labels;
    global $temp_arr;

    if (preg_match('/\s*\S*@\S*/', $input_code[$i])) {
        fwrite(STDERR, "Expecting label, but got symbol ". $input_code[$i]."\n");
        return 23;
    }    
    switch (strtoupper($input_code[0])){
        case 'LABEL':
            if($label != -1){
                array_push($temp_arr, $input_code[$i]);
            }
            $xw->addElement('arg'.$i, array('type'=>'label'));
            $xw->text($input_code[$i]);
            $xw->closeElement();
            return 0;
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
            return 0;
        case 'READ':
            $xw->addElement('arg'.$i, array('type'=>'type'));
            $xw->text($input_code[$i]);
            $xw->closeElement();
            return 0;
    }
}

/**
 * \brief Function for checking permissions and if file is exist
 * 
 * \param[in] file Path to file or directory
 * \param[in] stats optional parameter for checking if if file is writable
 * 
 * \return In success path to file 
 * \return Null in any other case
 */
function checkFile(string $file, $flag = 0){
    if($file != null){
        switch ($flag){
            case 0:
                if(is_executable($file)){
                    return $file;
                }
            case 1:
                if(is_writable($file)){
                    return $file;
                }
            case 2:
                if(is_readable($file)){
                    return $file;
                }
            default:
                fwrite(STDERR, "File ".$file." is not executable (in case of stats param, not writable)\n");
                return null;
        }
    }
    else{
        fwrite(STDERR, "You didn't specified any file or file does not exist\n");
        return null;
    }
}

/**
 * \brief Function for iteration through directories
 * It find all .src, .out and .rc files. Create array with corresponding files,
 * sort this array in natural way. After sorting, on same indexes of arrays 
 * there are files that corresponds to each other.
 * 
 * \note files .src, .out, .rc MUST have same string before '.' 
 * 
 * \param[in] files user defined direct
 * 
 * \return array of arrays with .src, .out, .rc files
 */
function iterFiles($files){
    $srcs = array();
    $outs = array();
    $rcs  = array();
    foreach ($files as $file) {
        $name = $file->getPathname();
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
    sort($srcs,SORT_NATURAL);
    sort($outs, SORT_NATURAL);
    sort($rcs, SORT_NATURAL);
    return array($srcs, $outs, $rcs);
}

/**
 * \brief Class that wrap basic functionality of XMLWriter class based on needs of this project 
 */
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