from pyutil.hashing import hash_item


def test_different_lists():
    item_a = [1, 2, 3]
    item_b = [1, 3, 2]

    assert type(hash_item(item_a)) == str
    assert hash_item(item_a) != hash_item(item_b)

def test_different_dict_ordering():
    item_a = {
        "a": {
            "b": {
                "c": 3,
                "h": 4,
                "i": 5
            },
            "f": 2,
            "k": 5,
        },
        "g": 2,
    }
    
    # same contents, different order
    item_b = {
        "g": 2,
        "a": {
            "b": {
                "h": 4,
                "c": 3,
                "i": 5
            },
            "k": 5,
            "f": 2,
        },
    }
    
    assert hash_item(item_a) == hash_item(item_b)
    
def test_custom_classes():
    class DummyClass:
        a = 1
    
    assert hash_item(DummyClass()) == hash_item(DummyClass())
