import pytest
from django.urls import reverse
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from django.conf import settings

# Define test cases that are expected to produce errors
error_test_cases = [
    ("not_2_rows.csv", ["Unrecognized City: sydne - ROW 3"]),
    ("not_2_rows.csv", ["Extra Columns only expected 3 (Country, City, Number)"]),
    ("not_2_rows.csv", ["Missing data - ROW: 5"]),
    ("check_city.csv", ["Unrecognized City: gaggaasdnadn - ROW 3"]),
    ("check_city.csv", ["Malformed Number, value is not an integer: hH - ROW: 4"]),
    (
        "check_city.csv",
        ["Unrecognized City: sydne - ROW 5"],
    ),
    ("cities_too_long.csv", ["Missing data - ROW: 1002"]),
    (
        "full_test_short.csv",
        ["Unrecognized City: gaggaasdnadn - ROW 8"],
    ),
    ("full_test_short.csv", ["Malformed Number, value is not an integer: hH - ROW: 9"]),
    (
        "full_test_short.csv",
        ["Unrecognized City: sydne - ROW 10"],
    ),
    ("full_test_short.csv", ["Extra Columns only expected 3 (Country, City, Number)"]),
    ("full_test_short.csv", ["Missing data - ROW: 12"]),
    ("not_a_real_city.csv", ["Unrecognized City: sydn - ROW 2"]),
    ("not_a_real_country.csv", ["Unrecognized Country: australi - ROW 2"]),
    ("city_not_in_country.csv", ["Incorrect Classification: City paris and Country: australia are not related - ROW 2"]),
]

@pytest.mark.parametrize("csv_file,expected_errors", error_test_cases)
@pytest.mark.django_db
def test_csv_error_handling(client, csv_file, expected_errors):
    url = reverse("upload_csv")
    file_path = os.path.join(settings.BASE_DIR, "testing/testingcsv", csv_file)

    with open(file_path, "rb") as fp:
        uploaded_file = SimpleUploadedFile(csv_file, fp.read(), content_type="text/csv")

    response = client.post(url, {"csv_file": uploaded_file}, format="multipart")
    assert (
        response.status_code == status.HTTP_200_OK or status.HTTP_400_BAD_REQUEST
    ), f"Unexpected status code for {csv_file}"

    data = response.json()
    errors_in_response = data.get("results", {}).get("errors", [])

    # Check if all expected errors are present in the response
    for expected_error in expected_errors:
        assert any(
            expected_error in error for error in errors_in_response
        ), f"Expected error not found in response for {csv_file}: {expected_error}"

