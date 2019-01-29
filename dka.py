import sys
import re
#DKA:xkysil00

#XXXXXXXXXXXXXXXXXXX
#funkce
#help
def printHelp():
  print('IPP, Projekt 2, DKA\n'
  'Vytvoril: Michal Kysilko, xkysil00\n'
  '--help viz společné zadání všech úloh.\n'
  '--input=filename\n'
  '\tzadaný vstupní textový soubor v UTF-8 s popisem konečného automatu.\n'
  '--output=filename\n\ttextový výstupní soubor (opět v UTF-8) s popisem výsledného ekviva-'
  'lentního konečného automatu v předepsaném formátu.\n'
  '-e, --no-epsilon-rules\n\tpro pouhé odstranění ε-pravidel vstupního konečného automatu.'
  'Parametr nelze kombinovat s parametrem -d (resp. --determinization).\n'
  '-d, --determinization\n\tprovede determinizaci bez generování nedostupných stavů (viz algo-'
  'ritmus IFJ, 4. přednáška, snímek 24/44). Parametr nelze kombinovat s parametrem -e (resp.'
  '--no-epsilon-rules).\n'
  '-i, --case-insensitive\n\tnebude brán ohled na velikost znaků při porovnávání symbolů či'
  'stavů (tj. a = A, ahoj = AhOj nebo A b = a B); ve výstupu potom budou všechna velká písmena'
  'převedena na malá.\n');
  sys.exit(0);

#zpracovani parametru
def checkParam(**p):
  inp = 0;
  outp = 0;
 
  for a in sys.argv:
    a2 = a.split('=');
    if a == "--help":
      p['help'] += 1;
    elif a2[0] == "--input":
      p['input'] = a2[1];
      inp += 1;
    elif a2[0] == "--output":
      p['output'] = a2[1]; 
      outp += 1; 
    elif a == "-e" or a == "--no-epsilon-rules":
      p['eps'] += 1;
    elif a == "-d" or a == "--determinization":
      p['det'] += 1;
    elif a == "-i" or a == "--case-insensitive":
      p['case'] += 1; 


  #parametry -d a -e nesmeji byt v kombinaci
  if p['eps'] == 1 and p['det'] == 1:
    sys.stderr.write('Chybna kombinace parametru. Zadejte --help pro napovedu.\n');
    sys.exit(1);

  #pokud je zadan parametr --help, nesmi byt zadan zadny jiny
  if p['help'] == 1 and p['input'] == 0 and p['output'] == 0 and p['eps'] == 0 and p['det'] == 0 and p['case'] == 0:
    printHelp();
  elif p['help'] == 1:
    sys.stderr.write('Chybna kombinace parametru. Zadejte POUZE --help pro napovedu.\n');
    sys.exit(1);

  #musi byt zadany alespon 1 parametr
  if p['help'] == 0 and p['input'] == 0 and p['output'] == 0 and p['eps'] == 0 and p['det'] == 0 and p['case'] == 0:
    sys.stderr.write('Nejsou zadany zadne validni parametry.\n');
    sys.exit(1);

  #parametry se nesmi opakovat
  if p['help'] > 1 or inp > 1 or outp > 1 or p['eps'] > 1 or p['det'] > 1 or p['case'] > 1:
    sys.stderr.write('Parametry se nesmi opakovat.\n');
    sys.exit(1);

  return p;

#pom fce pro abecedu
def isval(char):
  pom = 'ěščřžýáíéúůťňď';
  asp = re.findall(char, pom);
  if (char >= 'a' and char <= 'z') or (char >= 'A' and char <= 'Z') or asp or char.isdigit():
    return 1;
  else:
    return 0;

#je znak validni pro nazev stavu?
def iscinit(char):
  if (char >= 'a' and char <= 'z') or (char >= 'A' and char <= 'Z'):
    return 1;
  else:
    return 0;

#je znak validni pro abecedu?
def isvalidchar(char):
  
  if char == '(':
    char = '\(';
  elif char == ')':
    char = '\)';

  pom='\(\){}->,.|# \n\t';
  asp = re.findall(char, pom);
  if not asp and not char.isalpha() and not char.isdigit():
    return 0;
  else:
    return 1;


