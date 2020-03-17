import abc


class BaseDataWriter(metaclass=abc.ABCMeta):

    destination_class = None

    def get_destination(self, *args, **kwargs):
        return self.destination_class(*args, **kwargs)

    @abc.abstractmethod
    def write_line(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def write_lines(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def get_result(self, *args, **kwargs):
        pass


class BaseCSVDataWriter(BaseDataWriter):

    header = ''
    format_line = ''
    filename = 'file.csv'

    def __init__(self):
        self.__destination = self.get_destination(self.filename)
        self.__destination.write(self.header)

    def _get_formatted_line(self, instance_dict):
        for key in instance_dict.keys():
            if instance_dict[key] is None:
                instance_dict[key] = '-'
        return self.format_line.format(**instance_dict)

    def write_line(self, instance):
        self.__destination.write(self._get_formatted_line(instance))

    def write_lines(self, instances):
        self.__destination.write(''.join([self._get_formatted_line(inst) for inst in instances]))

    def get_result(self):
        return self.__destination.save()
