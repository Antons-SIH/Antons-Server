def HttpResponse(success, data, error):
    
    return ({ 'success': success, 'data': data, 'error': error })

def HttpApiResponse(data):
    return HttpResponse(True, data, None)

def HttpErrorResponse(error):
    return HttpResponse(False, None, error)