import pytest
from django.urls import reverse
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from django.conf import settings


city_count_test_cases = [
    ("basic.csv", {"Sydney": 10}),
    ("check_city.csv", {"Sydney": 10}),
    (
        "full_test_short.csv",
        {"Sydney": 10, "Canberra": 22, "Brisbane": 20, "Darwin": 21},
    ),
    ("group_cities.csv", {"Sydney": 10, "Canberra": 23, "Darwin": 21}),
    ("missing_rows.csv", {"Sydney": 10, "Canberra": 11, "Brisbane": 20}),
    ("multiple_cities.csv", {"Sydney": 10, "Canberra": 15, "Darwin": 16}),
    ("not_2_rows.csv", {"Sydney": 10}),
]


@pytest.mark.parametrize("csv_file,expected_city_counts", city_count_test_cases)
@pytest.mark.django_db
def test_csv_city_counts(client, csv_file, expected_city_counts):
    url = reverse("upload_csv")
    file_path = os.path.join(settings.BASE_DIR, "testing/testingcsv", csv_file)

    with open(file_path, "rb") as fp:
        uploaded_file = SimpleUploadedFile(csv_file, fp.read(), content_type="text/csv")

    response = client.post(url, {"csv_file": uploaded_file}, format="multipart")
    assert (
        response.status_code == status.HTTP_200_OK
    ), f"Failed on {csv_file} with status code"

    data = response.json()
    cities_in_response = {
        item["city"]: item["number"] for item in data.get("results", {}).get("data", [])
    }
    for city, expected_count in expected_city_counts.items():
        assert (
            cities_in_response.get(city, 0) == expected_count
        ), f"{city} count mismatch in response for {csv_file}"
