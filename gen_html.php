<?php

$html = fopen('output.html', 'w');
if(!$html){
    fwrite(STDERR, "html file cant be created\n");
    exit(10);
} 
else{
    fwrite($html,'<html>');
}

fwrite($html, "<body>\n
<h1>Output of testing</h1>\n
<p>My first paragraph.</p>\n
</body>\n");

fwrite($html,'</html>');

?>