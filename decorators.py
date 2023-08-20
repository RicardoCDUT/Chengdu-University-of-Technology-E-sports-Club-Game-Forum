from functools import wraps
from flask import abort, flash, request
from flask_login import current_user
import datetime


def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.id == 1:
            abort(403)
        return func(*args, **kwargs)

    return decorated_function




def stat(database, obj,_type):
    def decorator(func):
        # noinspection PyCallingNonCallable
        @wraps(func)
        def statistic(*args, **kwargs):
            td = datetime.date.today()
            vst = obj.query.filter_by(day=td,_type=_type).first()
            if _type=='post' and request.method == 'GET':
                return func(*args, **kwargs)
            if vst is None:
                new_vst = obj(day=td, times=1,_type=_type)
                database.session.add(new_vst)
            else:
                vst.times += 1
            database.session.commit()
            return func(*args, **kwargs)
        return statistic
    return decorator
