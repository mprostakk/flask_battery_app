const headers = {
  'Content-Type': 'application/json'
}

const prefixUrl = 'http://localhost/api';

const clearBattries = () => {
  const panel = document.getElementById('panel-battery');  
  const panelBattery = panel.lastChild;
  while(panelBattery.firstChild) {
    panelBattery.removeChild(panelBattery.lastChild);
  }
}

const getBatteries = () => {
  axios.get(prefixUrl + '/battery/all').then(resp => {
    const panel = document.getElementById('panel-battery');  
    const panelBattery = document.createElement('div');
    panelBattery.style.overflow = "auto";
    panelBattery.style.maxHeight = "300px";
  
    let i = 0;
    if(resp.data.success){
      resp.data.data.forEach(element => {
        i++;
        const div = document.createElement("section");
        const a = document.createElement("a");
        a.className = "panel-block";
        if(!element.is_active){
          a.style.backgroundColor = "pink";
        }
  
        const columns = document.createElement("div");
        columns.className = "columns is-mobile";
        a.appendChild(columns);
  
        let icon = document.createElement("i");
        let columnInfo = document.createElement("div");
        columnInfo.className = "column";
  
        if(element.last_charge){
          if(element.is_plugged){
            icon.className = "fas fa-bolt";
            columnInfo.innerHTML = "Plugged"
          }
          else {
            if(element.last_charge.charge_type == 'charging'){
              icon.className = "fas fa-battery-full";
              columnInfo.innerHTML = "Charged"
            }
            else if (element.last_charge.charge_type == 'maintenance'){
              icon.className = "fas fa-battery-three-quarters";
              columnInfo.innerHTML = "Maintenance"
            } 
            else if (element.last_charge.charge_type == 'discharging') {
              icon.className = "fas fa-battery-empty";
              columnInfo.innerHTML = "Discharged"
            }
          }
          if(element.last_charge.charge_type == 'charging'){
            icon.style.color = "green";
          }
          else if (element.last_charge.charge_type == 'maintenance'){
            icon.style.color = "blue";
          } 
          else if (element.last_charge.charge_type == 'discharging'){
            icon.style.color = "red";
          }
        }
        else{
          icon.className = "fas fa-times";
          columnInfo.innerHTML = "NoData"
        }
  
        icon.style.minWidth = "20px";
  
        let column = document.createElement("div");
        column.className = "column";
        columnInfo.style.textAlign = 'center';
  
        let columnIcon = column.cloneNode();
        columnIcon.className = "column";
        columnIcon.appendChild(icon);
  
        let columnID = column.cloneNode();
        columnID.className = "column has-text-centered is-1";
        columnID.style.textAlign = 'center';
        columnID.innerHTML = element.id;
  
        let columnVoltage = column.cloneNode();
        columnVoltage.className = "column";
        if(element.last_charge){
          if(element.last_charge.end_date){
            columnVoltage.innerHTML = element.last_charge.end_voltage + "v";
          }
          else{
            columnVoltage.innerHTML = element.last_charge.start_voltage + "v";
          }
        }
        else{
          columnVoltage.innerHTML = element.full_charge_voltage + "v";
        }
  
        let columnCapacity = column.cloneNode();
        columnCapacity.className = "column";
        columnCapacity.innerHTML = element.capacity + "mAh";
        
        let columnCells = column.cloneNode();
        columnCells.className = "column";
        columnCells.innerHTML = element.no_of_cells + "cells";
  
        let columnDischargeRate = column.cloneNode();
        columnDischargeRate.className = "column";
        columnDischargeRate.innerHTML = element.discharge_rate + "C";
  
        columnID.style.minWidth = "60px";
        columnIcon.style.minWidth = "60px";
        columnInfo.style.minWidth = "120px";
        columnInfo.style.textAlign = 'center';
        columnVoltage.style.minWidth = "60px";
        columnCapacity.style.minWidth = "100px";
        columnCells.style.minWidth = "60px";
        columnDischargeRate.style.minWidth = "60px";
        
        columns.appendChild(columnID);
        columns.appendChild(columnIcon);
        columns.appendChild(columnInfo);
        columns.appendChild(columnVoltage);
        columns.appendChild(columnCapacity);
        columns.appendChild(columnCells);
        columns.appendChild(columnDischargeRate);
  
        if (element.last_charge){
          let c3 = column.cloneNode();
          c3.className = "column";
          if(element.last_charge.end_date){
            c3.innerHTML = element.last_charge.end_date.toString().substr(0, 10);
          }
          else {
            c3.innerHTML = element.last_charge.start_date.toString().substr(0, 10);
          }
          columns.appendChild(c3);
        }
  
        let inp = document.createElement("input");
        inp.type = "radio";
        inp.style.display = "none";
        inp.name = "ac1";
        inp.id = i.toString();
        div.appendChild(inp);
        
        let columns2 = document.createElement("article");
        columns2.className = "columns is-mobile";
  
        a.onclick = () => {
          if(inp.checked == true){
            inp.checked = false;
          } 
          else{
            inp.checked = true;
          }
        }
  
        let buttonEdit = document.createElement("button");
        buttonEdit.className = "button";
        buttonEdit.innerText = "Edit";
        buttonEdit.onclick = () => {editBatteryBeforeScript(element)};
        
        let buttonCharge = document.createElement("button");
        if(element.is_plugged){
          buttonCharge.style.marginLeft = "25px";
          buttonCharge.className = "button is-danger";
          buttonCharge.innerText = "End charge";
          buttonCharge.onclick = () => {endChargeModalBefore(element.last_charge.id)};
        }
        else{
          buttonCharge.style.marginLeft = "25px";
          buttonCharge.className = "button is-success";
          buttonCharge.innerText = "Add charge";
          buttonCharge.onclick = () => {onChargeModal(element.id)};
        }

        let buttonSearch = document.createElement("button");
        buttonSearch.style.marginLeft = "25px";
        buttonSearch.className = "button";
        buttonSearch.innerText = "Search Charges";
        buttonSearch.onclick = () => {
          document.getElementById('search-charge').value = element.id;
          searchCharge();
        }
        
        columns2.appendChild(buttonEdit);
        columns2.appendChild(buttonCharge);
        columns2.appendChild(buttonSearch);
  
        div.appendChild(a);
        div.appendChild(columns2);
  
        panelBattery.appendChild(div);
      });

      clearBattries();
      panel.appendChild(panelBattery);
    }
  })
  .then(() => {
      searchBatteries();
  })  
}

