""" this context processor, adds the build info to the project. """

def release(request):
    version = "0.1"
    return { "release" : version }

def revision(request):
    hash = "e3624"
    return { "git_revision" : hash }
    
