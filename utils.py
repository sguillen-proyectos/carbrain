import urllib2

def check_internet():
  try:
    url = urllib2.urlopen('http://motherfuckingwebsite.com/')
    return True
  except Exception as e:
    pass

  return False

def get_position2(counter):
  locations = [{ "lat":-16.462000, "lng":-68.108986 },{ "lat":-16.461825, "lng":-68.108739 },{ "lat":-16.461784, "lng":-68.108438 },{ "lat":-16.461867, "lng":-68.108213 },{ "lat":-16.461877, "lng":-68.107977 },{ "lat":-16.461723, "lng":-68.107784 },{ "lat":-16.461609, "lng":-68.107602 }]
  return locations[counter]

def get_position(gps):
  latitude = float(gps[0][0:2] + '.' + gps[0][2:4] + gps[0][5:])
  longitude = float(gps[2][0:3] + '.' + gps[2][3:5] + gps[2][6:])

  g = float(gps[0][0:2])
  m = float(gps[0][2:4])
  s = float('0.' + gps[0][5:])
  s *= 60.
  latitude = g + (m/60.) + (s/3600.)

  if gps[1] == 'S':
    latitude = -latitude

  g = float(gps[2][0:3])
  m = float(gps[2][3:5])
  s = float('0.' + gps[2][6:])
  s *= 60.
  longitude = g + (m/60.) + (s/3600.)

  if gps[3] == 'W':
    longitude = -longitude

  return {
    "lat" : latitude,
    "lng" : longitude
  }
