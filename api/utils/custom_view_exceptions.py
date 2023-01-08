from rest_framework.exceptions import APIException

class NotYourProfile(APIException):
    status_code = 403
    default_detail = "You cannot edit a profile that doesn't belong to you!"

class CantFollowYourself(APIException):
    status_code = 403
    default_detail = "You cannot follow yourself!"

class UpdatePost(APIException):
    status_code = 403
    default_detail = "You can't update an post that does not belong to you!"

class CantRateYourPost(APIException):
    status_code = 403
    default_detail = "You can't rate/review your own Post!"

class AlreadyRated(APIException):
    status_code = 400
    default_detail = "You have already rated this Post!"

class AlreadyFavorited(APIException):
    status_code = 400
    default_detail = "You have already favorited this Post"