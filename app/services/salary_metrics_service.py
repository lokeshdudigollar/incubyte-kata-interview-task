from app.schema.salary_metrics_schema import SalaryMetricsByCountryResponse, SalaryMetricsByJobTitleResponse



class SalaryMetricsService:
    def __init__(self, repo):
        self.repo = repo

    def get_metrics_by_country(self, country: str):
        min_salary, max_salary, avg_salary = self.repo.get_salary_metrics_by_country(country)

        return SalaryMetricsByCountryResponse(
            country=country,
            min_salary=min_salary,
            max_salary=max_salary,
            average_salary=avg_salary
        )

    def get_average_by_job_title(self, job_title: str):
        avg_salary = self.repo.get_average_salary_by_job_title(job_title)

        return SalaryMetricsByJobTitleResponse(
            job_title=job_title,
            average_salary=avg_salary
        )