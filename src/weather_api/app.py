from datetime import datetime
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flasgger import Swagger, swag_from
import sqlite3

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

def fetch_records(cursor):
    column_names = [desc[0] for desc in cursor.description]
    return [dict(zip(column_names, row)) for row in cursor.fetchall()]



class Weather(Resource):
    @swag_from('weather.yml')
    def get(self):
        db_path = '../db/weather_data.sqlite'

        query_params = []
        where_clause = []

        station_id = request.args.get('station_id')
        if station_id:
            where_clause.append('station_id = ?')
            query_params.append(station_id)

        date = request.args.get('date')
        if date:
            try:
                date_obj = datetime.strptime(date, "%m/%d/%Y")
                date_str = datetime.strftime(date_obj, "%Y-%m-%d")
                where_clause.append('date = ?')
                query_params.append(date_str)
            except ValueError:
                return {"error": "Invalid date format. Use 'mm/dd/yyyy'."}, 400

        limit = request.args.get('limit', 10)
        offset = int(request.args.get('offset', 0))
        if where_clause:
            where_clause = 'WHERE ' + ' AND '.join(where_clause)

        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT * FROM weather_data
                {where_clause}
                LIMIT ? OFFSET ?
            """, query_params + [limit, offset])

            results = fetch_records(cursor)

        return jsonify(results)

class WeatherStats(Resource):
    @swag_from('weather_stats.yml')
    def get(self):
        db_path = '../db/weather_data.sqlite'

        query_params = []
        where_clause = []

        station_id = request.args.get('station_id')
        if station_id:
            where_clause.append('station_id = ?')
            query_params.append(station_id)

        date = request.args.get('date')
        if date:
            try:
                date_obj = datetime.strptime(date, "%m/%d/%Y")
                date_str = datetime.strftime(date_obj, "%Y-%m-%d")
                where_clause.append('date = ?')
                query_params.append(date_str)
            except ValueError:
                return {"error": "Invalid date format. Use 'mm/dd/yyyy'."}, 400

        limit = request.args.get('limit', 10)
        offset = int(request.args.get('offset', 0))

        if where_clause:
            where_clause = 'WHERE ' + ' AND '.join(where_clause)

        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT * FROM weather_data
                {where_clause}
                LIMIT ? OFFSET ?
            """, query_params + [limit, offset])

            results = fetch_records(cursor)

        return jsonify(results)

api.add_resource(Weather, '/api/weather')
api.add_resource(WeatherStats, '/api/weather/stats')

if __name__ == '__main__':
    app.run(debug=True)
