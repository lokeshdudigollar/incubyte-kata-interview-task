def employee_data(**overrides):
    data = {
        "full_name": "Lokesh Dudigollar",
        "job_title": "Software Engineer",
        "country": "India",
        "salary": 300000
    }
    data.update(overrides)
    return data