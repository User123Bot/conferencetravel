import pandas as pd
from geopy.distance import great_circle
from geopy.geocoders import Nominatim
from typing import Tuple, Dict, List

geolocator = Nominatim(user_agent="myGeocodeApp")

# cache geocode locations - city - lat/long
location_cache: Dict[str, Tuple[float, float]] = {}


def get_location(city: str) -> Tuple[float, float]:

    if not isinstance(city, str):
        raise TypeError("City name must be a string.")

    # check cache for the city
    if city in location_cache:
        return location_cache[city]

    # else use geocode, then add to cache
    location = geolocator.geocode(city)
    if location is None:
        # TODO - update to show a message within the webpage UI too
        raise ValueError(f"Location {city} could not be found using GeoCode.")
    location_cache[city] = (location.latitude, location.longitude)

    return location_cache[city]


def calculate_distance(origin: str, destination: str) -> float:
    origin_loc = get_location(origin)
    destination_loc = get_location(destination)
    distance = great_circle(origin_loc, destination_loc).kilometers
    return distance


def calculate_single_trip_emissions(distance_km: float) -> float:
    # Assumptions based on the provided method @TODO - add link to document/website
    radiative_forcing_factor_2023 = 1.7  # Assumed RFF for 2023
    distance_uplift_factor = 0.08  # Distance uplift factor

    # Conversion factors for different flight categories

    # kg CO2e per passenger per km for domestic flights
    conversion_factor_domestic = 0.27258
    # kg CO2e per passenger per km for short haul flights
    conversion_factor_short_haul = 0.18592
    # kg CO2e per passenger per km for long haul flights to/from UK
    conversion_factor_long_haul_international = 0.17580

    if distance_km < 0:
        raise ValueError("Distance cannot be negative.")
    # determine the conversion factor based on the flight distance
    if distance_km <= 600:
        # domestic flight
        conversion_factor = conversion_factor_domestic
    elif 600 < distance_km <= 3700:
        # short haul flight
        conversion_factor = conversion_factor_short_haul
    else:
        # long haul flight
        conversion_factor = conversion_factor_long_haul_international

    # Calculate the emissions
    emissions_kg_CO2e = (
        conversion_factor
        * distance_km
        * radiative_forcing_factor_2023
        * (1 + distance_uplift_factor)
    )
    return emissions_kg_CO2e


def calculate_emissions_for_multiple_routes(
    origins: List[Tuple[str, int]], destinations: List[str]
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    routes_data = []
    for origin, attendees in origins:
        for destination in destinations:
            distance_km = calculate_distance(origin, destination)
            emissions_kg_CO2e = calculate_single_trip_emissions(distance_km)
            total_emissions = emissions_kg_CO2e * attendees
            routes_data.append(
                {
                    "Origin": origin,
                    "Destination": destination,
                    "Distance_km": distance_km,
                    "Emissions_kg_CO2e_per_attendee": emissions_kg_CO2e,
                    "Attendees": attendees,
                    "Total_Emissions_kg_CO2e": total_emissions,
                }
            )

    # creating dataFrame from collected data
    detailed_df = pd.DataFrame(routes_data)

    if detailed_df.empty:
        return detailed_df, pd.DataFrame()

    destination_coords = pd.DataFrame(
        [
            {
                "Destination": destination,
                "Lat": get_location(destination)[0],
                "Lng": get_location(destination)[1],
            }
            for destination in set(detailed_df["Destination"])
        ]
    )

    # aggregating total emissions by destination
    total_emissions_by_destination = (
        detailed_df.groupby("Destination")
        .agg(
            {
                "Total_Emissions_kg_CO2e": "sum",
            }
        )
        .reset_index()
        .sort_values(by="Total_Emissions_kg_CO2e")
        .round()
    )

    # Merge to include lat/lng
    total_emissions_by_destination = total_emissions_by_destination.merge(
        destination_coords, on="Destination", how="left"
    )

    return detailed_df, total_emissions_by_destination
