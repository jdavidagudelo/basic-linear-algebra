from unittest.case import TestCase
from functions import Variable, Constant, Product, Sum, Power
import math


class MatrixTest(TestCase):
    evaluate_values = [1, 2, 3, 4, 5, 6, 7, 8,
                       1.9, 2.9, 29992.209992, 100, -11, -12, 0,
                       -12.092, math.pi, math.e]
    constant_values = [1, 2, 3, 4, 5, 6, 7, 8,
                       1.9, 2.9, 29992.209992, 100, -11, -12, 0,
                       -12.092, math.pi, math.e]
    evaluate_powers = [1, 2, 3, 4, 5, 6, 7, 8,
                       1.9, 2.9, 11.209992, 10, -11, -12, 0,
                       -12.092, math.pi, math.e]

    variable_names = ['x', 'y', 'z', 'myVar', 'my_var']

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_evaluate_power_function(self):
        for constant_value in self.constant_values:
            for exponent in self.evaluate_powers:
                power = Power(Constant(constant_value), exponent)
                if constant_value > 0:
                    for value in self.evaluate_values:
                        self.assertAlmostEqual(power.evaluate(value), constant_value ** exponent)
                elif exponent % 1 == 0:
                    for value in self.evaluate_values:
                        if exponent > 0 and value != 0:
                            self.assertEqual(power.evaluate(value), constant_value ** exponent)
            for second_constant_value in self.constant_values:
                sum_result = Sum([Constant(constant_value), Constant(second_constant_value)])
                for exponent in self.evaluate_powers:
                    power = Power(sum_result, exponent)
                    if constant_value + second_constant_value > 0:
                        for value in self.evaluate_values:
                            self.assertAlmostEqual(power.evaluate(value),
                                                   (constant_value + second_constant_value) ** exponent)
                    elif exponent % 1 == 0:
                        for value in self.evaluate_values:
                            if exponent > 0 and value != 0:
                                self.assertAlmostEqual(power.evaluate(value),
                                                       (constant_value + second_constant_value) ** exponent)
        for constant_value in self.constant_values:
            for variable_name in self.variable_names:
                for second_constant_value in self.constant_values:
                    sum_result = Sum([Constant(constant_value), Variable(variable_name),
                                      Constant(second_constant_value)])
                    for exponent in self.evaluate_powers:
                        power = Power(sum_result, exponent)
                        for value in self.evaluate_values:
                            if constant_value * value * second_constant_value > 0:
                                self.assertAlmostEqual(power.evaluate(value),
                                                       (constant_value + value + second_constant_value) ** exponent)
                            elif exponent % 1 == 0:
                                if exponent > 0 and value != 0:
                                    self.assertAlmostEqual(power.evaluate(value),
                                                           (constant_value + value + second_constant_value) ** exponent)

    def test_print_power_function(self):
        for constant_value in self.constant_values:
            for exponent in self.evaluate_powers:
                power = Power(Constant(constant_value), exponent)
                self.assertEqual('{0}'.format(power), '({0})^{1}'.format(constant_value, exponent))
            for second_constant_value in self.constant_values:
                sum_result = Sum([Constant(constant_value), Constant(second_constant_value)])
                for exponent in self.evaluate_powers:
                    power = Power(sum_result, exponent)
                    self.assertEqual('{0}'.format(power), '({0}+{1})^{2}'.format(constant_value, second_constant_value,
                                                                           exponent))
        for constant_value in self.constant_values:
            for variable_name in self.variable_names:
                for second_constant_value in self.constant_values:
                    sum_result = Sum([Constant(constant_value), Variable(variable_name),
                                      Constant(second_constant_value)])
                    for exponent in self.evaluate_powers:
                        power = Power(sum_result, exponent)
                        self.assertEqual('{0}'.format(power),
                                         '({0}+{1}+{2})^{3}'.format(constant_value,
                                                                    variable_name,
                                                                    second_constant_value,
                                                                    exponent))

    def test_simplify_power_function(self):
        for constant_value in self.constant_values:
            for exponent in self.evaluate_powers:
                power = Power(Constant(constant_value), exponent)
                if exponent == 1:
                    self.assertEqual(power.simplify(), Constant(constant_value))
                elif exponent == 0:
                    self.assertEqual(power.simplify(), Constant.one())
                else:
                    self.assertEqual(power.simplify(), power)
            for second_constant_value in self.constant_values:
                sum_result = Sum([Constant(constant_value), Constant(second_constant_value)])
                for exponent in self.evaluate_powers:
                    power = Power(sum_result, exponent)
                    if exponent == 1:
                        self.assertEqual(power.simplify(), sum_result)
                    elif exponent == 0:
                        self.assertEqual(power.simplify(), Constant.one())
                    else:
                        self.assertEqual(power.simplify(), power)
        for constant_value in self.constant_values:
            for variable_name in self.variable_names:
                for second_constant_value in self.constant_values:
                    sum_result = Sum([Constant(constant_value), Variable(variable_name),
                                      Constant(second_constant_value)])
                    for exponent in self.evaluate_powers:
                        power = Power(sum_result, exponent)
                        if exponent == 1:
                            self.assertEqual(power.simplify(), sum_result)
                        elif exponent == 0:
                            self.assertEqual(power.simplify(), Constant.one())
                        else:
                            self.assertEqual(power.simplify(), power)

    def test_derivative(self):
        pass