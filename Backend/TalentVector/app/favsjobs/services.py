from .models import FavsJobs

def create_favjob(data):
    favjob = FavsJobs(**data)
    favjob.save()
    return favjob

def list_favjobs(user_id):
    favs_jobs = FavsJobs.objects(user_id=user_id).order_by("-created_at")
    return favs_jobs

def delete_favjob(user_id, favjob_id):
    favjobs = list_favjobs(user_id=user_id)
    for favjob in favjobs:
        if favjob.id == favjob_id:
            favjob.delete()
            return True
    return False
