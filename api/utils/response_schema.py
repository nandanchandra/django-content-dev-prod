def response_schema(message='response_schema',errors=[]):
    
    if errors==[]:
    
        response_schema = {
            'message': message
            }
    
    elif errors is not None:
    
        response_schema = {
            'errors' :errors ,
            'message': message
        }
        
    return response_schema