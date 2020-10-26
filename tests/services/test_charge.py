import pytest
import logging

from backend.services.charge import add_new_charge, get_charge, get_all_charges, \
                                    get_charges_for_battery, end_charge
from backend.services.battery import add_new_battery
from backend.models.chargestateenum import ChargeStateEnum


LOGGER = logging.getLogger(__name__)


BATTERY = {
    'model': 'Test',
    'is_active': True,
    'capacity': 100,
    'no_of_cells': 10,
    'discharge_rate': 0.8,
    'maintenance_voltage': 2.2,
    'full_charge_voltage': 3.7,
    'min_voltage': 2.0,
}


CHARGE = {
    'battery_id': 1,
    'charging_station_id': 5,
    'start_voltage': 4.4,
    'charge_type': str(ChargeStateEnum.charging)
}


class TestChargeServices:

    @pytest.mark.usefixtures('db')
    def test_get_charge(self):
        add_new_battery(BATTERY)
        add_new_charge(CHARGE)

        resp, status = get_charge(1)

        assert status == 200
        assert resp['success'] is True

        data = resp['data']
        assert data['end_date'] is None
        assert data['start_voltage'] == CHARGE['start_voltage']

    @pytest.mark.usefixtures('db')
    def test_get_all_charges(self):
        add_new_battery(BATTERY)
        add_new_battery(BATTERY)

        add_new_charge(CHARGE)
        charge = CHARGE.copy()
        charge['battery_id'] = 2
        add_new_charge(charge)

        resp, status = get_all_charges()

        data = resp['data']
        assert status == 200
        assert resp['success'] is True
        assert len(data) == 2

    @pytest.mark.usefixtures('db')
    def test_get_charges_for_battery(self):
        # First Battery
        add_new_battery(BATTERY)
        # Second Battery
        add_new_battery(BATTERY)

        # Adding charge to first Battery
        add_new_charge(CHARGE)

        charge_for_second_battery = {
            'battery_id': 2,
            'charging_station_id': 5,
            'start_voltage': 4.4,
            'charge_type': str(ChargeStateEnum.charging)
        }

        # Adding one charge for second Battery
        add_new_charge(charge_for_second_battery)

        charges = get_charges_for_battery(1)
        charges_for_second_battery = get_charges_for_battery(2)

        assert len(charges[0]['data']) == 1
        assert len(charges_for_second_battery[0]['data']) == 1

    @pytest.mark.usefixtures('db')
    def test_add_new_charge(self):
        add_new_battery(BATTERY)

        resp, status = add_new_charge(CHARGE)

        assert status == 200
        assert resp['success'] is True

        data = resp['data']
        assert data['id'] == 1
        assert data['battery_id'] == CHARGE['battery_id']
        assert data['charging_station_id'] == CHARGE['charging_station_id']

    @pytest.mark.usefixtures('db')
    def test_add_two_charges(self):
        add_new_battery(BATTERY)
        resp, status = add_new_charge(CHARGE)

        assert status == 200
        assert resp['success'] is True
        resp, status = add_new_charge(CHARGE)
        assert resp['success'] is False

    @pytest.mark.usefixtures('db')
    def test_add_charge_negative_start_voltage(self):
        add_new_battery(BATTERY)
        charge_copy = CHARGE.copy()
        charge_copy['start_voltage'] = -2.2

        resp, status = add_new_charge(charge_copy)

        assert status == 422
        assert resp['success'] is False

    @pytest.mark.usefixtures('db')
    def test_add_new_charge_no_battery(self):
        resp, status = add_new_charge(CHARGE)
        err = resp['error']

        assert status == 422
        assert resp['success'] is False

    @pytest.mark.usefixtures('db')
    def test_add_new_charge_bad_charge_type(self):
        add_new_battery(BATTERY)
        charge_copy = CHARGE.copy()
        charge_copy['charge_type'] = '12345'

        resp, status = add_new_charge(charge_copy)

        assert status == 422
        assert resp['success'] is False
        assert resp['error']['message'] is not None

    @pytest.mark.usefixtures('db')
    def test_end_charge_no_data(self):
        add_new_battery(BATTERY)
        add_new_charge(CHARGE)

        resp, status = end_charge({}, 1)

        assert status == 400
        assert "No input data provided" in resp['error']['message'][0]

    @pytest.mark.usefixtures('db')
    def test_end_charge_no_end_voltage(self):
        add_new_battery(BATTERY)
        add_new_charge(CHARGE)

        resp, status = end_charge({'end_date': '20-11-2021'}, 1)

        assert status == 400

    @pytest.mark.usefixtures('db')
    def test_end_charge_two_times(self):
        add_new_battery(BATTERY)
        add_new_charge(CHARGE)

        resp, status = end_charge({
            "end_date": "2020-08-06T09:41:24.637836",
            "end_voltage": 19.0999
        }, 1)

        assert resp['success'] is True

        resp, status = end_charge({
            "end_date": "2020-08-06T09:41:24.637836",
            "end_voltage": 19.0999
        }, 1)

        assert resp['success'] is False
