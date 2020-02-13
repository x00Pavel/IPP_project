PARSER=parse.php
SRC=for_test

test:
	cat ${SRC} | php ${PARSER}