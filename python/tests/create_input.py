import unittest
import numpy as np
import ase

from chemiscope import create_input

TEST_FRAMES = [ase.Atoms("CO2")]
TEST_FRAMES_DECORATED = [ase.Atoms("CO2"), ase.Atoms("NH3")]
for f in TEST_FRAMES_DECORATED:
    f.info["energy"] = 123.456
    f.arrays["beauty"] = range(len(f.numbers))
TEST_FRAMES_DECORATED[1].arrays["center_atoms_mask"] = [True, False, False, False]


class TestCreateInputMeta(unittest.TestCase):
    def test_meta(self):
        meta = {}
        data = create_input(frames=TEST_FRAMES, meta=meta)
        self.assertEqual(data["meta"]["name"], "<unknown>")
        self.assertEqual(len(data["meta"].keys()), 1)

        meta = {"name": ""}
        data = create_input(frames=TEST_FRAMES, meta=meta)
        self.assertEqual(data["meta"]["name"], "<unknown>")
        self.assertEqual(len(data["meta"].keys()), 1)

        meta = {"name": "foo"}
        data = create_input(frames=TEST_FRAMES, meta=meta)
        self.assertEqual(data["meta"]["name"], "foo")
        self.assertEqual(len(data["meta"].keys()), 1)

        meta = {"name": "foo", "description": "bar"}
        data = create_input(frames=TEST_FRAMES, meta=meta)
        self.assertEqual(data["meta"]["name"], "foo")
        self.assertEqual(data["meta"]["description"], "bar")
        self.assertEqual(len(data["meta"].keys()), 2)

        meta = {"name": "foo", "references": ["bar"]}
        data = create_input(frames=TEST_FRAMES, meta=meta)
        self.assertEqual(data["meta"]["name"], "foo")
        self.assertEqual(len(data["meta"]["references"]), 1)
        self.assertEqual(data["meta"]["references"][0], "bar")
        self.assertEqual(len(data["meta"].keys()), 2)

        meta = {"name": "foo", "authors": ["bar"]}
        data = create_input(frames=TEST_FRAMES, meta=meta)
        self.assertEqual(data["meta"]["name"], "foo")
        self.assertEqual(len(data["meta"]["authors"]), 1)
        self.assertEqual(data["meta"]["authors"][0], "bar")
        self.assertEqual(len(data["meta"].keys()), 2)

    def test_meta_unknown_keys_warning(self):
        meta = {"name": "foo", "what_is_this": "I don't know"}
        with self.assertWarns(UserWarning) as cm:
            data = create_input(frames=TEST_FRAMES, meta=meta)

        self.assertEqual(data["meta"]["name"], "foo")
        self.assertEqual(len(data["meta"].keys()), 1)

        self.assertEqual(
            cm.warning.args, ("ignoring unexpected metadata: what_is_this",)
        )

    def test_meta_conversions(self):
        meta = {"name": 33}
        data = create_input(frames=TEST_FRAMES, meta=meta)
        self.assertEqual(data["meta"]["name"], "33")
        self.assertEqual(len(data["meta"].keys()), 1)

        meta = {"name": ["foo", "bar"], "description": False}
        data = create_input(frames=TEST_FRAMES, meta=meta)
        self.assertEqual(data["meta"]["name"], "['foo', 'bar']")
        self.assertEqual(data["meta"]["description"], "False")
        self.assertEqual(len(data["meta"].keys()), 2)

        meta = {"name": "foo", "references": (3, False)}
        data = create_input(frames=TEST_FRAMES, meta=meta)
        self.assertEqual(data["meta"]["name"], "foo")
        self.assertEqual(len(data["meta"]["references"]), 2)
        self.assertEqual(data["meta"]["references"][0], "3")
        self.assertEqual(data["meta"]["references"][1], "False")
        self.assertEqual(len(data["meta"].keys()), 2)

        meta = {"name": "foo", "authors": (3, False)}
        data = create_input(frames=TEST_FRAMES, meta=meta)
        self.assertEqual(data["meta"]["name"], "foo")
        self.assertEqual(len(data["meta"]["authors"]), 2)
        self.assertEqual(data["meta"]["authors"][0], "3")
        self.assertEqual(data["meta"]["authors"][1], "False")
        self.assertEqual(len(data["meta"].keys()), 2)


