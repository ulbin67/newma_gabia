import os
import numpy as np
import pandas as pd
from datetime import datetime
import joblib
from .models import DoneApply, Apply
from django.conf import settings
from django.db.models import Sum

def 달별박스수계산():
    done_applies = DoneApply.objects.all()

    monthly_box_counts = {}

    for apply in done_applies:
        month = apply.done_at.month
        if month not in monthly_box_counts:
            monthly_box_counts[month] = 0

        box_num = apply.box_num if apply.box_num is not None else 0
        monthly_box_counts[month] += box_num

    monthly_done_box_count = [
        {'month': month, 'total_box': total_box}
        for month, total_box in monthly_box_counts.items()
    ]

    data = monthly_done_box_count

    labels = [f"{datetime.now().year}-{item['month']:02}" for item in data]
    box_nums = [item['total_box'] for item in data]
    return labels, box_nums