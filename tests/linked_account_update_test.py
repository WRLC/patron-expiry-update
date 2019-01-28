from linked_account_update import update_linked_accounts as ula

# test settings
def test_settings():
	assert ula.UPDATE_IZ_KEY == 'test'
	assert ula.LINKED_IZ_KEYS == 'test'

def test_read_report_generator():
    report_data = ula.read_report_generator(ula.REPORT_FILE)
    assert next(report_data)['Primary Identifier'] == '1021191850004617'


