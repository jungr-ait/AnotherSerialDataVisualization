import configparser


class Plotter:
    def __init__(self, format_str='', title='', buffer_size=100, interval_ms=100):
        self.format_str = format_str
        self.title = title
        self.buffer_size = buffer_size
        self.interval_ms = interval_ms

    def add_to_config(self, section):

        fmt = self.format_str.replace('%', '%%')
        section['format_str'] = fmt
        section['title'] = self.title
        section['buffer_size'] = str(self.buffer_size)
        section['interval_ms'] = str(self.interval_ms)

    def load_from_config(self, section):
        fmt = section.get('format_str', '%%f,%%f,%%f')
        self.format_str = fmt.replace('%%', '%')
        self.title = section.get('title', 'default')
        self.buffer_size = int(section.get('buffer_size', '100'))
        self.interval_ms = int(section.get('interval_ms', '100'))

        print('load from section')
        print(self.format_str)
        print(self.title)
        print(str(self.buffer_size))
        print(str(self.interval_ms))



if __name__ == '__main__':
    config = configparser.ConfigParser()

    config['Serial'] = {'device' : '/dev/ttyUSB0',
                        'baud_rate' : '115200'}

    config['Plotter1'] = {}
    plotter1 =  config['Plotter1']

    plotter1['format_str' ] = 'acc:%%f,%%f,%%f'
#    plotter1 = {'format_str' : 'acc:%%f,%%f,%%f',
#                          'title:' : 'accelerometer',
#                          'buffer_size' : '100',
#                          'interval_ms': '100'}

    plotter1['jelle'] = 'dd'

    config['Plotter2'] = {'format_str' : 'gyr:%%f,%%f,%%f',
                          'title:' : 'gyroscope',
                          'buffer_size' : '100',
                          'interval_ms': '100'}


    p3 = Plotter('gyr:%f,%f,%f','gyroscope')
    config['Plotter3'] = {}
    p3.add_to_config(config['Plotter3'])


    print('Save config file....')
    with open('example.ini', 'w') as configfile:
        config.write(configfile)
        configfile.close()

    print('Load config file....')

    config_rd = configparser.ConfigParser()
    config_rd.sections()
    config_rd.read('example.ini')

    items = config_rd.items()
    p4 = Plotter()

    p4.load_from_config(config_rd['Plotter3'])


