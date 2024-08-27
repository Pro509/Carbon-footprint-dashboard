from flask import Flask, jsonify
import requests
import csv
from io import StringIO

app = Flask(__name__)

# URLs for the CSV files (replace these with your actual URLs)
csv_urls = [
    'https://example.com/manufacturing_data.csv',
    'https://example.com/energy_consumption.csv',
    'https://example.com/transport_data.csv'
]

def fetch_csv_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def parse_csv_data(csv_string):
    csv_file = StringIO(csv_string)
    csv_reader = csv.DictReader(csv_file)
    return list(csv_reader)

def calculate_emissions(manufacturing_data, energy_data, transport_data):
    # This is a simplified calculation. Replace this with your actual calculation logic.
    manufacturing_emissions = sum(float(row.get('emissions', 0)) for row in manufacturing_data)
    energy_emissions = sum(float(row.get('emissions', 0)) for row in energy_data)
    transport_emissions = sum(float(row.get('emissions', 0)) for row in transport_data)

    total_emissions = manufacturing_emissions + energy_emissions + transport_emissions

    return {
        'totalEmissions': total_emissions,
        'manufacturingEmissions': manufacturing_emissions,
        'energyEmissions': energy_emissions,
        'transportEmissions': transport_emissions
    }

@app.route('/emissions', methods=['GET'])
def get_emissions():
    try:
        csv_data = [fetch_csv_data(url) for url in csv_urls]
        parsed_data = [parse_csv_data(data) for data in csv_data]
        emissions_data = calculate_emissions(*parsed_data)
        return jsonify(emissions_data)
    except requests.RequestException as e:
        return jsonify({'error': f'Error fetching CSV data: {str(e)}'}), 500
    except Exception