#Syntakticka analyza
def analyze_syntax(**p):

  last = 0;
  if p['input'] == 0:
    vstup = sys.stdin;
  else:
    vstup = open(p['input'], 'r', encoding='utf-8');
    
  ss = vstup.read();

  #odstraneni komentaru a bilych znaku - mezery nelze odstranit globalne, potrebujeme je u pravidel

  if p['case'] == 1:
    ss = ss.lower();

  ss = re.sub('^#.*', '', ss);
  ss = re.sub('(?P<i1>[^\'])#.*', '\g<i1>', ss); 
  ss = re.sub('\n', ' ', ss);
  ss = re.sub('\'[\r\n\t]*\'[\r\n\t]*\'[\r\n\t]*\'', '\'\'\'\'', ss);
  ss = re.sub('(?P<id1>.)[\t\n\r]+(?P<id2>[^\'])', '\g<id1>\g<id2>', ss);
  ss = re.sub('(?P<id1>[^\'])[\t\n\r]+(?P<id2>.)', '\g<id1>\g<id2>', ss);
  ss = re.sub('^[ ]*', '', ss);
  ss = re.sub(',[ ]*', ',', ss);
  ss = re.sub('[ ]*,', ',', ss);
  ss = re.sub('(?P<id1>[^\'])[ ]*\'', '\g<id1>\'', ss);
  ss = re.sub('[ ]*[)]', ')', ss);
  ss = re.sub('[ ]*[}]', '}', ss);
  ss = re.sub('[ ]*[{]', '{', ss);
  ss = re.sub('[{][ ]*', '{', ss);
  ss = re.sub('[ ]*-', '-', ss);
  ss = re.sub('>[ ]*', '>', ss);
  ss = re.sub('[ \r\n\t]*$', '', ss);
  ss = re.sub('[ ][ ]*', ' ', ss);

  if ss[0] != '(' or ss[1] != '{':
    sys.stderr.write('Chyba syntaxe!\n');
    sys.exit(40);

  state = 1;
  count = 0;

  for i in range(2,len(ss)):
    char = ss[i];

    if state == 1 and char == '}': #prazdny blok
      state = 3;
    elif state == 1 and iscinit(char): #ocekava identifikator - pismeno
      state = 2;
    elif state == 2 and (iscinit(char) or char.isdigit() or (char == '_' and (ss[i+1] != ',' and ss[i+1] != '}'))):
      pass;
    elif state == 2 and char == '}': #konec bloku
      state = 3;
    elif state == 2 and char == ',':
      state = 1;
    elif state == 3 and char == ',':
      state = 4;
    elif state == 4 and char == '{': #2. blok - abeceda
      state = 11;
    elif state == 11 and char == '}': #prazdny blok
      state = 15;
    elif state == 11 and (char.isalpha() or char.isdigit()):
      state = 12;
    elif state == 11 and char == '\'':
      state = 13;
    elif state == 12 and char == ',':
      state = 11;
    elif state == 13 and isvalidchar(char):
      state = 14
    elif state == 13 and char == '\'':
      count += 1;
      if count == 2:
        state = 14;
        count = 0;
    elif state == 14 and char == '\'':
      state = 12;
    elif state == 12 and char == '}':
      state = 15;
    elif state == 15 and char == ',':
      state = 20;
    elif state == 20 and char == '{': #3. blok - pravidla
      state = 21;
    elif state == 21 and char == '}': #prazdny blok
      state = 29;
    elif state == 21 and iscinit(char):
      state = 22;
    elif state == 22 and (iscinit(char) or char.isdigit() or (char == '_' and (ss[i+1] != ',' and ss[i+1] != '}'))):
      pass;
    elif state == 22 and char == '\'' and ss[i+1] == '\'' and ss[i+2] == '\'':
      state = 221;
    elif state == 22 and char == '\'' and ss[i+1] == '\'' and ss[i+2] != '\'':
      state = 221;
    elif state == 22 and char == '\'' and isvalidchar(ss[i+1]):
      state = 23;
    elif state == 221 and char == '\'':
      count += 1;
      if count == 1 and ss[i+1] == '-':
        state = 22;
      elif count == 3:
        state = 25;
        count = 0;
    elif state == 22 and char == ' ':
      state = 23;
    elif state == 22 and char == '-':
      state = 26;
    elif state == 23 and isvalidchar(char) and ss[i-1] == '\'' and ss[i+1] == '\'':
      state = 222;
    elif state == 222 and char == '\'':
      state = 25;
    elif state == 23 and isvalidchar(char) and ss[i-1] != '\'':
      state = 24;
    elif state == 24 and char == '\'' and ss[i-2] == '\'':
      state = 25;
    elif state == 24 and char == '-':
      state = 26;
    elif state == 25 and char == '-':
      state = 26;
    elif state == 26 and char == '>':
      state = 27;
    elif state == 27 and iscinit(char):
      state = 28;
    elif state == 28 and (iscinit(char) or char.isdigit() or (char == '_' and (ss[i+1] != ',' and ss[i+1] != '}'))):
      pass;
    elif state == 28 and char == ',':
      state = 21;
    elif state == 28 and char == '}':
      state = 29;
    elif state == 29 and char == ',': #4. blok - pocatecni stav
      state = 30;
    elif state == 30 and char == ',': #prazdny blok
      state = 40;
    elif state == 30 and iscinit(char):
      state = 31;
    elif state == 31 and (iscinit(char) or char.isdigit() or (char == '_' and (ss[i+1] != ',' and ss[i+1] != '}'))):
      pass;
    elif state == 31 and char == ',':
      state = 40;
    elif state == 40 and char == '{': #5. blok - koncove stavy
      state = 41;
    elif state == 41 and char == '}': #prazdny blok
      state = 43;
    elif state == 41 and iscinit(char):
      state = 42;
    elif state == 42 and (iscinit(char) or char.isdigit() or (char == '_' and (ss[i+1] != ',' and ss[i+1] != '}'))):
      pass;
    elif state == 42 and char == ',':
      state = 41;
    elif state == 42 and char == '}':
      state = 43;
    elif state == 43 and char == ')':
      state = 50;
    elif state == 50 and char:
      sys.stderr.write('Syntakticka chyba! Prebytecne znaky za automatem.\n');
      sys.exit(40);
    else:
      sys.stderr.write('Syntakticka chyba!\n');
      sys.exit(40);


  return ss;


