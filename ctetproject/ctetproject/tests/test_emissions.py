from django.test import TestCase
from ctetproject.emissions_algo import (
    get_location,
    calculate_distance,
    calculate_single_trip_emissions,
    calculate_emissions_for_multiple_routes,
)
import logging
from unittest.mock import patch

logging.basicConfig(level=logging.INFO)


class EmissionsAlgorithmTests(TestCase):

    def setUp(self):
        super().setUp()
        print(f"--" * 40)
        test_id = self.id()
        logging.info(f"Running test: {test_id}")

    def test_distance_calculation(self):
        # test distance calculation logic, check for a float on return for valid city names
        origin = "New York"
        destination = "Los Angeles"
        distance = calculate_distance(origin, destination)
        self.assertTrue(isinstance(distance, float))

    def test_single_trip_emissions(self):
        # test emission calculation for a single trip over a known set distance
        distance = 1000  # Example distance
        emissions = calculate_single_trip_emissions(distance)
        self.assertTrue(isinstance(emissions, float))

    def test_multiple_route_emissions(self):
        # test emissions calculation for multiple routes attendee multiplier
        origins = [("New York", 10), ("Chicago", 20)]
        destinations = ["Los Angeles", "San Francisco"]
        detailed_df, total_emissions_df = calculate_emissions_for_multiple_routes(
            origins, destinations
        )
        self.assertEqual(len(detailed_df), 4)
        self.assertEqual(len(total_emissions_df), 2)

    def test_zero_distance(self):
        # zero distance, city and origin are the same
        origin = destination = "New York"
        distance = calculate_distance(origin, destination)
        self.assertEqual(distance, 0)

    def test_negative_distance_error(self):
        # error raised for negative distance values
        with self.assertRaises(ValueError):
            calculate_single_trip_emissions(-100)

    def test_boundary_conditions(self):
        # boundary distances for categories, i.e. short/long haul etc.
        distances = [600, 3700]  # boundary distances for categories
        for distance in distances:
            emissions = calculate_single_trip_emissions(distance)
            self.assertTrue(isinstance(emissions, float))

    @patch("ctetproject.emissions_algo.geolocator.geocode")
    def test_geocode_failure_handling(self, mock_geocode):
        # geocode fail to find city test
        mock_geocode.return_value = None
        with self.assertRaises(ValueError):
            get_location("Atlantis")  # assuming Atlantis won't be found

    def test_invalid_input_types(self):
        # type validation for city input - expecting string argument
        with self.assertRaises(TypeError):
            get_location(123)  # passing a number instead of a string as city name

    def test_api_response_mocking(self):
        # handling of geolocation API responses by mocking a successful geocode
        with patch("ctetproject.emissions_algo.geolocator.geocode") as mock_geocode:
            mock_geocode.return_value = type(
                "Geo", (object,), {"latitude": 40.7128, "longitude": -74.0060}
            )
            location = get_location("New York")
            self.assertEqual(location, (40.7128, -74.0060))

    def test_caching_functionality(self):
        # call once to set cache, then testing the caching functionality, avoid redundant API calls
        get_location("New York")
        with patch("ctetproject.emissions_algo.geolocator.geocode") as mock_geocode:
            # this should not be called by API
            get_location("New York")
            mock_geocode.assert_not_called()

    def test_empty_inputs_for_multiple_routes(self):
        # testing empty input lists for multuple routes
        detailed_df, total_emissions_df = calculate_emissions_for_multiple_routes(
            [], []
        )
        self.assertTrue(detailed_df.empty)
        self.assertTrue(total_emissions_df.empty)

    @patch("ctetproject.emissions_algo.geolocator.geocode")
    def test_large_data_sets(self, mock_geocode):
        #  tests with large dataset by mocking geocode responses for fake locations.
        mock_geocode.return_value = type(
            "Geo", (object,), {"latitude": 0, "longitude": 0}
        )
        origins = [("City" + str(i), 1) for i in range(100)]
        destinations = ["City" + str(j) for j in range(100, 200)]
        detailed_df, _ = calculate_emissions_for_multiple_routes(origins, destinations)
        self.assertEqual(len(detailed_df), 10000)  # 100 origins x 100 destinations
