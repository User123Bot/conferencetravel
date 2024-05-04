import pytest
from django.urls import reverse
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from django.conf import settings

# Define test cases that are expected to produce errors
error_test_cases = [
    ("not_2_rows.csv", ["Unrecognized City or Country: sydne : Country: australia"]),
    ("not_2_rows.csv", ["Extra Columns only expected 3 (Country, City, Number)"]),
    ("not_2_rows.csv", ["Missing data in row: 5"]),
    ("check_city.csv", ["Malformed number, value is not an integer: hH, row 4"]),
    ("check_city.csv", ["Unrecognized City or Country: sydne : Country: australia"]),
    (
        "check_city.csv",
        ["Unrecognized City or Country: gaggaasdnadn : Country: australia"],
    ),
    ("cities_too_long.csv", ["Missing data in row: 1002"]),
    (
        "full_test_short.csv",
        ["Unrecognized City or Country: gaggaasdnadn : Country: australia"],
    ),
    ("full_test_short.csv", ["Malformed number, value is not an integer: hH, row 9"]),
    (
        "full_test_short.csv",
        ["Unrecognized City or Country: sydne : Country: australia"],
    ),
    ("full_test_short.csv", ["Extra Columns only expected 3 (Country, City, Number)"]),
    ("full_test_short.csv", ["Missing data in row: 12"]),
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

