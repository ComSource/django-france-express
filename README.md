django-france-express
=====================

**Django module for France Express (Geodis) shipping**

This module has been inspired from the [django-colissimo](https://github.com/matm/django-colissimo) module by [matm](https://github.com/matm)

## Generate initial data for the shipping module

You will need first to fill your rate file, e.g. `rates_2012.txt` and
then generate your fixtures via:

    cd france_express/fixtures
	python gen_fixtures.py rates_2012.txt > initial_data.json

## Install

Install the module in your python path:

    python setup.py install

Add `france_express` to your `INSTALLED_APPS` in your `settings.py`

	INSTALLED_APPS = (
		...
		'france_express',
		...
	)

Setup the database for your application, in the root directory of your
python project:

    python manage.py syncdb
	
This should create france_express tables and load fixtures. If not, do
this manually:

    python manage.py loaddata PATH/TO/APP/fixtures/initial_data.json

## Example

Here is an example of how you can use this app to calculate shipping
cost in your website :

    from france_express.models import Rate
	
	...
	
	r = Rate()
	department = 95
	total_weight = 12.
	rs = r.get_rates(department, total_weight)
	
The `rs` object now lists possible rates given offer of your choice:

	[<Rate: max 19.00kg (messagerie-zone-006) 18.51 EUR>, <Rate: max 15.00kg (express-zone-003) 34.12 EUR>]
