import unittest
from preprocessor import add_namespace
from preprocessor import traverse

class TestsAddNamespace(unittest.TestCase):
    def test_when_no_namespace_given_do_nothing(self):
        provided = {'NodeName': 'NodeValue'}
        expected = provided
        received = add_namespace(provided, ns=None)
        self.assertDictEqual(expected, received)

    def test_when_namespace_is_empty_do_nothing(self):
        provided = {'NodeName': 'NodeValue'}
        expected = provided
        received = add_namespace(provided, ns='')
        self.assertDictEqual(expected, received)

    def test_return_a_copy_not_original(self):
        namespace = 'lorem'
        provided = {'NodeName': 'NodeValue'}
        received_with_ns = add_namespace(provided, ns=namespace)
        self.assertIsNot(provided, received_with_ns)
        received_no_ns = add_namespace(provided, ns=None)
        self.assertIsNot(provided, received_no_ns)

    def test_when_no_prefix_exists_add_prefixes(self):
        namespace = 'lorem'
        provided = {'NodeName': 'NodeValue', 'SecondNodeName': 'SecondValue'}
        expected = {'lorem:NodeName': 'NodeValue', 'lorem:SecondNodeName': 'SecondValue'}
        received = add_namespace(provided, ns=namespace)
        self.assertDictEqual(expected, received)

    def test_when_prefix_exists_dont_replace(self):
        namespace = 'ipsum'
        provided = {'bare_node': 'NodeValue', 'dolor:prefixed_node': 'SecondValue'}
        expected = {'ipsum:bare_node': 'NodeValue', 'dolor:prefixed_node': 'SecondValue'}
        received = add_namespace(provided, ns=namespace)
        self.assertDictEqual(expected, received)


class TestsTraverseDict(unittest.TestCase):
    def test_when_no_nesting_return_value(self):
        provided = {'a': 'leaf_value'}
        received = traverse(provided, lambda d: d)
        self.assertEqual(provided['a'], received['a'])

    def test_when_values_are_nested_return_traversed_values(self):
        provided = {'a': {'b':'nested_leaf'}, 'c': 'leaf_value'}
        received = traverse(provided, lambda d: d)
        expected = {'a': {'b':'nested_leaf'}, 'c': 'leaf_value'}
        self.assertEqual(expected['a'], received['a'])

    def test_when_fn_provided_return_after_application(self):
        apply_me = lambda d: {k.upper(): v for k, v in d.items()}
        provided = {'a': {'b': 'nested_leaf'}, 'c': 'leaf_value'}
        received = traverse(provided, apply_me)
        expected = {'A': {'B': 'nested_leaf'}, 'C': 'leaf_value'}
        self.assertEqual(expected, received, 'Should return data with function applied')


if __name__ == '__main__':
    unittest.main()
