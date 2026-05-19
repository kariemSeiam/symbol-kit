# Grammar (L6)

The composition DSL. Agents consume this to generate UIs from data.

## Overview

The grammar is a small expression language. Every expression evaluates to a string of glyphs.

```ebnf
expression  = literal | atom | invocation | repetition | sequence ;
literal     = '"' { char } '"' ;
atom        = '@' identifier ;                    (* @black-circle *)
invocation  = identifier '(' [ args ] ')' ;       (* PROGRESS(0.6, 10) *)
repetition  = expression '×' integer ;            (* @black-circle × 5 *)
sequence    = expression { '+' expression } ;
args        = expression { ',' expression } ;
identifier  = letter { letter | digit | '-' | '_' } ;
```

## Usage

```python
from symbolkit import render

render('PROGRESS(0.6, 10)')   # → '▰▰▰▰▰▰▱▱▱▱'
render('STATUS_DOT("live")')  # → '●'
render('SEVERITY(3, 5)')      # → '●●●○○'
```

## Reference

See [stdlib.md](grammar/stdlib.md) for all functions.
See [symbol-kit.ebnf](grammar/symbol-kit.ebnf) for the formal grammar.
