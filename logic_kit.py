from sympy import logic
import re

alphabet = "abcdefghijklmnopqrstuvwxyz"

def simplify(expr):
  expr = format(expr)
  return logic.simplify_logic(expr)


def remove_spaces(expr):
  expr = expr.split(' ')
  return ''.join(expr)


def remove_dublicate_negs(expr):
  return expr.replace('~~', '')


def clarify_conjunction(expr):
  seq_found = re.search(r"(?:(?:~{0,}[A-z])|~{0,}\(.*\)){2}", expr)
  while seq_found:
    pat = seq_found.group(0)
    bracketCnt = 0
    first_operand = True
    a = ""
    b = ""
    for l in pat:
      if l == '(':
        bracketCnt += 1
        if len(a) > 0 and a != '~' and bracketCnt == 1:
          first_operand = False # a(...)
      elif l == ')':
        bracketCnt -= 1
        if bracketCnt == 0 and first_operand:
          first_operand = False # (...)b, (...)(...)
          a += l
          continue
      elif l == '~' and len(a) > 0 and bracketCnt == 0:
        first_operand = False # a~b, a~(...)
      elif l in alphabet and len(a) > 0 and bracketCnt == 0 and a != '~':
        first_operand = False # ab
      
      if (first_operand):
        a += l
      else:
        b += l
    expr = expr.replace(pat, f"{a} & {b}", 1)
    seq_found = re.search(r"(?:(?:~{0,}[A-z])|~{0,}\([^\(\)]*\)){2}", expr)
  return expr    


def replace_operator(operator, rep, expr):
  op_found = re.search(r"[^&|+>=!/]+\{}[^&|+>=!/]+".format(operator), expr)
  while op_found:
    pat = op_found.group(0)
    operands = pat.split(operator)
    expr = expr.replace(pat, f"{rep}({operands[0]}, {operands[1]})", 1)
    op_found = re.search(r"[^&|+>=!/]+\{}[^&|+>=!/]+".format(operator), expr)
  return expr


def format(expr):
  expr = remove_spaces(expr)
  expr = remove_dublicate_negs(expr)
  expr = clarify_conjunction(expr)

  # Important to save the operators order to keep it correct
  expr = replace_operator('=', "Equivalent", expr)
  expr = replace_operator('>', "Implies", expr)
  expr = replace_operator('!', "Nor", expr)
  expr = replace_operator('/', "Nand", expr)
  expr = replace_operator('+', "Xor", expr)

  return expr

def start():
  print(f"""
    +--------+------------+--------+------------+
    | Symbol | Operation  | Symbol | Operation  |   Note that:
    +--------+------------+--------+------------+   ab = a & b
    |   &    |    AND     |   !    |    NOR     |   (...)(...) = (...) & (...)
    +--------+------------+--------+------------+  
    |   |    |    OR      |   /    |    NAND    |
    +--------+------------+--------+------------+  
    |   +    |    XOR     |   >    |  IMPLIES   |
    +--------+------------+--------+------------+  
    |   =    | EQUIVALENT |   ~    |    NOT     |
    +--------+------------+--------+------------+                      
  """)
  
  expr = ""
  while (expr != "exit"):
    print("Input your logic expression:")
    expr = input(">>> ")
    if (expr == "exit"): break
    print(f"""
      {simplify(expr)}
    """)

if __name__ == "__main__":
  start()