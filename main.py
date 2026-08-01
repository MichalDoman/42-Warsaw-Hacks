import requests
from flask import Flask, jsonify, render_template

from core.services.dashboard_services import get_dashboard_data

app = Flask(__name__)

@app.route("/")
def dashboard():
    try:
        return render_template(
            "dashboard.html",
            dashboard=get_dashboard_data(),
            error_message=None,
        )
    except requests.Timeout:
        return render_template(
            "dashboard.html",
            dashboard=None,
            error_message="42 API response timeout.",
        ), 504
    except requests.HTTPError as error:
        response = error.response
        message = (
            f"HTTP error: {error}"
            if response is None
            else f"42 API response status code: {response.status_code}. {response.text}"
        )
        return render_template(
            "dashboard.html",
            dashboard=None,
            error_message=message,
        ), 502
    except requests.RequestException as error:
        return render_template(
            "dashboard.html",
            dashboard=None,
            error_message=f"Error connecting to 42 API: {error}",
        ), 502
    except (RuntimeError, ValueError) as error:
        return render_template(
            "dashboard.html",
            dashboard=None,
            error_message=f"Configuration error: {error}",
        ), 500


@app.route("/api/dashboard")
def dashboard_api():
    try:
        return jsonify(get_dashboard_data())
    except requests.RequestException as error:
        return jsonify({"error": str(error)}), 502
    except (RuntimeError, ValueError) as error:
        return jsonify({"error": str(error)}), 500


def main() -> None:
    app.run(host="127.0.0.1", port=5000, debug=True)


if __name__ == "__main__":
    main()
