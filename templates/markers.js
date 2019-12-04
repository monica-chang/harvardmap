var labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz123456789';
var labelIndex = 0;

var markers = [
    ['Smith Center', 42.3727 , -71.1186],
    ['Apley Court', 42.3724, -71.1181],
    ['Canaday Hall', 42.3753 , -71.1159],
    ['Grays Hall', 42.3736 , -71.1178],
    ['Greenough Hall', 42.3729 , -71.1138],
    ['Hollis Hall', 42.3750, -71.1179],
    ['Holworthy Hall', 42.3755 , -71.1172],
    ['Hurlbut Hall', 42.3721 , -71.1139],
    ['Lionel Hall', 42.3751 , -71.1184],
    ['Mower Hall', 42.3755 , -71.1182],
    ['Mass Hall', 42.3744, -71.1183],
    ['Matthews Hall', 42.3741, -71.1181],
    ['Stoughton Hall', 42.3754 , -71.1177],
    ['Straus Hall', 42.3741, -71.1186],
    ['Thayer Hall', 42.3750 , -71.1167],
    ['Weld Hall', 42.3739 , -71.1171],
    ['Wigg Hall', 42.3731 , -71.1171],
    ['Adams House', 42.3717 , -71.1167],
    ['Cabot House', 42.3812 , -71.1247],
    ['Currier House', 42.3818, -71.1255],
    ['Dunster House', 42.3686, -71.1158],
    ['Eliot House', 42.3703, -71.1209],
    ['Kirkland House', 42.3708 , -71.1205],
    ['Leverett House', 42.3701, -71.1174],
    ['Lowell House', 42.3720 , -71.1181],
    ['Mather House', 42.3686, -71.1153],
    ['Pforzheimer House', 42.3821 , -71.1248],
    ['Quincy House', 42.3705, -71.1174],
    ['Winthrop House', 42.3702,  -71.1191],
    ['Cabot Library', 42.3762 , -71.1162],
    ['Law School Library', 42.3780 , -71.1186],
    ['Lamont Library', 42.3727, -71.1155],
    ['Widener Library', 42.3734, -71.1165],
    ['Capital One Cafe', 42.3727, -71.1197],
    ['Flour Bakery', 42.3730 , -71.1225],
    ['Peets Cafe', 42.3726 , -71.1206],
    ['Starbucks', 42.3733 , -71.1192],
    ['Tatte Bakery and Cafe', 42.3727 , -71.1170]
  ];

function initialize() {

var myOptions = {
  center: new google.maps.LatLng(42.3744, -71.1162),
  zoom: 15,


 };
var map = new google.maps.Map(document.getElementById("default"),
  myOptions);

setMarkers(map, markers)

}



  function setMarkers(map, markers) {
    var marker, i 
    for (i = 0; i < markers.length; i++) {
      var lat = markers[i][1]
      var long = markers[i][2]
      var inside = markers[i][0]

      latlngset = new google.maps.LatLng(lat, long);
      var marker = new google.maps.Marker({
        position: latlngset,
        label: labels[i],
        map: map,
        title: inside
    });

      var content = inside

      var infowindow = new google.maps.InfoWindow()
      google.maps.event.addListener(marker,'click', (function(marker,content,infowindow){ 
        return function() {
          infowindow.setContent(content);
          infowindow.open(map,marker);
        };
      })(marker,content,infowindow));  

  }
}


google.maps.event.addDomListener(window, 'load', initialize);
