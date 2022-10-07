#!/usr/bin/python
import sleekxmpp, pyaes, multiprocessing, json, base64, hashlib, math, datetime


class NefitEasy:
    userMode = None  # clock or manual
    manualSetpoint = None
    setpoint = None
    temperature = None
    outsideTemperature = None
    boilerIndicator = None  # CH, HW or No
    systemPressure = None
    hotWater = None
    override = None
    overrideSetpoint = None
    overrideDuration = None
    powerSave = None
    holidayMode = None
    firePlace = None
    sundayToday = None
    sundayTomorrow = None
    usage = {}
    lastUpdated = datetime.datetime.now()

    event = None
    container = {}

    def __init__(self, serialNumber, accessKey, password):
        secret = bytearray.fromhex('58f18d70f667c9c79ef7de435bf0f9b1553bbb6e61816212ab80e5b0d351fbb1')
        self.key = hashlib.md5(bytearray(accessKey, 'utf8') + secret).digest() + hashlib.md5(
            secret + bytearray(password, 'utf8')).digest()
        self.recipient = 'rrcgateway_{0}@wa2-mz36-qrmzh6.bosch.de'.format(serialNumber)
        self.sender = 'rrccontact_{0}@wa2-mz36-qrmzh6.bosch.de'.format(serialNumber)

        self.client = sleekxmpp.ClientXMPP(jid=self.sender, password='Ct7ZR03b_{0}'.format(accessKey),
                                           sasl_mech='DIGEST-MD5')
        self.client.add_event_handler('session_start', self.SessionStart)
        self.client.register_plugin('xep_0199')

    def SessionStart(self, event):
        self.client.send_presence()
        self.client.get_roster()

    def Connect(self):
        self.client.connect()
        self.client.process(block=False)

    def Disconnect(self):
        self.client.disconnect()

    def Decrypt(self, data):
        if not data:
            return ''

        cipher = pyaes.Decrypter(pyaes.AESModeOfOperationECB(self.key), padding=pyaes.PADDING_NONE)
        decrypted = cipher.feed(base64.b64decode(data)) + cipher.feed()

        return decrypted.decode('utf8').rstrip(chr(0))

    def Message(self, message):
        if message['type'] in ('chat', 'normal'):
            headers = message['body'].split('\n')[:-1]
            body = message['body'].split('\n')[-1:][0]

            if 'HTTP/1.0 400 Bad Request' in headers:
                return

            response = self.Decrypt(body)

            if 'Content-Type: application/json' in headers:
                response = response.strip()

                if len(response) > 1:
                    response = json.loads(response.strip())

            self.container[id(self.event)] = response
        self.event.set()

    def Send(self, body):
        body = body.replace('\r', '\n')
        message = self.client.make_message(mto=self.recipient, mfrom=self.sender, mbody=body)
        message['lang'] = None
        str_data = sleekxmpp.xmlstream.tostring(message.xml, xmlns=message.stream.default_ns, stream=message.stream, top_level=True)
        str_data = str_data.replace('&amp;#13;', '')

        return message.stream.send_raw(str_data)

    def Get(self, url):
        self.event = multiprocessing.Event()
        self.client.add_event_handler('message', self.Message)
        self.Send('GET {0} HTTP/1.1\rUser-Agent: NefitEasy\r\r'.format(url))
        self.event.wait(timeout=10)
        self.client.del_event_handler('message', self.Message)

        if id(self.event) in self.container.keys():
            response = self.container[id(self.event)]
            del (self.container[id(self.event)])
        else:
            reponse = None
      #  return response

    def Encrypt(self, data):
        if len(data) % 16 != 0:
            data = data + (16 - len(data) % 16) * chr(0)

        cipher = pyaes.Encrypter(pyaes.AESModeOfOperationECB(self.key), padding=pyaes.PADDING_NONE)
        ciphertext = cipher.feed(data) + cipher.feed()

        return base64.b64encode(ciphertext)

    def Put(self, url, data):
        data = data if isinstance(data, str) else json.dumps(data, separators=(',', ':'))
        encrypted_data = self.Encrypt(data).decode('utf8')
        body = '\r'.join([
            'PUT {0} HTTP/1.1'.format(url),
            'Content-Type: application/json',
            'Content-Length: {0}'.format(len(encrypted_data)),
            'User-Agent: NefitEasy\r',
            encrypted_data
        ])
        self.event = multiprocessing.Event()
        self.client.add_event_handler('message', self.Message)
        self.Send(body)
        self.event.wait(timeout=10)
        self.client.del_event_handler('message', self.Message)

    def GetThermostatData(self):
        self.Connect()

        status = self.Get('/ecus/rrc/uiStatus')['value']
        outdoorTemperature = self.Get('/system/sensors/temperatures/outdoor_t1')['value']
        systemPressure = self.Get('/system/appliance/systemPressure')['value']

        self.userMode = status['UMD']
        self.manualSetpoint = float(status['MMT'])
        self.setpoint = float(status['TSP'])
        self.temperature = float(status['IHT'])
        self.outsideTemperature = outdoorTemperature
        self.boilerIndicator = status['BAI']
        self.systemPressure = systemPressure
        self.hotWater = True if status['DHW'] == 'on' else False
        self.override = True if status['TOR'] == 'on' else False
        self.overrideSetpoint = float(status['TOT'])
        self.overrideDuration = float(status['TOD'])
        self.powerSave = True if status['ESI'] == 'on' else False
        self.holidayMode = True if status['HMD'] == 'on' else False
        self.firePlace = True if status['FPA'] == 'on' else False
        self.sundayToday = True if status['DAS'] == 'on' else False
        self.sundayTomorrow = True if status['TAS'] == 'on' else False

        self.lastUpdated = datetime.datetime.now()

        self.Disconnect()

    def GetThermostatUsage(self):
        self.Connect()

        self.usagePointer = math.ceil(self.Get('/ecus/rrc/recordings/gasusagePointer')['value'] / 32.0)

        data = self.Get('/ecus/rrc/recordings/gasusage?page={0}'.format(self.usagePointer))['value']

        for datum in data:
            date = datetime.datetime.strptime(datum['d'], '%d-%m-%Y') if datum['d'] != '255-256-65535' else False

            if date and date not in self.usage:
                self.usage[date] = {'centralHeating': datum['ch'], 'hotWater': datum['hw'],
                                    'averageOutsideTemperature': datum['T'] / 10.0}

        self.Disconnect()

    def SetTemperature(self, temperature):
        self.Connect()

        self.Put('/heatingCircuits/hc1/temperatureRoomManual', {'value': float(temperature)})
        self.Put('/heatingCircuits/hc1/manualTempOverride/status', {'value': 'on'})
        self.Put('/heatingCircuits/hc1/manualTempOverride/temperature', {'value': float(temperature)})

        self.Disconnect()


# Enter serialNumber, accessKey and password and uncomment to test

NefitEasy = NefitEasy('101-119-889', 'FaFz-4ZBK-6ukX-fVAa', '#Easycontrol357')

NefitEasy.GetThermostatData()

print(NefitEasy.userMode)
print(NefitEasy.manualSetpoint)
print(NefitEasy.setpoint)
print(NefitEasy.temperature)
print(NefitEasy.outsideTemperature)
print(NefitEasy.boilerIndicator)
print(NefitEasy.systemPressure)
print(NefitEasy.hotWater)
print(NefitEasy.override)
print(NefitEasy.overrideSetpoint)
print(NefitEasy.overrideDuration)
print(NefitEasy.powerSave)
print(NefitEasy.holidayMode)
print(NefitEasy.firePlace)
print(NefitEasy.sundayToday)
print(NefitEasy.sundayTomorrow)

#NefitEasy.SetTemperature(20)