def Qnewcheck(Qcc,Qd):
  for f in Qd:
    if Qcc == f:
      return 1;
  return 0;

def Fdcheck(Qc, F):
  for q in Qc:
    for f in F:
      if q == f:
        return 1;
  return 0;

#normalizace abecedy pro vystup
def print_abc_normalize(abeceda_seznam):
  Af_print = [];
  for A in abeceda_seznam:
    if A == '_':
      Af_print.append('\' \'');
    elif A == '\'\'':
      Af_print.append('\'\'\'\'');
    else:
      A = re.sub('(?P<i>.)','\'\g<i>\'',A);
      Af_print.append(A)
  return Af_print;  

#normalizce stavu pro vystup
def print_normalize(Fd):
  Fd_print = [];
  for Fdd in Fd:
    sFdd = Fdd[0];
    for iFdd in range(1,len(Fdd)):
      sFdd = sFdd + '_' + Fdd[iFdd];
    Fd_print.append(sFdd);
  return Fd_print;

#epsilon uzaver
def eps_uzaver(stavy_s, st, pravidla_s):
  Q = [];
  Q1 = [];
  Q.append(st);

  while Q1 != Q:
    Q1 = Q;
    for pravidlo in pravidla_s:
      q = re.sub('^(?P<i>.*) .*', '\g<i>', pravidlo);
      p = re.sub('[a-zA-Z][a-zA-Z0-9_]* ->(?P<i>.*)', '\g<i>', pravidlo);
      if Q1.count(q) > 0 and stavy_s.count(p) > 0 and Q.count(p) == 0:
        Q.append(p);
  return Q;


