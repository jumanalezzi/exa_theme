from exa_app.branding import get_branding


def get_madar_branding():
	"""Madar Settings branding fields, taken from exa_app so the product is named in one place."""
	brand = get_branding()
	return {
		"app_name_ar": brand["app_name_ar"],
		"app_name_en": brand["app_name"],
		"light_logo": brand["logo_light"],
		"dark_logo": brand["logo_dark"],
		"favicon": brand["favicon"],
	}


def apply_branding(settings):
	"""Overwrite the name and logos of a Madar Settings document in memory with exa_app's branding."""
	settings.update(get_madar_branding())
	return settings
