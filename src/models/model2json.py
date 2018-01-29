import numpy as np
JSON_SAFE = [bool, int, float, str, unicode, type(None)]

def numpy_to_json(x, failsafe=np.nan):
    """
    Generic numpy types like int* float* have a .item() method and no shape
    Complex numpy types like array have a .tolist() method and a non-null shape

    Parameters
    ----------
    v: a Numpy object
        The object to be converted

    failsafe: a JSON safe object
        The object to be returned if conversion fails

    Returns
    -------
    A JSON safe object

    Usage
    -----
    if 'numpy' in str(type(x)):
        numpy_to_json(x, failsafe=np.nan)
    """
    try:
        if isinstance(x, np.generic):
            if hasattr(x, 'item') and not(bool(x.shape)):
                return x.item()
            else:
                print("Generic Numpy type, but has no .item() method")
                return failsafe
        elif ((hasattr(x, 'tolist')) and ('array' in str(type(x)).lower())):
            return x.tolist()
        else:
            print("Couldn't Convert {}".format(type(x)))
            return failsafe
    except:
        print("Conversion from NumPy failed. Please Check input")
        return x

def list_tuple_to_json(l):
    """
    Iterates over elements of a list or tuple
        Each JSON safe item is written as-is
        Dict items invoke dict_to_json()
        List/Tuple items invoke list_tuple_to_json recursively
        sklearn items are converted to dicts and passed to dict_to_json()
        Numpy items are passed to numpy_to_json
    """
    c = [None for x in l]
    for idx, item in enumerate(l):
        if type(item) in JSON_SAFE:
            c[idx] = item
        elif hasattr(v, "__call__"):
            d[k] = joblib.dump(v, 'func-{}'.format(k))             
        elif isinstance(item, dict):
            c[idx] = dict_to_json(item)
        elif isinstance(item, list) or isinstance(item, tuple):
            c[idx] = list_tuple_to_json(item)
        elif 'numpy' in str(type(item)):
            c[idx] = numpy_to_json(item)
        elif hasattr(item, '__dict__'):
            c[idx] = dict_to_json(item.__dict__)
        else:
            c[idx] = type(item)
    return c



def dict_to_json(d):
    """
    """
    c = {}
    for k in d.keys():
        v = d.get(k)
        if type(v) in JSON_SAFE:
            c[k] = v
        elif hasattr(v, "__call__"):
            d[k] = joblib.dump(v, 'func-{}'.format(k)) 
        elif isinstance(v, dict):
            c[k] = dict_to_json(v)
        elif isinstance(v, list) or isinstance(v, tuple):
            c[k] = list_tuple_to_json(v)
        elif 'numpy' in str(type(v)):
            c[k] = numpy_to_json(v)
        elif 'sklearn' in str(type(v)):
            if hasattr(v, '__dict__'):
                c[k] = dict_to_json(v.__dict__)
            else:
                c[k] = type(v)
        else:
            c[k] = type(v)
    return c



def estimator_to_json(est):
    """
    """
    d = {}
    e = est.__dict__
    for k in e.keys():
        v = e.get(k)
        if type(v) in JSON_SAFE:
            d[k] = v
        elif hasattr(v, "__call__"):
            d[k] = joblib.dump(v, 'func-{}'.format(k)) 
        elif isinstance(v, dict):
            d[k] = dict_to_json(v)
        elif isinstance(v, list) or isinstance(v, tuple):
            d[k] = list_tuple_to_json(v)
        elif 'numpy' in str(type(v)):
            d[k] = numpy_to_json(v)
        elif hasattr(v, '__dict__'):
            d[k] = dict_to_json(v.__dict__)
        else:
            d[k] = type(v)
    return d
