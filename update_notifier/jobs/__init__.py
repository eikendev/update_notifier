from . import frequent


def register_jobs(jq):
    jq.run_repeating(frequent.job_check_updates, 300, first=0)
