"""
CODE TEMPLATES
Generates improved code templates for each optimization pattern
"""

class CodeTemplates:
    """Provides code templates for standard optimizations"""
    
    @staticmethod
    def nested_loops_template(context: dict) -> str:
        """Generate code to replace nested loops with dictionary lookup"""
        return """
# BEFORE: Nested loops O(n²)
# for item1 in list1:
#     for item2 in list2:
#         if item1.id == item2.id:
#             process(item1, item2)

# AFTER: Dictionary lookup O(n)
lookup = {item.id: item for item in list2}
for item1 in list1:
    if item1.id in lookup:
        process(item1, lookup[item1.id])
"""
    
    @staticmethod
    def query_batch_template(context: dict) -> str:
        """Generate code for batched queries"""
        return """
# BEFORE: N queries in loop
# for user_id in user_ids:
#     user = db.query(f"SELECT * FROM users WHERE id={user_id}")
#     process(user)

# AFTER: Single batch query
users = db.query(f"SELECT * FROM users WHERE id IN ({','.join(user_ids)})")
for user in users:
    process(user)
"""
    
    @staticmethod
    def string_concat_template(context: dict) -> str:
        """Generate code for efficient string building"""
        return """
# BEFORE: O(n²) string concatenation in loop
# result = ""
# for item in items:
#     result += str(item) + ", "

# AFTER: O(n) with list + join
result = ", ".join(str(item) for item in items)
"""
    
    @staticmethod
    def generator_template(context: dict) -> str:
        """Generate code for lazy evaluation with generators"""
        return """
# BEFORE: Creates full list in memory
# def process_items(items):
#     results = [expensive_transform(item) for item in items]
#     return results

# AFTER: Lazy generator
def process_items(items):
    return (expensive_transform(item) for item in items)
"""
    
    @staticmethod
    def caching_template(context: dict) -> str:
        """Generate code with function caching"""
        return """
# BEFORE: Repeated expensive calculation
# def analyze():
#     result1 = expensive_calc(data)
#     result2 = expensive_calc(data)
#     return result1 + result2

# AFTER: With caching
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_calc(data):
    # implementation
    pass

def analyze():
    result1 = expensive_calc(data)
    result2 = expensive_calc(data)  # Uses cache
    return result1 + result2
"""
