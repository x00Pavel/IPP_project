PARSER=parse.php
SRC_PARSE=./tests/parse-only/
XMLCMP=java -jar ./JExamXML/jexamxml.jar

test_parse:
	php7.2 ${PARSER} <${SRC_PARSE}read_test.src > read_test.my
	${XMLCMP} read_test.my ${SRC_PARSE}read_test.out diff.my

errors:
# TODO markwodn this info
	@echo "10 - chybějící parametr skriptu (je-li třeba) nebo použití zakázané kombinace parametrů;"
	@echo -e '11 - chyba při otevírání vstupních souborů (např. neexistence, nedostatečné oprávnění); \n12 - chyba při otevření výstupních souborů pro zápis (např. nedostatečné oprávnění);'
	@echo "20 – 69 - návratové kódy chyb specifických pro jednotlivé skripty;"
	@echo -e '\t 21 - chybná nebo chybějící hlavička ve zdrojovém kódu zapsaném v IPPcode20;'
	@echo -e '\t 22 - neznámý nebo chybný operační kód ve zdrojovém kódu zapsaném v IPPcode20;'
	@echo -e '\t 23 - jiná lexikální nebo syntaktická chyba zdrojového kódu zapsaného v IPPcode20.'
	@echo "99 - interní chyba (neovlivněná vstupními soubory či parametry příkazové řádky; např. chyba alokace paměti)"