#Semanticka kontrola a algoritmy
def sem_alg(ss, **p):
  #PRAVIDLA
  # 1. - neprazdna vstupni abeceda
  # 2. - stavy a abeceda nejsou disjunktni
  # 3. - startujici stav neni v mnozine stavu
  # 4. - koncovy stav neni v mnozine stavu
  # ==> semanticka chyba - navrat hodnota 41
  # pravidla/stavy/symboly BUDOU mnozinach pouze jednou (ale uzivatel je tam muze dat vicekrat)

  if p['output'] != 0:
    vystup = open(p['output'], mode='w', newline='\n', encoding='utf-8');
  else:
    vystup = sys.stdout;

  #MNOZINA STAVU
  stavy = re.sub('^\({(?P<i1>.*)},{.*},{.*},[a-zA-Z]?[a-zA-Z0-9_]*,{.*}\)', '\g<i1>', ss);

  # mnozina stavu nesmi byt prazdna
  if not stavy:
    sys.stderr.write('Semanticka chyba! Prazdna mnozina stavu!\n');
    sys.exit(41);

  stavy_seznam = stavy.split(',');

  #odstraneni duplikatu
  for stav_stavy in stavy_seznam:
    while stavy_seznam.count(stav_stavy) > 1:
      stavy_seznam.remove(stav_stavy);


  #ABECEDA
  abeceda = re.sub('^\({.*},{(?P<i1>.*)},{.*},[a-zA-Z]?[a-zA-Z0-9_]*,{.*}\)', '\g<i1>', ss);
  abeceda = re.sub(',\',\'(?P<i>,?)', ',_coma\g<i>', abeceda);

  # 1. - neprazdna vstupni abeceda
  if not abeceda:
    sys.stderr.write('Semanticka chyba! Prazdna vstupni abeceda!\n');
    sys.exit(41);

  abeceda_s = abeceda.split(',');
  abeceda_seznam = [];

  for znak_abecedy in abeceda_s:
    znak_abecedy = re.sub('\'(?P<id1>[^\'])\'', '\g<id1>', znak_abecedy);
    if znak_abecedy == '_coma':
      znak_abecedy = ',';
    if znak_abecedy == '\'\'\'\'':
      znak_abecedy = '\'\'';
    if znak_abecedy == ' ':
      znak_abecedy = '_';
    abeceda_seznam.append(znak_abecedy);
    
  for znak_abecedy in abeceda_seznam:
    while abeceda_seznam.count(znak_abecedy) > 1:
      abeceda_seznam.remove(znak_abecedy);

  # 2. - stavy a abeceda nejsou disjunktni
  for znak_abecedy in abeceda_seznam:
    for stav in stavy_seznam:
      if znak_abecedy == stav:
        sys.stderr.write('Semanticka chyba! Abeceda obsahuje symbol se shodnym nazvem jako nektery stav\n');
        sys.exit(41);


  #PRAVIDLA
  pravidla = re.sub('^\({.*},{.*},{(?P<i1>.*)},[a-zA-Z]?[a-zA-Z0-9_]*,{.*}\)', '\g<i1>', ss);
  pravidla = re.sub('\',\'', '\'_coma\'', pravidla);
  pravidla_s = pravidla.split(',');

  pravidla_seznam = [];
  for pravidlo in pravidla_s:
    #regularni vyrazy pro snadnejsi zpracovani pravidel
    pravidlo = re.sub('\'[ ]\'', ' _', pravidlo);  #nahradi mezeru za zpracovatelne '_'
    pravidlo = re.sub('_coma', ',', pravidlo);  #MOZNA BUDE DELAT POTIZE !!!!!!!!!!!!!11
    pravidlo = re.sub('\'(?P<id1>.)\'', ' \g<id1>', pravidlo); #odstrani apostrofy a prida mezeru pred symbol
    pravidlo = re.sub('(?P<id1>[^ ])\'\'-', '\g<id1>-', pravidlo); #z pravidla s''->r udela s->r
    pravidlo = re.sub('^(?P<i>[^ ])-', '\g<i> -', pravidlo); #z s->r udela s ->r
    pravidla_seznam.append(pravidlo);

  #odstraneni duplikatu
  for pravidlo in pravidla_seznam:
    while pravidla_seznam.count(pravidlo) > 1:
      pravidla_seznam.remove(pravidlo);

  #STARTOVNI STAV
  start = re.sub('^\({.*},{.*},{.*},(?P<i1>[a-zA-Z]?[a-zA-Z0-9_]*),{.*}\)', '\g<i1>', ss);

  # 3. - startujici stav neni v mnozine stavu
  found = 0;
  if start:
    for stav_stavy in stavy_seznam:
      if stav_stavy == start:
        found = 1;
        break;
    if found == 0:
      sys.stderr.write('Semanticka chyba! Startovni stav neni v mnozine stavu!\n');
      sys.exit(41);

  #KONCOVE STAVY
  fin = re.sub('^\({.*},{.*},{.*},[a-zA-Z]?[a-zA-Z0-9_]*,{(?P<i1>.*)}\)', '\g<i1>', ss);
  fin_seznam = fin.split(',');

  #odstraneni duplikatu
  for stav_fin in fin_seznam:
    while fin_seznam.count(stav_fin) > 1:
      fin_seznam.remove(stav_fin);


  # 4. - koncovy stav neni v mnozine stavu
  found = 0;
  if fin:
    for stav_stavy in stavy_seznam:
      for stav_fin in fin_seznam:
        if stav_stavy == stav_fin:
          found += 1;
          break;
    if found != len(fin_seznam):
      sys.stderr.write('Semanticka chyba! Nektery(nebo vice) koncovy stav neni v mnozine stavu!\n');
      sys.exit(41);

  #odstraneni epsilon prechodu
  #vstup  M=(stavy_seznam, abeceda_seznam, pravidla_seznam, start, fin_seznam)
  #vystup Me=(stavy_seznam, abeceda_seznam, R,               start, F)
  if p['eps'] == 1 or p['det'] == 1:
    R = [];
    for s in stavy_seznam:
      eps_u = eps_uzaver(stavy_seznam, s, pravidla_seznam);
      for rule in pravidla_seznam:
        s2 = re.sub('^(?P<i>.*) .*', '\g<i>', rule);
        a = re.sub('.* (?P<i>.?)->.*', '\g<i>', rule);
        q = re.sub('.*>(?P<i>.*)', '\g<i>', rule);
        if abeceda_seznam.count(a) > 0 and eps_u.count(s2) > 0 and stavy_seznam.count(q) > 0:
          rule2 = re.sub('^[^ ]*', '', rule);
          rule2 = s + rule2;
          if R.count(rule2) == 0:
            R.append(rule2);

    F = [];
    found = 0;
    for s in stavy_seznam:
      eps_u = eps_uzaver(stavy_seznam, s, pravidla_seznam);
      for f in fin_seznam:
        for e in eps_u:
          if f == e:
            found = 1;
      if found == 1:
        F.append(s);
      found = 0;


  if p['eps'] == 1:
    stavy_seznam.sort();
    Qf_print = stavy_seznam;
    Af_print = print_abc_normalize(abeceda_seznam);
    Af_print.sort();
   
    Rd = [];
    for prav in R:
      prav = re.sub(' _-', '  -', prav);
      prav = re.sub('(?P<i1>[^ ]*) (?P<i2>.)->(?P<i3>.*)', '\g<i1> \'\g<i2>\' -> \g<i3>', prav);
      Rd.append(prav);
    
    Rd.sort();
    F.sort();
    Ff_print = F;

  if p['eps'] == 0 and p['det'] == 0:
    stavy_seznam.sort();
    Qf_print = stavy_seznam;
    Af_print = print_abc_normalize(abeceda_seznam);
    Af_print.sort();
   
    Rd = [];
    for prav in pravidla_seznam:
      prav = re.sub(' _-', '  -', prav);
      prav = re.sub('(?P<i1>[^ ]*) (?P<i2>.)->(?P<i3>.*)', '\g<i1> \'\g<i2>\' -> \g<i3>', prav);
      Rd.append(prav);
    
    Rd.sort();
    fin_seznam.sort();
    Ff_print = fin_seznam;

  #NORMALIZOVANY TISK1
  if p['eps'] == 1 or (p['eps'] == 0 and p['det'] == 0):
    print('(\n{', sep='', end='', file = vystup);
    for i in Qf_print:
      if i == Qf_print[len(Qf_print)-1]:
        print(i, sep='', end='', file = vystup);
      else:
        print(i,', ', sep='', end='', file = vystup);
    print('},\n', sep='', end='', file = vystup);
    print('{', sep='', end='', file = vystup);
    for i in Af_print:
      if i == Af_print[len(Af_print)-1]:
        print(i, sep='', end='', file = vystup);
      else:
        print(i,', ', sep='', end='', file = vystup);
    print('},\n', sep='', end='', file = vystup);
    print('{\n', sep='', end='', file = vystup);
    for i in Rd:
      print(i,',',sep='', file = vystup);
    print('},\n', sep='', end='', file = vystup);
    print(start,',',sep='', file = vystup);
    print('{', sep='', end='', file = vystup);
    for i in Ff_print:
      if i == Ff_print[len(Ff_print)-1]:
        print(i, sep='', end='', file = vystup);
      else:
        print(i,', ', sep='', end='', file = vystup);
    print('}', sep='', file = vystup);
    print(')', end='', file = vystup);
    sys.exit(0);

  #odstraneni nedeterminismu
  #vstup M=(stavy_seznam, abeceda_seznam, R, start, F)
  #vystp Md=(Qd, abeceda_seznam, Rd, start, Fd)
  if p['det'] == 1:
    sd = [];
    sd.append(start);
    Qnew = [];
    Qnew.append(sd);
    Rd = [];
    Qd = [];
    Qc = [];
    Qcc = [];
    Fd = [];
    ws = '';
    ls = '';
    i = 0;

    while Qnew:
      Qc = Qnew[i];
      Qnew.remove(Qc);
      if Qd.count(Qc) == 0:
        Qd.append(Qc);

      for a in abeceda_seznam:
        Qcc= [];
        for r in R:
          s = re.sub('^(?P<i>.*) .*', '\g<i>', r);
          r2 = re.sub('.* (?P<i>.?)->.*', '\g<i>', r);
          q = re.sub('.*>(?P<i>.*)', '\g<i>', r);
          if r2 == a and Qc.count(s) > 0 and Qcc.count(q) == 0:
            Qcc.append(q);
        if Qcc:
          Qc.sort();
          Qcc.sort();
          ws = Qc[0];
          ls = Qcc[0];
          for w in range(1,len(Qc)):
            ws = ws +'_'+Qc[w];
          for l in range(1,len(Qcc)):
            ls = ls +'_'+Qcc[l];
          if a == '_':
            a = ' ';
          new_rule= ws+' '+'\''+ a +'\''+' -> '+ls;
          ws = '';
          ls = '';
          if Rd.count(new_rule) == 0:
            Rd.append(new_rule);
        if Qcc and not Qnewcheck(Qcc,Qd):
          if Qnew.count(Qcc) == 0:
            Qnew.append(Qcc);
      if Fdcheck(Qc, F):
        if Fd.count(Qc) == 0:
          Fd.append(Qc);

  Rd.sort();
  Qf_print = print_normalize(Qd);
  Ff_print = print_normalize(Fd);
  Af_print = print_abc_normalize(abeceda_seznam);

  Af_print.sort();
  Qf_print.sort();
  Ff_print.sort();

  #TISK NORMALIZOVANY2
  print('(\n{', sep='', end='', file = vystup);
  for i in Qf_print:
    if i == Qf_print[len(Qf_print)-1]:
      print(i, sep='', end='', file = vystup);
    else:
      print(i,', ', sep='', end='', file = vystup);
  print('},\n', sep='', end='', file = vystup);
  print('{', sep='', end='', file = vystup);
  for i in Af_print:
    if i == Af_print[len(Af_print)-1]:
      print(i, sep='', end='', file = vystup);
    else:
      print(i,', ', sep='', end='', file = vystup);
  print('},\n', sep='', end='', file = vystup);
  print('{\n', sep='', end='', file = vystup);
  for i in Rd:
    print(i,',',sep='', file = vystup);
  print('},\n', sep='', end='', file = vystup);
  print(start,',',sep='', file = vystup);
  print('{', sep='', end='', file = vystup);
  for i in Ff_print:
    if i == Ff_print[len(Ff_print)-1]:
      print(i, sep='', end='', file = vystup);
    else:
      print(i,', ', sep='', end='', file = vystup);
  print('}', sep='', file = vystup);
  print(')', end='', file = vystup);


    
 
#XXXXXXXXXXXXXXXXXXX
#main
param = {'help':0, 'input':0, 'output':0, 'eps':0, 'det':0, 'case':0};
param = checkParam(**param);

#syntakticka analyza
ss = analyze_syntax(**param);

#semanticka analyza + algoritmy
sem_alg(ss, **param);