class TestCreateInputProperties(unittest.TestCase):
    def test_properties(self):
        properties = {"name": {"target": "atom", "values": [2, 3, 4]}}
        data = create_input(frames=TEST_FRAMES, properties=properties)
        self.assertEqual(data["properties"]["name"]["target"], "atom")
        self.assertEqual(data["properties"]["name"]["values"], [2, 3, 4])
        self.assertEqual(len(data["properties"]["name"].keys()), 2)

        properties = {"name": {"target": "atom", "values": ["2", "3", "4"]}}
        data = create_input(frames=TEST_FRAMES, properties=properties)
        self.assertEqual(data["properties"]["name"]["target"], "atom")
        self.assertEqual(data["properties"]["name"]["values"], ["2", "3", "4"])
        self.assertEqual(len(data["properties"]["name"].keys()), 2)

        properties = {
            "name": {
                "target": "atom",
                "values": [2, 3, 4],
                "description": "foo",
            },
        }
        data = create_input(frames=TEST_FRAMES, properties=properties)
        self.assertEqual(data["properties"]["name"]["target"], "atom")
        self.assertEqual(data["properties"]["name"]["description"], "foo")
        self.assertEqual(data["properties"]["name"]["values"], [2, 3, 4])
        self.assertEqual(len(data["properties"]["name"].keys()), 3)

        properties = {
            "name": {
                "target": "atom",
                "values": [2, 3, 4],
                "units": "foo",
            },
        }
        data = create_input(frames=TEST_FRAMES, properties=properties)
        self.assertEqual(data["properties"]["name"]["target"], "atom")
        self.assertEqual(data["properties"]["name"]["units"], "foo")
        self.assertEqual(data["properties"]["name"]["values"], [2, 3, 4])
        self.assertEqual(len(data["properties"]["name"].keys()), 3)

    def test_ndarray_properties(self):
        # shape N
        properties = {"name": {"target": "atom", "values": np.array([2, 3, 4])}}
        data = create_input(frames=TEST_FRAMES, properties=properties)
        self.assertEqual(data["properties"]["name"]["target"], "atom")
        self.assertEqual(data["properties"]["name"]["values"], [2, 3, 4])
        self.assertEqual(len(data["properties"].keys()), 1)

        # shape N
        properties = {"name": {"target": "atom", "values": np.array(["2", "3", "4"])}}
        data = create_input(frames=TEST_FRAMES, properties=properties)
        self.assertEqual(data["properties"]["name"]["target"], "atom")
        self.assertEqual(data["properties"]["name"]["values"], ["2", "3", "4"])
        self.assertEqual(len(data["properties"].keys()), 1)

        # shape N x 1
        properties = {"name": {"target": "atom", "values": np.array([[2], [3], [4]])}}
        data = create_input(frames=TEST_FRAMES, properties=properties)
        self.assertEqual(data["properties"]["name"]["target"], "atom")
        self.assertEqual(data["properties"]["name"]["values"], [2, 3, 4])
        self.assertEqual(len(data["properties"].keys()), 1)

        # shape N x 3
        properties = {
            "name": {
                "target": "atom",
                "values": np.array([[1, 2, 4], [1, 2, 4], [1, 2, 4]]),
            }
        }
        data = create_input(frames=TEST_FRAMES, properties=properties)
        self.assertEqual(data["properties"]["name[1]"]["target"], "atom")
        self.assertEqual(data["properties"]["name[1]"]["values"], [1, 1, 1])
        self.assertEqual(data["properties"]["name[2]"]["target"], "atom")
        self.assertEqual(data["properties"]["name[2]"]["values"], [2, 2, 2])
        self.assertEqual(data["properties"]["name[3]"]["target"], "atom")
        self.assertEqual(data["properties"]["name[3]"]["values"], [4, 4, 4])
        self.assertEqual(len(data["properties"].keys()), 3)

    def test_invalid_name(self):
        properties = {"": {"target": "atom", "values": [2, 3, 4]}}
        with self.assertRaises(Exception) as cm:
            create_input(frames=TEST_FRAMES, properties=properties)
        self.assertEqual(
            str(cm.exception), "the name of a property can not be the empty string"
        )

        properties = {False: {"target": "atom", "values": [2, 3, 4]}}
        with self.assertRaises(Exception) as cm:
            create_input(frames=TEST_FRAMES, properties=properties)
        self.assertEqual(
            str(cm.exception),
            "the name of a property name must be a string, "
            + "got 'False' of type <class 'bool'>",
        )

    def test_invalid_target(self):
        properties = {"name": {"values": [2, 3, 4]}}
        with self.assertRaises(Exception) as cm:
            create_input(frames=TEST_FRAMES, properties=properties)
        self.assertEqual(str(cm.exception), "missing 'target' for the 'name' property")

        properties = {"name": {"target": "atoms", "values": [2, 3, 4]}}
        with self.assertRaises(Exception) as cm:
            create_input(frames=TEST_FRAMES, properties=properties)
        self.assertEqual(
            str(cm.exception),
            "the target must be 'atom' or 'structure' for the 'name' property",
        )

    def test_invalid_types_metadata(self):
        properties = {"name": {"target": "atom", "values": [2, 3, 4], "units": False}}
        data = create_input(frames=TEST_FRAMES, properties=properties)
        self.assertEqual(data["properties"]["name"]["units"], "False")

        properties = {
            "name": {"target": "atom", "values": [2, 3, 4], "description": False}
        }
        data = create_input(frames=TEST_FRAMES, properties=properties)
        self.assertEqual(data["properties"]["name"]["description"], "False")

    def test_property_unknown_keys_warning(self):
        properties = {"name": {"target": "atom", "values": [2, 3, 4], "what": False}}
        with self.assertWarns(UserWarning) as cm:
            create_input(frames=TEST_FRAMES, properties=properties)
        self.assertEqual(cm.warning.args, ("ignoring unexpected property key: what",))

    def test_invalid_values_types(self):
        properties = {"name": {"target": "atom", "values": 3}}
        with self.assertRaises(Exception) as cm:
            create_input(frames=TEST_FRAMES, properties=properties)
        self.assertEqual(
            str(cm.exception), "unknown type (<class 'int'>) for property 'name'"
        )

        properties = {"name": {"target": "atom", "values": {"test": "bad"}}}
        with self.assertRaises(Exception) as cm:
            create_input(frames=TEST_FRAMES, properties=properties)
        self.assertEqual(
            str(cm.exception), "unknown type (<class 'dict'>) for property 'name'"
        )

        properties = {"name": {"target": "atom", "values": [{}, {}, {}]}}
        with self.assertRaises(Exception) as cm:
            create_input(frames=TEST_FRAMES, properties=properties)
        self.assertEqual(
            str(cm.exception),
            "unsupported type in property 'name' values: should be string or number",
        )

    def test_wrong_number_of_values(self):
        properties = {"name": {"target": "atom", "values": [2, 3]}}
        centers = [(0, 0), (0, 1), (0, 2)]
        with self.assertRaises(Exception) as cm:
            create_input(frames=TEST_FRAMES, properties=properties, centers=centers)
        self.assertEqual(
            str(cm.exception),
            "wrong size for the property 'name' with target=='atom': "
            + "expected 3 values, got 2",
        )

        properties = {"name": {"target": "structure", "values": [2, 3, 5]}}
        with self.assertRaises(Exception) as cm:
            create_input(frames=TEST_FRAMES, properties=properties)
        self.assertEqual(
            str(cm.exception),
            "wrong size for the property 'name' with target=='structure': "
            + "expected 1 values, got 3",
        )


class TestCreateInputEnvironments(unittest.TestCase):
    def test_environment(self):
        centers_list = [
            (0, 0, 3.5),
            (1, 1, 2.5),
            (1, 3, 3),
            (3, 2, 4.0),
            (4, 2, 5),
            (4, 4, 5),
        ]
        data = create_input(frames=TEST_FRAMES + TEST_FRAMES, centers=centers_list)
        self.assertEqual(len(data["environments"]), 6)

        for i, env in enumerate(data["environments"]):
            self.assertEqual(env["structure"], centers_list[i][0])
            self.assertEqual(env["center"], centers_list[i][1])
            self.assertEqual(env["cutoff"], centers_list[i][2])

    def test_ase_frames(self):
        data = create_input(frames=TEST_FRAMES_DECORATED)
        self.assertEqual(len(data["environments"]), 4)
        self.assertEqual(len(data["properties"]["beauty"]["values"]), 4)


if __name__ == "__main__":
    unittest.main()