const clearCharges = () => {
  const panel = document.getElementById('panel-charge');  
  const panelCharge = panel.lastChild;

  while(panelCharge.firstChild) {
    panelCharge.removeChild(panelCharge.lastChild);
  }
}

let last_a = null;

const getCharges = () => {
  axios.get(prefixUrl + '/charge').then(resp => {
    if(resp.data.success){
      const panel = document.getElementById('panel-charge');
      const panelCharge = document.createElement('div');
      panelCharge.style.overflow = "auto";
      panelCharge.style.maxHeight = "300px";

      resp.data.data.forEach(element => {
        const a = document.createElement("a");
        a.className = "panel-block";
        a.onclick = () => {  
          if (last_a) {
            last_a.className = last_a.className.replace(' is-active', '');
          }
          a.className += ' is-active';
          last_a = a;
          getCharge(element.id);
        }
  
        const columns = document.createElement("div");
        columns.className = "columns is-mobile";
        a.appendChild(columns);
  
        let icon = createIconForCharge(element);
  
        let column = document.createElement("div");
        column.className = "column";
        column.style.textAlign = "center";
        
        let columnIcon = column.cloneNode();
        columnIcon.className = "column";
        columnIcon.appendChild(icon);
  
        let columnId = column.cloneNode();
        columnId.className = "column has-text-centered";
        columnId.innerHTML = element.id;
  
        let columnChargeType = column.cloneNode();
        columnChargeType.className = "column";
        columnChargeType.innerHTML = element.charge_type;
  
        let columnBatteryID = column.cloneNode();
        columnBatteryID.className = "column";
        columnBatteryID.innerHTML = element.battery_id;
  
        let columnStartDate = column.cloneNode();
        columnStartDate.className = "column";
        columnStartDate.style = "white-space: nowrap;";
        columnStartDate.innerHTML = formatDate(new Date(element.start_date));
  
        columnBatteryID.style.minWidth = "60px";
        columnIcon.style.minWidth = "60px";
        columnChargeType.style.minWidth = "120px";
        columnStartDate.style.minWidth = "200px";

        columns.appendChild(columnBatteryID);
        columns.appendChild(columnIcon);
        columns.appendChild(columnChargeType);
        columns.appendChild(columnStartDate);
        
        if(!element.end_date){
          let endButton = document.createElement('button');
          endButton.innerHTML = "End";
          endButton.className = "button is-danger float-right";
          endButton.style.margin = "10px";
          endButton.style.height = "25px";
          endButton.onclick = () => {endChargeModalBefore(element.id)};
          columns.appendChild(endButton);
        } 
        else {
          let endData = column.cloneNode();
          endData.style = "white-space: nowrap;";
          endData.innerHTML = formatDate(new Date(element.end_date));
          columns.appendChild(endData);
        }
        panelCharge.appendChild(a);      
      })

      clearCharges();
      panel.appendChild(panelCharge);
    }
  })
  .then(() => {
      searchCharge();
  })
}

