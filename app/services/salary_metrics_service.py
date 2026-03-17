from app.schema.salary_metrics_schema import SalaryMetricsByCountryResponse, SalaryMetricsByJobTitleResponse



class SalaryMetricsService:
    def __init__(self, repo):
        self.repo = repo

    def get_salary_metrics_by_country(self, country: str) -> SalaryMetricsByCountryResponse:
        result = self.repo.get_salary_metrics_by_country(country)
        if result:
            min_salary, max_salary, avg_salary = result
        else:
            min_salary = max_salary = avg_salary = None

        return SalaryMetricsByCountryResponse(
            country=country,
            min_salary=min_salary,
            max_salary=max_salary,
            average_salary=avg_salary
        )

    def get_salary_metrics_by_job_title(self, job_title: str) -> SalaryMetricsByJobTitleResponse:
        avg_salary = self.repo.get_average_salary_by_job_title(job_title)

        return SalaryMetricsByJobTitleResponse(
            job_title=job_title,
            average_salary=avg_salary
        )