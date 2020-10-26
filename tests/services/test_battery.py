import pytest
import logging

from backend.services.battery import *
from backend.services.charge import add_new_charge, end_charge
from backend.models.chargestateenum import ChargeStateEnum


LOGGER = logging.getLogger(__name__)


SAMPLE_BATTERY = {
    "is_active": True,
    "capacity": 2000,
    "model": "Test",
    "no_of_cells": 4,
    "discharge_rate": 0.8,
    "maintenance_voltage": 3.4,
    "full_charge_voltage": 4.2,
    "min_voltage": 2.7,
}


CHARGE = {
    'battery_id': 1,
    'charging_station_id': 5,
    'start_voltage': 4.4,
    'charge_type': str(ChargeStateEnum.charging)
}


def add_batteries_to_db(number_of_batteries, json=None):
    if json is None:
        battery = SAMPLE_BATTERY.copy()
    else:
        battery = json

    for _ in range(number_of_batteries):
        add_new_battery(battery)


@pytest.mark.usefixtures('db')
def test_index(app, client):
    res = client.get('/api/battery')
    assert res.status_code == 200


@pytest.mark.usefixtures('db')
def test_add(app, client):
    res = client.get('/api/battery/all')
    assert res.status_code == 200


class TestBatteryServices:

    @pytest.mark.usefixtures('db')
    def test_add_battery(self):
        resp, status = add_new_battery(SAMPLE_BATTERY)

        if status != 200:
            LOGGER.error(str(resp))
            raise str(resp)

        assert status == 200
        assert resp['success'] == True

        data = resp['data']
        assert data['id'] == 1
        assert data['is_active'] == True
        assert data['model'] == 'Test'
        assert data['capacity'] == 2000
        assert data['no_of_cells'] == 4
        assert data['discharge_rate'] == 0.8
        assert data['maintenance_voltage'] == 3.4
        assert data['full_charge_voltage'] == 4.2
        assert data['min_voltage'] == 2.7

    @pytest.mark.usefixtures('db')
    def test_add_no_battery(self):
        resp, status = add_new_battery({})

        assert status == 400
        assert resp['success'] == False

    @pytest.mark.usefixtures('db')
    def test_add_bad_battery(self):
        resp, status = add_new_battery({
            'model': None,
        })

        assert status == 422
        assert resp['success'] == False

    @pytest.mark.usefixtures('db')
    def test_add_battery_without_capacity(self):
        resp, status = add_new_battery({
            "is_active": True,
            "model": "TestModel",
            "no_of_cells": 4,
            "discharge_rate": 4,
            "maintenance_voltage": 3.4,
            "full_charge_voltage": 4.2,
            "min_voltage": 2.7
        })

        assert status == 422
        assert resp['success'] is False

    @pytest.mark.usefixtures('db')
    def test_add_battery_with_minus_no_of_cells(self):
        battery = SAMPLE_BATTERY.copy()
        battery['no_of_cells'] = -4
        resp, status = add_new_battery(battery)

        assert status == 422
        assert resp['success'] is False

    @pytest.mark.usefixtures('db')
    def test_add_battery_with_minus_capacity(self):
        battery = SAMPLE_BATTERY.copy()
        battery['capacity'] = -2000
        resp, status = add_new_battery(battery)

        assert status == 422
        assert resp['success'] is False

    @pytest.mark.usefixtures('db')
    def test_add_battery_with_minus_discharge_rate(self):
        battery = SAMPLE_BATTERY.copy()
        battery['discharge_rate'] = -4.2
        resp, status = add_new_battery(battery)

        assert status == 422
        assert resp['success'] is False

    @pytest.mark.usefixtures('db')
    def test_add_battery_with_minus_maintenance_voltage(self):
        battery = SAMPLE_BATTERY.copy()
        battery['maintenance_voltage'] = -4.4
        resp, status = add_new_battery(battery)

        assert status == 422
        assert resp['success'] is False

    @pytest.mark.usefixtures('db')
    def test_add_battery_with_minus_no_min_voltage(self):
        battery = SAMPLE_BATTERY.copy()
        battery['min_voltage'] = -2.4
        resp, status = add_new_battery(battery)

        assert status == 422
        assert resp['success'] is False

    @pytest.mark.usefixtures('db')
    def test_add_battery_with_smaller_full_charge_voltage_then_min_voltage(self):
        battery = SAMPLE_BATTERY.copy()
        battery['full_charge_voltage'] = 4.2
        battery['min_voltage'] = 10.3
        resp, status = add_new_battery(battery)

        assert status == 422
        assert resp['success'] is False

    @pytest.mark.usefixtures('db')
    def test_add_battery_with_bigger_maintenance_voltage_then_full_charge_voltage(self):
        battery = SAMPLE_BATTERY.copy()
        battery['maintenance_voltage'] = 5.2
        battery['full_charge_voltage'] = 4.3
        resp, status = add_new_battery(battery)

        assert status == 422
        assert resp['success'] is False

    @pytest.mark.usefixtures('db')
    def test_add_battery_with_production_date_in_future(self):
        battery = SAMPLE_BATTERY.copy()
        battery['production_date'] = "2099-02-20"
        resp, status = add_new_battery(battery)

        assert status == 422
        assert resp['success'] is False

    @pytest.mark.usefixtures('db')
    def test_add_battery_with_production_date_before_first_usage(self):
        battery = SAMPLE_BATTERY.copy()
        battery['production_date'] = "2020-02-21"
        battery['first_usage_date'] = "2020-02-20"
        resp, status = add_new_battery(battery)

        assert status == 422
        assert resp['success'] is False

    @pytest.mark.usefixtures('db')
    def test_add_battery_with_minus_no_of_battery_cycles(self):
        battery = SAMPLE_BATTERY.copy()
        battery['no_of_battery_cycles'] = -1
        resp, status = add_new_battery(battery)

        assert status == 422
        assert resp['success'] is False

    @pytest.mark.usefixtures('db')
    def test_add_battery_with_company_name_special_characters(self):
        company_name = 'dsęęœπąśðæðśćżąæśð„æð”ðafds\ndfs\tfsa'

        battery = SAMPLE_BATTERY.copy()
        battery['company'] = company_name
        resp, status = add_new_battery(battery)

        assert resp['data']['company'] == company_name
        assert status == 200
        assert resp['success'] is True

    @pytest.mark.usefixtures('db')
    def test_add_battery_with_default_is_active(self):
        resp, status = add_new_battery({
            "capacity": 2000,
            "no_of_cells": 4,
            "discharge_rate": 4,
            "maintenance_voltage": 3.4,
            "full_charge_voltage": 4.2,
            "min_voltage": 2.7
        })

        assert resp['data']['is_active'] is False
        assert status == 200
        assert resp['success'] is True

    @pytest.mark.usefixtures('db')
    def test_get_all_batteries(self):
        battery = SAMPLE_BATTERY.copy()

        for _ in range(3):
            add_new_battery(battery)
        battery['is_active'] = False
        for _ in range(5):
            add_new_battery(battery)
        battery['is_active'] = True
        for _ in range(3):
            add_new_battery(battery)

        resp, status = get_all_batteries()
        assert status == 200

        data = resp['data']
        assert len(data) == 11

    @pytest.mark.usefixtures('db')
    def test_get_all_active_batteries(self):
        battery = SAMPLE_BATTERY.copy()

        for _ in range(3):
            add_new_battery(battery)
        battery['is_active'] = False
        for _ in range(5):
            add_new_battery(battery)
        battery['is_active'] = True
        for _ in range(2):
            add_new_battery(battery)

        resp, status = get_all_active_batteries()
        assert status == 200

        data = resp['data']
        assert len(data) == 5

    @pytest.mark.usefixtures('db')
    def test_get_battery_id(self):
        battery = SAMPLE_BATTERY.copy()

        for x in range(3):
            add_new_battery(battery)
            resp, status = get_battery(x + 1)
            assert status == 200
            data = resp['data']
            assert data['id'] == x + 1

    @pytest.mark.usefixtures('db')
    def test_add_battery_bad_json(self):
        bad_json = {
            '__________': 1
        }

        resp, status = add_new_battery(bad_json)
        assert status == 422
        assert resp['success'] is False

    @pytest.mark.usefixtures('db')
    def test_add_battery_invalid_json(self):
        bad_json = {
            'invaild': -21.21
        }

        resp, status = add_new_battery(bad_json)
        assert status == 422
        assert resp['success'] is False

    @pytest.mark.usefixtures('db')
    def test_get_all_plugged_batteries(self):
        battery = SAMPLE_BATTERY.copy()

        for _ in range(2):
            add_new_battery(battery)
        battery['is_active'] = False

        charge = CHARGE.copy()
        charge['battery_id'] = 1
        add_new_charge(charge)

        resp, status = get_all_plugged_batteries()
        assert status == 200
        data = resp['data']
        assert len(data) == 1

        charge['battery_id'] = 2
        add_new_charge(charge)

        resp, status = get_all_plugged_batteries()
        assert status == 200
        data = resp['data']
        assert len(data) == 2

        end_json = {
            "end_date": "2020-08-06T09:41:24.637836",
            "end_voltage": 19.0999
        }
        end_charge(end_json, 2)

        resp, status = get_all_plugged_batteries()
        assert status == 200
        data = resp['data']
        assert len(data) == 1

    @pytest.mark.usefixtures('db')
    def test_delete_batteries(self):
        battery = SAMPLE_BATTERY.copy()

        for _ in range(3):
            add_new_battery(battery)

        charge = CHARGE.copy()
        charge['battery_id'] = 1
        add_new_charge(charge)

        resp, status = get_all_batteries()
        assert status == 200
        data = resp['data']
        assert len(data) == 3

        resp, status = delete_battery(1)
        assert status == 200
        assert resp['success'] is True

        # delete same battery
        resp, status = delete_battery(1)
        assert status == 422
        assert resp['success'] is False

        resp, status = get_all_batteries()
        assert status == 200
        data = resp['data']
        assert len(data) == 2

        resp, status = delete_battery(100)
        assert resp['success'] is False

    @pytest.mark.usefixtures('db')
    def test_update_battery(self):
        battery = SAMPLE_BATTERY.copy()
        battery['is_active'] = True
        battery['capacity'] = 3000

        for _ in range(2):
            add_new_battery(battery)

        update_json = {
            "is_active": False,
            "capacity": 1337
        }

        update_battery(update_json, 1)

        resp, status = get_all_batteries()
        assert status == 200
        data = resp['data']
        assert len(data) == 2
        assert data[0]['capacity'] == 1337
        assert data[0]['is_active'] == False

    @pytest.mark.usefixtures('db')
    def test_update_battery_bad_data(self):
        battery = SAMPLE_BATTERY.copy()

        for _ in range(2):
            add_new_battery(battery)

        update_json = {
            "bad_value_sdasda": False,
            "capacity": 1337
        }
        resp, status = update_battery(update_json, 1)
        assert resp['success'] is False

        resp, status = update_battery(update_json, 999999)
        assert resp['success'] is False
