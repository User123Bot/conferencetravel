from django.shortcuts import render
import csv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .emissions_algo import calculate_emissions_for_multiple_routes
import uuid
import logging
import os
from django.conf import settings


# connect the emissions algorithm
class CalculateEmissionsView(APIView):
    def post(self, request, *args, **kwargs):
        # guest information - origin, number of attendees
        origins = request.data.get("origins")
        #  ideal conference locations are the set of destinations
        destinations = request.data.get("destinations")

        #  algorithm output
        detailed_emissions_df, total_emissions_df = (
            calculate_emissions_for_multiple_routes(origins, destinations)
        )

        detailed_emissions = detailed_emissions_df.to_dict("records")
        total_emissions = total_emissions_df.to_dict("records")

        return Response(
            {
                "detailed_emissions": detailed_emissions,
                "total_emissions": total_emissions,
            }
        )


# Utility function to load cities
def load_cities_from_csv(file_path):
    cities_countries = {}
    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            city_ascii = row["city_ascii"].strip().lower()
            country = row["country"].strip().lower()
            # use the id when needed for quicker lookup
            id = row["id"].strip().lower()
            cities_countries[(city_ascii, country)] = True
    return cities_countries


# Load cities and countries into a global set for quick lookup
cities_set = load_cities_from_csv(
    os.path.join(settings.BASE_DIR, "./ctetproject/assets/world_cities/worldcities.csv")
)


@api_view(["GET"])
def index(request):
    return Response({"message": "Welcome to the CTET API"})


class CSVUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):

        logging.debug("Starting CSV file processing.")

        file_obj = request.FILES["csv_file"]
        if not file_obj:
            return JsonResponse({"error": "No file uploaded"}, status=400)

        if not file_obj.name.endswith(".csv"):
            return JsonResponse({"error": "File is not a CSV"}, status=400)

        # This dictionary will store city as key and a tuple (total_number, id) as value
        city_data = {}

        # List to store error messages
        errors = []

        # Read the uploaded CSV file and print the column headers
        try:
            decoded_file = file_obj.read().decode("utf-8").splitlines()
            reader = csv.DictReader(decoded_file)

            headers = reader.fieldnames  # This will capture the headers

            # check to make sure that the columns are in fact city and number in that order
            expected_columns = {"Country", "City", "Number"}
            if not expected_columns.issubset(set(reader.fieldnames)):
                return JsonResponse(
                    {
                        "error": "CSV does not have the required columns: Country, City and Number"
                    },
                    status=400,
                )

            counter = 1
            for row in reader:
                counter += 1
                # Check for missing values or extra columns
                if len(row) != 3:
                    if len(row) < 2:
                        errors.append(
                            f"Missing Columns: Make sure it is Country, City and Number"
                        )
                    else:
                        errors.append(
                            f"Extra Columns only expected 3 (Country, City, Number)"
                        )
                    continue  # Skip this row

                country = row["Country"].strip().lower()
                city = row["City"].strip().lower()
                number_str = row["Number"]

                # Skip rows with missing data
                if not country or not city or not number_str:
                    errors.append(f"Missing data in row: {counter}")
                    continue

                # Check if the number column is correctly formatted as an integer
                try:
                    number = int(number_str)
                except ValueError:
                    errors.append(
                        f"Malformed number, value is not an integer: {number_str}, row {counter}"
                    )
                    continue

                # Check if the city exists
                if (city, country) not in cities_set:
                    errors.append(
                        f"Unrecognized City or Country: {city} : Country: {country}"
                    )
                    continue

                # Aggregate numbers for duplicate city values
                if (country, city) in city_data:
                    # Update the total number for the city
                    existing_number, _ = city_data[(country, city)]
                    city_data[(country, city)] = (
                        existing_number + number,
                        str(uuid.uuid4()),
                    )
                else:
                    # Assign a new UUID for new city entry
                    city_data[(country, city)] = (number, str(uuid.uuid4()))

                # Everything is fine, append the object
                objects_list = [
                    {
                        "id": id_,
                        "country": country.capitalize(),
                        "city": city.capitalize(),
                        "number": total,
                    }
                    for (country, city), (total, id_) in city_data.items()
                ]

            logging.info("Finished CSV file processing.")

            # Check if there were any errors and print them
            if errors:
                for error in errors:
                    print(error)  # Print each error to the console

            logging.info("Final objects list:")
            for obj in objects_list:
                logging.info(obj)

            return JsonResponse(
                {
                    "message": "CSV processed successfully\n",
                    "results": {
                        "headers": headers,  # This includes the headers from the CSV file
                        "data": objects_list,  # This includes the processed data
                        "errors": errors,
                    },
                },
                status=200,
            )

        except Exception as e:
            print("Error processing CSV: ", e)
            return JsonResponse({"error": "Error processing CSV"}, status=400)


class CtetAPIView(APIView):
    def get(self, request):
        return Response({})
