PARSER=parse.php
TRASH=./tests/for_test

test:
	cat ${TRASH} | php7.2 ${PARSER}