const getCharge = (id) => {
  axios.get(`${prefixUrl}/charge/${id}`)
  .then(resp => {
    const data = resp.data.data;

    document.getElementById('chargeinfo-battery-id').innerText = `id: ${data.battery_id}`;
    document.getElementById('chargeinfo-charge-id').innerText = `id: ${data.id}`;
    document.getElementById('chargeinfo-charge-charge_type').innerText = data.charge_type;

    let icon = document.getElementById('chargeinfo-charge-charge_type-icon');
    let new_icon = createIconForCharge(data);

    new_icon.className += ' fa-2x'
    new_icon.id = "chargeinfo-charge-charge_type-icon";
    icon.parentNode.replaceChild(new_icon, icon);

    if(data.charging_station_id){
        document.getElementById('chargeinfo-charge-charging_station_id').innerText = data.charging_station_id;
    }
    else{
        document.getElementById('chargeinfo-charge-charging_station_id').innerText = "No data";
    }

    document.getElementById('chargeinfo-charge-start_date').innerText = formatDate(new Date(data.start_date));

    if(data.end_date){
        document.getElementById('chargeinfo-charge-end_date').innerText = formatDate(new Date(data.end_date));
    }
    else{
        document.getElementById('chargeinfo-charge-end_date').innerText = "No data";
    }

    document.getElementById('chargeinfo-charge-start_voltage').innerText = `${data.start_voltage} V`;
    if(data.end_voltage){
        document.getElementById('chargeinfo-charge-end_voltage').innerText = `${data.end_voltage} V`;
    }
    else{
        document.getElementById('chargeinfo-charge-end_voltage').innerText = "No data";
    }
    document.getElementById('chargeinfo-charge-status').innerText = data.status;

    getMeasure(data.id);
  })
  .catch(err => {
       const messages = err.response.data.error;
       alertErrors(messages);
  })
}

