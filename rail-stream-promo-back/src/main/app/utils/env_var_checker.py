from typing import Optional

#=============================
# Simple validation of environment variables; 
# Eliminates empty variables, undefined variables
#=============================
def env_var_check(*env_vars: Optional[str]) -> bool:

    errors: list[str] = []
    var_ptr: int = 1
    
    for var in env_vars:

        if var is None:
            errors.append(f"ENV variable number {var_ptr} is not set (None)")

        elif not var.strip():
            errors.append(f"ENV variable number {var_ptr} is empty (_)")
        var_ptr += 1
    
    if errors:
        print("env variable configuration errors:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    return True
