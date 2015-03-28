import urllib2

def check_internet():
  try:
    url = urllib2.urlopen('http://motherfuckingwebsite.com/')
    return True
  except Exception as e:
    pass

  return False

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
