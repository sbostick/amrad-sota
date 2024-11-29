# Example calculator class to be used in the example functional test case
# from //coreinfra-org/app-base-python

class Calculator:
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero!")
        return a / b

    def add(self, a, b):
        return a + b
