
function fetchData() {
  // Make a GET request to a Django API endpoint
fetch('/hvac/api/airunit', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json',
    // You can include additional headers if needed, such as authentication tokens
  },
})
  .then((response) => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json(); // Parse the JSON response
  })
  .then((data) => {
    // Update the UI with the received data
    console.log('Received data:', data);
    // You can manipulate the DOM to display the data here

      document.getElementById('sa').innerText = `Supply Air Temperature: ` + data[0]['sa']['temp'] + ' F';
      document.getElementById('supply_cfm').innerText = `Supply Flow: ` + data[0]['sa']['cfm'] + ' CFM';
      document.getElementById('supply_fan_speed').innerText = `Supply Fan Speed: ` + data[0]['supply_fan']['speed']+ ' %';
      document.getElementById("cooling_coil_temp").innerText = `Cooling Coil Temperature: ` + data[0]['cooling_coil']['temp'];
      document.getElementById("heating_coil_temp").innerText = `Heating Coil Temperature: ` + data[0]['heating_coil']['temp'];
      document.getElementById("mixed_air_temp").innerText = `Supply Air Fan Speed: ` + data[0]['supply_fan']['speed'];
      document.getElementById("return_air_temp").innerText = `Return Air Temperature: ` + data[0]['ra']['temp'];
      document.getElementById("return_fan_speed").innerText = `Return Air Fan Speed: ` + data[0]['return_fan']['speed'];
      document.getElementById("mixed_air_damper_position").innerText = `Mixed Air Damper Position: `  + data[0]['ma_damper']['position'];
      document.getElementById("exhaust_air_damper_position").innerText = `Return Air Damper Position: ` + data[0]['ea_damper']['position'];
      document.getElementById("return_air_cfm").innerText = `Return Air Flow: ` + data[0]['ra']['cfm'];
      document.getElementById("outdoor_air_temp").innerText = `Outdoor Air Temperature: ` + data[0]['oa']['temp'];
      document.getElementById("outdoor_air_damper_position").innerText = `Outside Air Damper Position: ` + data[0]['oa_damper']['position'];
      document.getElementById("outdoor_air_cfm").innerText = `Outdoor Air Flow: ` + data[0]['outdoor_air_flow'];

  })
  .catch((error) => {
    console.error('Error:', error);
  });

  // Get Room Values
  // Make a GET request to a Django API endpoint
fetch('/hvac/api/room/1', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json',
    // You can include additional headers if needed, such as authentication tokens
  },
})
  .then((response) => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json(); // Parse the JSON response
  })
  .then((data) => {
    // Update the UI with the received data
    console.log('Received data:', data);
    // You can manipulate the DOM to display the data here
      document.getElementById('Conference Room').innerText = `Conference Room Temp: ` + data['air']['temp'] + ' F';
  })
  .catch((error) => {
    console.error('Error:', error);
  });

  fetch('/hvac/api/room/2', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      // You can include additional headers if needed, such as authentication tokens
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json(); // Parse the JSON response
    })
    .then((data) => {
      // Update the UI with the received data
      console.log('Received data:', data);
      // You can manipulate the DOM to display the data here
        document.getElementById('Break Room').innerText = `Break Room Temperature: ` + data['air']['temp'] + ' F';
    })
    .catch((error) => {
      console.error('Error:', error);
    });

  fetch('/hvac/api/room/3', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      // You can include additional headers if needed, such as authentication tokens
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json(); // Parse the JSON response
    })
    .then((data) => {
      // Update the UI with the received data
      console.log('Received data:', data);
      // You can manipulate the DOM to display the data here
        document.getElementById('Office').innerText = `Office Temp: ` + data['air']['temp'] + ' F';
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  }


// Fetch data every 5 seconds (adjust the interval as needed)
setInterval(fetchData, 5000);    