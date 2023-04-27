from django.utils.text import slugify

def unslugify(text):
    if text == 'valentines-day':
        return "Valentine's Day"
    return slugify(text, allow_unicode=True).replace('-', ' ').title()