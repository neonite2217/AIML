import pytest
import pandas as pd
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from geospatial_clustering import (
    haversine_distance,
    nearest_neighbor_tsp,
    assign_zone
)


class TestHaversineDistance:
    def test_same_point(self):
        dist = haversine_distance(40.7128, -74.0060, 40.7128, -74.0060)
        assert dist == 0.0

    def test_known_distance(self):
        dist = haversine_distance(40.7128, -74.0060, 40.7580, -73.9855)
        assert 5.0 < dist < 7.0

    def test_symmetric(self):
        d1 = haversine_distance(40.7128, -74.0060, 40.7580, -73.9855)
        d2 = haversine_distance(40.7580, -73.9855, 40.7128, -74.0060)
        assert abs(d1 - d2) < 0.001


class TestTSP:
    def test_single_point(self):
        points = [(40.7128, -74.0060)]
        route, dist = nearest_neighbor_tsp(points)
        assert route == [0]
        assert dist == 0

    def test_two_points(self):
        points = [(40.7128, -74.0060), (40.7580, -73.9855)]
        route, dist = nearest_neighbor_tsp(points)
        assert len(route) == 2
        assert dist > 0

    def test_multiple_points(self):
        points = [
            (40.7128, -74.0060),
            (40.7580, -73.9855),
            (40.7484, -73.9857),
            (40.7831, -73.9712)
        ]
        route, dist = nearest_neighbor_tsp(points)
        assert len(route) == 4
        assert len(set(route)) == 4
        assert dist > 0


class TestZoneAssignment:
    def test_downtown_zone(self):
        row = pd.Series({'lng': -73.98, 'lat': 40.70})
        zone = assign_zone(row)
        assert zone == "Downtown/Financial District"

    def test_uptown_zone(self):
        row = pd.Series({'lng': -74.10, 'lat': 40.80})
        zone = assign_zone(row)
        assert zone == "Uptown/North Zone"

    def test_midtown_zone(self):
        row = pd.Series({'lng': -74.05, 'lat': 40.72})
        zone = assign_zone(row)
        assert zone == "Midtown/Central Zone"


class TestDataLoading:
    @pytest.fixture
    def sample_data(self):
        return pd.DataFrame({
            'lat': [40.7128, 40.7580, 40.7484],
            'lng': [-74.0060, -73.9855, -73.9857]
        })

    def test_data_shape(self, sample_data):
        assert sample_data.shape == (3, 2)

    def test_columns_exist(self, sample_data):
        assert 'lat' in sample_data.columns
        assert 'lng' in sample_data.columns
