#!/usr/bin/env bash

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# IPP - dka - veřejné testy - 2011/2012
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Činnost: 
# - vytvoří výstupy studentovy úlohy v daném interpretu na základě sady testů
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

TASK=dka
#INTERPRETER=perl
#EXTENSION=pl
INTERPRETER=python3
EXTENSION=py

# cesta pro ukládání chybového výstupu studentského skriptu
LOCAL_OUT_PATH="."  
LOG_PATH="."


# test01: mini definice automatu; Expected output: test01.out; Expected return code: 0
$INTERPRETER $TASK.$EXTENSION --input=test01.in --output=$LOCAL_OUT_PATH/test01.out --determinization 2> $LOG_PATH/test01.err
echo -n $? > test01.!!!

# test02: jednoducha determinizace (z prednasek); Expected output: test02.out; Expected return code: 0
$INTERPRETER $TASK.$EXTENSION --input=test02.in -d > $LOCAL_OUT_PATH/test02.out 2> $LOG_PATH/test02.err
echo -n $? > test02.!!!

# test03: pokrocila determinizace; Expected output: test03.out; Expected return code: 0
$INTERPRETER $TASK.$EXTENSION -d --input=test03.in --output=$LOCAL_OUT_PATH/test03.out 2> $LOG_PATH/test03.err
echo -n $? > test03.!!!

# test04: diakritika a UTF-8 na vstupu; Expected output: test04.out; Expected return code: 0
$INTERPRETER $TASK.$EXTENSION --input=test04.in > $LOCAL_OUT_PATH/test04.out 2> $LOG_PATH/test04.err
echo -n $? > test04.!!!

# test05: slozitejsi formatovani vstupniho automatu (specialni znaky); Expected output: test05.out; Expected return code: 0
$INTERPRETER $TASK.$EXTENSION --input=test05.in --output=$LOCAL_OUT_PATH/test05.out 2> $LOG_PATH/test05.err
echo -n $? > test05.!!!

# test06: vstup ze zadani; Expected output: test06.out; Expected return code: 0
$INTERPRETER $TASK.$EXTENSION -d --output=$LOCAL_OUT_PATH/test06.out < test06.in 2> $LOG_PATH/test06.err
echo -n $? > test06.!!!

# test07: odstraneni vymazavacich prechodu (priklad z IFJ04); Expected output: test07.out; Expected return code: 0
$INTERPRETER $TASK.$EXTENSION -e --input=test07.in --output=$LOCAL_OUT_PATH/test07.out 2> $LOG_PATH/test07.err
echo -n $? > test07.!!!

# test08: Chybna kombinace parametru -e a -d; Expected output: test08.out; Expected return code: 1
$INTERPRETER $TASK.$EXTENSION --input=test08.in --output=$LOCAL_OUT_PATH/test08.out -d --no-epsilon-rules 2> $LOG_PATH/test08.err
echo -n $? > test08.!!!

# test09: chyba vstupniho formatu; Expected output: test09.out; Expected return code: 40
$INTERPRETER $TASK.$EXTENSION --input=test09.in --output=$LOCAL_OUT_PATH/test09.out 2> $LOG_PATH/test09.err
echo -n $? > test09.!!!

# test10: semanticka chyba vstupniho formatu (start. stav neni v mnozine stavu); Expected output: test10.out; Expected return code: 41
$INTERPRETER $TASK.$EXTENSION --input=test10.in --output=$LOCAL_OUT_PATH/test10.out 2> $LOG_PATH/test10.err
echo -n $? > test10.!!!

# test90: Bonus RUL - prepinac rules-only (bez rozsireni vraci chybu); Expected output: test90.out; Expected return code: 0
$INTERPRETER $TASK.$EXTENSION --input=test90.in --output=$LOCAL_OUT_PATH/test90.out --rules-only 2> $LOG_PATH/test90.err
echo -n $? > test90.!!!

# test91: Bonus WCH - oddeleni elementu nejen carkami, ale i bilymi znaky (bez rozsireni vraci chybu); Expected output: test91.out; Expected return code: 0
$INTERPRETER $TASK.$EXTENSION --input=test91.in --output=$LOCAL_OUT_PATH/test91.out --white-char 2> $LOG_PATH/test91.err
echo -n $? > test91.!!!

# test92:  Bonus RUL a WCH - slozitejsi formatovani -r a -w (bez rozsireni vraci chybu); Expected output: test92.out; Expected return code: 0
$INTERPRETER $TASK.$EXTENSION -w --input=test92.in -r --output=$LOCAL_OUT_PATH/test92.out 2> $LOG_PATH/test92.err
echo -n $? > test92.!!!

