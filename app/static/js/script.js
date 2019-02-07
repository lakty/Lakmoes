let map;
function openSearch(){
    $('#searchAddress').modal('show');
    if (! map) {
        map = L.map('map').setView([51.505, -0.09], 13);
        const osmUrls = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
        L.tileLayer(osmUrls).addTo(map);
        map.invalidateSize();
    }
}
function get_location(form) {
  var json;
  $.ajax({
    async: false,
    url: "/location",
    data: $('#'+form).serialize(),
    type: 'POST',
    success: function(response) {
      json = JSON.parse(response);
    },
    error: function(error) {
      console.error();
      return 0;
    }

  });
  return json;
};
function get_len(form, address, long, lati) {
  $('#map').show();
  map.invalidateSize();
    const res = get_location(form);
    save_location(res, address, long, lati);
}
function save_location(data, address, long, lati){
  map.setView([data['latitude'], data['longitude']]);
  if (marker) {
    map.removeLayer(marker);
  }
  let data_str = JSON.stringify([data['latitude'], data['longitude'], data['location']]);
  let func_str = `select_value(${data_str}, "${address}", "${long}", "${lati}");`;
  var marker = L.marker([data['latitude'], data['longitude']]).addTo(map)
  .bindPopup(data['location']+`<br><button class='form-control' onclick='${func_str}'>Зберегти</button>`)
  .openPopup();
}
function select_value(data, address, long, lati) {
  var input_address = document.getElementById('addressStr');
  var input_lo = document.getElementById(long);
  var input_lat = document.getElementById(lati);
  var place = document.getElementById(address);
  input_address.value = data[2];
  input_lo.value = data[1];
  input_lat.value = data[0];
  place.removeAttribute('disabled');
  place.value = data[2];
  $('#searchAddress').modal('hide')
}