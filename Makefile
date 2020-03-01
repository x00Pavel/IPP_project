PARSER=parse.php
TEST=test.php
SRC_PARSE=tests/parse-only/
XMLCMP=java -jar ./JExamXML/jexamxml.jar
YELOW=\033[1;33m
RED=\033[0;33m
NC=\033[0m # No Color

make:
	php7.3${PARSER} --stats=./tests/stats --comments --loc --labels --jumps --comments <./tests/for_test > output.xml

test_only:

	# php7.3 ${TEST} --parse-only --recursive --directory=./ipp-2020-tests/parse-only > output.html
	php7.3 ${TEST} --parse-only --recursive --directory=./looool > output.html
	# php ${TEST} --parse-only --recursive --directory=./tests/parse-only > output.html


test_parse:
	@echo "${YELOW}--------READ_TEST--------${NC}"
	php7.3 ${PARSER} <${SRC_PARSE}read_test.src > ${SRC_PARSE}read_test.my
	${XMLCMP} ${SRC_PARSE}read_test.my ${SRC_PARSE}read_test.out ${SRC_PARSE}read_test_diff.my
	@echo "${YELOW}--------SIMPLE_TEST--------${NC}"
	php7.3 ${PARSER} <${SRC_PARSE}simple_tag.src > ${SRC_PARSE}simple_tag.my
	${XMLCMP} ${SRC_PARSE}simple_tag.my ${SRC_PARSE}simple_tag.out ${SRC_PARSE}simple_tag_diff.my
	@echo "${YELOW}--------WRITE_TEST--------${NC}"
	php7.3 ${PARSER} <${SRC_PARSE}write_test.src > ${SRC_PARSE}write_test.my
	${XMLCMP} ${SRC_PARSE}write_test.my ${SRC_PARSE}write_test.out ${SRC_PARSE}write_test_diff.my
		

clean:
	php7.3 clean.php ./

view:
	xdg-open output.html

errors:
# TODO markwodn this info
	@echo "${YELOW}10${NC} - chybějící parametr skriptu (je-li třeba) nebo použití zakázané kombinace parametrů;"
	@echo -e '${YELOW}11${NC} - chyba při otevírání vstupních souborů (např. neexistence, nedostatečné oprávnění); \n12 - chyba při otevření výstupních souborů pro zápis (např. nedostatečné oprávnění);'
	@echo "${YELOW}20 – 69${NC} - návratové kódy chyb specifických pro jednotlivé skripty;"
	@echo -e '\t ${YELOW}21${NC} - chybná nebo chybějící hlavička ve zdrojovém kódu zapsaném v IPPcode20;'
	@echo -e '\t ${YELOW}22${NC} - neznámý nebo chybný operační kód ve zdrojovém kódu zapsaném v IPPcode20;'
	@echo -e '\t ${YELOW}23${NC} - jiná lexikální nebo syntaktická chyba zdrojového kódu zapsaného v IPPcode20.'
	@echo "${YELOW}99${NC} - interní chyba (neovlivněná vstupními soubory či parametry příkazové řádky; např. chyba alokace paměti)"

zip:
	zip -r xyadlo00.zip ${PARSER} ${TEST} functions.php interpret.py clean.php rozsireni