const getMeasure = (chargeId) => {
  axios.get(`${prefixUrl}/measure/${chargeId}`)
  .then(resp => {

    const data = resp.data.data;
    const chargeChart = document.getElementById('line-chart');
    
    chargeChart.innerText = "";

    chartDates = [];
    chartAmps = [];
    chartVoltage = [];

    data.forEach(element => {
      const {amps, capacity, temperature, voltage, charge_id, id, timestamp} = element;
      chargeChart.innerText += `(${amps},${capacity},${temperature},${voltage}); `
      chartAmps.push(amps);
      chartVoltage.push(voltage);
      chartDates.push(timestamp.substr(12, 10));
    })

    new Chart(document.getElementById('line-chart'), {
      type: 'line',
      data: {
        labels: chartDates,
        datasets: [{
          data: chartVoltage,
          label: 'Voltage',
          yAxisID: 'Voltage',
          borderColor: "#3e95cd",
          fill: false,
        },
        {
          data: chartAmps,
          label: 'Amps',
          yAxisID: 'Amps',
          borderColor: "#c45850",
          fill: false
        }
        ]
      },
      options: {
        scales: {
          yAxes: [{
            id: 'Voltage',
            type: 'linear',
            position: 'left',
          }, {
            id: 'Amps',
            type: 'linear',
            position: 'right',
          }]
        }
      }
    })
  })
  .catch(err => {
    console.log(err);
  })
}

getBatteries();
getCharges();

function formatDate(date) {
  let hours = date.getHours();
  let minutes = date.getMinutes();
  let ampm = hours >= 12 ? 'pm' : 'am';
  hours = hours % 12;
  hours = hours ? hours : 12; // the hour '0' should be '12'
  minutes = minutes < 10 ? '0'+minutes : minutes;
  let strTime = hours + ':' + minutes + '' + ampm;
  return date.getDate()+ "/" + (date.getMonth()+1) +  "/" + date.getFullYear() + "  " + strTime;
}

const modalBattery = document.getElementById('battery-modal');
const modalCharge = document.getElementById('charge-modal');
const modalEndCharge = document.getElementById('end-charge-modal');

const onBatteryModal = () => {
  modalBattery.className += 'is-active';
}

const offBatteryModal = () => {
  modalBattery.className = modalBattery.className.replace('is-active', '');
}

const onEndChargeModal = () => {
  modalEndCharge.className += 'is-active';
}

const offEndChargeModal = () => {
  modalEndCharge.className = modalEndCharge.className.replace('is-active', '');
}

const onChargeModal = (batteryID) => {
  modalCharge.className += 'is-active';
  document.getElementById('formAddCharge_id').value = batteryID;
}

const offChargeModal = () => {
  modalCharge.className = modalCharge.className.replace('is-active', '');
}

let panelTabsBattery = document.getElementById("panel-tabs-battery");
let last_active = panelTabsBattery.children[0];

panelTabsBattery.childNodes.forEach(el => {
  el.onclick = () => {    
    last_active.className = "";
    el.className = "is-active";
    last_active = el;
    batteryTabState = el.innerText;
    searchBatteries();
  }
})

const searchCharge = () => {
  let panelCharge = document.getElementById('panel-charge');
  let search = document.getElementById('search-charge');
  let a = panelCharge.getElementsByTagName('a')

  for (let i = 1; i < a.length; i++) {
    let txtValue = a[i].children[0].children[0].innerText;
    if (search.value == '' || txtValue == search.value ) {
      a[i].style.display = "";
    }
    else {
      a[i].style.display = "none";
    }
  }
}

let batteryTabState = 'All';

const searchBatteries = () => {
  let search = document.getElementById('search-battery');
  let panelBattery = document.getElementById('panel-battery');
  let divs = panelBattery.getElementsByTagName('section');

  for (let i = 0; i < divs.length; i++) {
    let txtValue = divs[i].children[1].children[0].children[0].innerText;
    let stateValue = divs[i].children[1].children[0].children[2].innerText;

    let flag = true;
    if (batteryTabState !== 'All') {
      if(batteryTabState === "Active"){
        flag = divs[i].children[1].style.backgroundColor !== "pink";
      }
      else {
        flag = batteryTabState == stateValue;
      }
      
    }

    if (txtValue.toUpperCase().indexOf(search.value) > -1 && flag) {
        divs[i].style.display = "";
    }
    else {
        divs[i].style.display = "none";
    }
  }
}

const endChargeModalBefore = (chargeId) =>{
  document.getElementById('end-charge-modal-charge-id').value = chargeId;
  onEndChargeModal();
}

