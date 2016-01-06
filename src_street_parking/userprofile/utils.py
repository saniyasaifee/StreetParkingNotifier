from userprofile.models import UserProfile

'''this is used the create user profile'''
def create_profile(user):
    profile_obj = UserProfile
    # pylint: disable=E1101
    profile_obj.objects.create(user=user)
    # pylint enable=E1101
    return profile_obj
