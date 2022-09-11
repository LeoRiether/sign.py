from functools import wraps

def once(f):
    """
        Used as a decorator to make a function run only once
        Ex:
            @once
            def build_sbox():
                print("I shall build this sbox")
                # *code that builds the sbox*
                return

            # This should only print "I shall build this sbox" once!
            build_sbox()
            build_sbox()
            build_sbox()
            build_sbox()
    """
    ran = False
    ret = None

    @wraps(f)
    def f_once(*args, **kwargs):
        nonlocal ran, ret
        if not ran:
            ran = True
            ret = f(*args, **kwargs)
        return ret 

    return f_once

