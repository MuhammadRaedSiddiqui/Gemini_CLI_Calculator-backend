from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import ast
import operator
import math
import re

router = APIRouter(prefix="/arithmetic", tags=["Arithmetic"])

class EvaluateRequest(BaseModel):
    expression: str = Field(..., description="Arithmetic expression to evaluate")

class EvaluateResponse(BaseModel):
    result: float
    expression: str

# Safe evaluation using AST
class SafeEvaluator:
    """Safe arithmetic expression evaluator using AST."""
    
    ALLOWED_OPS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
        ast.Mod: operator.mod,
    }
    
    ALLOWED_FUNCTIONS = {
        'sqrt': math.sqrt,
        'abs': abs,
        'pow': pow,
    }
    
    @classmethod
    def evaluate(cls, expr: str) -> float:
        """Safely evaluate an arithmetic expression."""
        try:
            node = ast.parse(expr, mode='eval')
            return cls._eval_node(node.body)
        except Exception as e:
            raise ValueError(f"Invalid expression: {str(e)}")
    
    @classmethod
    def _eval_node(cls, node):
        """Recursively evaluate AST nodes."""
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Num):  # For older Python versions
            return node.n
        elif isinstance(node, ast.BinOp):
            op = cls.ALLOWED_OPS.get(type(node.op))
            if op is None:
                raise ValueError(f"Operator {type(node.op).__name__} not allowed")
            left = cls._eval_node(node.left)
            right = cls._eval_node(node.right)
            return op(left, right)
        elif isinstance(node, ast.UnaryOp):
            op = cls.ALLOWED_OPS.get(type(node.op))
            if op is None:
                raise ValueError(f"Operator {type(node.op).__name__} not allowed")
            operand = cls._eval_node(node.operand)
            return op(operand)
        elif isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Invalid function call")
            func_name = node.func.id
            if func_name not in cls.ALLOWED_FUNCTIONS:
                raise ValueError(f"Function {func_name} not allowed")
            func = cls.ALLOWED_FUNCTIONS[func_name]
            args = [cls._eval_node(arg) for arg in node.args]
            return func(*args)
        else:
            raise ValueError(f"Node type {type(node).__name__} not allowed")


def evaluate_arithmetic_expression(expression: str) -> float:
    """
    Safely evaluates a basic arithmetic expression.
    
    Args:
        expression: A string containing arithmetic operations (+, -, *, /, parentheses)
        
    Returns:
        The result of the evaluated expression
        
    Raises:
        ValueError: If the expression is invalid or contains unsupported operations
    """
    if not expression or not expression.strip():
        raise ValueError("Expression cannot be empty")
    
    # Remove whitespace
    expression = expression.strip()
    
    # Validate characters (only allow numbers, operators, parentheses, decimal points)
    if not re.match(r'^[\d\+\-\*/\(\)\.\s]+$', expression):
        raise ValueError("Expression contains invalid characters")
    
    try:
        # Parse the expression into an AST
        node = ast.parse(expression, mode='eval')
        
        # Evaluate using a safe evaluator
        result = SafeEvaluator._eval_node(node.body)
        
        return float(result)
    except SyntaxError:
        raise ValueError("Invalid syntax in expression")
    except ZeroDivisionError:
        raise ValueError("Division by zero")
    except Exception as e:
        raise ValueError(f"Failed to evaluate expression: {str(e)}")


@router.post("/evaluate", response_model=EvaluateResponse)
async def evaluate(request: EvaluateRequest):
    """
    Safely evaluate an arithmetic expression.
    
    Supports:
    - Basic operators: +, -, *, /, %, **
    - Parentheses for grouping
    - Functions: sqrt, abs, pow
    
    Example: "2 + 3 * 4" returns 14
    """
    try:
        # Normalize expression
        expr = request.expression.strip()
        
        # Validate not empty
        if not expr:
            raise HTTPException(status_code=400, detail="Expression cannot be empty")
        
        # Safely evaluate
        result = SafeEvaluator.evaluate(expr)
        
        # Check for invalid results
        if math.isnan(result) or math.isinf(result):
            raise HTTPException(status_code=400, detail="Result is not a valid number")
        
        return EvaluateResponse(result=result, expression=request.expression)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ZeroDivisionError:
        raise HTTPException(status_code=400, detail="Division by zero")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")