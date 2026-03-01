import logic_kit
import unittest



class LogicKitTests(unittest.TestCase):
  def test_remove_spaces(self):
    case = 'a b'
    res = logic_kit.remove_spaces(case)
    self.assertEqual(res, "ab")

    case = 'a    b'
    res = logic_kit.remove_spaces(case)
    self.assertEqual(res, "ab")
    
    case = ' a  b'
    res = logic_kit.remove_spaces(case)
    self.assertEqual(res, "ab")
    
    case = ' ( ) ( ) '
    res = logic_kit.remove_spaces(case)
    self.assertEqual(res, "()()")


  def test_clarify_conjunction(self):
    case = 'ab'
    res = logic_kit.clarify_conjunction(case)
    self.assertEqual(res, "a&b")

    case = '~ab'
    res = logic_kit.clarify_conjunction(case)
    self.assertEqual(res, "~a&b")

    case = 'a~b'
    res = logic_kit.clarify_conjunction(case)
    self.assertEqual(res, "a&~b")

    case = '~a~b'
    res = logic_kit.clarify_conjunction(case)
    self.assertEqual(res, "~a&~b")

    case = '(a)b'
    res = logic_kit.clarify_conjunction(case)
    self.assertEqual(res, "(a)&b")

    case = 'a(b)'
    res = logic_kit.clarify_conjunction(case)
    self.assertEqual(res, "a&(b)")

    case = '~(a)b'
    res = logic_kit.clarify_conjunction(case)
    self.assertEqual(res, "~(a)&b")

    case = 'a~(b)'
    res = logic_kit.clarify_conjunction(case)
    self.assertEqual(res, "a&~(b)")

    case = 'abc'
    res = logic_kit.clarify_conjunction(case)
    self.assertEqual(res, "a&b&c") 

    # case = '(a)(b)(c)'
    # res = logic_kit.clarify_conjunction(case)
    # self.assertEqual(res, "(a) & (b) & (c)") # TODO: fix!


  def replace_operator_case(self, oper, rep):
    case = f'a{oper}b' 
    res = logic_kit.replace_operator(oper, rep, case)
    self.assertEqual(res, f"({rep}(a, b))")

    case = f'~a{oper}b'
    res = logic_kit.replace_operator(oper, rep, case)
    self.assertEqual(res, f"({rep}(~a, b))")
    
    case = f'a{oper}~b'
    res = logic_kit.replace_operator(oper, rep, case)
    self.assertEqual(res, f"({rep}(a, ~b))")

    case = f'~a{oper}~b'
    res = logic_kit.replace_operator(oper, rep, case)
    self.assertEqual(res, f"({rep}(~a, ~b))")

    case = f'~(a){oper}~(b)'
    res = logic_kit.replace_operator(oper, rep, case)
    self.assertEqual(res, f"({rep}(~(a), ~(b)))")
    
    case = f'(a){oper}~(b)'
    res = logic_kit.replace_operator(oper, rep, case)
    self.assertEqual(res, f"({rep}((a), ~(b)))")

    case = f'~(a){oper}(b)'
    res = logic_kit.replace_operator(oper, rep, case)
    self.assertEqual(res, f"({rep}(~(a), (b)))")

    case = f'(a){oper}(b)'
    res = logic_kit.replace_operator(oper, rep, case)
    self.assertEqual(res, f"({rep}((a), (b)))")

    case = f'a{oper}b{oper}c'
    res = logic_kit.replace_operator(oper, rep, case)
    self.assertEqual(res, f"({rep}(({rep}(a, b)), c))")

    case = f'~a{oper}~b{oper}~c'
    res = logic_kit.replace_operator(oper, rep, case)
    self.assertEqual(res, f"({rep}(({rep}(~a, ~b)), ~c))")

    case = f'(a){oper}(b){oper}(c)'
    res = logic_kit.replace_operator(oper, rep, case)
    self.assertEqual(res, f"({rep}(({rep}((a), (b))), (c)))")

    case = f'~(a){oper}~(b){oper}~(c)'
    res = logic_kit.replace_operator(oper, rep, case)
    self.assertEqual(res, f"({rep}(({rep}(~(a), ~(b))), ~(c)))")

    case = f'a{oper}(b{oper}c)'
    res = logic_kit.replace_operator(oper, rep, case)
    self.assertEqual(res, f"({rep}(a, (({rep}(b, c)))))")


  def test_replace_operators_all(self):
    self.replace_operator_case('>', "Implies")
    self.replace_operator_case('=', "Equivalent")
    self.replace_operator_case('!', "Nor")
    self.replace_operator_case('/', "Nand")
    self.replace_operator_case('+', "Xor")


  def test_remove_dublicate_negs(self):
    case = 'a' 
    res = logic_kit.remove_dublicate_negs(case)
    self.assertEqual(res, "a")

    case = '~a'
    res = logic_kit.remove_dublicate_negs(case)
    self.assertEqual(res, "~a")

    case = '~~a' 
    res = logic_kit.remove_dublicate_negs(case)
    self.assertEqual(res, "a")

    case = '~~~a' 
    res = logic_kit.remove_dublicate_negs(case)
    self.assertEqual(res, "~a")

    case = '~~a~~b' 
    res = logic_kit.remove_dublicate_negs(case)
    self.assertEqual(res, "ab")

    case = '~a~b' 
    res = logic_kit.remove_dublicate_negs(case)
    self.assertEqual(res, "~a~b")


  def test_priority_of_operators(self):
    case = 'a + b & c' 
    res = logic_kit.format_logic(case)
    self.assertEqual(res, "(Xor(a, b&c))")

  

if __name__ == "__main__":
  unittest.main()