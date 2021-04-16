from models import User
from zipcodeCityState import get_citystate_data
from werkzeug.security import generate_password_hash, check_password_hash
from __init__ import db


def findUserToUpdate(emailAddress):
    user = User.query.filter_by(emailAddress=emailAddress).first()
    return user


def updateEmailAddress(user, newEmailAddress):
    user.emailAddress = newEmailAddress
    db.session.commit()
    return


def updateName(user, newName):
    user.name = newName
    db.session.commit()
    return


def updatePassword(user, newPassword):
    user.password = generate_password_hash(newPassword, method='sha256')
    db.session.commit()
    return


def updateZipcode(user, newZipcode):
    user.zipcode = newZipcode
    cityStateData = get_citystate_data(newZipcode)
    newCity = cityStateData[0]
    newState = cityStateData[1]
    user.city = newCity
    user.state = newState
    db.session.commit()
    return


def updateUserRadius(user, newUserRadius):
    user.userRadius = newUserRadius
    db.session.commit()
    return


def updateUserImage(user, newUserImage):
    user.userImage = newUserImage
    db.session.commit()
    return


def updateHiking(user, newHiking):
    user.hiking = newHiking
    db.session.commit()
    return


def updateMountainBiking(user, newMountainBiking):
    user.mountainBiking = newMountainBiking
    db.session.commit()
    return


def updateCamping(user, newCamping):
    user.camping = newCamping
    db.session.commit()
    return
