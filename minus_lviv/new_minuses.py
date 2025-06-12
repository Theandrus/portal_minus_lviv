from minusstore.models import MinusstoreMinusrecord,PreModerationRecord


def new_minuses():
	pre_moderation_record = PreModerationRecord.objects.all().values_list('minus_id')

	new_m = MinusstoreMinusrecord.objects.exclude(id__in=pre_moderation_record).order_by("-id")[:10]
	return new_m
