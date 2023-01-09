from rest_framework.exceptions import APIException

class NotYourProfile(APIException):
    default_detail = "You cannot edit a profile that doesn't belong to you!"

class CantFollowYourself(APIException):
    default_detail = "You cannot follow yourself!"

class UpdatePost(APIException):
    default_detail = "You can't update an post that does not belong to you!"

class CantRateYourPost(APIException):
    default_detail = "You can't rate/review your own Post!"

class AlreadyRated(APIException):
    default_detail = "You have already rated this Post!"

class AlreadyFavorited(APIException):
    default_detail = "You have already favorited this Post"