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
function checkArgsCount(string $input_code){
    global $input_code;
    // Check for comments on line with code
    if(strpos($input_code, '#')){
        $input_code = substr($input_code, 0, strpos($input_code, '#'));
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