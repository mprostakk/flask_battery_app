import pytest
import logging

from backend.services.charge import add_new_charge
from backend.services.battery import add_new_battery
from backend.services.chargemeasurement import get_all_measure, get_measure_for_charge, add_measure_to_charge
from backend.models.chargestateenum import ChargeStateEnum


LOGGER = logging.getLogger(__name__)


CHARGE_MEASUREMENT = {
    'charge_id': 1,
    'timestamp': '2018-12-19 09:26:03.478039',
    'voltage': 10.2,
    'amps': 4.5,
    'temperature': 25.22,
    'capacity': 2000
}


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


class TestChargeMeasurementService:

    @pytest.mark.usefixtures('db')
    def test_add_measure_to_charge_no_data(self):
        add_new_battery(BATTERY)
        add_new_charge(CHARGE)

        resp, status = add_measure_to_charge({})

        assert status == 422
        assert 'No input data provided' in resp['error']['message'][0]

    @pytest.mark.usefixtures('db')
    def test_add_measure_to_charge(self):
        add_new_battery(BATTERY)
        add_new_charge(CHARGE)

        resp, status = add_measure_to_charge(CHARGE_MEASUREMENT)

        assert status == 200
        assert resp['success'] is True
        assert resp['data']['voltage'] == CHARGE_MEASUREMENT['voltage']

    @pytest.mark.usefixtures('db')
    def test_get_all_measure(self):
        add_new_battery(BATTERY)
        add_new_charge(CHARGE)
        add_measure_to_charge(CHARGE_MEASUREMENT)

        resp, status = get_all_measure()

        assert status == 200
        assert resp['success'] is True

    @pytest.mark.usefixtures('db')
    def test_get_measure_for_charge(self):
        add_new_battery(BATTERY)
        add_new_charge(CHARGE)
        add_measure_to_charge(CHARGE_MEASUREMENT)

        resp, status = get_measure_for_charge(1)

        assert status == 200
        assert resp['success'] is True
