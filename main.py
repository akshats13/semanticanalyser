import tokenize


class SemanticAnalyzer:
    def __init__(self):
        self.variables = {}

    def analyze(self, code):
        lines = code.split("\n")
        for line in lines:
            line = line.strip()
            if line and not line.startswith("#"):
                tokens = line.split("=")
                if len(tokens) == 2:
                    variable = tokens[0].strip()
                    expression = tokens[1].strip()
                    try:
                        value = self.evaluate_expression(expression)
                        self.variables[variable] = value
                    except ValueError as e:
                        print(f"Error: {e}")
                else:
                    print(f"Error: Invalid expression: {line}")

    def evaluate_expression(self, expression):
        tokens = self.tokenize_expression(expression)
        result = self.evaluate_tokens(tokens)
        return result

    def tokenize_expression(self, expression):
        tokens = []
        current_token = ""
        for char in expression:
            if char.isspace():
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
            else:
                current_token += char
        if current_token:
            tokens.append(current_token)
        return tokens

    def evaluate_tokens(self, tokens):
        operators = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y,
            '%': lambda x, y: x % y
        }

        stack = []
        for token in tokens:
            if token.isdigit():
                stack.append(int(token))
            elif token.isalpha():
                if token not in self.variables:
                    raise ValueError(f"Undefined variable: {token}")
                stack.append(self.variables[token])
            elif token in operators:
                if len(stack) < 2:
                    raise ValueError("Invalid expression")
                operand2 = stack.pop()
                operand1 = stack.pop()
                operation = operators[token]
                result = operation(operand1, operand2)
                stack.append(result)
            elif token == '(':
                stack.append('(')
            elif token == ')':
                expression = []
                while stack and stack[-1] != '(':
                    expression.insert(0, stack.pop())
                if not stack or stack[-1] != '(':
                    raise ValueError("Invalid expression")
                stack.pop()  # Remove '('
                operand = self.evaluate_tokens(expression)
                stack.append(operand)
            else:
                raise ValueError("Invalid token: " + token)

        if len(stack) != 1:
            raise ValueError("Invalid expression")

        return stack[0]

    def get_analysis_result(self):
        return self.variables


def main():
    # Initialize the semantic analyzer
    semantic_analyzer = SemanticAnalyzer()

    # Read and process the code
    code = '''
    # Sample code
    x = 10
    y = 5
    z = x + y
    result = (x + y) / z
    '''

    # Run the semantic analysis
    semantic_analyzer.analyze(code)

    # Get the analysis result or perform any further actions
    analysis_result = semantic_analyzer.get_analysis_result()

    # Print the output or perform any desired actions
    for variable, value in analysis_result.items():
        print(f"{variable} = {value}")


if __name__ == '__main__':
    main()