const endChargeModal = () => {
  chargeId = document.getElementById('end-charge-modal-charge-id').value;
  endCharge(chargeId);
}

const endCharge = (chargeId) => {
  end_voltage = document.getElementById('formEndCharge_end_voltage').value;
  data = {
    "end_voltage": end_voltage
  };
  axios.patch(`${prefixUrl}/charge/end/` + chargeId, data, headers)
  .then((resp) => {
    offEndChargeModal();
    getBatteries();
    getCharges();
  })
  .catch((err) => {
    const messages = err.response.data.error;
    alertErrors(messages);
  })
}

const endChargeModalReturn = () => {
  chargeId = document.getElementById('end-charge-modal-charge-id').value;
  return endChargeReturn(chargeId);
}

const endChargeReturn = (chargeId) => {
  end_voltage = document.getElementById('formEndCharge_end_voltage').value;
  data = {
    "end_voltage": end_voltage
  };
  return axios.patch(`${prefixUrl}/charge/end/` + chargeId, data, headers)
}

const addCharge = () => {
  batteryId = document.getElementById('formAddCharge_id').value;
  stationId = document.getElementById('formAddCharge_stationid').value;
  start_voltage = document.getElementById('formAddCharge_start_voltage').value;
  charge_type = document.getElementById('formAddCharge_charge_type').value;

  data = {
    "battery_id": batteryId,
    "start_voltage": start_voltage,
    "charge_type": charge_type,
    "charging_station_id": stationId
  };
  
  axios.post(`${prefixUrl}/charge/`, data, headers)
  .then((resp) => {
    getBatteries();
    getCharges();
    offChargeModal();
  })
  .catch((err) => {
    const messages = err.response.data.error;
    alertErrors(messages);
  })
}

const alertErrors = (message) => {
  for (var key in message) {
    if (!message.hasOwnProperty(key)) continue;
    var obj = message[key];
    for (var prop in obj) {
        if (!obj.hasOwnProperty(prop)) continue;
        alert(obj[prop]);
    }
  }
}

const newBatteryBeforeScript = () => {
  document.getElementById('battery-modal-model').value = '';
  document.getElementById('battery-modal-company').value = '';
  document.getElementById('battery-modal-first-usage-date').value = '';
  document.getElementById('battery-modal-production-date').value = '';
  document.getElementById('battery-capacity').value = '';

  document.getElementById('battery-modal-number-of-cells').value = '';
  document.getElementById('battery-modal-discharge-rate').value = '';
  document.getElementById('battery-modal-is-active').checked = true;
  document.getElementById('battery-modal-full-charge-voltage').value = '';
  document.getElementById('battery-modal-maintenance-voltage').value = '';
  
  document.getElementById('battery-modal-min-voltage').value = '';
  document.getElementById('battery-modal-new-button').style.display = "block";
  document.getElementById('battery-modal-edit-button').style.display = "none";
  document.getElementById('battery-modal-delete-button').style.display = "none";
  onBatteryModal();
}

const editBatteryBeforeScript = (battery) => {
  document.getElementById('battery-modal-battery-id').value = battery.id;

  document.getElementById('battery-modal-model').value = battery.model;
  document.getElementById('battery-modal-company').value = battery.company;
  document.getElementById('battery-modal-first-usage-date').value = battery.first_usage_date;
  document.getElementById('battery-modal-production-date').value = battery.production_date;
  document.getElementById('battery-capacity').value = battery.capacity;

  document.getElementById('battery-modal-number-of-cells').value = battery.no_of_cells;
  document.getElementById('battery-modal-discharge-rate').value = battery.discharge_rate;
  document.getElementById('battery-modal-is-active').checked = battery.is_active;
  document.getElementById('battery-modal-full-charge-voltage').value = battery.full_charge_voltage;
  document.getElementById('battery-modal-maintenance-voltage').value = battery.maintenance_voltage;
  
  document.getElementById('battery-modal-min-voltage').value = battery.min_voltage;
  document.getElementById('battery-modal-new-button').style.display = "none";
  document.getElementById('battery-modal-edit-button').style.display = "block";
  document.getElementById('battery-modal-delete-button').style.display = "block";
  
  onBatteryModal();
}

