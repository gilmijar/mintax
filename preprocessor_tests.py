import unittest
from preprocessor import add_namespace, namespace_traverse, get_namespace


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
        received = namespace_traverse(provided, fn=lambda d, _: d)
        self.assertEqual(provided['a'], received['a'])

    def test_when_values_are_nested_return_traversed_values(self):
        provided = {'a': {'b':'nested_leaf'}, 'c': 'leaf_value'}
        received = namespace_traverse(provided, fn=lambda d, _: d)
        expected = {'a': {'b':'nested_leaf'}, 'c': 'leaf_value'}
        self.assertEqual(expected['a'], received['a'])

    def test_when_fn_provided_return_after_application(self):
        apply_me = lambda d, _: {k.upper(): v for k, v in d.items()}
        provided = {'a': {'b': 'nested_leaf'}, 'c': 'leaf_value'}
        received = namespace_traverse(provided, fn=apply_me)
        expected = {'A': {'B': 'nested_leaf'}, 'C': 'leaf_value'}
        self.assertEqual(expected, received, 'Should return data with function applied')


class TestsExtractNamespace(unittest.TestCase):
    def test_when_namespace_not_given_return_empty_str(self):
        received = get_namespace('dolor')
        self.assertEqual('', received)
        received = get_namespace(':dolor')
        self.assertEqual('', received)

    def test_when_namespace_is_given_return_namespace(self):
        received = get_namespace('amet:dolor')
        self.assertEqual('amet', received)


class TestIntegrations(unittest.TestCase):
    def setUp(self):
        self.provided = {
            'test_ns:top_node_1': {
                'sub_1_node_1': {
                    'sub_2_node_1': 'Lorem',
                    'fixed_ns_l2:sub_2_node_2': 'Ipsum'
                },
                'fixed_ns_l1:sub_1_node_2': {
                    'sub_2_node_3': 'Dolor',
                    'sub_2_node_4': 'Sit Amet'
                },
                'sub_1_node_3': 'Consectetur'
            }
        }

        self.expected = {
            'test_ns:top_node_1': {
                'test_ns:sub_1_node_1': {
                    'test_ns:sub_2_node_1': 'Lorem',
                    'fixed_ns_l2:sub_2_node_2': 'Ipsum'
                },
                'fixed_ns_l1:sub_1_node_2': {
                    'fixed_ns_l1:sub_2_node_3': 'Dolor',
                    'fixed_ns_l1:sub_2_node_4': 'Sit Amet'
                },
                'test_ns:sub_1_node_3': 'Consectetur'
            }
        }

    def test_happy_path(self):
        received = namespace_traverse(self.provided, fn=add_namespace)
        self.assertDictEqual(received, self.expected)

if __name__ == '__main__':
    unittest.main()
