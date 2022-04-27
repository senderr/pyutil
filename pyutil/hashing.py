import hashlib
import logging
import pickle

logger = logging.getLogger(__name__)


def hash_item(i):
    """Hash a python object by pickling and then applying MD5 to resulting bytes"""
    if isinstance(i, dict):
        hash = hash_dict(i)
        print(f"Hashing item: {i} --> {hash}")
        return hash_dict(i)
    try:
        hash = hashlib.md5(pickle.dumps(i)).hexdigest()
    except TypeError:
        logger.warning(f"Unable to hash {i}, using hash of the object's class instead")
        hash = hashlib.md5(pickle.dumps(i.__class__)).hexdigest()
    except AttributeError:
        logger.warning(f"Unable to hash the objects class, using hash of class name instead")
        hash = hashlib.md5(pickle.dumps(i.__class__.__name__)).hexdigest()
    print(f"Hashing item: {i} --> {hash}")
    return hash


def hash_dict(d: dict) -> str:
    """Hash dict in order-agnostic manner by ordering keys and hashes of values"""

    if len(d) == 0:
        # Empty dict
        return "0"

    # order keys and hash result
    key_hash = hash_item(list(sorted(d.keys())))

    # hash_item will call this function recursively if dict is passed
    values = [hash_item(i) for i in d.values()]

    return hash_item([key_hash, sorted(values)])
