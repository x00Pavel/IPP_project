<?php
$dir   = new RecursiveDirectoryIterator($argv[1], RecursiveDirectoryIterator::SKIP_DOTS);
$files = new RecursiveIteratorIterator($dir, RecursiveIteratorIterator::SELF_FIRST);

$yellow = "\\033[1;33m";
$nc = "\\033[0m";
foreach ($files as $file) {
    $name = $file->getPathname();
    if (preg_match('/.*\.my.*/', $name) | preg_match('/.*\.diff.*/', $name)){
        
        
        shell_exec("rm $name");
    } 
}
?>