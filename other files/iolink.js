const url = 'http://192.168.0.4';
const data = {"code": "request", "cid": 10, "adr": "iolinkmaster/port[3]/iolinkdevice/pdout/setdata", "data": {"newvalue": "01"}}

serial_1 = "/iolinkmaster/port[1]/iolinkdevice/serial"
serial_2 = "/iolinkmaster/port[2]/iolinkdevice/serial"
serial_3 = "/iolinkmaster/port[3]/iolinkdevice/serial"
serial_4 = "/iolinkmaster/port[4]/iolinkdevice/serial"
serial_5 = "/iolinkmaster/port[5]/deviceinfo/serialnumber"
serial_6 = "/iolinkmaster/port[6]/iolinkdevice/serial"
serial_7 = "/iolinkmaster/port[7]/iolinkdevice/serial"
serial_8 = "/iolinkmaster/port[8]/iolinkdevice/serial"
port_1 = "/iolinkmaster/port[1]/iolinkdevice/pdin/"
port_2 = "/iolinkmaster/port[2]/iolinkdevice/pdin/"
port_3 = "/iolinkmaster/port[3]/iolinkdevice/pdin/"
port_4 = "/iolinkmaster/port[4]/iolinkdevice/pdin/"
port_5 = "/iolinkmaster/port[5]/iolinkdevice/pdin//"
port_6 = "/iolinkmaster/port[6]/iolinkdevice/pdin/"
port_7 = "/iolinkmaster/port[7]/iolinkdevice/pdin/"
port_8 = "/iolinkmaster/port[8]/iolinkdevice/pdout/"
payload_read = {"code": "request", "cid": 4711, "adr": "/getdatamulti", "data": { "datatosend": [serial_1, port_1, serial_2, port_2, serial_3, port_3, serial_4, port_4,serial_5, port_5, serial_6, port_6, serial_7, port_7, serial_8,port_8]}}
fetch(url, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(data)
})
  .then(response => response.json())
  .then(responseData => {
    console.log('Response:', responseData);
  })
  .catch(error => {
    console.error('Error:', error);
  });

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload_read)
  })
    .then(response => response.json())
    .then(responseData => {
      console.log('Response:', responseData);
    })
    .catch(error => {
      console.error('Error:', error);
    });
  


  fetch(url, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(responseData => {
        console.log('Response:', responseData);
    })
    .catch(error => {
        console.error('Error:', error);
    });
    
    const data2 = {"code": "request", "cid": 10, "adr": "iolinkmaster/port[3]/iolinkdevice/pdout/setdata", "data": {"newvalue": "00"}}
    
    
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data2)
    })
    .then(response => response.json())
  .then(responseData => {
      console.log('Response:', responseData);
    })
    .catch(error => {
        console.error('Error:', error);
  });
