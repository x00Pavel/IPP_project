PARSER=parse.php
TEST=test.php
SRC_PARSE=./tests/parse-only/
XMLCMP=java -jar ./JExamXML/jexamxml.jar
YELOW=\033[1;33m
RED=\033[0;33m
NC=\033[0m # No Color

make:
	php7.2 ${PARSER} --stats=./tests/stats --comments --loc --labels --jumps <./tests/for_test 

test_only:
	php ${TEST} --parse-only --recursive --directory=./tests/parse-only


test_parse:
	@echo "${YELOW}--------READ_TEST--------${NC}"
	php7.2 ${PARSER} <${SRC_PARSE}read_test.src > read_test.my
	${XMLCMP} read_test.my ${SRC_PARSE}read_test.out read_test_diff.my
	@echo "${YELOW}--------SIMPLE_TEST--------${NC}"
	php7.2 ${PARSER} <${SRC_PARSE}simple_tag.src > simple_tag.my
	${XMLCMP} simple_tag.my ${SRC_PARSE}simple_tag.out simple_tag_diff.my
	@echo "${YELOW}--------WRITE_TEST--------${NC}"
	php7.2 ${PARSER} <${SRC_PARSE}write_test.src > write_test.my
	${XMLCMP} write_test.my ${SRC_PARSE}write_test.out write_test_diff.my
		

clean:
	rm -r ./tests/parse-only/*.diff*
	rm -r ./tests/parse-only/*.my*


errors:
# TODO markwodn this info
	@echo "10 - chybějící parametr skriptu (je-li třeba) nebo použití zakázané kombinace parametrů;"
	@echo -e '11 - chyba při otevírání vstupních souborů (např. neexistence, nedostatečné oprávnění); \n12 - chyba při otevření výstupních souborů pro zápis (např. nedostatečné oprávnění);'
	@echo "20 – 69 - návratové kódy chyb specifických pro jednotlivé skripty;"
	@echo -e '\t 21 - chybná nebo chybějící hlavička ve zdrojovém kódu zapsaném v IPPcode20;'
	@echo -e '\t 22 - neznámý nebo chybný operační kód ve zdrojovém kódu zapsaném v IPPcode20;'
	@echo -e '\t 23 - jiná lexikální nebo syntaktická chyba zdrojového kódu zapsaného v IPPcode20.'
	@echo "99 - interní chyba (neovlivněná vstupními soubory či parametry příkazové řádky; např. chyba alokace paměti)"