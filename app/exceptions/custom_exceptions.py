class JobNotFoundException(Exception):
    def __init__(self, job_id: int):
        super().__init__(f"Job not found with id: {job_id}")
        self.job_id = job_id


class CompanyNotFoundException(Exception):
    def __init__(self, company_id: int):
        super().__init__(f"Company not found with id: {company_id}")
        self.company_id = company_id


class OptimisticLockException(Exception):
    pass


class AuthenticationException(Exception):
    pass


class InvalidFileException(Exception):
    pass
