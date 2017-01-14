class OperationNotSupportedException(Exception):
    pass


class Function(object):
    def evaluate(self, value):
        raise OperationNotSupportedException('Operation not implemented yet.')

    def simplify(self):
        raise OperationNotSupportedException('Operation not implemented yet.')


class Variable(Function):
    name = None

    def __init__(self, name):
        self.name = name

    def evaluate(self, value):
        return value

    def derivative(self):
        return Constant.one()

    def simplify(self):
        return self

    def __eq__(self, other):
        if not isinstance(other, Variable):
            return False
        return self.name == other.name

    def __str__(self):
        return '{0}'.format(self.name)


class Constant(Function):
    constant = 0.0

    def __init__(self, constant):
        self.constant = constant

    @staticmethod
    def zero():
        return Constant(0.0)

    @staticmethod
    def one():
        return Constant(1.0)

    def evaluate(self, value):
        return self.constant

    def simplify(self):
        return self

    def derivative(self):
        return Constant.zero()

    def __eq__(self, other):
        if not isinstance(other, Constant):
            return False
        return self.constant == other.constant

    def __str__(self):
        return '{0}'.format(self.constant)


class Sum(Function):
    summands = []

    def __init__(self, summands):
        self.summands = summands

    def evaluate(self, value):
        result = 0.0
        for function in self.summands:
            result += function.evaluate(value)
        return result

    def simplify(self):
        result_summands = []
        constant_value = None
        variables_count = {}
        simplified_summands = []
        for function in self.summands:
            simplified_summands.append(function.simplify())
        for function in simplified_summands:
            if isinstance(function, Constant):
                if constant_value is None:
                    constant_value = 0.0
                constant_value += function.constant
            elif isinstance(function, Variable):
                if variables_count.get(function.name, None) is None:
                    variables_count[function.name] = 0
                variables_count[function.name] += 1
            else:
                result_summands.append(function.simplify())
        if constant_value is not None:
            result_summands = [Constant(constant_value)] + result_summands
        if len(variables_count) > 0:
            functions_variables = []
            for variable_name in variables_count:
                product = Product([Constant(variables_count[variable_name]),
                                   Variable(variable_name)]).simplify()
                if product != Constant.zero():
                    functions_variables.append(product)
            result_summands = result_summands + functions_variables
        if constant_value == 0.0 and len(result_summands) > 1:
            result_summands = result_summands[1:]
        if len(result_summands) == 1:
            return result_summands[0]
        return Sum(result_summands)

    def derivative(self):
        result_summands = []
        for function in self.summands:
            result_summands.append(function.derivative())
        return Sum(result_summands).simplify()

    def __eq__(self, other):
        if not isinstance(other, Sum):
            return False
        return self.summands == other.summands

    def __str__(self):
        result = ''
        for function in self.summands:
            result = '{0}+{1}'.format(result, function) if result != '' else '{0}'.format(function)
        return result


class Product(Function):
    multiplicands = []

    def __init__(self, multiplicands):
        self.multiplicands = multiplicands

    def evaluate(self, value):
        result = 1.0
        for function in self.multiplicands:
            result *= function.evaluate(value)
        return result

    def simplify(self):
        constant_value = None
        result_multiplicands = []
        variables_count = {}
        simplified_multiplicands = []
        for function in self.multiplicands:
            simplified_multiplicands.append(function.simplify())
        for function in simplified_multiplicands:
            if isinstance(function, Constant):
                if constant_value is None:
                    constant_value = 1
                constant_value *= function.constant
            elif isinstance(function, Variable):
                if variables_count.get(function.name, None) is None:
                    variables_count[function.name] = 0
                variables_count[function.name] += 1
            else:
                result_multiplicands.append(function.simplify())
        if constant_value is not None and constant_value != 0.0:
            result_multiplicands = [Constant(constant_value)] + result_multiplicands
        if len(variables_count) > 0:
            functions_variables = []
            for variable_name in variables_count:
                power = Power(Variable(variable_name), variables_count[variable_name]).simplify()
                if power != Constant.one():
                    functions_variables.append(power)
            result_multiplicands = result_multiplicands + functions_variables
        if constant_value == 0.0:
            result_multiplicands = [Constant.zero()]
        if constant_value == 1.0 and len(result_multiplicands) > 1:
            result_multiplicands = result_multiplicands[1:]
        if len(result_multiplicands) == 1:
            return result_multiplicands[0]
        return Product(result_multiplicands)

    def derivative(self):
        simplified = self.simplify()
        if not isinstance(simplified, Product):
            return simplified.derivative()
        current_derivative = Sum(
            [Product([simplified.multiplicands[0].derivative(), simplified.multiplicands[1]]),
             Product([simplified.multiplicands[0], simplified.multiplicands[1].derivative()])
             ]).simplify()
        current_product = Product(simplified.multiplicands[:2]).simplify()
        for i in range(2, len(simplified.multiplicands)):
            current_derivative = Sum(
                [Product([current_derivative, simplified.multiplicands[i]]),
                 Product([current_product, simplified.multiplicands[i].derivative()])
                 ]).simplify()
            current_product = Product(simplified.multiplicands[:(i + 1)]).simplify()
        return current_derivative.simplify()

    def __eq__(self, other):
        if not isinstance(other, Product):
            return False
        return self.multiplicands == other.multiplicands

    def __str__(self):
        result = ''
        for function in self.multiplicands:
            result = '{0}*{1}'.format(result, function) if result != '' else '{0}'.format(function)
        return result


class Power(Function):
    power = None
    function = None

    def __init__(self, function, power):
        self.power = power
        self.function = function

    def evaluate(self, value):
        return self.function.evaluate(value) ** self.power

    def simplify(self):
        if self.power == 0:
            return Constant.one()
        if self.power == 1:
            return self.function
        return Power(self.function, self.power)

    def derivative(self):
        simplified = self.simplify()
        if not isinstance(simplified, Power):
            return simplified.derivative()
        return Product([Constant(self.power),
                        self.function.derivative(), Power(self.function, self.power - 1)]).simplify()

    def __eq__(self, other):
        if not isinstance(other, Power):
            return False
        return self.function == other.function and self.power == other.power

    def __str__(self):
        return '({0})^{1}'.format(self.function, self.power)