const addNewBattery = (type="NEW") => {
  model = document.getElementById('battery-modal-model').value;
  company = document.getElementById('battery-modal-company').value;
  first_usage_date = document.getElementById('battery-modal-first-usage-date').value;
  production_date = document.getElementById('battery-modal-production-date').value;
  capacity = document.getElementById('battery-capacity').value;

  no_of_cells = document.getElementById('battery-modal-number-of-cells').value;
  discharge_rate = document.getElementById('battery-modal-discharge-rate').value;
  is_active = document.getElementById('battery-modal-is-active').checked.toString();
  full_charge_voltage = document.getElementById('battery-modal-full-charge-voltage').value;
  maintenance_voltage = document.getElementById('battery-modal-maintenance-voltage').value;
  
  min_voltage = document.getElementById('battery-modal-min-voltage').value;
  
  console.log(document.getElementById('battery-modal-is-active').checked);

  data = {
    "model": model,
    "company": company,
    "first_usage_date": first_usage_date,
    "production_date": production_date,
    "capacity": capacity,
    "no_of_cells": no_of_cells,
    "discharge_rate": discharge_rate,
    "is_active": is_active,
    "full_charge_voltage": full_charge_voltage,
    "maintenance_voltage": maintenance_voltage,
    "min_voltage": min_voltage
  };

  data = removeEmpty(data);

  if(type ==="NEW"){
    axios.post(`${prefixUrl}/battery/`, data, headers)
    .then((resp) => {
      getBatteries();
      getCharges();
      offBatteryModal();
    })
    .catch((err) => {
     const messages = err.response.data.error;
     alertErrors(messages);
    })
  } 
  else if(type==="EDIT"){
    axios.patch(`${prefixUrl}/battery/` + document.getElementById('battery-modal-battery-id').value, data, headers)
    .then((resp) => {
      getBatteries();
      getCharges();
      offBatteryModal();
    })
    .catch((err) => {
       const messages = err.response.data.error;
       alertErrors(messages);
    })
  } 
  if(type==="DELETE"){
    axios.delete(`${prefixUrl}/battery/` + document.getElementById('battery-modal-battery-id').value, data, headers)
    .then((resp) => {
      getBatteries();
      getCharges();
      offBatteryModal();
    })
    .catch((err) => {
       const messages = err.response.data.error;
       alertErrors(messages);
    })
  }
}

const removeEmpty = (obj) => {
  Object.keys(obj).forEach((k) => (!obj[k] && obj[k] !== undefined) && delete obj[k]);
  return obj;
};

let orderButton = document.getElementById('order');
orderButton.onclick = () => {
  if(!orderButton.classList.contains('animate')){
    endChargeModalReturn()
    .then((resp) => {
      orderButton.className += ' animate';
      setTimeout(() => {
        orderButton.className = orderButton.className.replace(' animate', '');
        getBatteries();
        getCharges();
        offEndChargeModal();
      }, 6000);
    })
    .catch((err) => {
       const messages = err.response.data.error;
       alertErrors(messages);
    })
  }
}

const createIconForCharge = (element) => {
  let icon = document.createElement("i");
  icon.style.width = "20px";
  icon.className = "fas fa-bolt";

  if(element.end_date){
    if(element.charge_type == 'charging'){
      icon.className = "fas fa-battery-full";
    }
    else if (element.charge_type == 'maintenance'){
      icon.className = "fas fa-battery-three-quarters";
    } 
    else if (element.charge_type == 'discharging') {
      icon.className = "fas fa-battery-empty";
    }
  }

  if(element.charge_type == 'charging'){
    icon.style.color = "green";
  }
  else if (element.charge_type == 'maintenance'){
    icon.style.color = "blue";
  }
  else if (element.charge_type == 'discharging') {
    icon.style.color = "red";
  }

  return icon;
}
