import server.structures as structures
from app.forms import ChangePasswordForm
from app.forRoutes.info import info
from server.storage import storage

def ChangePassword(form: ChangePasswordForm) -> list: # success, message
    if form.validate_on_submit():
        old_passwd = form.oldpassword.data
        new_passwd = form.newpassword.data
        ret_passwd = form.retpassword.data
        user = storage.getUser(info()["id"])
        if user.password != old_passwd:
            return [0, "Incorrect old password"]
        if new_passwd != ret_passwd:
            return [0, "New passwords don't match"]
        user.password = new_passwd
        storage.saveUser(user)
        return [1, "Password successfully changed"]
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    print(form.oldpassword.data)
    print(form.newpassword.data)
    print(form.retpassword.data)
    return [0, "Fill ..."]
