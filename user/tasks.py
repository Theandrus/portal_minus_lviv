from liqpay import LiqPay
from minus_lviv import settings
from minus_lviv.celery import app
from user.models import Subscription
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@app.task
def check_payment_status():
    subs = Subscription.objects.all()
    for sub in subs:
        order_id = sub.order_id
        liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
        res = liqpay.api("request", {
            "action": "status",
            "version": "3",
            "order_id": order_id
        })
        s = Subscription.objects.filter(order_id=order_id)
        if s.filter(is_paid=False):
            if res.get('status') == 'subscribed':
                s.update(is_paid=True)
                pass
            else:
                pass
        else:
            pass
